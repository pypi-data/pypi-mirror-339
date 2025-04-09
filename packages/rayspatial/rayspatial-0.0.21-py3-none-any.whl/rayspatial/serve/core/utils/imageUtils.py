import os

import rasterio
from shapely import box
from shapely.geometry import shape
import geopandas as gpd
from rasterio.warp import transform_bounds
from rayspatial.serve.common.obj.image import Band, Image
from rayspatial.serve.common import constants


class ImageUtils:
    @staticmethod
    def transform_bbox_to_4326(bbox, from_crs):
        geometry = box(bbox[0], bbox[1], bbox[2], bbox[3])
        gdf = gpd.GeoDataFrame(geometry=[geometry], crs=from_crs)
        gdf_4326 = gdf.to_crs(epsg=4326)
        bounds = gdf_4326.geometry.iloc[0].bounds
        return [bounds[0], bounds[1], bounds[2], bounds[3]]
    
    @staticmethod
    def transform_bbox_to_crs(bbox,from_crs=constants.EPSG_4326, to_crs=constants.EPSG_3857):
        transform_bbox = list(transform_bounds(from_crs, ImageUtils.get_crs_epsg(to_crs), *bbox))
        return transform_bbox
    
    @staticmethod
    def get_crs_epsg(crs):
        try:
            return Crayspatial.from_wkt(f"{crs}").to_epsg()
        except:
            return f"{crs}"
    
    @staticmethod
    def cover_paths_to_image_obj(paths):
        image_id = os.path.basename(os.path.dirname(paths[0]))
        image = Image(id=image_id, bands=[],properties={})
        imageBbox = []
        for path in paths:
            band_id = os.path.basename(path).split(".")[0].replace(f"{image_id}_", "")
            band = Band(id=band_id, tif_url=path)
            with rasterio.open(path) as src:
                band.data_type = f"{src.dtypes[0]}"
                band.precision = str(src.profile["dtype"])
                band.max = src.meta.get("max")
                band.min = src.meta.get("min")
                band.crs = ImageUtils.get_crs_epsg(src.crs)
                band.crs_transform = list(src.transform)
                band.nodata = src.nodata
                band.width = src.width
                band.height = src.height
                band.size = src.width * src.height
                band.bbox = ImageUtils.transform_bbox_to_crs([src.bounds.left, src.bounds.bottom, src.bounds.right, src.bounds.top], src.crs, constants.EPSG_4326)
                band.geometry = f"{shape(box(*band.bbox))}"
                band.center = [band.bbox[1] + (band.bbox[3] - band.bbox[1]) / 2,band.bbox[0] + (band.bbox[2] - band.bbox[0]) / 2]
                imageBbox = band.bbox
                band.image_id = image_id
                image.bands.append(band)
        image.properties["bbox"] = imageBbox
        image.properties["center"] = [ imageBbox[1] + (imageBbox[3] - imageBbox[1]) / 2,imageBbox[0] + (imageBbox[2] - imageBbox[0]) / 2]
        return ImageUtils.sort_image_bands(image)

    @staticmethod
    def get_sort_index(band):
        try:
            return constants.LANDSATC2L2_BANDS_SORT.index(band.id)
        except ValueError:
            return len(constants.LANDSATC2L2_BANDS_SORT)
        
    @staticmethod
    def sort_image_bands(image):
        image.bands = sorted(image.bands, key=ImageUtils.get_sort_index)
        return image

