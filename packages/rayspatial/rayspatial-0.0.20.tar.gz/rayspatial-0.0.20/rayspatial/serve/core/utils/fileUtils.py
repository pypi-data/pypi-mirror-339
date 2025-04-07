import os
import glob


class FileUtils:
    @staticmethod
    def get_all_image_files(path) -> list:
        if os.path.isdir(path) is False:
            if path.endswith((".tif", ".TIF", ".tiff", ".TIFF")):
                return [path]
            else:
                raise Exception("Local file not suppose load to image")
        tif_paths = glob.glob(os.path.join(path, "*.tif"))
        tif_paths.extend(glob.glob(os.path.join(path, "*.TIF")))
        tif_paths.extend(glob.glob(os.path.join(path, "*.tiff")))
        tif_paths.extend(glob.glob(os.path.join(path, "*.TIFF")))
        return list(set(tif_paths))
