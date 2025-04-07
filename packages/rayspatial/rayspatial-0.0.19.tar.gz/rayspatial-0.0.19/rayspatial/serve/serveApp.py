from starlette.requests import Request
from ray import serve
import ray

@serve.deployment
class ServeApp:
    async def __call__(self, request: Request):
        import rayspatial
        print(f"{rayspatial.__version__}")
        requestJson = await request.json()
        params = requestJson["params"]
        header = requestJson["header"]
        return rayspatial.serve.exe.ServeExecute.execute_serve(params, header)