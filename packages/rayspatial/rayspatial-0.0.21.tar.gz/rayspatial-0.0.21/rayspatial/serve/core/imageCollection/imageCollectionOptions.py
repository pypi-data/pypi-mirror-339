from geopandas import GeoDataFrame
import pandas as pd
from rayspatial.serve.common.obj.image import Image
from rayspatial.serve.core.dataframe.imageDataFrame import ImageDataFrame
import rasterio
import numpy.ma as ma
import numpy as np
class ImageCollectionOptions:
    
    @staticmethod
    def mosaic(header, images: list[Image],method:str):
        def mosaic_type_aggfunc(type):
            print("--------------------",type)
            if type == "median":
                return lambda x: np.ma.median(np.ma.stack(x), axis=0)
            elif type == "mean":
                return lambda x: np.ma.mean(np.ma.stack(x), axis=0)
            elif type == "max":
                return lambda x: np.ma.max(np.ma.stack(x), axis=0)
            elif type == "min":
                return lambda x: np.ma.min(np.ma.stack(x), axis=0)
            elif type == "sum":
                return lambda x: np.ma.sum(np.ma.stack(x), axis=0)
            elif type == "std":
                return lambda x: np.ma.std(np.ma.stack(x), axis=0)
            elif type == "count":
                return lambda x: np.ma.count(np.ma.stack(x), axis=0)
            elif type in ["first", "last"]:
                def fill_masked_areas(arrays):
                    if len(arrays) == 0:
                        return np.nan
                    # 根据类型选择起始数组和遍历方向
                    result = arrays[0].copy() if type == "first" else arrays[-1].copy()
                    mask = np.ma.getmask(result)
                    if not np.any(mask):
                        return result
                    # 根据类型决定遍历序列
                    arr_sequence = arrays[1:] if type == "first" else reversed(arrays[:-1])
                    for arr in arr_sequence:
                        current_mask = np.ma.getmask(result)
                        if not np.any(current_mask):
                            break
                        fill_positions = current_mask & ~np.ma.getmask(arr)
                        if np.any(fill_positions):
                            result[fill_positions] = arr[fill_positions]
                    final_mask = np.ma.getmask(result)
                    return np.ma.masked_array(result, mask=final_mask) if np.any(final_mask) else result
                return fill_masked_areas
            else:
                raise ValueError(f"Invalid mosaic type: {type}")
        all_bands_dataFrame_list = []
        for image in images:
            image = ImageDataFrame.format_image_bands_data(image, header)
            all_bands_dataFrame_list.append(image.bands_data)
        all_bands_dataFrame = GeoDataFrame(pd.concat(all_bands_dataFrame_list, ignore_index=True))
        # 定义聚合函数，对band_data使用numpy.ma.mean进行掩码平均，其他列取第一个值
        aggfunc = {col: (mosaic_type_aggfunc(method)) if col == 'band_data' else 'first' 
                   for col in all_bands_dataFrame.columns if col not in ['id','geometry']}
        # 使用dissolve进行镶嵌操作
        mosaic_bands = all_bands_dataFrame.dissolve(by='id', aggfunc=aggfunc).reset_index()
        mosaic_image = images[0]
        mosaic_image.bands_data = mosaic_bands
        return mosaic_image