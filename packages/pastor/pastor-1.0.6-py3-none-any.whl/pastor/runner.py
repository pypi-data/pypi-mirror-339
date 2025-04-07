import os
import time
import uuid
from datetime import datetime
from typing import List, Dict, Text

from pastor.uicore.config import step_type, database_url, base_url
from pastor.dbcore.engine import DBEngine
from pastor.uicore.driver import AutoDriver
from pastor.uicore.element import ElementObj
from pastor.uicore.local import gc
from pastor.uicore.web_action import Action

try:
    import allure

    USE_ALLURE = True
except ModuleNotFoundError:
    USE_ALLURE = False

from loguru import logger

from pastor import utils, exceptions
from pastor.client import HttpSession
from pastor.exceptions import ValidationFailure, ParamsError, NotFoundError
from pastor.ext.uploader import prepare_upload_step
from pastor.loader import load_project_meta, load_testcase_file
from pastor.parser import build_url, parse_data, parse_variables_mapping
from pastor.response import ResponseObject
from pastor.testcase import Config, Step
from pastor.utils import merge_variables
from pastor.models import (
    TConfig,
    TStep,
    VariablesMapping,
    StepData,
    TestCaseSummary,
    TestCaseTime,
    TestCaseInOut,
    ProjectMeta,
    TestCase,
    Hooks,
    StepTypeEnum, TUiLocation, SqlData,
)


