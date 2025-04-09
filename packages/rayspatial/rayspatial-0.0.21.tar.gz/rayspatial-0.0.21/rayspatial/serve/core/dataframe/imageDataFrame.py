from geopandas import GeoDataFrame
from shapely.wkt import loads
from rayspatial.serve.common.obj.image import Image, Band
from rayspatial.serve.core.utils.imageReadUtils import ImageReadUtils
from rayspatial.serve.core.utils.imageWriteUtils import ImageWriteUtils
from rayspatial.serve.common import constants


class ImageDataFrame:
    # ------- imageDataFrame -------
    # bands_data: GeoDataFrame
    # id | type |crs |crs_transform|data_type|max|min|precision|tif_url|properties|nodata|geometry|image_id|width|height|size|bbox|center|band_data|image_id|data_change_flag|flag_id|meta

    @staticmethod
    def format_image_bands_data(image: Image, header):
        if image.bands_data is not None or not image.bands:
            return image
        datas = []
        for band in image.bands:
            band_item = band.model_dump()
            tif_data, tif_meta, geometry = ImageReadUtils.read_image(band.tif_url, header=header)
            band_item.update({"image_id": image.id})
            band_item.update({"band_data": tif_data})
            band_item.update({"data_change_flag": True})
            band_item.update({"flag_id": image.flag_id})
            band_item.update({"meta": tif_meta})
            band_item.update({"geometry": loads(geometry)})
            image.properties.update({"geometry": geometry})
            datas.append(band_item)
        image.bands_data = GeoDataFrame(
            datas,
            geometry=[
                loads(
                    f"{d.get('geometry') if d.get('geometry') else image.properties.get('geometry')}"
                )
                for d in datas
            ],
            crs= constants.EPSG_4326,
        )
        return image

    @staticmethod
    def ignore_image_dataframe_to_image(imagedf: Image):
        if imagedf.bands_data is None:
            return imagedf
        bands = []
        for index, row in (
            imagedf.bands_data.iterrows() if imagedf.bands_data is not None else []
        ):
            row.tif_url = ImageWriteUtils.write_band(row)
            row.geometry = f"{row.geometry}"
            row.band_data = None
            bands.append(Band.model_validate(row.to_dict()))
        if bands:
            imagedf.bands = bands
        imagedf.bands_data = None
        return imagedf

    @staticmethod
    def two_image_operate(op1, op2, operate):
        if isinstance(op2, (int, float)):
            op1.bands_data.band_data = eval(f"op1.bands_data.band_data {operate} op2")
        else:
            if op1.bands_data is None:
                return op2
            if op2.bands_data is None:
                return op1
            if (
                len(op1.bands) != len(op2.bands)
                and len(op1.bands) != 1
                and len(op2.bands) != 1
            ):
                raise ValueError(
                    f"Images must contain the same number of bands or only 1 band. Got {len(op1.bands)} and {len(op2.bands)}"
                )
            op1_data = op1.bands_data.reset_index(drop=True)
            op2_data = op2.bands_data.reset_index(drop=True)
            if len(op1_data) == 1 and len(op2_data) > 1:
                shorter_row = op1_data.iloc[0]
                result_data = op2_data.copy()
                for idx in range(len(op2_data)):
                    result_data.at[idx, "band_data"] = eval(
                        f"shorter_row['band_data'] {operate} op2_data.at[idx, 'band_data']"
                    )
            elif len(op2_data) == 1 and len(op1_data) > 1:
                shorter_row = op2_data.iloc[0]
                result_data = op1_data.copy()
                for idx in range(len(op1_data)):
                    result_data.at[idx, "band_data"] = eval(
                        f"op1_data.at[idx, 'band_data'] {operate} shorter_row['band_data']"
                    )
            elif len(op1_data) == len(op2_data):
                result_data = op1_data.copy()
                for idx in range(len(op1_data)):
                    result_data.at[idx, "band_data"] = eval(
                        f"op1_data.at[idx, 'band_data'] {operate} op2_data.at[idx, 'band_data']"
                    )
            op1.bands_data = result_data
            op1.bands_data.tif_url = None
            op1.bands_data.data_change_flag = True
        return op1

    @staticmethod
    def images_operate(images, operate, header):
        if len(images) <= 1:
            return images
        else:
            for i in range(len(images) - 1):
                images[i + 1] = ImageDataFrame.format_image_bands_data(
                    images[i + 1], header
                )
            median_data = np.median(
                [img.bands_data.band_data for img in images], axis=0
            )
            images[0].bands_data.band_data = median_data
            images[0].bands_data.tif_url = None
            images[0].bands_data.data_change_flag = True
            return images[0]
