# !/usr/bin/env python
# -*- coding: utf-8 -*-

from rayspatial.engine.function_node import FunctionNode
from rayspatial.engine.function_helper import FunctionHelper
from rayspatial.serve.core.error.gve_error import RSError, RSErrorCode


class Geometry(FunctionNode):
    def __init__(self, geoJson=None):
        self.resp = None
        data = {"geometry": geoJson["geometry"], "proj": geoJson["proj"]}
        super(Geometry, self).__init__("Image", data)
        self.updateStep("/geometry", data, self)

    @staticmethod
    def BBox(west: [int, float], south: [int, float], east: [int, float], north: [int, float]):
        if west is not None and not isinstance(west, (int, float)):
            raise RSError(
                RSErrorCode.ARGS_ERROR, f"west only supports arguments of type (int,float), passed in as type{type(west)}"
            )

        if south is not None and not isinstance(south, (int, float)):
            raise RSError(
                RSErrorCode.ARGS_ERROR, f"south only supports arguments of type (int,float), passed in as type{type(south)}"
            )

        if east is not None and not isinstance(east, (int, float)):
            raise RSError(
                RSErrorCode.ARGS_ERROR, f"east only supports arguments of type (int,float), passed in as type{type(east)}"
            )

        if north is not None and not isinstance(north, (int, float)):
            raise RSError(
                RSErrorCode.ARGS_ERROR, f"north only supports arguments of type (int,float), passed in as type{type(north)}"
            )

        data = {
            "coordinates": [west, south, east, north]
        }
        for i in data["coordinates"]:
            if not i:
                raise RSError(RSErrorCode.ARGS_ERROR, "The coordinates parameter is incomplete")

        return FunctionHelper.apply(
            "Geometry.BBox", "engine.Geometry", data
        )

    @staticmethod
    def LinearRing(coordinates: list):
        if coordinates is not None and not isinstance(coordinates, list):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"coordinates only supports arguments of type list, passed in as {type(coordinates)}",
            )
        data = {
            "coordinates": coordinates,
        }
        if "coordinates" not in data:
            raise RSError(RSErrorCode.ARGS_ERROR, "The coordinates parameter cannot be empty")

        return FunctionHelper.apply(
            "Geometry.LinearRing", "engine.Geometry", data
        )

    @staticmethod
    def LineString(coordinates: list):
        if coordinates is not None and not isinstance(coordinates, list):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"coordinates only supports arguments of type list, passed in as {type(coordinates)}",
            )
        data = {
            "coordinates": coordinates,
        }
        if "coordinates" not in data:
            raise RSError(RSErrorCode.ARGS_ERROR, "The coordinates parameter cannot be empty")

        return FunctionHelper.apply(
            "Geometry.LineString", "engine.Geometry", data
        )

    @staticmethod
    def Rectangle(coordinates: list):
        if coordinates is not None and not isinstance(coordinates, list):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"coordinates only supports arguments of type list, passed in as {type(coordinates)}",
            )
        data = {
            "coordinates": coordinates,
        }
        if "coordinates" not in data:
            raise RSError(RSErrorCode.ARGS_ERROR, "The coordinates parameter cannot be empty")

        return FunctionHelper.apply(
            "Geometry.Rectangle", "engine.Geometry", data
        )

    @staticmethod
    def Polygon(coordinates: list):
        if coordinates is not None and not isinstance(coordinates, list):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"coordinates only supports arguments of type list, passed in as {type(coordinates)}",
            )
        data = {
            "coordinates": coordinates,
        }
        if "coordinates" not in data:
            raise RSError(RSErrorCode.ARGS_ERROR, "The coordinates parameter cannot be empty")
        fun_node = FunctionHelper.apply(
            "/geometry/Polygon", "engine.Geometry", data
        )
        return fun_node

    @staticmethod
    def Point(coordinates: list):
        if coordinates is not None and not isinstance(coordinates, list):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"coordinates only supports arguments of type list, passed in as {type(coordinates)}",
            )

        data = {
            "coordinates": coordinates,
        }
        if "coordinates" not in data:
            raise RSError(RSErrorCode.ARGS_ERROR, "The coordinates parameter cannot be empty")
        fun_node = FunctionHelper.apply(
            "Geometry.Point", "engine.Geometry", data
        )
        Geometry.updateStep(FunctionNode("/geometry/Point", data), "/geometry/Point", data, fun_node)
        return fun_node

    @staticmethod
    def MultiPoint(coordinates: list):
        if coordinates is not None and not isinstance(coordinates, list):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"coordinates only supports arguments of type list, passed in as {type(coordinates)}",
            )

        data = {
            "coordinates": coordinates,
        }
        if "coordinates" not in data:
            raise RSError(RSErrorCode.ARGS_ERROR, "The coordinates parameter cannot be empty")
        fun_node = FunctionHelper.apply(
            "Geometry.MultiPoint", "engine.Geometry", data
        )
        Geometry.updateStep(FunctionNode("/geometry/MultiPoint", data), "/geometry/MultiPoint", data, fun_node)
        return fun_node

    @staticmethod
    def MultiLineString(coordinates: list):
        if coordinates is not None and not isinstance(coordinates, list):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"coordinates only supports arguments of type list, passed in as {type(coordinates)}",
            )

        data = {
            "coordinates": coordinates,
        }
        if "coordinates" not in data:
            raise RSError(RSErrorCode.ARGS_ERROR, "The coordinates parameter cannot be empty")
        fun_node = FunctionHelper.apply(
            "Geometry.MultiLineString", "engine.Geometry", data
        )
        Geometry.updateStep(FunctionNode("/geometry/MultiLineString", data), "/geometry/MultiLineString", data,
                            fun_node)
        return fun_node

    @staticmethod
    def MultiPolygon(coordinates: list):
        if coordinates is not None and not isinstance(coordinates, list):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"coordinates only supports arguments of type list, passed in as {type(coordinates)}",
            )

        data = {
            "coordinates": coordinates,
        }
        if "coordinates" not in data:
            raise RSError(RSErrorCode.ARGS_ERROR, "The coordinates parameter cannot be empty")
        fun_node = FunctionHelper.apply(
            "Geometry.MultiPolygon", "engine.Geometry", data
        )
        Geometry.updateStep(FunctionNode("/geometry/MultiPolygon", data), "/geometry/MultiPolygon", data, fun_node)
        return fun_node

    def area(self):
        data = {
            "geometry": self,
        }
        fun_node = FunctionHelper.apply(
            "Geometry.area", "object", data
        )
        Geometry.updateStep(FunctionNode("/geometry/area", data), "/geometry/area", data, fun_node)
        return fun_node

    def bounds(self):
        data = {
            "geometry": self,
        }
        fun_node = FunctionHelper.apply(
            "Geometry.bounds", "object", data
        )
        Geometry.updateStep(FunctionNode("/geometry/bounds", data), "/geometry/bounds", data, fun_node)
        return fun_node

    def buffer(self, distance: [int, float]):
        if distance is not None and not isinstance(distance, (int, float)):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"distance only supports arguments of type(int, float), passed in as {type(distance)}",
            )
        data = {
            "geometry": self,
            "bufferDist": distance
        }
        fun_node = FunctionHelper.apply(
            "Geometry.buffer", "engine.Geometry", data
        )
        Geometry.updateStep(FunctionNode("/geometry/buffer", data), "/geometry/buffer", data, fun_node)
        return fun_node

    def centroid(self):
        data = {
            "geometry": self,
        }
        fun_node = FunctionHelper.apply(
            "Geometry.centroid", "object", data
        )
        Geometry.updateStep(FunctionNode("/geometry/centroid", data), "/geometry/centroid", data, fun_node)
        return fun_node

    def contains(self, geometry_two):
        if geometry_two is not None and not isinstance(geometry_two, Geometry):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"geometry_two supports only the engine.Geometry parameter, passed as {type(geometry_two)}",
            )
        data = {
            "geometry_one": self,
            "geometry_two": geometry_two
        }
        fun_node = FunctionHelper.apply(
            "Geometry.contains", "object", data
        )
        Geometry.updateStep(FunctionNode("/geometry/contains", data), "/geometry/contains", data, fun_node)
        return fun_node

    def containedIn(self, geometry_two):
        if geometry_two is not None and not isinstance(geometry_two, Geometry):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"geometry_two supports only the engine.Geometry parameter, passed as {type(geometry_two)}",
            )
        data = {
            "geometry_one": self,
            "geometry_two": geometry_two
        }
        fun_node = FunctionHelper.apply(
            "Geometry.containedIn", "object", data
        )
        Geometry.updateStep(FunctionNode("/geometry/containedIn", data), "/geometry/containedIn", data, fun_node)
        return fun_node

    def convexHull(self):
        data = {
            "geometry": self,
        }
        fun_node = FunctionHelper.apply(
            "Geometry.convexHull", "engine.Geometry", data
        )
        Geometry.updateStep(FunctionNode("/geometry/convexHull", data), "/geometry/convexHull", data, fun_node)
        return fun_node

    def coordinates(self):
        data = {
            "geometry": self,
        }
        fun_node = FunctionHelper.apply(
            "Geometry.coordinates", "object", data
        )
        Geometry.updateStep(FunctionNode("/geometry/coordinates", data), "/geometry/coordinates", data, fun_node)
        return fun_node

    def difference(self, geometry_two):
        if geometry_two is not None and not isinstance(geometry_two, Geometry):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"geometry_two supports only the engine.Geometry parameter, passed as {type(geometry_two)}",
            )
        data = {
            "geometry_one": self,
            "geometry_two": geometry_two
        }
        fun_node = FunctionHelper.apply(
            "Geometry.difference", "engine.Geometry", data
        )
        Geometry.updateStep(FunctionNode("/geometry/difference", data), "/geometry/difference", data, fun_node)
        return fun_node

    def disjoint(self, geometry_two):
        if geometry_two is not None and not isinstance(geometry_two, Geometry):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"geometry_two supports only the engine.Geometry parameter, passed as {type(geometry_two)}",
            )
        data = {
            "geometry_one": self,
            "geometry_two": geometry_two
        }
        return FunctionHelper.apply(
            "Geometry.disjoint", "object", data
        )

    def dissolve(self):
        data = {
            "geometry": self,
        }
        fun_node = FunctionHelper.apply(
            "Geometry.dissolve", "engine.Geometry", data
        )
        Geometry.updateStep(FunctionNode("/geometry/dissolve", data), "/geometry/dissolve", data, fun_node)
        return fun_node

    def intersection(self, geometry_two):
        if geometry_two is not None and not isinstance(geometry_two, Geometry):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"geometry_two supports only the engine.Geometry parameter, passed as {type(geometry_two)}",
            )
        data = {
            "geometry_one": self,
            "geometry_two": geometry_two
        }
        fun_node = FunctionHelper.apply(
            "Geometry.intersection", "engine.Geometry", data
        )
        Geometry.updateStep(FunctionNode("/geometry/intersection", data), "/geometry/intersection", data, fun_node)
        return fun_node

    def length(self):
        data = {
            "geometry": self,
        }
        fun_node = FunctionHelper.apply(
            "Geometry.length", "object", data
        )
        Geometry.updateStep(FunctionNode("/geometry/length", data), "/geometry/length", data, fun_node)
        return fun_node

    def perimeter(self):
        data = {
            "geometry": self,
        }
        fun_node = FunctionHelper.apply(
            "Geometry.perimeter", "object", data
        )
        Geometry.updateStep(FunctionNode("/geometry/perimeter", data), "/geometry/perimeter", data, fun_node)
        return fun_node

    def simplify(self):
        data = {
            "geometry": self,
        }
        fun_node = FunctionHelper.apply(
            "Geometry.simplify", "engine.Geometry", data
        )
        Geometry.updateStep(FunctionNode("/geometry/simplify", data), "/geometry/simplify", data, fun_node)
        return fun_node

    def symmetricDifference(self, geometry_two):
        if geometry_two is not None and not isinstance(geometry_two, Geometry):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"geometry_two supports only the engine.Geometry parameter, passed as {type(geometry_two)}",
            )
        data = {
            "geometry_one": self,
            "geometry_two": geometry_two
        }
        fun_node = FunctionHelper.apply(
            "Geometry.symmetricDifference", "engine.Geometry", data
        )
        Geometry.updateStep(FunctionNode("/geometry/symmetricDifference", data), "/geometry/symmetricDifference", data,
                            fun_node)
        return fun_node

    def type(self):
        data = {
            "geometry": self,
        }
        fun_node = FunctionHelper.apply(
            "Geometry.type", "object", data
        )
        Geometry.updateStep(FunctionNode("/geometry/type", data), "/geometry/type", data, fun_node)
        return fun_node

    def union(self, geometry_two):
        if geometry_two is not None and not isinstance(geometry_two, Geometry):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"geometry_two supports only the engine.Geometry parameter, passed as {type(geometry_two)}",
            )
        data = {
            "geometry_one": self,
            "geometry_two": geometry_two
        }
        fun_node = FunctionHelper.apply(
            "Geometry.union", "engine.Geometry", data
        )
        Geometry.updateStep(FunctionNode("/geometry/union", data), "/geometry/union", data, fun_node)
        return fun_node

    @staticmethod
    def toWKT(geometry):
        if geometry is not None and not isinstance(geometry, Geometry):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"geometry supports only the engine.Geometry parameter, passed as {type(geometry)}",
            )
        data = geometry
        fun_node = FunctionHelper.apply(
            "Geometry.toWKT", "object", data
        )
        Geometry.updateStep(FunctionNode("/geometry/toWKT", data), "/geometry/toWKT", data, fun_node)
        return fun_node
