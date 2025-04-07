from starlette.requests import Request
from ray import serve
import logging
@serve.deployment
class ServeApp:
    async def __call__(self, request: Request):
        import rayspatial
        logging.info(f"{rayspatial.__version__}")
        requestJson = await request.json()
        params = requestJson["params"]
        header = requestJson["header"]
        return rayspatial.serve.exe.ServeExecute.execute_serve(params, header)