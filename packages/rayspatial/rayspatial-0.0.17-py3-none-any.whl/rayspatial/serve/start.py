import ray
from datetime import datetime
from rayspatial.serve.config.config import engine_config,config
from ray.runtime_env import RuntimeEnv
from rayspatial.serve.logger.logger import logger
from ray import serve
from rayspatial.serve.serveApp import ServeApp
import os

class RsEngineStart:
    ServeApplication = ServeApp.bind()
    config = engine_config
    @staticmethod
    def start():
        startTime = datetime.now()
        logger.info(f"{startTime} Hello EveryOne. This is rayspatial Engine")
        startTime = datetime.now()
        print(f"{startTime} Hello EveryOne . This is ray spatial Engine")
        if ray.is_initialized():
            logger.info("ray is initialized.")
            return
        if RsEngineStart.config.ray_address_ip is not None:
            logger.info(f"connect ray_address: {RsEngineStart.config.ray_address_ip}")
            # 使用uv作为依赖管理工具
            runtime_env = {"working_dir":os.getcwd(),"pip":{"packages":["rayspatial==0.0.13"]}}
            ray.init(
                f"ray://{RsEngineStart.config.ray_address_ip}:{RsEngineStart.config.ray_address_port}",
                runtime_env=runtime_env
            )
            serve.start(http_options={"host": RsEngineStart.config.ray_address_ip, "port": config.config_ray["serve_port"]})
        else:
            # 本地模式下同样使用uv
            runtime_env = {"working_dir":os.getcwd(),"pip":{"packages":["rayspatial==0.0.13"]}}
            ray.init(runtime_env=runtime_env)
            serve.start(http_options={"host": "0.0.0.0", "port": config.config_ray["serve_port"]})
        serve.run(RsEngineStart.ServeApplication, route_prefix="/rs")
        print(
            f"{datetime.now()}rayspatialEngine Started . Use Time :{datetime.now() - startTime}"
        )
        return

    @staticmethod
    def stop():
        serve.shutdown()
        ray.shutdown()
        print("Rs Engine Stopped.")

    def set_config(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self.config, key, value)
        return


RsEngine = RsEngineStart()
