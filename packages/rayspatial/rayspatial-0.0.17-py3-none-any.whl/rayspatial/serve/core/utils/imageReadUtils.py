from typing import Tuple, Optional, Any
import rasterio
import numpy as np
from rasterio.io import DatasetReader
from rasterio.transform import from_origin
from rasterio.warp import calculate_default_transform
from rasterio.errors import RasterioError
from rasterio.merge import merge

from rayspatial.serve.config.config import engine_config
from rayspatial.serve.common import constants
from rayspatial.serve.core.utils.imageUtils import ImageUtils


class ImageReadUtils:

    @staticmethod
    def read_image(
        path: str, scale: Optional[float] = None, header = None
    ) -> Tuple[np.ma.MaskedArray, dict]:
        try:
            with rasterio.open(path) as src:
                meta_data = src.meta.copy()
                resolution = ImageReadUtils._get_resolution(src)
                target_scale = scale or engine_config.scale or header.scale or 1,
                height, width = ImageReadUtils._calculate_dimensions(
                    src, resolution, target_scale
                )
                if height == 0 or width == 0:
                    data = src.read(masked=True)
                else:
                    data = ImageReadUtils._read_scaled_data(src, height, width)
                    transform = src.transform * src.transform.scale(
                        (src.width / data.shape[-1]), (src.height / data.shape[-2])
                    )
                    meta_data.update(
                        transform=transform,
                        height=height,
                        width=width,
                        crs=src.crayspatial.to_wkt(),
                        scale=target_scale,
                        dtype=src.dtypes[0],
                    )
                if isinstance(data.mask, np.bool_):
                    data.mask = bool(data.mask)
                return data, meta_data
        except RasterioError as e:
            raise RasterioError(f"read image error: {str(e)}")

    @staticmethod
    def _get_resolution(src: DatasetReader) -> Tuple[float, float]:
        x_resolution = abs(src.transform.a)
        y_resolution = abs(src.transform.e)
        if "UTM" not in src.meta["crs"].to_wkt():
            dst_crs = constants.EPSG_3857
            transform, _, _ = calculate_default_transform(
                src.crs, dst_crs, src.width, src.height, *src.bounds
            )
            x_resolution = abs(transform.a)
            y_resolution = abs(transform.e)
        return x_resolution, y_resolution

    @staticmethod
    def _calculate_dimensions(
        src: DatasetReader, resolution: Tuple[float, float], scale: float
    ) -> Tuple[int, int]:
        x_resolution, y_resolution = resolution
        h_factor = y_resolution / scale
        w_factor = x_resolution / scale

        return (int(src.height * h_factor), int(src.width * w_factor))

    @staticmethod
    def _read_scaled_data(
        src: DatasetReader, height: int, width: int
    ) -> np.ma.MaskedArray:
        return src.read(
            masked=True,
            out_shape=(src.count, height, width),
            window=((0, src.height), (0, src.width)),
        )

    @staticmethod
    def _cover_data_crs(
        data: np.ma.MaskedArray, meta: dict, dst_crs: str, header: Optional[dict]
    ) -> (np.ma.MaskedArray, dict):
        transform, width, height = calculate_default_transform(meta["crs"], dst_crs, src.width, src.height, *src.bounds)
        # 利用矩阵重投影源数据
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })
        # 创建一个内存文件对象
        memfile = rasterio.MemoryFile()
        # 利用内存文件对象输出重投影后的数据
        with memfile.open(**kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest,
                    num_threads=100
                )
        return memfile.open()

    @staticmethod
    def _cover_data_to_dataSet(
        data: np.ma.MaskedArray, meta: dict, header: Optional[dict] = None
    ) -> (rasterio.io.DatasetReader):
        memfile = rasterio.MemoryFile() 
        dst = memfile.open(**meta) 
        dst.write(data)
        src = memfile.open()
        return src
        
    
    @staticmethod
    def _cover_data_to_bounds_with_nodata(
        data: np.ma.MaskedArray, meta: dict, to_bounds: list,to_bounds_crs = constants.EPSG_4326, header: Optional[dict] = None
    ) -> (np.ma.MaskedArray, dict):
        to_bounds = ImageUtils.transform_bbox_to_crs(to_bounds,from_crs=to_bounds_crs, to_crs=meta["crs"])
        dataset = ImageReadUtils._cover_data_to_dataSet(data,meta)
        dest, transform = rasterio.merge.merge([dataset], bounds=to_bounds)
        masked_dest = np.ma.masked_equal(dest, meta["nodata"])
        meta.update({
            "transform": transform,
            "height": masked_dest.shape[1],
            "width": masked_dest.shape[2],
            "bounds": to_bounds
        })
        return masked_dest, meta
