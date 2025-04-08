"""Tests for pyregeon."""

import shutil
import tempfile
import unittest
from os import path

import geopandas as gpd
import osmnx as ox
from shapely.geometry import Point, Polygon

import pyregeon
from pyregeon import settings


class NaiveTestObject(pyregeon.RegionMixin):
    pass


class TestObject(pyregeon.RegionMixin):
    crs = "epsg:4326"


class TestObjectCaps(pyregeon.RegionMixin):
    CRS = "epsg:4326"


def _test_region_and_class(region, _class):
    obj = _class()
    obj.region = region
    assert isinstance(obj.region, gpd.GeoDataFrame)
    assert obj.region.crs is not None


class TestRegion(unittest.TestCase):
    def setUp(self):
        self.nominatim_query = "Pully, Switzerland"
        self.gdf = ox.geocode_to_gdf(self.nominatim_query)
        self.gser = self.gdf["geometry"]
        self.naive_gdf = gpd.GeoDataFrame(
            self.gdf.drop("geometry", axis="columns"), geometry=list(self.gser)
        )
        self.naive_gser = self.naive_gdf["geometry"]
        self.geom = self.gser.iloc[0]
        self.bounds = self.gdf.total_bounds
        self.tmp_dir = tempfile.mkdtemp()
        self.filepath = path.join(self.tmp_dir, "foo.gpkg")
        self.gdf.to_file(self.filepath)

        self.regions_with_crs = [
            self.nominatim_query,
            self.gser,
            self.gdf,
            self.filepath,
        ]
        self.naive_regions = [
            self.bounds,
            self.naive_gser,
            self.naive_gdf,
            self.geom,
            [self.geom],
        ]

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_set_region(self):
        # test with no required CRS argument
        for region in self.regions_with_crs:
            for _class in [
                NaiveTestObject,
                TestObject,
                TestObjectCaps,
            ]:
                _test_region_and_class(region, _class)

        # test requiring CRS argument
        for region in self.naive_regions:
            obj = NaiveTestObject()
            # we cannot set the region argument without a CRS
            with self.assertRaises(ValueError):
                obj.region = region
            # in classes with a "crs" or "CRS" attribute set, the region CRS will be
            # inferred from there
            for _class in [
                TestObject,
                TestObjectCaps,
            ]:
                _test_region_and_class(region, _class)

    def test_generate_grid(self):
        # since we tested the init combinations above, we can just test the grid for a
        # single instance
        obj = TestObject()
        # use it in a projected CRS (in meters) so that the grid units are in meters too
        obj.region = self.gdf.to_crs("epsg:2056")

        # test the grid generation with no keyword args
        res = 100
        grid_gser = obj.generate_regular_grid_gser(res)
        assert isinstance(grid_gser, gpd.GeoSeries)
        assert grid_gser.crs == obj.region.crs
        assert grid_gser.index.name == settings.GRID_INDEX_NAME
        # test that a higher resolution gives a greater or equal number of items
        assert len(obj.generate_regular_grid_gser(res * 0.5).index) >= len(
            grid_gser.index
        )
        # test that a lower resolution gives a smaller or equal number of items
        assert len(obj.generate_regular_grid_gser(res * 2).index) <= len(
            grid_gser.index
        )

        # test keyword args
        # test that offsetting the grid to "center" displaces the grid so that the left
        # bound is smaller (or equal) and the top bound is greater (or equal)
        total_bounds = obj.generate_regular_grid_gser(res, offset="center").total_bounds
        assert total_bounds[0] <= grid_gser.total_bounds[0]
        assert total_bounds[3] >= grid_gser.total_bounds[3]

        # test the geometry type
        for geometry_type, GeomType in zip(["polygon", "point"], [Polygon, Point]):
            for geom in obj.generate_regular_grid_gser(
                res, geometry_type=geometry_type
            ):
                assert isinstance(geom, GeomType)

        # test the index name
        grid_gser = obj.generate_regular_grid_gser(res, grid_index_name="foo")
        assert grid_gser.index.name == "foo"

        # test the standalone function (rather than the object method) to test the CRS
        # argument
        # test that for naive geometries, we need to pass a CRS argument
        with self.assertRaises(ValueError):
            grid_gser = pyregeon.generate_regular_grid_gser(
                self.naive_gser,
                res,
            )
        crs = "epsg:4326"
        grid_gser = pyregeon.generate_regular_grid_gser(
            self.naive_gser,
            res,
            crs=crs,
        )
        assert isinstance(grid_gser, gpd.GeoSeries)
        assert grid_gser.crs == crs
        # test that for non-naive geometries, we don't need to pass a CRS argument
        region_gser = obj.region["geometry"]
        grid_gser = pyregeon.generate_regular_grid_gser(
            region_gser,
            res,
        )
        assert isinstance(grid_gser, gpd.GeoSeries)
        assert grid_gser.crs == region_gser.crs
        # test that for non-naive geometries, if we pass a CRS argument, it is ignored
        grid_gser = pyregeon.generate_regular_grid_gser(
            region_gser,
            res,
            crs=crs,
        )
        assert isinstance(grid_gser, gpd.GeoSeries)
        # ACHTUNG: note that we can test this because we have set the CRS of
        # `obj.region` (and thus `region_gser`) to epsg 2056 above
        assert grid_gser.crs != crs