class Pastor(object):
    config: Config
    teststeps: List[Step]

    success: bool = False  # indicate testcase execution result
    __config: TConfig
    __teststeps: List[TStep]
    __project_meta: ProjectMeta = None
    __case_id: Text = ""
    __export: List[Text] = []
    __step_datas: List[StepData] = []
    __session: HttpSession = None
    __session_variables: VariablesMapping = {}
    # time
    __start_at: float = 0
    __duration: float = 0
    # log
    __log_path: Text = ""
    # ui 驱动
    __driver: AutoDriver = None
    # 运行类型，API，UI，SQL
    __type: StepTypeEnum = None
    # 是否引用用例
    __is_reference: bool = False
    # 判断是否为登录文件，以文件名是否包含login判断，当读取cookie不需要登录时，登录case需要登录，这里做过滤
    __is_login_case: bool = False

    @property
    def driver(self):
        return self.__driver

    def __init_tests__(self):
        self.__config = self.config.perform()
        self.__teststeps = []
        for step in self.teststeps:
            self.__teststeps.append(step.perform())

    @property
    def raw_testcase(self) -> TestCase:
        if not hasattr(self, "__config"):
            self.__init_tests__()

        return TestCase(config=self.__config, teststeps=self.__teststeps)

    def with_project_meta(self, project_meta: ProjectMeta) -> "Pastor":
        self.__project_meta = project_meta
        return self

    def with_session(self, session: HttpSession) -> "Pastor":
        self.__session = session
        return self

    def with_case_id(self, case_id: Text) -> "Pastor":
        self.__case_id = case_id
        return self

    def with_driver(self, driver: AutoDriver) -> "Pastor":
        self.__driver = driver
        return self

    def with_is_reference(self, is_reference: bool) -> "Pastor":
        self.__is_reference = is_reference
        return self

    def with_variables(self, variables: VariablesMapping) -> "Pastor":
        self.__session_variables = variables
        return self

    def with_export(self, export: List[Text]) -> "Pastor":
        self.__export = export
        return self

    def __call_hooks(
            self, hooks: Hooks, step_variables: VariablesMapping, hook_msg: Text,
    ):
        """ call hook actions.

        Args:
            hooks (list): each hook in hooks list maybe in two format.

                format1 (str): only call hook functions.
                    ${func()}
                format2 (dict): assignment, the value returned by hook function will be assigned to variable.
                    {"var": "${func()}"}

            step_variables: current step variables to call hook, include two special variables

                request: parsed request dict
                response: ResponseObject for current response

            hook_msg: setup/teardown request/testcase

        """
        logger.info(f"call hook actions: {hook_msg}")

        if not isinstance(hooks, List):
            logger.error(f"Invalid hooks format: {hooks}")
            return

        for hook in hooks:
            if isinstance(hook, Text):
                # format 1: ["${func()}"]
                logger.debug(f"call hook function: {hook}")
                parse_data(hook, step_variables, self.__project_meta.functions)
            elif isinstance(hook, Dict) and len(hook) == 1:
                # format 2: {"var": "${func()}"}
                var_name, hook_content = list(hook.items())[0]
                hook_content_eval = parse_data(
                    hook_content, step_variables, self.__project_meta.functions
                )
                logger.debug(
                    f"call hook function: {hook_content}, got value: {hook_content_eval}"
                )
                logger.debug(f"assign variable: {var_name} = {hook_content_eval}")
                step_variables[var_name] = hook_content_eval
            else:
                logger.error(f"Invalid hook format: {hook}")

    def __run_step_ui(self, step: TStep):
        """
        运行及校验UI自动化
        :param step:
        :return:
        """
        step_data = StepData(name=step.name)
        locations = step.location

        # setup hooks
        if step.setup_hooks:
            self.__call_hooks(step.setup_hooks, step.variables, "setup ui request")

        # sql handle
        if step.pre_sql:
            self.__run_sql(step.pre_sql, step)

        location_info = []
        if locations:
            for location in locations:
                if isinstance(location.skip, Text) and "$" in location.skip:
                    location.skip = parse_data(
                        location.skip, step.variables, self.__project_meta.functions
                    )
                if location.skip is True:
                    continue

                parsed_location_dict = parse_data(
                    location.model_dump(), step.variables, self.__project_meta.functions
                )
                ui_location_obj = TUiLocation(**parsed_location_dict)

                # logger.info(f"location_info: {vars(ui_location_obj)}")
                location_info.append(vars(ui_location_obj))
                if not hasattr(Action, ui_location_obj.action):
                    funcs = [w for w in dir(Action) if callable(getattr(Action, w)) and not w.startswith("__")]
                    logger.error(f'action: {ui_location_obj.action}, 操作方法不存在以下列表中:{funcs}')
                    raise AttributeError(f'action: {ui_location_obj.action}, 操作方法不存在以下列表中:{funcs}')
                getattr(Action, ui_location_obj.action)(self.__driver, ui_location_obj)
                # if 'click' == ui_location_obj.action.lower() and '发送验证码' == ui_location_obj.desc:
                #     # 请求数据库获取手机验证码
                #     db = DBEngine(f'mysql+pymysql://root:rJCuKfeVB6nUZfSk@47.101.134.204:3306/sit_cas_new?charset=utf8mb4')
                #     codes = db.fetchone('select code from cn_sms_code order by created_at desc limit 1')
                #     if codes:
                #         # 当前step中
                #         logger.info(f'登录获取手机验证码: {codes}')
                #         step_data.export_vars = codes[0]
                #         step.variables.update(codes[0])
                time.sleep(ui_location_obj.sleep)

        # sql handle
        if step.post_sql:
            self.__run_sql(step.post_sql, step)

        # teardown hooks
        if step.teardown_hooks:
            self.__call_hooks(step.teardown_hooks, step.variables, "teardown request")

        # validate
        validators = step.validators
        success = False

        def log_req_resp_details():
            err_msg = "\n\n{} DETAILED UI LOCATION {}\n\n".format("*" * 32, "*" * 32)
            for v in location_info:
                err_msg += f"{v}\n"
            err_msg += "\n"
            logger.error(err_msg)

        element_obj = ElementObj(self.__driver)

        try:
            element_obj.validate(
                validators, step.variables, self.__project_meta.functions
            )
            success = True
        except ValidationFailure:
            success = False
            log_req_resp_details()
            # log testcase duration before raise ValidationFailure
            self.__duration = time.time() - self.__start_at
            raise
        finally:
            self.success = success
            step_data.success = success

        return step_data

    def __run_step_request(self, step: TStep) -> StepData:
        """run teststep: request"""
        step_data = StepData(name=step.name)

        # parse
        prepare_upload_step(step, self.__project_meta.functions)
        request_dict = step.request.model_dump()
        request_dict.pop("upload", None)
        parsed_request_dict = parse_data(
            request_dict, step.variables, self.__project_meta.functions
        )
        parsed_request_dict["headers"].setdefault(
            "HRUN-Request-ID",
            f"HRUN-{self.__case_id}-{str(int(time.time() * 1000))[-6:]}",
        )
        step.variables["request"] = parsed_request_dict

        # setup hooks
        if step.setup_hooks:
            self.__call_hooks(step.setup_hooks, step.variables, "setup request")

        # sql handle
        if step.pre_sql:
            self.__run_sql(step.pre_sql, step)

        # prepare arguments
        method = parsed_request_dict.pop("method")
        url_path = parsed_request_dict.pop("url")
        url = build_url(self.__config.base_url, url_path)
        parsed_request_dict["verify"] = self.__config.verify
        parsed_request_dict["json"] = parsed_request_dict.pop("req_json", {})

        # request
        resp = self.__session.request(method, url, **parsed_request_dict)
        resp_obj = ResponseObject(resp)
        step.variables["response"] = resp_obj

        # sql handle
        if step.post_sql:
            self.__run_sql(step.post_sql, step)

        # teardown hooks
        if step.teardown_hooks:
            self.__call_hooks(step.teardown_hooks, step.variables, "teardown request")

        def log_req_resp_details():
            err_msg = "\n{} DETAILED REQUEST & RESPONSE {}\n".format("*" * 32, "*" * 32)

            # log request
            err_msg += "====== request details ======\n"
            err_msg += f"url: {url}\n"
            err_msg += f"method: {method}\n"
            headers = parsed_request_dict.pop("headers", {})
            err_msg += f"headers: {headers}\n"
            for k, v in parsed_request_dict.items():
                v = utils.omit_long_data(v)
                err_msg += f"{k}: {repr(v)}\n"

            err_msg += "\n"

            # log response
            err_msg += "====== response details ======\n"
            err_msg += f"status_code: {resp.status_code}\n"
            err_msg += f"headers: {resp.headers}\n"
            err_msg += f"body: {repr(resp.text)}\n"
            logger.error(err_msg)

        # extract
        extractors = step.extract
        extract_mapping = resp_obj.extract(extractors, step.variables, self.__project_meta.functions)
        step_data.export_vars = extract_mapping

        variables_mapping = step.variables
        variables_mapping.update(extract_mapping)

        # validate
        validators = step.validators
        session_success = False
        try:
            resp_obj.validate(
                validators, variables_mapping, self.__project_meta.functions
            )
            session_success = True
        except ValidationFailure:
            session_success = False
            log_req_resp_details()
            # log testcase duration before raise ValidationFailure
            self.__duration = time.time() - self.__start_at
            raise
        finally:
            self.success = session_success
            step_data.success = session_success

            if hasattr(self.__session, "data"):
                # pastor.client.HttpSession, not locust.clients.HttpSession
                # save request & response meta data
                self.__session.data.success = session_success
                self.__session.data.validators = resp_obj.validation_results

                # save step data
                step_data.data = self.__session.data

        return step_data

    def __run_step_testcase(self, step: TStep) -> StepData:
        """run teststep: referenced testcase"""
        step_data = StepData(name=step.name)
        step_variables = step.variables
        step_export = step.export

        # setup hooks
        if step.setup_hooks:
            self.__call_hooks(step.setup_hooks, step_variables, "setup testcase")

        if hasattr(step.testcase, "config") and hasattr(step.testcase, "teststeps"):
            testcase_cls = step.testcase
            case_result = (
                testcase_cls()
                .with_session(self.__session)
                .with_case_id(self.__case_id)
                .with_variables(step_variables)
                .with_export(step_export)
                .run()
            )
        elif isinstance(step.testcase, Text):
            if os.path.isabs(step.testcase):
                ref_testcase_path = step.testcase
            else:
                ref_testcase_path = os.path.join(
                    self.__project_meta.RootDir, step.testcase
                )
            case_result = (
                Pastor()
                .with_session(self.__session)
                .with_case_id(self.__case_id)
                .with_is_reference(True)
                .with_driver(self.__driver)
                .with_variables(step_variables)
                .with_export(step_export)
                .run_path(ref_testcase_path)
            )

        else:
            raise exceptions.ParamsError(
                f"Invalid teststep referenced testcase: {step.dict()}"
            )

        # teardown hooks
        if step.teardown_hooks:
            self.__call_hooks(step.teardown_hooks, step.variables, "teardown testcase")

        step_data.data = case_result.get_step_datas()  # list of step data
        step_data.export_vars = case_result.get_export_variables()
        step_data.success = case_result.success
        self.success = case_result.success

        if step_data.export_vars:
            logger.info(f"export variables: {step_data.export_vars}")

        return step_data

    def __run_step(self, step: TStep) -> Dict:
        """run teststep, teststep maybe a request or referenced testcase"""
        logger.info(f"run step begin: {step.name} >>>>>>")
        # _type = os.getenv('type', 'api')
        _step_type = step.step_type
        if _step_type not in StepTypeEnum:
            raise NotFoundError(f'type={_step_type},设置错误,只能设置API,UI,SQL！')
        _type = self.__type
        _type = _step_type if (_type != _step_type and len(_step_type) != 0) else _type

        if _type == StepTypeEnum.API:
            if step.request:
                step_data = self.__run_step_request(step)
            elif step.testcase:
                step_data = self.__run_step_testcase(step)
            else:
                raise ParamsError(
                    f"teststep is neither a request nor a referenced testcase: {step.model_dump()}"
                )
        elif _type == StepTypeEnum.UI:
            if not self.__driver:
                # 初始化webdriver，并打开浏览器页面
                self.__driver = AutoDriver(self.__config.ignore_cache)
                self.__driver.open(self.__config.base_url)

            if step.location or step.validators:
                # step_data = self.__run_step_ui(step)
                try:
                    step_data = self.__run_step_ui(step)
                except Exception:
                    if self.__driver:
                        self.__driver.quit()
                    raise
            elif step.testcase:
                step_data = self.__run_step_testcase(step)
            else:
                raise ParamsError(
                    f"teststep is neither a location nor a referenced testcase: {step.dict()}"
                )
        else:
            raise NotFoundError("请正确设置参数type，只可为api，ui!")

        self.__step_datas.append(step_data)
        logger.info(f"run step end: {step.name} <<<<<<\n")
        return step_data.export_vars

    def __parse_config(self, config: TConfig):
        config.variables.update(self.__session_variables)
        config.variables = parse_variables_mapping(
            config.variables, self.__project_meta.functions
        )
        config.name = parse_data(
            config.name, config.variables, self.__project_meta.functions
        )
        config.base_url = parse_data(
            config.base_url, config.variables, self.__project_meta.functions
        )

    def run_testcase(self, testcase: TestCase) -> "Pastor":
        """run specified testcase

        Examples:
            >>> testcase_obj = TestCase(config=TConfig(...), teststeps=[TStep(...)])
            >>> Pastor().with_project_meta(project_meta).run_testcase(testcase_obj)

        """
        self.__config = testcase.config
        self.__teststeps = testcase.teststeps

        # prepare
        self.__project_meta = self.__project_meta or load_project_meta(
            self.__config.path
        )
        self.__parse_config(self.__config)
        self.__start_at = time.time()
        self.__step_datas: List[StepData] = []
        self.__session = self.__session or HttpSession()
        # save extracted variables of teststeps
        extracted_variables: VariablesMapping = {}
        self.__type = step_type()
        self.__config.base_url = self.__config.base_url if self.__config.base_url else base_url()

        if self.__type == StepTypeEnum.UI:
            if not self.__driver:
                self.__driver = AutoDriver(self.__config.ignore_cache)
                self.__driver.open(self.__config.base_url)

        # run teststeps
        for step in self.__teststeps:

            # override variables
            # step variables > extracted variables from previous steps
            step.variables = merge_variables(step.variables, extracted_variables)
            # step variables > testcase config variables
            step.variables = merge_variables(step.variables, self.__config.variables)

            # parse variables
            step.variables = parse_variables_mapping(
                step.variables, self.__project_meta.functions
            )

            if isinstance(step.skip, Text) and "$" in step.skip:
                step.skip = parse_data(
                    step.skip, step.variables, self.__project_meta.functions
                )
            if step.skip is True:
                continue

            # run step
            if USE_ALLURE:
                with allure.step(f"step: {step.name}"):
                    extract_mapping = self.__run_step(step)
            else:
                extract_mapping = self.__run_step(step)

            # save extracted variables to session variables
            extracted_variables.update(extract_mapping)

        self.__session_variables.update(extracted_variables)
        self.__duration = time.time() - self.__start_at
        if self.__driver and not self.__is_reference:
            self.__driver.quit()
        return self

    def __run_sql(self, sql_datas: List[SqlData], step: TStep):
        # 按 config > env的顺序配置个本地缓存数据源，使用可以直接调用gc.engine
        if self.__config.datasource:
            datasource = os.getenv(self.__config.datasource.strip().upper(), None)
            if datasource is None:
                raise ValueError(f'未查询到数据源：{datasource}，请确认！')
            gc.engine = DBEngine(datasource)
        elif database_url():
            gc.engine = DBEngine(database_url())

        for sql_data in sql_datas:
            # 数据源顺序 step datasource > config datasource > env database_url
            _datasource = sql_data.datasource if sql_data.datasource else (
                self.__config.datasource if self.__config.datasource else database_url())
            _datasource = sql_data.datasource if sql_data.datasource else self.__config.datasource
            if _datasource:
                datasource_url = os.getenv(_datasource.strip().upper(), None)
                if datasource_url is None:
                    raise ValueError(f'未查询到env配置的数据源：{_datasource}，请确认！')
            elif database_url():
                datasource_url = database_url()
            else:
                datasource_url = None

            if datasource_url:
                db = DBEngine(datasource_url)
                gc.engine = db
                for dml in sql_data.dml:
                    result = db.fetchall(dml)
                    # [step.variables.update(r) for r in result]
                    # self.__sql_return_data = result
                    for r in result:
                        step.variables.update(r)
                        step.variables.setdefault('sql_return_data', {})
                        step.variables.get('sql_return_data').update(r)

    def run_path(self, path: Text) -> "Pastor":
        if not os.path.isfile(path):
            raise exceptions.ParamsError(f"Invalid testcase path: {path}")

        testcase_obj = load_testcase_file(path)
        return self.run_testcase(testcase_obj)

    def run(self) -> "Pastor":
        """ run current testcase

        Examples:
            >>> TestCaseRequestWithFunctions().run()

        """
        self.__init_tests__()
        testcase_obj = TestCase(config=self.__config, teststeps=self.__teststeps)
        return self.run_testcase(testcase_obj)

    def get_step_datas(self) -> List[StepData]:
        return self.__step_datas

    def get_export_variables(self) -> Dict:
        # override testcase export vars with step export
        export_var_names = self.__export or self.__config.export
        export_vars_mapping = {}
        for var_name in export_var_names:
            if var_name not in self.__session_variables:
                raise ParamsError(
                    f"failed to export variable {var_name} from session variables {self.__session_variables}"
                )

            export_vars_mapping[var_name] = self.__session_variables[var_name]

        return export_vars_mapping

    def get_summary(self) -> TestCaseSummary:
        """get testcase result summary"""
        start_at_timestamp = self.__start_at
        start_at_iso_format = datetime.utcfromtimestamp(start_at_timestamp).isoformat()
        return TestCaseSummary(
            name=self.__config.name,
            success=self.success,
            case_id=self.__case_id,
            time=TestCaseTime(
                start_at=self.__start_at,
                start_at_iso_format=start_at_iso_format,
                duration=self.__duration,
            ),
            in_out=TestCaseInOut(
                config_vars=self.__config.variables,
                export_vars=self.get_export_variables(),
            ),
            log=self.__log_path,
            step_datas=self.__step_datas,
        )

    def test_start(self, param: Dict = None) -> "Pastor":
        """main entrance, discovered by pytest"""
        self.__init_tests__()
        self.__project_meta = self.__project_meta or load_project_meta(
            self.__config.path
        )
        self.__case_id = self.__case_id or str(uuid.uuid4())
        self.__log_path = self.__log_path or os.path.join(
            self.__project_meta.RootDir, "logs", f"{self.__case_id}.run.log"
        )
        log_handler = logger.add(self.__log_path, level="DEBUG")

        # parse config name
        config_variables = self.__config.variables
        if param:
            config_variables.update(param)
        config_variables.update(self.__session_variables)
        self.__config.name = parse_data(
            self.__config.name, config_variables, self.__project_meta.functions
        )

        if USE_ALLURE:
            # update allure report meta
            allure.dynamic.title(self.__config.name)
            allure.dynamic.description(f"TestCase ID: {self.__case_id}")

        logger.info(
            f"Start to run testcase: {self.__config.name}, TestCase ID: {self.__case_id}"
        )

        try:
            return self.run_testcase(
                TestCase(config=self.__config, teststeps=self.__teststeps)
            )
        finally:
            logger.remove(log_handler)
            logger.info(f"generate testcase log: {self.__log_path}")
