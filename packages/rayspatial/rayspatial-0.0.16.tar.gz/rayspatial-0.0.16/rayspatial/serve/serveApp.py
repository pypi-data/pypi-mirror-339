from starlette.requests import Request
from ray import serve
import ray

@serve.deployment(num_replicas='auto',target_ongoing_requests=1, ray_actor_options={"num_cpus": 0.2, "num_gpus": 0})
class ServeApp:
    async def __call__(self, request: Request):
        import rayspatial
        print(f"{rayspatial.__version__}")
        requestJson = await request.json()
        params = requestJson["params"]
        header = requestJson["header"]
        return rayspatial.serve.exe.ServeExecute.execute_serve(params, header)