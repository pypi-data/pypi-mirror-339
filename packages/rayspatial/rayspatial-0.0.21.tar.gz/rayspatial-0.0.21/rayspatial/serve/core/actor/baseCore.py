from rayspatial.serve.core.image.imageBase import ImageBase
from rayspatial.serve.core.datasource.datasourceBase import DatasourceBase
from rayspatial.serve.core.imageCollection.imageCollectionBase import ImageCollectionBase
class BaseCore(ImageBase, DatasourceBase, ImageCollectionBase ):
    def __init__(self):
        pass



