from fastapi import FastAPI

from pastor import __version__
from .routers import deps, debugtalk, debug

app = FastAPI()


@app.get("/prun/version")
async def get_prun_version():
    return {"code": 0, "message": "success", "result": {"Pastor": __version__}}


app.include_router(deps.router)
app.include_router(debugtalk.router)
app.include_router(debug.router)
