import imp
import os
from typing import Tuple, Union
from rayspatial.serve.config.config import config
from rayspatial.serve.common.obj.imageCollection import ImageCollection
from rayspatial.serve.common.obj.image import Band, Image
from pathlib import Path 
from shapely.geometry import Polygon
from fastapi.encoders import jsonable_encoder
from shapely import wkb
import planetary_computer
import pandas as pd
import pyarrow as pa
import pyarrow.dataset as ds
from rayspatial.serve.common.constants import STAC_COLLECTION_BAND_MAPS
import logging
class DatasourceBase:
    
    @staticmethod
    def filter_scenes(dataset, **kwargs):
        """
        Filter collection creating new view.

        Parameters
        ----------
        **kwargs :
            Supported filters:
            - cloud_cover_lt: float
            - date_range: Tuple[str, str]
            - bbox: Tuple[float, float, float, float]
        """
        filter_expr = None

        # Build filter expression
        if len(dataset.to_table()) == 0:
            return dataset

        if "cloud_cover_lt" in kwargs:
            if "eo:cloud_cover" not in dataset.schema.names:
                raise ValueError("Collection has no cloud cover data")

            if not isinstance(kwargs["cloud_cover_lt"], (int, float)):
                raise ValueError("Invalid cloud cover value")
            elif kwargs["cloud_cover_lt"] < 0 or kwargs["cloud_cover_lt"] > 100:
                raise ValueError("Invalid cloud cover value")

            filter_expr = ds.field("eo:cloud_cover") < kwargs["cloud_cover_lt"]

        if "date_range" in kwargs:
            if "datetime" not in dataset.schema.names:
                raise ValueError("Collection has no datetime data")

            start, end = kwargs["date_range"]

            if not (start and end):
                raise ValueError("Invalid date range")
            elif start > end:
                raise ValueError("Invalid date range")
            elif start == end:
                raise ValueError("Date range must be > 1 day")
            elif len(start) != 10 or len(end) != 10:
                raise ValueError("Date format must be 'YYYY-MM-DD'")

            start_ts = pd.Timestamp(start).tz_localize("UTC")
            end_ts = pd.Timestamp(end).tz_localize("UTC")

            # Convert to Arrow timestamps
            start_timestamp = pa.scalar(start_ts, type=pa.timestamp("us", tz="UTC"))
            end_timestamp = pa.scalar(end_ts, type=pa.timestamp("us", tz="UTC"))

            date_filter = (ds.field("datetime") >= start_timestamp) & (
                ds.field("datetime") <= end_timestamp
            )
            filter_expr = (
                date_filter if filter_expr is None else filter_expr & date_filter
            )

        if "bbox" in kwargs:
            if "scene_bbox" not in dataset.schema.names:
                raise ValueError("Collection has no bbox data")
            bbox = kwargs["bbox"]

            if len(bbox) != 4:
                raise ValueError("Invalid bbox format")
            elif bbox[0] > bbox[2] or bbox[1] > bbox[3]:
                raise ValueError("Invalid bbox coordinates")
            elif any(not isinstance(coord, (int, float)) for coord in bbox):
                raise ValueError("Invalid bbox coordinates")

            bbox_filter = (
                (ds.field("scene_bbox").x0 >= bbox[0])
                & (ds.field("scene_bbox").y0 >= bbox[1])
                & (ds.field("scene_bbox").x1 <= bbox[2])
                & (ds.field("scene_bbox").y1 <= bbox[3])
            )
            filter_expr = (
                bbox_filter if filter_expr is None else filter_expr & bbox_filter
            )

        if "geometries" in kwargs:
            if "scene_bbox" not in  dataset.schema.names:
                raise ValueError("Collection has no bbox data")
            geometries = kwargs["geometries"]

            if not all(isinstance(geom, Polygon) for geom in geometries):
                raise ValueError("Invalid geometry format")

            bbox_filters = [
                (ds.field("scene_bbox").x0 >= geom.bounds[0])
                & (ds.field("scene_bbox").y0 >= geom.bounds[1])
                & (ds.field("scene_bbox").x1 <= geom.bounds[2])
                & (ds.field("scene_bbox").y1 <= geom.bounds[3])
                for geom in geometries
            ]
            filter_expr = bbox_filters[0]
            for bbox_filter in bbox_filters[1:]:
                filter_expr |= bbox_filter
        
        if "id" in kwargs:
            if "id" not in dataset.schema.names:
                raise ValueError("Collection has no id data")
            id_filter = ds.field("id") == kwargs["id"]
            filter_expr = id_filter if filter_expr is None else filter_expr & id_filter
        
        if "ids" in kwargs:
            if "id" not in dataset.schema.names:
                raise ValueError("Collection has no id data")
            id_filter = ds.field("id").isin(kwargs["ids"])
            filter_expr = id_filter if filter_expr is None else filter_expr & id_filter

        if filter_expr is None:
            raise ValueError("No valid filters provided")

        filtered_dataset = dataset.filter(filter_expr)
        return filtered_dataset
    @classmethod
    def _format_date_range(
        cls, start_date: pd.Timestamp, end_date: pd.Timestamp
    ) -> str:
        """Format date range for collection name."""
        if start_date.year == end_date.year:
            return f"{start_date.strftime('%Y%m')}-{end_date.strftime('%m')}"
        return f"{start_date.strftime('%Y%m')}-{end_date.strftime('%Y%m')}"
    @classmethod
    def create_name(
        cls, custom_name: str, date_range: Tuple[str, str], data_source: str
    ) -> str:
        """Create standardized collection name."""
        if "_" in custom_name:
            raise ValueError("Custom name cannot contain underscore (_)")

        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])

        name_parts = [
            custom_name.lower().replace(" ", "-"),
            cls._format_date_range(start_date, end_date),
            data_source.split("-")[0].lower(),
        ]
        return "_".join(name_parts)
    
    @classmethod
    def from_local(cls, path: Union[str, Path]):
        """
        Create collection from local partitioned dataset.

        Parameters
        ----------
        path : str or Path
            Path to dataset directory with Hive-style partitioning
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Dataset not found at {path}")

        try:
            dataset = ds.dataset(
                str(path),
                format="parquet",
                partitioning=ds.HivePartitioning(
                    pa.schema([("year", pa.int32()), ("month", pa.int32())])
                ),
                exclude_invalid_files=True,
                filesystem=None,
            )
        except Exception as e:
            raise ValueError(f"Invalid dataset at {path}: {str(e)}")

        return dataset
    
        
    @staticmethod
    def get_stac_parquet_to_images(org_collection_name,date_range, params):
        collection_name = DatasourceBase.create_name("rs", date_range, str(org_collection_name))
        collection_path = Path(config.config_base.get('home_dir'),f"{config.config_base.get('stac_dir')}",f"{collection_name}_stac")
        if not collection_path.exists():
            raise Exception(f"Collection {org_collection_name} not found in local stac directory")
        collection = DatasourceBase.from_local(collection_path)
        filterCollection = DatasourceBase.filter_scenes(collection, **jsonable_encoder(params, exclude_none=True))
        df = filterCollection.to_table().to_pandas()
        images = []
        for index, d in df.iterrows():
            image = Image(bands=[],id=d['id'])
            imageGeometry = wkb.loads(d['geometry'])
            image.properties = {
                "datetime": d['datetime'],
                "geometry":  imageGeometry.wkt,
                "bbox": d['bbox'],
                "center": [imageGeometry.centroid.y, imageGeometry.centroid.x]
            }
            for k,v in d["assets"].items():
                if "image/tiff" in v["type"] or "image/geotiff" in v["type"]:
                    band = Band()
                    band.id = STAC_COLLECTION_BAND_MAPS.get(org_collection_name,{}).get(k,k)
                    band.tif_url = planetary_computer.sign_url(v["href"], copy=False)
                    band.properties = {
                        "datetime": d['datetime'],
                        "bbox": list(d['bbox'].values()),
                        "center": [imageGeometry.centroid.y, imageGeometry.centroid.x]
                    }
                    image.bands.append(band)
            images.append(image)
        return images
    
    
    
    def _datasource_stac_imageCollection(self, header, params):
        collections = params.collections
        imageCollections = ImageCollection()
        date_range = params.datetime
        images = []
        for collection in collections:
            imageCollections.id = collection
            images.extend(self.get_stac_parquet_to_images(collection, date_range, params))
        imageCollections.images = images
        return imageCollections
    
    
    
    
    def _datasource_stac_image(self, header, params):
        logger.debug("---------_stac_image---------")
        collections = params.collections
        date_range = params.datetime
        images = []
        images.extend(self.get_stac_parquet_to_images(collections[0], date_range, params))
        return images[0]
        