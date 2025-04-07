# !/usr/bin/env python
# -*- coding: utf-8 -*-


from ipyleaflet import GeoJSON, WMSLayer, VectorTileLayer


class GVEVectorLayer(VectorTileLayer):
    def __init__(self, name, url, **kwargs):
        super().__init__(url=url, name=name, **kwargs)


class GVEGeometryLayer(GeoJSON):
    def __init__(self, name: str, gve_object, style: dict = None, **kwargs):
        if style is None:
            style = {}
        new_kwargs = {
            "data": gve_object,
            "name": name,
            "style": style,
            "hover_style": {}
        }
        new_kwargs.update(kwargs)
        super().__init__(**new_kwargs)


class GVEImageLayer(WMSLayer):
    def __init__(self, name: str, gve_object, **kwargs):
        if isinstance(gve_object, dict):
            url = gve_object.get("bands")[0].get("tif_url")
            url = "https://api3.geovisearth.com/titiler/cog/tile/{z}/{x}/{y}.png?url=" + url + "&"
            new_kwargs = {
                "url": url,
                "name": name,
                "hover_style": {},
                "style_callback": None,
            }
            new_kwargs.update(kwargs)
            super().__init__(**new_kwargs)

