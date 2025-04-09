'''
Download ST_LUCAS samples based on built request.
'''

import os
import tempfile
import json
import zipfile
from pathlib import Path
from shutil import copy
from copy import deepcopy
try:
    import requests
    from requests.exceptions import HTTPError, ConnectionError, InvalidSchema, InvalidURL, MissingSchema

    from osgeo import gdal, ogr
    gdal.UseExceptions()

    from owslib.wfs import WebFeatureService
    from owslib.util import ServiceException
    from owslib import __version__ as owslib_version
except ModuleNotFoundError:
    pass # ignored by dynamic version in pyproject.toml


from .logger import Logger
from .exceptions import LucasDownloadError, LucasDataError

__version__ = '2.0.0'

class LucasIO:
    _additional_layers = ["obs_radius_areas", "cprn_areas", "rg_repre_areas"]
    """
    LUCAS features input / output class.

    :param str url: WFS endpoint
    :param str version: WFS version to be used
    """
    def __init__(self,
                 url='https://geoforall.fsv.cvut.cz/st_lucas',
                 version='1.1.0'):
        Logger.debug(f"Using owslib version {owslib_version}")
        self._wfs_url = url + "/geoserver/wfs"
        self._wfs_version = version

        self._mtd_url = url + "/st_lucas_metadata.json"
        self._request = None

        self._path = None # path to GPKG file
        # to avoid Access Violation error on MS Windows
        # https://lists.osgeo.org/pipermail/qgis-developer/2025-January/067283.html
        self._ds = None

    def __del__(self):
        if self._ds is not None:
            self._ds.Close()

    @property
    def data(self):
        return self._path

    @data.setter
    def data(self, path):
        """Set data property from existing GPKG file.

        :param str path: path to existing GPKG file
        """
        try:
            ds = gdal.OpenEx(path, gdal.OF_VECTOR | gdal.OF_READONLY)
            driver = ds.GetDriver().ShortName
            if driver != "GPKG":
                ds.Close()
                raise LucasDataError(f"Unexpected input file: {driver}")
        except RuntimeError as e:
            raise LucasDataError(f"Unable to open input file: {e}")

        self._path = path
        self._ds = ds

    @property
    def metadata(self):
        """Get metadata.

        :return dict: metadata dictionary
        """
        try:
            md = deepcopy(self._ds.GetMetadata())
        except RuntimeError as e:
            raise LucasDataError(f"Unable to get metadata: {e}")

        return md

    @staticmethod
    def __get_tempfile_name(extension):
        return os.path.join(tempfile.gettempdir(),
                            "st_lucas_{n}.{e}".format(
                                n=next(tempfile._get_candidate_names()),
                                e=extension)
                            )

    @staticmethod
    def _getfeature(wfs, args, suffix=None):
        try:
            response = wfs.getfeature(**args)
        except (ServiceException, AttributeError, TypeError) as e:
            raise LucasDownloadError(f"Unable to get features from WFS server: {e}")

        return response.read()

    def download(self, request):
        """
        Download LUCAS features from dedicated WFS server based on
        specified request :class:`.request.LucasRequest`.

        :param LucasRequest: request
        """
        # allow to run download method multiple times
        if self._ds is not None:
            self._ds.Close()
            self._ds = None

        # create connection
        self._request = request
        try:
            wfs = WebFeatureService(url=self._wfs_url, version=self._wfs_version)
        except (HTTPError, ConnectionError, InvalidSchema, InvalidURL, MissingSchema, AttributeError, UnicodeError) as e:
            raise LucasDownloadError(f"Cannot connect to server: {e}")

        Logger.debug(f"Connected to {self._wfs_url}")

        # collect getfeature() arguments
        args = {
            'srsname': "http://www.opengis.net/gml/srs/epsg.xml#3035"
        }
        args.update(request.build())
        Logger.debug(f"Request: {args}")

        gml = self._getfeature(wfs, args)
        Logger.info(
            "Download process successfuly finished. Size of downloaded data: {}kb".format(
                int(len(gml) / 1000)
            ))

        self._path = self.__get_tempfile_name("gpkg")
        self._ds = self._load(gml)

        # process additional layers
        for prop_name in self._additional_layers:
            prop = getattr(self._request, prop_name)
            if prop is True:
                prop_args = deepcopy(args)
                prop_args["typename"] = "{}:{}_{}".format(
                    self._request.gh_workspace,
                    self._request.gh_typename,
                    prop_name
                )
                gml = self._getfeature(wfs, prop_args, prop_name)
                self._load(gml, prop_name)

        # perform postprocessing
        self._postprocessing(self._ds)

    def _load(self, gml, layer_suffix=None):
        """Load features from GML string and creates temporary GPKG file.

        :param str gml: GML string to be loaded
        :param layer_suffix: layer suffix or None

        :return (str, GDALDataset): path to temporary GPKG file, related GDAL Dataset
        """

        # 1. store GML string into temporary file
        path_gml = self.__get_tempfile_name("gml")
        Logger.debug(f"WFS GML path: {path_gml}")
        with open(path_gml, 'wb') as f:
            f.write(gml)

        # 2. convert GML to GPKG
        layer_name = self._request.gh_typename
        if layer_suffix:
            layer_name += f"_{layer_suffix}"
        try:
            ds = gdal.VectorTranslate(self._path if self._ds is None else self._ds, path_gml,
                                      srcSRS="EPSG:3035", dstSRS="EPSG:3035",
                                      layerName=layer_name,
                                      accessMode=None if layer_suffix is None else "append",
                                      geometryType="CONVERT_TO_LINEAR")
        except RuntimeError as e:
            raise LucasDataError(f"Unable to translate into GPKG: {e}")

        return ds

    def _postprocessing(self, ds):
        """Delete gml_id column. If data are space time aggregated, delete columns which aren't required

        :param GDALDataset ds: GPKG dataset
        """
        def _group(name):
            return {
                "LC_LU": "LAND COVER,LAND USE",
                "LC_LU_SO": "LAND COVER,LAND USE,SOIL",
                "FO": "FORESTRY",
                "CO": "COPERNICUS",
                "IN": "INSPIRE"
            }[name]

        try:
            for idx in range(ds.GetLayerCount()):
                layer = ds.GetLayerByIndex(idx)
                defn = layer.GetLayerDefn()
                layer.DeleteField(defn.GetFieldIndex('gml_id'))
            if self._request.st_aggregated and self._request.years is not None:
                # delete attributes which do not pass temporal filter
                layer_defn = layer.GetLayerDefn()
                delete_attr = []
                for i in range(layer_defn.GetFieldCount()):
                    attr = layer_defn.GetFieldDefn(i).GetName()
                    try:
                        if int(attr[-4:]) not in self._request.years:
                            delete_attr.append(attr)
                    except ValueError:
                        # some attributes are timeless (eg. point_id, ..., count_survey)
                        pass
                for attr in delete_attr:
                    layer.DeleteField(defn.GetFieldIndex(attr))

            # read LUCAS JSON metadata from server
            try:
                r = requests.get(self._mtd_url)
                lucas_metadata = json.loads(r.content)
            except (HTTPError, json.decoder.JSONDecodeError) as e:
                raise LucasDataError(f"Postprocessing failed: {e}")

            # write metadata into GPKG
            # note:
            #  values are provided as strings due to GDAL < 3.3 limitation
            #  -> Dictionary must contain tuples of strings
            metadata = ({
                "LUCAS_TABLE": self._request.typename.split(":")[1],
                "LUCAS_ST": str(int(self._request.st_aggregated)),
                "LUCAS_CLIENT_VERSION": __version__,
                "LUCAS_DB_VERSION": str(lucas_metadata["version"]),
                "LUCAS_MAX_FEATURES": str(lucas_metadata["max_features"]),
            })
            if self._request.group is not None:
                metadata["LUCAS_GROUP"] = _group(self._request.group.upper())
            ds.SetMetadata(metadata)
            ds.FlushCache()
        except RuntimeError as e:
            raise LucasDataError(f"Postprocessing failed: {e}")

    def __check_data(self):
        """Check whether LUCAS features are downloaded.

        Raise LucasDownloadError of failure
        """
        if self._path is None:
            raise LucasDownloadError("No LUCAS features downloaded")

    def __check_additional_layer_name(self, layer):
        """Check layer name of additional layers.

        :param str layer: layer name

        Raise LucasDataError of failure
        """
        if layer is not None and layer not in self._additional_layers:
            raise LucasDataError(f"Unsupported layer name {layer}")

    def to_gml(self, layer=None, epsg=3035):
        """Get downloaded LUCAS features as `OGC GML
        <https://www.ogc.org/standards/gml>`__ string.

        :param str layer: layer name or None for default
        :param int epsg: target EPSG code

        :return str: GML string
        """
        self.__check_data()
        self.__check_additional_layer_name(layer)

        path_gml = self.__get_tempfile_name("gml")

        try:
            gdal.VectorTranslate(path_gml, self._path,
                                 dstSRS=f"EPSG:{epsg}",
                                 format="GML",
                                 layers=["lucas_points_{}".format(layer)]
                                 if layer is not None else None
                                 )
        except RuntimeError as e:
            raise LucasDataError(f"Unable to translate into GML: {e}")

        with open(path_gml) as fd:
            data = fd.read()

        return data

    def to_gpkg(self, output_path, epsg=3035):
        """Save downloaded LUCAS features into `OGC GeoPackage
        <https://www.ogc.org/standards/gml>`__ file.

        Raises LucasDataError on failure.

        :param str output_path: path to the output OGC GeoPackage file
        :param int epsg: target EPSG code
        """
        self.__check_data()

        out_path = Path(output_path)

        # Delete file if exists
        if out_path.exists():
            try:
                out_path.unlink()
            except PermissionError as e:
                raise LucasDataError(f"Unable to overwrite existing file: {e}")

        if epsg != 3035:
            try:
                gdal.VectorTranslate(output_path, self._path, dstSRS=f"EPSG:{epsg}")
            except RuntimeError as e:
                raise LucasDataError(f"Unable to translate into GPKG: {e}")
        else:
            # Copy file from temporary directory
            try:
                copy(self._path, out_path)
            except PermissionError as e:
                raise LucasDataError(f"Permission denied: {e}")

    def to_geopandas(self, layer=None, epsg=3035):
        """Get downloaded LUCAS features as GeoPandas `GeoDataFrame
        <https://geopandas.org/docs/reference/api/geopandas.GeoDataFrame.html>`__
        structure.

        :param str layer: layer name or None for default
        :param int epsg: target EPSG code

        :return GeoDataFrame:

        """
        from geopandas import read_file

        self.__check_data()
        self.__check_additional_layer_name(layer)

        if epsg != 3035:
            try:
                _path = self.__get_tempfile_name("gpkg")
                gdal.VectorTranslate(_path, self._path, dstSRS=f"EPSG:{epsg}")
            except RuntimeError as e:
                raise LucasDataError(f"Unable to translate into GPKG: {e}")
        else:
            _path = self._path

        return read_file(_path, layer="lucas_points_{}".format(layer) if layer is not None else None
        )

    def count(self, layer_identifier=None):
        """Get number of downloaded LUCAS features.

        :param str layer_identifier: specify layer name to be processed (None for LUCAS points)

        Layer identifiers: obs_radius_areas, cprn_areas, rg_repre_areas

        :return int: number of downloaded features
        """
        self.__check_data()

        try:
            if layer_identifier is None:
                layer = self._ds.GetLayer()
            else:
                layer = self._ds.GetLayerByName("{}_{}".format(
                    self._request.gh_typename, layer_identifier
                ))
            nop = layer.GetFeatureCount()
        except RuntimeError as e:
            raise LucasDataError(f"Postprocessing failed: {e}")

        return nop

    def is_empty(self):
        """Check whether downloaded LUCAS feature collection is empty.

        :return bool: True for empty collection otherwise False
        """
        return self.count() < 1

    def get_images(self, year, point_id, nuts0=None):
        """Get images of selected point and its surroundings from Eurostat FTP server.

        :param int year: year of the measurement
        :param int point_id: id of the LUCAS point
        :param str nuts0: NUTS0 code

        :return images: dictionary of images (URL)
        """
        if nuts0 is None:
            try:
                layer = self._ds.GetLayer(0)
                layer.SetAttributeFilter(f"point_id={point_id} AND survey_year={year}")
                num_points = layer.GetFeatureCount()
                if num_points != 1:
                    raise LucasDataError(f"Unexpected number of selected points: {num_points}")
                nuts0 = layer.GetNextFeature().GetFieldAsString("nuts0")
            except RuntimeError as e:
                raise LucasDataError(f"Unable to get images: {e}")

        images = {}
        url = f'https://gisco-services.ec.europa.eu/lucas/photos/{str(year)}/{nuts0}/{str(point_id)[0:3]}/{str(point_id)[3:6]}/{str(point_id)}'
        for i in ("P", "S", "N", "E", "W"):
            images[i] = f"{url}{i}.jpg"

        return images

    def download_images(self, images, save_dir):
        """Save images of LUCAS point into zip file.

        :param dict images: dictionary with URLs of LUCAS point images received by get_images method
        :param str save_dir: directory path to save the downloaded images

        :return str: path to created zip file
        """
        if not Path(save_dir).exists():
            raise IOError(f"No such directory: {save_dir}")

        year = images["P"].split("/")[5]
        zip_name = images["P"].split("/")[-1].replace("P.jpg", f"_{year}.zip")
        path_to_zipfile = os.path.join(save_dir, zip_name)
        image_list = []
        for key, url in images.items():
            response = requests.get(url)
            if response.status_code == 200:
                image_list.append((key, response.content))

        if len(image_list) == 0:
            Logger.warning("None images available for given LUCAS point")
            return None

        with zipfile.ZipFile(path_to_zipfile, 'w') as zip_file:
            for key, image_data in image_list:
                zip_file.writestr(key + '.jpg', image_data)
        Logger.info(f"LUCAS photos downloaded to: {path_to_zipfile}")

        return path_to_zipfile
