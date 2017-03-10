from qgis.core import *
from GlobalMapTiles import GlobalMercator

import sqlite3
import sys
import os
import site
import importlib
import uuid
import json
import glob
import zlib
from VectorTileHelper import VectorTile


class _GeoTypes:
    POINT = "Point"
    LINE_STRING = "LineString"
    POLYGON = "Polygon"


GeoTypes = _GeoTypes()


class VtReader:
    geo_types = {
        1: GeoTypes.POINT,
        2: GeoTypes.LINE_STRING,
        3: GeoTypes.POLYGON}

    layer_sort_ids = {
        "poi": 0,
        "transportation": 1,
        "transportation_name": 2,
        "housenumber": 3,
        "building": 4,
        "place": 5,
        "aeroway": 6,
        "boundary": 7,
        "park": 8,
        "water_name": 9,
        "waterway": 10,
        "landuse": 11,
        "landcover": 12
    }

    _extent = 4096
    _directory = os.path.abspath(os.path.dirname(__file__))
    _temp_dir = "%s/tmp" % _directory
    file_path = "%s/sample data/zurich_switzerland.mbtiles" % _directory

    def __init__(self, iface):
        self.iface = iface
        self._import_libs()
        self._counter = 0
        self._bool = True
        self._mbtile_id = "name"

    def reinit(self):
        """
         * Reinitializes the VtReader
         >> Cleans the temp directory
         >> Cleans the feature cache
         >> Cleans the qgis group cache
        """

        self._clear_temp_dir()
        self.features_by_path = {}
        self.qgis_layer_groups_by_feature_path = {}

    def _clear_temp_dir(self):
        """
         * Removes all files from the temp_dir
        """
        if not os.path.exists(self._temp_dir):
            os.makedirs(self._temp_dir)
        files = glob.glob("%s/*" % self._temp_dir)
        for f in files:
            os.remove(f)

    def _get_empty_feature_collection(self):
        """
         * Returns an empty GeoJSON FeatureCollection
        """

        from geojson import FeatureCollection
        crs = {  # crs = coordinate reference system
            "type": "name",
            "properties": {
                    "name": "urn:ogc:def:crs:EPSG::3857"}}
        return FeatureCollection([], crs=crs)

    def _import_libs(self):
        """
         * Imports the external libraries that are required by this plugin
        """

        site.addsitedir(os.path.join(self._temp_dir, '/ext-libs'))
        self._import_library("google.protobuf")
        self.mvt = self._import_library("mapbox_vector_tile")
        self.geojson = self._import_library("geojson")

    def _import_library(self, lib):
        print "importing: ", lib
        module = importlib.import_module(lib)
        print "import successful"
        return module

    def do_work(self, zoom_level):
        self.reinit()
        self._connect_to_db()
        tile_data_tuples = self._load_tiles_from_db(zoom_level)
        tiles = self._decode_all_tiles(tile_data_tuples)
        self._process_tiles(tiles)
        self._create_qgis_layer_hierarchy()

    def _connect_to_db(self):
        """
         * Since an mbtile file is a sqlite database, we can connect to it
        """

        try:
            self.conn = sqlite3.connect(self.file_path)
            self.conn.row_factory = sqlite3.Row
            print "Successfully connected to db"
        except:
            print "Db connection failed:", sys.exc_info()
            return

    def _load_tiles_from_db(self, zoom_level):
        print "Reading data from db"
        sql_command = "SELECT zoom_level, tile_column, tile_row, tile_data FROM tiles WHERE zoom_level = {} LIMIT 3;".format(zoom_level)
        tile_data_tuples = []
        try:
            cur = self.conn.cursor()
            for row in cur.execute(sql_command):
                zoom_level = row["zoom_level"]
                tile_col = row["tile_column"]
                tile_row = row["tile_row"]
                binary_data = row["tile_data"]
                tile = VectorTile(zoom_level, tile_col, tile_row)
                tile_data_tuples.append((tile, binary_data))
        except:
            print "Getting data from db failed:", sys.exc_info()
            return
        return tile_data_tuples

    def _decode_all_tiles(self, tiles_with_encoded_data):
        tiles = []
        for tile_data_tuple in tiles_with_encoded_data:
            tile = tile_data_tuple[0]
            encoded_data = tile_data_tuple[1]
            tile.decoded_data = self._decode_binary_tile_data(encoded_data)
            tiles.append(tile)
        return tiles

    def _process_tiles(self, tiles):
        totalNrTiles = len(tiles)
        print "Processing {} tiles".format(totalNrTiles)
        for index, tile in enumerate(tiles):
            self._write_features(tile)
            print "Progress: {0:.1f}%".format(100.0 / totalNrTiles * (index + 1))

    def _decode_binary_tile_data(self, data):
        try:
            # The offset of 32 signals to the zlib header that the gzip header is expected but skipped.
            file_content = zlib.decompress(data, 32 + zlib.MAX_WBITS)
            decoded_data = self.mvt.decode(file_content)
        except:
            print "decoding data with mapbox_vector_tile failed", sys.exc_info()
            return
        return decoded_data

    def _create_qgis_layer_hierarchy(self):
        """
         * Creates a hierarchy of groups and layers in qgis
        """
        print "Creating hierarchy in qgis"
        root = QgsProject.instance().layerTreeRoot()
        group_name = os.path.splitext(os.path.basename(self.file_path))[0]
        rootGroup = root.addGroup(group_name)
        # print "all paths: ", self.features_by_path.keys()
        feature_paths = sorted(self.features_by_path.keys(), key=lambda path: VtReader._get_feature_sort_id(path))
        for feature_path in feature_paths:
            target_group, layer_name = self._get_group_for_path(feature_path, rootGroup)
            feature_collection = self.features_by_path[feature_path]
            file_src = self._create_unique_file_name()
            with open(file_src, "w") as f:
                json.dump(feature_collection, f)
            layer = VtReader._add_vector_layer(file_src, layer_name, target_group)
            VtReader._load_named_style(layer, feature_path.split(".")[0])

    @staticmethod
    def _get_feature_sort_id(feature_path):
        # print "get sort id for: ", feature_path
        first_node = feature_path.split(".")[0]
        sort_id = 999
        if first_node in VtReader.layer_sort_ids:
            sort_id = VtReader.layer_sort_ids[first_node]
        return sort_id

    def _get_group_for_path(self, path, root_group):
        """
         * Returns the group for the specified path
         >> If the group not already exists, it will be created
         >> The path has to be delimited by '.'
         >> The last element in the path will be used as name for the vector layer, the other elements will be used to create the group hierarchy
         >> Example: The path 'zurich.poi.police' will create two groups 'zurich' and 'poi' (if not already existing) and 'police' will be returned as name for the layer to create
        """

        group_names = path.split(".")
        current_group = root_group
        current_path = ""
        target_layer_name = ""
        for index, name in enumerate(group_names):
            target_layer_name = name
            is_last = index == len(group_names) - 1
            if is_last:
                break
            current_path += "." + name
            if current_path not in self.qgis_layer_groups_by_feature_path:
                self.qgis_layer_groups_by_feature_path[current_path] = VtReader._create_group(name, current_group)
            current_group = self.qgis_layer_groups_by_feature_path[current_path]
        return current_group, target_layer_name

    @staticmethod
    def _create_group(name, parent_group):
        new_group = parent_group.addGroup(name)
        return new_group

    @staticmethod
    def _load_named_style(layer, root_group_name):
        style_name = "{}.qml".format(layer.name())
        # style_name = "{}.qml".format(root_group_name)
        style_path = os.path.join(VtReader._directory, "styles/{}".format(style_name))
        if os.path.isfile(style_path):
            res = layer.loadNamedStyle(style_path)
            if res[1]:  # Style loaded
                layer.setCustomProperty("layerStyle", style_path)
                print "Style successfully applied: ", style_name

    @staticmethod
    def _add_vector_layer(json_src, layer_name, layer_target_group):
        """
         * Creates a QgsVectorLayer and adds it to the group specified by layer_target_group
        """

        # load the created geojson into qgis
        layer = QgsVectorLayer(json_src, layer_name, "ogr")
        QgsMapLayerRegistry.instance().addMapLayer(layer, False)
        layer_target_group.addLayer(layer)
        return layer

    def _write_features(self, tile):
        # iterate through all the features of the data and build proper gejson conform objects.
        for layer_name in tile.decoded_data:

            print "Handle features of layer: ", layer_name
            tile_features = tile.decoded_data[layer_name]["features"]
            for index, feature in enumerate(tile_features):
                geojson_feature, geo_type = VtReader._create_geojson_feature(feature, tile)
                if geojson_feature:
                    feature_path = VtReader._get_feature_path(layer_name, geojson_feature)
                    if feature_path not in self.features_by_path:
                        self.features_by_path[feature_path] = self._get_empty_feature_collection()

                    self.features_by_path[feature_path].features.append(geojson_feature)

                # TODO: remove the break after debugging
                # print "feature: ", feature
                # print "   data: ", data
                # break

    @staticmethod
    def _get_feature_class_and_subclass(feature):
        feature_class = None
        feature_subclass = None
        if "class" in feature.properties:
            feature_class = feature.properties["class"]
            if "subclass" in feature.properties:
                feature_subclass = feature.properties["subclass"]
                if feature_subclass == feature_class:
                    feature_subclass = None
        if feature_subclass:
            assert feature_class, "A feature with a subclass should also have a class"
        return feature_class, feature_subclass

    @staticmethod
    def _get_feature_path(layer_name, feature):
        feature_class, feature_subclass = VtReader._get_feature_class_and_subclass(feature)
        feature_path = layer_name
        if feature_class:
            feature_path += "." + feature_class
            if feature_subclass:
                feature_path += "." + feature_subclass
        return feature_path

    @staticmethod
    def _create_geojson_feature(feature, tile):
        """
        Creates a proper GeoJSON feature for the specified feature
        """
        from geojson import Feature, Point, Polygon, LineString

        geo_type = VtReader.geo_types[feature["type"]]
        coordinates = feature["geometry"]
        coordinates = VtReader._map_coordinates_recursive(coordinates, lambda coords: VtReader._calculate_geometry(coords, tile))

        if geo_type == GeoTypes.POINT:
            # Due to mercator_geometrys nature, the point will be displayed in a List "[[]]", remove the outer bracket.
            coordinates = coordinates[0]

        if geo_type == GeoTypes.POINT:
            geometry = Point(coordinates)
        elif geo_type == GeoTypes.POLYGON:
            geometry = Polygon(coordinates)
        elif geo_type == GeoTypes.LINE_STRING:
            geometry = LineString(coordinates)
        else:
            raise Exception("Unexpected geo_type: {}".format(geo_type))

        feature_json = Feature(geometry=geometry, properties=feature["properties"])

        return feature_json, geo_type

    @staticmethod
    def _map_coordinates_recursive(coordinates, func):
        """
        Recursively traverses the array of coordinates (depth first) and applies the specified function
        """
        tmp = []
        for coord in coordinates:
            is_coordinate_tuple = len(coord) == 2 and all(isinstance(c, int) for c in coord)
            if is_coordinate_tuple:
                newval = func(coord)
                tmp.append(newval)
            else:
                tmp.append(VtReader._map_coordinates_recursive(coord, func))
        return tmp

    @staticmethod
    def _calculate_geometry(coordinates, tile):
        """
        Does a mercator transformation on the specified coordinate tuple
        """
        # calculate the mercator geometry using external library
        # geometry:: 0: zoom, 1: easting, 2: northing
        tmp = GlobalMercator().TileBounds(tile.column, tile.row, tile.zoom_level)
        delta_x = tmp[2] - tmp[0]
        delta_y = tmp[3] - tmp[1]
        merc_easting = int(tmp[0] + delta_x / VtReader._extent * coordinates[0])
        merc_northing = int(tmp[1] + delta_y / VtReader._extent * coordinates[1])
        return [merc_easting, merc_northing]

    @staticmethod
    def _create_unique_file_name(ending="geojson"):
        unique_name = "{}.{}".format(uuid.uuid4(), ending)
        return os.path.join(VtReader._temp_dir, unique_name)
