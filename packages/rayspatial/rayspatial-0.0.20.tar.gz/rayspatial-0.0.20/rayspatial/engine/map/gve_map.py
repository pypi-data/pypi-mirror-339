# !/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from ipyleaflet import Map, basemaps, WMSLayer, TileLayer, projections, LayersControl
from typing import Iterator
from xyzservices.lib import TileProvider
from rayspatial import engine
from rayspatial.engine.map.gve_layer import GVEGeometryLayer, GVEImageLayer, GVEVectorLayer
from rayspatial.engine.serialize.serializer import serializer
from rayspatial.engine.function_node import Rs
import ipyleaflet



def _layer_name_generator(i: int = 1) -> Iterator:
    while True:
        yield "Layer %d" % i
        i += 1


class Map(ipyleaflet.Map):
    base = TileProvider({
        # "url": "https://tiles1.geovisearth.com/base/v1/img/{z}/{x}/{y}?format=webp&tmsIds=w&token=8ea497106a52a8e07dc2df6172fbc392d8aa90113cca67511b783e29d2c75bd7",
        "url": "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        "name": "img", "attribution": "geovisLayer"
    })
    cia = TileLayer(
        url='https://tiles3.geovisearth.com/base/v1/cia/{z}/{x}/{y}?clientId=99f564cd-50be-4e41-8b00-02aef8868b2b&secretId=6v0CDo9hSZmDQ2ZaEF-MXOs93Pk&sign=43e32712689f1b8bebd51332b7c40c58135e1eae64cce9ce015946a9c7bec4dc&expireTime=10334598503',
        format='image/png',
        name="注记",
        transparent=True
    )

    def __init__(self, **kwargs):
        self._layer_name_iterator = _layer_name_generator()
        # zoom
        kwargs["crs"] = projections.EPSG3857
        # basemap
        kwargs["basemap"] = Map.base
        # scroll_wheel_zoom
        kwargs["scroll_wheel_zoom"] = True
        # center
        if "center" not in kwargs.keys():
            # Beijing
            kwargs["center"] = (39.916668, 116.383331)
        else:
            center = kwargs["center"]
            kwargs["center"] = (center[1], center[0])
        # zoom
        if "zoom" not in kwargs.keys():
            kwargs["zoom"] = 4
        # style
        if "height" not in kwargs.keys():
            self._height = "600px"

        else:
            if isinstance(kwargs["height"], int):
                self._height = str(kwargs["height"]) + "px"
            else:
                self._height = kwargs["height"]
            kwargs.pop("height")
        self._width = "100%"
        self.kwargs = kwargs
        super().__init__(**kwargs)

        self.layout.height = self._height
        self.layout.width = self._width
        self.add_control(ipyleaflet.LayersControl(position="topright"))
        # self.add_layer(Map.cia)

        def transform_tuples(tuple1, tuple2):
            return (tuple1[1], tuple1[0], tuple2[1], tuple2[0])

        def update_zoom_level(change):
            # zoom_level_widget.value = f'当前缩放级别: {change}'
            # 更新缩放级别
            if change['name'] == 'zoom':
                self.zoom = change.new

            # 更新中心点
            if change['name'] == 'bounds':
                self.bbox = transform_tuples(change['new'][0], change['new'][1])

        self.observe(update_zoom_level, names=['bounds', 'zoom'])

    def add_rs_layer(self, gve_object, name=None, **kwargs):
        from rayspatial.engine.function_node import Rs
        if name is None:
            name = self._layer_name_iterator.__next__()
        # if isinstance(gve_object, (engine.Feature, engine.FeatureCollection)):
        #     self.add_layer(GVEGeometryLayer(name, gve_object, **kwargs))
        if isinstance(gve_object, engine.AI):
            payload = gve_object.getInfo()
            self.center = payload.get("center")
            self.add_layer(GVEGeometryLayer(name, payload, **kwargs))
        elif isinstance(gve_object, dict):
            if gve_object.get("type") == "Mbtiles":
                pbf_url = gve_object.get("url")
                self.add_layer(GVEVectorLayer(name, pbf_url))
            elif gve_object.get("type") == "Image":
                self.center = (gve_object.get("center")[1], gve_object.get("center")[0])
                self.add_layer(GVEImageLayer(name, gve_object))
        elif isinstance(gve_object, engine.Image):
            payload = gve_object.getInfo()
            self.center = (payload.get("center")[1], payload.get("center")[0])
            if payload.get("type") == "Mbtiles":
                pbf_url = payload.get("url")
                self.add_layer(GVEVectorLayer(name, pbf_url))
            elif payload.get("type") == "Image":
                self.add_layer(GVEImageLayer(name, payload))
            # self.add_layer(GVEImageLayer(name, gve_object, **kwargs))
        rayspatial.step = []
        rayspatial.params = {}
        rayspatial.stepNum = 0
        rayspatial.node_chain_dict = dict()

    addLayer = add_rs_layer


