import os.path
import rasterio
from datetime import datetime

from rayspatial.serve.config.config import config


class ImageWriteUtils:
    @staticmethod
    def write_band(bandDf):
        if bandDf.data_change_flag:
            tmp_file = os.path.join(
                config.config_base.get("temp_dir"),
                bandDf.flag_id,
                bandDf.image_id,
                f"{bandDf.image_id}_{bandDf.id}.TIF",
            )
            if os.path.exists(tmp_file):
                new_flag_id = datetime.now().strftime(
                    f"%Y_%m{os.sep}%d{os.sep}%H%M%S%f"
                )
                bandDf.flag_id = new_flag_id
                tmp_file = os.path.join(
                    config.config_base.get("temp_dir"),
                    new_flag_id,
                    bandDf.image_id,
                    f"{bandDf.image_id}_{bandDf.id}.TIF",
                )
            os.makedirs(os.path.dirname(tmp_file), exist_ok=True)
            meta = bandDf.meta
            meta.update({"driver": "COG"})
            meta.update({"compress": "deflate"})
            del meta["scale"]
            del meta["bounds"]
            with rasterio.open(tmp_file, "w", **meta) as dst:
                dst.write(bandDf.band_data)
            return os.path.abspath(tmp_file)
        return bandDf.tif_url
