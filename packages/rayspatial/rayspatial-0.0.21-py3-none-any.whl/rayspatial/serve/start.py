from re import T
import ray
from datetime import datetime
from rayspatial.serve.config.config import engine_config,config
from ray import serve
from rayspatial.serve.serveApp import ServeApp
import os
from rayspatial.serve.logger.logger import logger

class RsEngineStart:
    
    config = engine_config
    @staticmethod
    def start():
        startTime = datetime.now()
        logger.info(f"{startTime} Hello EveryOne. This is rayspatial Engine")
        startTime = datetime.now()
        if ray.is_initialized():
            logger.info("ray is initialized.")
            return
        runtime_env = {"working_dir":os.getcwd(),"pip":{"packages":["rayspatial==0.0.21"]}}
        if RsEngineStart.config.ray_address_ip is not None:
            logger.info(f"connect ray_address: {RsEngineStart.config.ray_address_ip}")
            ray.init(
                f"ray://{RsEngineStart.config.ray_address_ip}:{RsEngineStart.config.ray_address_port}",
                runtime_env=runtime_env
            )
            serve.start(http_options={"host": RsEngineStart.config.ray_address_ip, "port": config.config_ray["serve_port"]})
        else:
            ray.init(runtime_env=runtime_env)
            serve.start(http_options={"host": "0.0.0.0", "port": config.config_ray["serve_port"]})
        num_cpus = ray.available_resources().get("CPU",0)
        num_gpus = ray.available_resources().get("GPU",0)
        replicas_cpu = 0.2
        replicas_num = "auto"
        logger.info(f"ray cluster resources: {num_cpus} cpus, {num_gpus} gpus , replicas_num: auto")
        ServeApplication = ServeApp.options(num_replicas= replicas_num,ray_actor_options={"num_cpus":replicas_cpu}).bind()
        serve.run(ServeApplication, name="RsEngineServe",route_prefix="/rs",logging_config={
        "encoding": "JSON",
        "log_level": "DEBUG",
        "enable_access_log": True,
    })
        logger.info(
            f"{datetime.now()}rayspatialEngine Started . Use Time :{datetime.now() - startTime} , replicas_num: {replicas_num}"
        )
        return

    @staticmethod
    def stop():
        serve.shutdown()
        ray.shutdown()
        logger.info("Rs Engine Stopped.")

    def set_config(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self.config, key, value)
        return


RsEngine = RsEngineStart()
