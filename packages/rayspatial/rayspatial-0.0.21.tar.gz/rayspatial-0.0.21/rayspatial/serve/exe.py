import copy
from datetime import datetime
import logging

from rayspatial.serve.common.obj.execute import ExecuteOperationModel
from rayspatial.serve.common.route import Routers
from rayspatial.serve.core.utils.resultHandle import handle_result
from rayspatial.serve.router.imageRouter import imageRoutes
from rayspatial.serve.router.datasourceRouter import datasourceRoutes
from rayspatial.serve.router.imageCollectionRouter import imageCollectionRoutes
from fastapi.encoders import jsonable_encoder
from rayspatial.serve.config.config import engine_config
from tqdm import tqdm
from rayspatial.serve.common.obj.requestHeader import RsHeader
import uuid
import logging

class ServeExecute:

    all_routes = {
        "image": imageRoutes,
        "datasource": datasourceRoutes,
        "imageCollection": imageCollectionRoutes,
    }

    @staticmethod
    def update_param(orgParams, resMap: dict, header, router):
        if isinstance(orgParams, str):
            return ServeExecute.update_param_string(orgParams, resMap, header, router)

        for k, v in orgParams.items():
            orgParams[k] = ServeExecute.update_param_value(v, resMap, header, router)

        return orgParams

    @staticmethod
    def update_param_string(orgParams, resMap: dict, header, router):
        if orgParams.startswith("$") and resMap.get(orgParams) is None:
            return {}
        return copy.deepcopy(resMap.get(orgParams, orgParams))

    @staticmethod
    def update_param_value(value, resMap: dict, header, router):
        if (
            isinstance(value, str)
            and value.startswith("$")
            and resMap.get(value) is None
        ):
            return {}
        if isinstance(value, str) and (resMap.get(value) is not None):
            return copy.deepcopy(resMap.get(value))
        if isinstance(value, dict):
            return ServeExecute.update_param_dict(value, resMap, header, router)
        if isinstance(value, list):
            return ServeExecute.update_param_list(value, resMap, header, router)
        return value

    @staticmethod
    def update_param_dict(value: dict, resMap: dict, header, router):
        for k1, v1 in value.items():
            value[k1] = ServeExecute.update_param_value(v1, resMap, header, router)
        return value

    @staticmethod
    def update_param_list(value: list, resMap: dict, header, router):
        resV = []
        for item in value:
            resV.append(ServeExecute.update_param_value(item, resMap, header, router))
        return resV

    @staticmethod
    def update_header(header):
        header.id  = f"{uuid.uuid4()}"
        if engine_config.scale is not None:
            header.scale = engine_config.scale
            logging.info(f"scale:{engine_config.scale}")
            
    @staticmethod
    def execute_serve(params: dict, header):
        executeOperationModel = ExecuteOperationModel(**params)
        header = RsHeader(**header)
        cur_res_map = {}
        response = None
        totalStep = len(executeOperationModel.operatorArr)
        ServeExecute.update_header(header)
        for index, executeOpera in tqdm(
            enumerate(executeOperationModel.operatorArr), desc="execute progress"
        ):
            response = None
            stepStartTime = datetime.now()
            inputParams = ServeExecute.update_param(
                executeOpera.params, cur_res_map, header, executeOpera.router
            )
            if executeOpera.order in cur_res_map.keys():
                response = copy.deepcopy(cur_res_map.get(executeOpera.order))
            else:
                baseRoute = executeOpera.router.split("/")[1]
                cur_route_func = ServeExecute.all_routes.get(
                    baseRoute, Routers()
                ).routes_map.get(executeOpera.router)
                if cur_route_func is None:
                    raise Exception(
                        f"Router not exist router:{executeOpera.router}, order:{executeOpera.order}"
                    )
                cur_header = copy.deepcopy(header)
                try:
                    cur_params = cur_route_func.param_info.get("inputParams")(**inputParams)
                except Exception as e:
                    logging.error(f"execute error :router:{executeOpera.router}, order:{executeOpera.order}, error: params not valid, error:{e}, inputParams:{inputParams}")
                    raise e
                response = cur_route_func.func(cur_header, cur_params)
            cur_res_map.update({f"{executeOpera.order}": response})
            stepEndTime = datetime.now()
            logging.debug(
                f"step {index + 1}/{totalStep}: {executeOpera.order} 【{executeOpera.router}】cost time:{(stepEndTime - stepStartTime).total_seconds() * 1000} ms"
            )
        return jsonable_encoder(handle_result(response), exclude_none=True)

    