import requests
from rayspatial.serve.config.config import engine_config,config
class ServeApi:
    @staticmethod
    def execute_serve_api(params,header):
        p = {"params": params, "header": header}
        if engine_config.ray_address_ip is None:
            serve_exe_result = requests.post(f"http://0.0.0.0:{config.config_ray['serve_port']}/rs", json=p)
        else:
            serve_exe_result = requests.post(f"http://{engine_config.ray_address_ip}:{config.config_ray['serve_port']}/rs", json=p)
        return serve_exe_result