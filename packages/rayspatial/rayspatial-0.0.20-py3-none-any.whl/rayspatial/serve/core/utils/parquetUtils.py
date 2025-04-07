import geopandas as gpd
from rayspatial.serve.common.obj.image import Image, Band
import requests

def get_stac_datasource_token(collection):
    try:
        res = requests.get(f"https://planetarycomputer.microsoft.com/api/sas/v1/token/{collection}").json()
        return res.get("token")
    except Exception as e:
        raise Exception(f"stac datasource get {collection} token failed")

def cover_stac_df_to_images(df, collection):
    token = get_stac_datasource_token(collection)
    res = df.to_dict(orient="records")
    images = []
    for item in res:
        image = Image(properties={},bands=[])
        image.id = item.get("image_id")
        image.properties.update({"datetime":item.get("datetime")})
        if item.get("bands"):
            for bandId, band in item.get("bands").items():
                if band:
                    band_obj = Band()
                    band_obj.id = bandId
                    band_obj.tif_url = f"{band.get('href')}?{token}"
                    image.bands.append(band_obj)
        
        images.append(image)
    
    return images

def read_stac_parquet_to_images(path, sql, collection):
    df = gpd.read_parquet(path)
    resDF = df.query(sql)
    res = cover_stac_df_to_images(resDF, collection)
    return res