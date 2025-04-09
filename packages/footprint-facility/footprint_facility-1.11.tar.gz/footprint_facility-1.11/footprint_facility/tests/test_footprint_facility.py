"""
   Copyright 2024 - Gael Systems

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from unittest import TestCase, skip
import json

import geojson
import shapely
from shapely import MultiPolygon, Polygon, Point, Geometry, wkt
from shapely.ops import transform as sh_transform
from pyproj import Transformer
import os
from os import walk

import footprint_facility
from footprint_facility import AlreadyReworkedPolygon

import logging

logging.basicConfig(level=logging.DEBUG)


#############################################################################
# Private Utilities to manipulate input test Footprint file
# - load
# - retrieve longitude/Latitude list according to the input
# - build shapely geometry
#############################################################################
def _load_samples():
    path = os.path.join(os.path.dirname(__file__),
                        'samples', 'footprints_basic.json')
    with open(path) as f:
        return json.load(f)['footprint']


def _split(txt, seps):
    """
    Split with list of separators
    """
    default_sep = seps[0]
    # we skip seps[0] because that's the default separator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]


def get_odd_values(fp):
    # [1::2] odd indexes
    return [float(x) for x in _split(fp['coords'], (' ', ','))[1::2]]


def get_even_values(fp):
    # [::2] even indexes
    return [float(x) for x in _split(fp['coords'], (' ', ','))[::2]]


def get_longitudes(fp):
    func = get_even_values
    if fp.get('coord_order') is not None:
        if fp['coord_order'].split()[1][:3:] == 'lon':
            func = get_odd_values
    return func(fp)


# Extract latitude coord list
def get_latitudes(fp):
    func = get_odd_values
    if fp.get('coord_order') is not None:
        if fp['coord_order'].split()[0][:3:] == 'lat':
            func = get_even_values
    return func(fp)


def fp_to_geometry(footprint) -> Geometry:
    lon = get_longitudes(footprint)
    lat = get_latitudes(footprint)
    return Polygon([Point(xy) for xy in zip(lon, lat)])


def geometry_compare(geom1, geom2, tolerance=0.0) -> bool:
    diff = geom2.area - geom1.area
    percentage = diff / geom2.area
    return abs(percentage) <= tolerance


def disk_on_globe(lon, lat, radius, func=None):
    """Generate a shapely.Polygon object representing a disk on the
    surface of the Earth, containing all points within RADIUS meters
    of latitude/longitude LAT/LON."""

    # Use local azimuth projection to manage distances in meter
    # then convert to lat/lon degrees
    local_azimuthal_projection = \
        "+proj=aeqd +R=6371000 +units=m +lat_0={} +lon_0={}".format(lat, lon)
    lat_lon_projection = "+proj=longlat +datum=WGS84 +no_defs"

    wgs84_to_aeqd = Transformer.from_crs(lat_lon_projection,
                                         local_azimuthal_projection)
    aeqd_to_wgs84 = Transformer.from_crs(local_azimuthal_projection,
                                         lat_lon_projection)

    center = Point(float(lon), float(lat))
    point_transformed = sh_transform(wgs84_to_aeqd.transform, center)
    buffer = point_transformed.buffer(radius)
    disk = sh_transform(aeqd_to_wgs84.transform, buffer)
    if func is None:
        return disk
    else:
        return func(disk)


#############################################################################
# Test Class
#############################################################################
class TestFootprintFacility(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.footprints = _load_samples()
        footprint_facility.check_time(enable=True,
                                      incremental=False,
                                      summary_time=True)

    @classmethod
    def tearDownClass(cls):
        footprint_facility.show_summary()

    def setUp(self):
        pass

    def test_check_cross_antimeridian_error(self):
        self.assertFalse(footprint_facility.
                         check_cross_antimeridian(MultiPolygon()))
        with self.assertRaises(TypeError):
            footprint_facility.check_cross_antimeridian(geojson.MultiPolygon())

    def test_check_contains_pole_north(self):
        geom = disk_on_globe(-160, 90, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))

    def test_check_contains_pole_south(self):
        geom = disk_on_globe(-160, -90, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))

    def test_check_no_pole_antimeridian(self):
        geom = disk_on_globe(-179, 0, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))

    def test_check_no_pole_no_antimeridian(self):
        geom = disk_on_globe(0, 0, 500 * 1000)
        self.assertFalse(footprint_facility.check_cross_antimeridian(geom))

    def test_check_samples(self):
        """
        Pass through all the entries of the sample file that are marked as
        testable, then ensure they can be managed and reworked without failure.
        """
        for footprint in self.footprints:
            if footprint.get('testable', True):
                geom = fp_to_geometry(footprint)
                result = footprint_facility.check_cross_antimeridian(geom)
                self.assertEqual(result, footprint['antimeridian'],
                                 f"longitude singularity not properly "
                                 f"detected({footprint['name']}).")

    def test_rework_with_north_pole(self):
        """This footprint contains antimeridian and North Pole.
        """
        geom = disk_on_globe(-160, 90, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.Polygon)
        self.assertAlmostEqual(int(rwkd.area), 1600, delta=100)

    def test_rework_with_south_pole(self):
        """This footprint contains antimeridian and South Pole.
        """
        geom = disk_on_globe(0, -90, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.Polygon)
        self.assertAlmostEqual(int(rwkd.area), 1600, delta=100)

    def test_rework_close_to_north_pole(self):
        """This footprint contains antimeridian and no pole, very close to
          the North Pole.
          Footprint crossing antimeridian and outside polar area:
          Result should be a multipolygon not anymore crossing antimeridian.
        """
        geom = disk_on_globe(-178, 81, 300 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertAlmostEqual(int(rwkd.area), 150, delta=10)

    def test_rework_close_to_south_pole(self):
        """This footprint contains antimeridian and no pole, very close to
          the South Pole.
          Footprint crossing antimeridian and outside polar area:
          Result should be a multipolygon not anymore crossing antimeridian.
        """
        geom = disk_on_globe(-178, -81, 300 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertAlmostEqual(int(rwkd.area), 150, delta=10)

    def test_rework_no_pole(self):
        """This footprint contains antimeridian and no pole.
          Footprint crossing antimeridian and outside polar area:
          Result should be a multipolygon not anymore crossing antimeridian.
        """
        geom = disk_on_globe(-178, 0, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        print(geom)
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        print(rwkd)
        self.assertIs(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertAlmostEqual(int(rwkd.area), 70, delta=10)

    def test_rework_no_pole_no_antimeridian(self):
        """This footprint none of antimeridian and pole.
          No change of the footprint is required here.
        """
        geom = disk_on_globe(0, 0, 500 * 1000)
        self.assertFalse(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertFalse(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertEqual(geom, rwkd)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprint is not equivalents to input.")
        self.assertAlmostEqual(int(rwkd.area), 70, delta=10)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_no_pole_no_antimeridian(self):
        """
        Index 15 is a S3B SLSTR footprint located over Atlantic sea.
        It does not intersect antimeridian nor pole.

        Product available in CDSE as:
        S3B_OL_2_LRR____20240311T111059_20240311T115453_20240311T134014_2634_090_308______PS2_O_NR_002
        product id: 247c85f8-a78c-4abf-9005-2171ad6d8455
        """
        index = 15
        geom = fp_to_geometry(self.footprints[index])
        self.assertFalse(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertFalse(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")
        self.assertAlmostEqual(int(rwkd.area), 3000, delta=50)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_no_pole_cross_antimeridian(self):
        """
        Index 17 is a S3B OLCI Level 1 ERR footprint located over Pacific sea.
        It intersects antimeridian but does not pass over the pole.

        Product available in CDSE as:
        S3B_OL_1_ERR____20240224T213352_20240224T221740_20240225T090115_2628_090_086______PS2_O_NT_003
        product id: 07a3fa27-787f-479c-9bb3-d267249ffad3
        """
        index = 17
        geom = fp_to_geometry(self.footprints[index])
        print(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        print(rwkd)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertAlmostEqual(int(rwkd.area), 3000, delta=50)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_south_pole_antimeridian_overlapping(self):
        """
        Index 18 is a very long S3A SLSTR WST footprint.
        It intersects antimeridian and passes over the South Pole.
        At the South Pole location the footprint overlaps.

        Product available in CDSE as:
        S3A_SL_2_WST____20240224T211727_20240224T225826_20240226T033733_6059_109_228______MAR_O_NT_003
        product id: 67a2b237-50dc-4967-98ce-bad0fbc04ad3
        """
        index = 18
        geom = fp_to_geometry(self.footprints[index])
        print(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.Polygon,
                      footprint_facility.to_geojson(rwkd))
        self.assertAlmostEqual(int(rwkd.area), 10850, delta=50)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_product_north_pole_antimeridian_overlapping(self):
        """
         Footprint with overlapping on the North Pole (index 10 in samples).
         It also passes other both North and South Pole.

         This product is an old historical product and this use case has not
         been retrieved in CDSE.
        """
        geometry = wkt.loads("POLYGON ((67.9659 89.3932, 138.166 89.8556, -139.854 89.4189, -132.845 88.8564, -130.448 88.2871, -129.245 87.7159, -128.522 87.144, -128.04 86.5717, -127.696 85.9992, -127.438 85.4265, -127.237 84.8538, -127.077 84.281, -126.945 83.7081, -126.835 83.1352, -126.743 82.5623, -126.663 81.9893, -126.594 81.4163, -126.533 80.8433, -126.48 80.2702, -126.432 79.6971, -126.39 79.124, -126.351 78.5508, -126.317 77.9776, -126.285 77.4044, -126.256 76.8312, -126.229 76.2579, -126.205 75.6846, -126.182 75.1113, -126.161 74.5379, -126.142 73.9645, -126.124 73.3911, -126.107 72.8176, -126.091 72.2442, -126.087 72.1008, -120.121 72.0238, -111.141 71.5501, -102.774 70.6752, -95.2394 69.4507, -88.6116 67.9344, -82.8603 66.1818, -77.8972 64.2412, -73.3102 61.9759, -69.6455 59.7598, -66.4539 57.4515, -63.6555 55.0689, -61.1847 52.6263, -58.987 50.1346, -57.0185 47.6024, -55.2434 45.0365, -53.6322 42.4422, -52.1612 39.8241, -50.8103 37.1857, -49.5633 34.5299, -48.4065 31.8592, -47.3283 29.1757, -46.3193 26.481, -45.3711 23.7768, -44.477 21.0643, -43.6308 18.3447, -42.8275 15.619, -42.0626 12.888, -41.3323 10.1525, -40.6333 7.4134, -39.9626 4.6712, -39.3177 1.92652, -38.6964 -0.820084, -38.0966 -3.56812, -37.5166 -6.31712, -36.9549 -9.06669, -36.4101 -11.8164, -35.881 -14.566, -35.3667 -17.3151, -34.8661 -20.0634, -34.3785 -22.8106, -33.9032 -25.5566, -33.4397 -28.3011, -32.9876 -31.044, -32.5465 -33.7851, -32.1163 -36.5243, -31.697 -39.2614, -31.2887 -41.9965, -30.8917 -44.7294, -30.5067 -47.4601, -30.1346 -50.1887, -29.7766 -52.9151, -29.4348 -55.6394, -29.1119 -58.3615, -28.8118 -61.0816, -28.5403 -63.7998, -28.3058 -66.516, -28.1215 -69.2304, -28.0087 -71.9429, -28.0038 -74.6535, -28.1748 -77.3619, -28.6634 -80.0674, -29.8241 -82.7679, -32.8484 -85.456, -45.4789 -88.0815, -164.905 -88.817, 168.83 -86.2853, 164.486 -83.6057, 162.956 -80.9077, 162.313 -78.2033, 162.065 -75.4955, 162.024 -72.7854, 162.109 -70.0733, 162.273 -67.3593, 162.494 -64.6434, 162.755 -61.9256, 163.047 -59.2059, 163.363 -56.484, 163.7 -53.7601, 164.053 -51.034, 164.421 -48.3058, 164.802 -45.5753, 165.195 -42.8427, 165.6 -40.1078, 166.016 -37.3709, 166.443 -34.6318, 166.881 -31.8909, 167.33 -29.148, 167.79 -26.4035, 168.261 -23.6574, 168.745 -20.9099, 169.242 -18.1614, 169.752 -15.4119, 170.276 -12.6619, 170.816 -9.91163, 171.373 -7.16139, 171.947 -4.41159, 172.541 -1.66264, 173.155 1.08503, 173.793 3.83093, 174.455 6.57451, 175.146 9.31522, 175.866 12.0524, 176.62 14.7854, 177.411 17.5133, 178.244 20.2355, 179.123 22.9507, -179.946 25.6581, -178.956 28.3563, -177.899 31.0438, -176.768 33.719, -175.549 36.38, -174.231 39.0244, -172.798 41.6494, -171.232 44.2516, -169.509 46.827, -167.602 49.3703, -165.478 51.8754, -163.095 54.3342, -160.402 56.7364, -157.337 59.0691, -153.824 61.3154, -149.775 63.4536, -145.086 65.4556, -139.648 67.2853, -133.363 68.8982, -126.174 70.2413, -118.109 71.2565, -109.329 71.889, -100.146 72.0977, -100.144 72.2411, -100.137 72.8146, -100.13 73.3881, -100.122 73.9616, -100.113 74.535, -100.104 75.1083, -100.094 75.6817, -100.083 76.255, -100.071 76.8283, -100.058 77.4016, -100.044 77.9748, -100.029 78.548, -100.012 79.1212, -99.9929 79.6944, -99.9718 80.2675, -99.9481 80.8407, -99.9213 81.4138, -99.8907 81.9869, -99.8554 82.5599, -99.8142 83.133, -99.7656 83.706, -99.7073 84.279, -99.6361 84.8519, -99.5471 85.4249, -99.4327 85.9978, -99.2801 86.5706, -99.0665 87.1434, -98.7459 87.716, -98.2112 88.2884, -97.1415 88.8602, -93.9489 89.4296, 44.1383 89.9156, 73.4717 89.4102, 156.879 87.2771, 162.653 84.5853, 164.313 81.8719, 164.937 79.1527, 165.146 76.4308, 165.147 73.7069, 165.028 70.9814, 164.834 68.2545, 164.589 65.526, 164.307 62.796, 163.998 60.0643, 163.666 57.3311, 163.317 54.5961, 162.953 51.8593, 162.576 49.1209, 162.187 46.3806, 161.786 43.6387, 161.376 40.895, 160.955 38.1497, 160.524 35.4028, 160.083 32.6544, 159.632 29.9047, 159.17 27.1538, 158.698 24.4019, 158.214 21.6492, 157.717 18.8959, 157.208 16.1423, 156.685 13.3886, 156.148 10.6352, 155.595 7.88235, 155.024 5.13045, 154.435 2.3799, 153.826 -0.368877, 153.195 -3.11541, 152.54 -5.8592, 151.859 -8.59969, 151.148 -11.3363, 150.406 -14.0683, 149.628 -16.795, 148.81 -19.5157, 147.948 -22.2293, 147.036 -24.9349, 146.068 -27.6312, 145.037 -30.3171, 143.934 -32.9908, 142.749 -35.6506, 141.47 -38.2944, 140.082 -40.9196, 138.569 -43.5231, 136.907 -46.1012, 135.074 -48.6491, 133.036 -51.1612, 130.755 -53.6301, 128.184 -56.0468, 125.266 -58.3993, 121.929 -60.6725, 118.089 -62.8467, 113.647 -64.8965, 108.494 -66.7892, 102.525 -68.4834, 95.6594 -69.9291, 87.8882 -71.0696, 79.3184 -71.8472, 70.2102 -72.2146, 60.9526 -72.1465, 51.9752 -71.6475, 43.6333 -70.7513, 36.1387 -69.5096, 29.5575 -67.9808, 23.8522 -66.2201, 18.9326 -64.2747, 14.6891 -62.1832, 11.0155 -59.976, 7.81747 -57.6765, 5.0143 -55.3028, 2.53966 -52.8691, 0.33913 -50.3861, -1.6317 -47.8626, -3.40871 -45.305, -5.02146 -42.719, -6.49405 -40.1088, -7.84626 -37.4779, -9.09463 -34.8293, -10.2528 -32.1654, -11.3322 -29.4882, -12.3427 -26.7995, -13.2922 -24.1006, -14.1879 -21.3929, -15.0358 -18.6776, -15.8408 -15.9555, -16.6075 -13.2276, -17.3397 -10.4947, -18.0408 -7.75738, -18.7138 -5.01639, -19.3611 -2.27227, -19.985 0.474428, -20.5876 3.22322, -21.1706 5.97365, -21.7355 8.7253, -22.2838 11.4778, -22.8166 14.2308, -23.3351 16.9839, -23.8401 19.7369, -24.3325 22.4895, -24.8129 25.2414, -25.2821 27.9925, -25.7405 30.7425, -26.1884 33.4913, -26.6261 36.2388, -27.0538 38.9847, -27.4715 41.7291, -27.8789 44.4718, -28.2758 47.2129, -28.6614 49.9522, -29.0348 52.6898, -29.3945 55.4256, -29.7384 58.1598, -30.0634 60.8922, -30.3651 63.6231, -30.6368 66.3524, -30.868 69.0802, -31.035 72.026, -31.1124 74.7506, -31.0433 77.4736, -30.707 80.1944, -29.798 82.9117, -27.2573 85.6202, -15.4 88.2797, 67.9659 89.3932))")
        expected = wkt.loads("POLYGON ((172.541 -1.66264, 171.947 -4.41159, 171.373 -7.16139, 170.816 -9.91163, 170.276 -12.6619, 169.752 -15.4119, 169.242 -18.1614, 168.745 -20.9099, 168.261 -23.6574, 167.79 -26.4035, 167.33 -29.148, 166.881 -31.8909, 166.443 -34.6318, 166.016 -37.3709, 165.6 -40.1078, 165.195 -42.8427, 164.802 -45.5753, 164.421 -48.3058, 164.053 -51.034, 163.7 -53.7601, 163.363 -56.484, 163.047 -59.2059, 162.755 -61.9256, 162.494 -64.6434, 162.273 -67.3593, 162.109 -70.0733, 162.024 -72.7854, 162.065 -75.4955, 162.313 -78.2033, 162.956 -80.9077, 164.486 -83.6057, 168.83 -86.2853, 180 -87.36198338092518, 180 -90, -180 -90, -180 -87.36198338092518, -164.905 -88.817, -45.4789 -88.0815, -32.8484 -85.456, -29.8241 -82.7679, -28.6634 -80.0674, -28.1748 -77.3619, -28.0038 -74.6535, -28.0087 -71.9429, -28.1215 -69.2304, -28.3058 -66.516, -28.5403 -63.7998, -28.8118 -61.0816, -29.1119 -58.3615, -29.4348 -55.6394, -29.7766 -52.9151, -30.1346 -50.1887, -30.5067 -47.4601, -30.8917 -44.7294, -31.2887 -41.9965, -31.697 -39.2614, -32.1163 -36.5243, -32.5465 -33.7851, -32.9876 -31.044, -33.4397 -28.3011, -33.9032 -25.5566, -34.3785 -22.8106, -34.8661 -20.0634, -35.3667 -17.3151, -35.881 -14.566, -36.4101 -11.8164, -36.9549 -9.06669, -37.5166 -6.31712, -38.0966 -3.56812, -38.6964 -0.820084, -38.88190842757092 0, -39.3177 1.92652, -39.9626 4.6712, -40.6333 7.4134, -41.3323 10.1525, -42.0626 12.888, -42.8275 15.619, -43.6308 18.3447, -44.477 21.0643, -45.3711 23.7768, -46.3193 26.481, -47.3283 29.1757, -48.4065 31.8592, -49.5633 34.5299, -50.8103 37.1857, -52.1612 39.8241, -53.6322 42.4422, -55.2434 45.0365, -57.0185 47.6024, -58.987 50.1346, -61.1847 52.6263, -63.6555 55.0689, -66.4539 57.4515, -69.6455 59.7598, -73.3102 61.9759, -77.8972 64.2412, -82.8603 66.1818, -88.6116 67.9344, -95.2394 69.4507, -102.774 70.6752, -111.141 71.5501, -112.8107414191941 71.63817978956261, -118.109 71.2565, -126.174 70.2413, -133.363 68.8982, -139.648 67.2853, -145.086 65.4556, -149.775 63.4536, -153.824 61.3154, -157.337 59.0691, -160.402 56.7364, -163.095 54.3342, -165.478 51.8754, -167.602 49.3703, -169.509 46.827, -171.232 44.2516, -172.798 41.6494, -174.231 39.0244, -175.549 36.38, -176.768 33.719, -177.899 31.0438, -178.956 28.3563, -179.946 25.6581, -180 25.50106498388834, -180 89.63275408880213, -180 90, 180 90, 180 89.63275408880213, 180 25.50106498388834, 179.123 22.9507, 178.244 20.2355, 177.411 17.5133, 176.62 14.7854, 175.866 12.0524, 175.146 9.31522, 174.455 6.57451, 173.793 3.83093, 173.155 1.08503, 172.91253696040647 0, 172.541 -1.66264), (-19.3611 -2.27227, -18.7138 -5.01639, -18.0408 -7.75738, -17.3397 -10.4947, -16.6075 -13.2276, -15.8408 -15.9555, -15.0358 -18.6776, -14.1879 -21.3929, -13.2922 -24.1006, -12.3427 -26.7995, -11.3322 -29.4882, -10.2528 -32.1654, -9.09463 -34.8293, -7.84626 -37.4779, -6.49405 -40.1088, -5.02146 -42.719, -3.40871 -45.305, -1.6317 -47.8626, 0.33913 -50.3861, 2.53966 -52.8691, 5.0143 -55.3028, 7.81747 -57.6765, 11.0155 -59.976, 14.6891 -62.1832, 18.9326 -64.2747, 23.8522 -66.2201, 29.5575 -67.9808, 36.1387 -69.5096, 43.6333 -70.7513, 51.9752 -71.6475, 60.9526 -72.1465, 70.2102 -72.2146, 79.3184 -71.8472, 87.8882 -71.0696, 95.6594 -69.9291, 102.525 -68.4834, 108.494 -66.7892, 113.647 -64.8965, 118.089 -62.8467, 121.929 -60.6725, 125.266 -58.3993, 128.184 -56.0468, 130.755 -53.6301, 133.036 -51.1612, 135.074 -48.6491, 136.907 -46.1012, 138.569 -43.5231, 140.082 -40.9196, 141.47 -38.2944, 142.749 -35.6506, 143.934 -32.9908, 145.037 -30.3171, 146.068 -27.6312, 147.036 -24.9349, 147.948 -22.2293, 148.81 -19.5157, 149.628 -16.795, 150.406 -14.0683, 151.148 -11.3363, 151.859 -8.59969, 152.54 -5.8592, 153.195 -3.11541, 153.826 -0.368877, 153.90772583407093 0, 154.435 2.3799, 155.024 5.13045, 155.595 7.88235, 156.148 10.6352, 156.685 13.3886, 157.208 16.1423, 157.717 18.8959, 158.214 21.6492, 158.698 24.4019, 159.17 27.1538, 159.632 29.9047, 160.083 32.6544, 160.524 35.4028, 160.955 38.1497, 161.376 40.895, 161.786 43.6387, 162.187 46.3806, 162.576 49.1209, 162.953 51.8593, 163.317 54.5961, 163.666 57.3311, 163.998 60.0643, 164.307 62.796, 164.589 65.526, 164.834 68.2545, 165.028 70.9814, 165.147 73.7069, 165.146 76.4308, 164.937 79.1527, 164.313 81.8719, 162.653 84.5853, 156.879 87.2771, 73.4717 89.4102, 72.66275828626124 89.42413766635043, 67.9659 89.3932, -15.4 88.2797, -27.2573 85.6202, -29.798 82.9117, -30.707 80.1944, -31.0433 77.4736, -31.1124 74.7506, -31.035 72.026, -30.868 69.0802, -30.6368 66.3524, -30.3651 63.6231, -30.0634 60.8922, -29.7384 58.1598, -29.3945 55.4256, -29.0348 52.6898, -28.6614 49.9522, -28.2758 47.2129, -27.8789 44.4718, -27.4715 41.7291, -27.0538 38.9847, -26.6261 36.2388, -26.1884 33.4913, -25.7405 30.7425, -25.2821 27.9925, -24.8129 25.2414, -24.3325 22.4895, -23.8401 19.7369, -23.3351 16.9839, -22.8166 14.2308, -22.2838 11.4778, -21.7355 8.7253, -21.1706 5.97365, -20.5876 3.22322, -19.985 0.474428, -19.877235830367965 0, -19.3611 -2.27227))")
        print(geometry)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geometry))
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(reworked)
        self.assertTrue(geometry_compare(reworked, expected, 0.0),
                        "Reworked geometry is not equivalent to the expected")

    def test_rework_cdse_product_line_no_pole_antimeridian(self):
        """Thin line footprint products shall be managed by product type first.
           No need to wast resources to recognize and handle thin polygons.
           index 16 footprint is S3A product type SR_2_LAN_LI from CDSE
           S3A_SR_2_LAN_LI_20240302T235923_20240303T001845_20240304T182116_1161_109_330______PS1_O_ST_005
        """
        index = 16
        geom = fp_to_geometry(self.footprints[index])
        print(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_linestring_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiLineString)
        self.assertAlmostEqual(int(rwkd.length), 180, delta=5)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_line_no_pole_no_antimeridian(self):
        """Thin line footprint products shall be managed by product type first.
           No need to wast resources to recognize and handle thin polygons.

           index 21 footprint is S3A product type SR_2_WAT from CDSE
           S3A_SR_2_WAT____20240312T172025_20240312T180447_20240314T075541_2661_110_083______MAR_O_ST_005
           cdse product id: f4b8547b-45ff-430c-839d-50a9be9c6105
        """
        index = 21
        geom = fp_to_geometry(self.footprints[index])
        self.assertFalse(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_linestring_geometry(geom)
        self.assertFalse(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.LineString)
        self.assertAlmostEqual(int(rwkd.length), 220, delta=5)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_south_hemisphere_no_pole_antimeridian(self):
        """
        Footprint index 2 is a small simple footprint crossing antimeridan
        """
        footprint = self.footprints[2]
        geom = fp_to_geometry(footprint)
        self.assertEqual(footprint_facility.check_cross_antimeridian(geom),
                         footprint['antimeridian'])
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertAlmostEqual(int(rwkd.area), 18, delta=1)
        print(footprint_facility.to_geojson(rwkd))

    def testSimplifySimple(self):
        """
        Ensure an already simple polygon is not affected by the algorithm
        """
        index = 0
        geom = fp_to_geometry(self.footprints[index])

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        rwkd = footprint_facility.simplify(geom, tolerance=.1,
                                           tolerance_in_meter=False)

        self.assertFalse(shapely.is_empty(rwkd) or shapely.is_missing(rwkd),
                         "Geometry is empty.")
        self.assertEqual(rwkd.area, origin_area, "Surface Area changed")
        self.assertEqual(len(shapely.get_coordinates(rwkd)), points_number)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")

    def test_simplify_simple_meter(self):
        """
        Ensure an already simple polygon is not affected by the algorithm
        """
        index = 0
        geom = fp_to_geometry(self.footprints[index])

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        rwkd = footprint_facility.simplify(geom, tolerance=1000,
                                           tolerance_in_meter=True)

        self.assertFalse(shapely.is_empty(rwkd) or shapely.is_missing(rwkd),
                         "Geometry is empty.")
        self.assertAlmostEqual(rwkd.area, origin_area, delta=0.0001,
                               msg="Surface Area changed")
        self.assertEqual(len(shapely.get_coordinates(rwkd)), points_number)
        self.assertTrue(shapely.equals(shapely.set_precision(geom, 0.0001),
                                       shapely.set_precision(rwkd, 0.0001)),
                        "Generated footprints are not equivalents")

    def testSimplifyAntimeridian(self):
        """
        Ensure an already simple polygon , crossing antimeridian
        is not affected by the algorithm
        """
        index = 3
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        rwkd = footprint_facility.simplify(geom, tolerance=.1,
                                           tolerance_in_meter=False)
        print(rwkd)

        self.assertEqual(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertFalse(shapely.is_empty(rwkd) or shapely.is_missing(rwkd),
                         "Geometry is empty.")
        self.assertTrue(geometry_compare(rwkd, geom, 0.1),
                        msg="Surface Area changed outside the tolerance rate.")

    def testLongNoAntimeridian(self):
        """
        Use Long polygon not located on the antimeridian.
        Simplification shall reduce the number of coordinates
        :return: simplified polygon
        """
        index = 15
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))

        print(footprint_facility.to_geojson(geom))

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        self.assertEqual(points_number, 211)
        self.assertAlmostEqual(origin_area, 2976.02, delta=0.01)

        # No change expected
        stats = self.simplify_bench(geom, tolerance=0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2976.02, delta=0.01)
        self.assertEqual(stats['Points']['new'], 211)

        # small choice
        stats = self.simplify_bench(geom, tolerance=.05)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2977.53, delta=0.01)
        self.assertEqual(stats['Points']['new'], 87)

        # Best choice for 1% area change
        stats = self.simplify_bench(geom, tolerance=.45)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 3005.78, delta=0.01)
        self.assertEqual(stats['Points']['new'], 26)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=1.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 3015.72, delta=0.01)
        self.assertEqual(stats['Points']['new'], 21)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=2.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 3036.00, delta=0.01)
        self.assertEqual(stats['Points']['new'], 13)

    def testLongWithAntimeridian(self):
        """
        Use Long polygon not located on the antimeridian.
        Simplification shall reduce the number of coordinates
        """
        index = 17
        print(fp_to_geometry(self.footprints[index]))
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))
        print(geom)

        expected = wkt.loads('MULTIPOLYGON (((172.5903563957689 0, 172.963 1.67973, 173.352 3.46961, 173.733 5.26056, 174.107 7.05198, 174.473 8.84373, 174.833 10.6359, 175.187 12.428, 175.535 14.2207, 175.878 16.0132, 176.215 17.8055, 176.547 19.5975, 176.874 21.3902, 177.197 23.1829, 177.515 24.9732, 177.829 26.7649, 178.139 28.5557, 178.446 30.3462, 178.749 32.136, 179.048 33.9253, 179.344 35.714, 179.637 37.5022, 179.927 39.2897, 180 39.74572027972022, 180 0, 180 -21.411921393034845, 179.741 -22.5742, 179.336 -24.3769, 178.925 -26.1785, 178.51 -27.9793, 178.088 -29.779, 177.66 -31.5775, 177.223 -33.3749, 176.777 -35.171, 176.32 -36.9658, 175.852 -38.7588, 175.37 -40.5512, 174.873 -42.3412, 174.359 -44.1293, 173.825 -45.9162, 173.268 -47.701, 172.686 -49.4835, 172.075 -51.2638, 171.43 -53.0416, 170.746 -54.8167, 170.016 -56.5887, 169.233 -58.3574, 168.387 -60.1222, 167.466 -61.8825, 166.457 -63.6378, 165.336 -65.3872, 164.084 -67.1292, 162.666 -68.8619, 161.038 -70.5835, 159.142 -72.2919, 156.895 -73.9811, 154.178 -75.6455, 150.818 -77.2759, 146.557 -78.8572, 141.004 -80.3652, 135.065 -81.5223, 132.042 -81.0921, 129.344 -80.6474, 126.895 -80.1846, 124.668 -79.7059, 122.641 -79.2133, 120.79 -78.7088, 119.098 -78.1939, 117.547 -77.6698, 116.121 -77.1376, 114.808 -76.5984, 113.595 -76.0528, 112.471 -75.5014, 111.428 -74.9449, 110.46 -74.3847, 109.555 -73.8191, 108.711 -73.2507, 107.92 -72.6785, 107.179 -72.1035, 106.44 -71.4926, 110.785 -70.9165, 115.711 -70.0864, 120.232 -69.1303, 124.351 -68.0648, 128.089 -66.9054, 131.476 -65.6648, 134.544 -64.3539, 137.324 -62.9855, 139.848 -61.5663, 142.146 -60.1027, 144.245 -58.6014, 146.165 -57.068, 147.93 -55.5066, 149.555 -53.9205, 151.058 -52.3129, 152.452 -50.686, 153.749 -49.0427, 154.959 -47.3846, 156.091 -45.7131, 157.154 -44.0299, 158.153 -42.336, 159.097 -40.6325, 159.989 -38.9207, 160.834 -37.2011, 161.637 -35.4739, 162.402 -33.7409, 163.132 -32.0018, 163.829 -30.2574, 164.497 -28.508, 165.138 -26.7543, 165.754 -24.9965, 166.347 -23.2349, 166.918 -21.4703, 167.47 -19.7018, 168.003 -17.93, 168.519 -16.1574, 169.02 -14.3815, 169.506 -12.603, 169.978 -10.8229, 170.437 -9.04089, 170.884 -7.25724, 171.319 -5.47231, 171.745 -3.68586, 172.16 -1.89834, 172.566 -0.109789, 172.5903563957689 0)), ((-180 0, -180 39.74572027972022, -179.787 41.0763, -179.503 42.8624, -179.222 44.6478, -178.944 46.4324, -178.669 48.2164, -178.397 49.9996, -178.127 51.7821, -177.859 53.5635, -177.596 55.3449, -177.334 57.1252, -177.076 58.9046, -176.821 60.6838, -176.569 62.4618, -176.322 64.2393, -176.08 66.0178, -175.841 67.7931, -175.609 69.5687, -175.385 71.3448, -175.171 73.1193, -173.043 73.0882, -170.927 73.034, -168.826 72.9582, -166.745 72.8609, -164.69 72.7427, -162.665 72.6038, -160.672 72.445, -158.716 72.2664, -156.8 72.0689, -154.927 71.853, -153.097 71.6194, -151.313 71.3688, -149.577 71.1018, -147.888 70.819, -146.248 70.5213, -144.657 70.2092, -143.114 69.8836, -141.62 69.545, -140.171 69.1934, -142.972 67.6634, -145.437 66.0924, -147.622 64.4891, -149.571 62.859, -151.322 61.2048, -152.904 59.5326, -154.344 57.8444, -155.661 56.142, -156.872 54.4279, -157.991 52.7036, -159.03 50.9696, -160 49.2286, -160.907 47.4802, -161.76 45.7255, -162.565 43.9653, -163.328 42.2001, -164.052 40.4305, -164.741 38.6567, -165.4 36.8793, -166.031 35.0986, -166.637 33.3148, -167.22 31.5282, -167.783 29.7392, -168.328 27.9478, -168.855 26.1542, -169.367 24.3589, -169.865 22.5615, -170.351 20.7634, -170.824 18.9629, -171.287 17.1613, -171.741 15.3589, -172.185 13.5553, -172.623 11.7509, -173.052 9.9454, -173.476 8.13948, -173.893 6.33294, -174.306 4.52588, -174.714 2.71852, -175.118 0.910718, -175.3200189385537 0, -175.519 -0.897023, -175.917 -2.70497, -176.313 -4.51289, -176.707 -6.32075, -177.1 -8.12844, -177.492 -9.93579, -177.883 -11.7429, -178.275 -13.5496, -178.668 -15.3557, -179.062 -17.1616, -179.458 -18.9665, -179.857 -20.7702, -180 -21.411921393034845, -180 0)))')
        self.assertTrue(geometry_compare(geom, expected, .01),
                        msg="reworked not well formed")

        # No change expected
        stats = self.simplify_bench(geom, tolerance=0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2961.08, delta=0.01)
        self.assertEqual(stats['Points']['new'], 216)

        # small choice
        stats = self.simplify_bench(geom, tolerance=.05)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2963.20, delta=0.01)
        self.assertEqual(stats['Points']['new'], 87)

        # Best choice for 1% area change
        stats = self.simplify_bench(geom, tolerance=.45)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2981.7, delta=0.1)
        self.assertEqual(stats['Points']['new'], 32)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=1.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2998.01, delta=0.01)
        self.assertEqual(stats['Points']['new'], 25)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=2.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 3067.11, delta=0.01)
        self.assertEqual(stats['Points']['new'], 18)

    def testLongWithAntimeridianAndPole(self):
        """
        Use Long polygon not located on the antimeridian.
        Simplification shall reduce the number of coordinates
        :return: simplified polygon
        """
        index = 18
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))
        print(footprint_facility.to_geojson(geom))

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        self.assertEqual(points_number, 268)
        self.assertAlmostEqual(origin_area, 10857.59, delta=0.01)

        # No change expected
        stats = self.simplify_bench(geom, tolerance=0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 10857.59, delta=0.01)
        self.assertEqual(stats['Points']['new'], 268)

        # small choice
        stats = self.simplify_bench(geom, tolerance=.05)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 10863.09, delta=0.01)
        self.assertEqual(stats['Points']['new'], 158)

        # Best choice for 1% area change
        stats = self.simplify_bench(geom, tolerance=.45)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 10940.81, delta=0.01)
        self.assertEqual(stats['Points']['new'], 76)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=1.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 11030.09, delta=0.01)
        self.assertEqual(stats['Points']['new'], 50)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=2.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 11082.19, delta=0.01)
        self.assertEqual(stats['Points']['new'], 43)

    def iter_among_simplify_tolerance(self, geometry, min: float, max: float,
                                      step: float):
        for tolerance in (map(lambda x: x / 10000.0,
                              range(int(min * 10000),
                                    int(max * 10000),
                                    int(step * 10000)))):
            print(self.simplify_bench(geometry, tolerance))

    @staticmethod
    def simplify_bench(geometry, tolerance=.1):
        origin_area = getattr(geometry, 'area', 0)
        origin_points_number = len(shapely.get_coordinates(geometry))

        reworked = footprint_facility.simplify(geometry, tolerance=tolerance,
                                               tolerance_in_meter=False)
        new_area = reworked.area
        variation_area = (new_area - origin_area) / origin_area
        new_points_number = len(shapely.get_coordinates(reworked))
        variation_point = ((new_points_number - origin_points_number) /
                           origin_points_number)
        return dict(value=tolerance,
                    Points=dict(
                        origin=origin_points_number,
                        new=new_points_number,
                        variation=variation_point),
                    Area=dict(
                        origin=origin_area,
                        new=new_area,
                        variation=variation_area))

    def testSimplifySynergyEurope(self):
        """
        Europe Syngery footprint has 297 point to be simplified
        :return:
        """
        index = 22
        geom = fp_to_geometry(self.footprints[index])
        self.assertTrue("EUROPE" in self.footprints[index]['name'],
                        f"Wrong name {self.footprints[index]['name']}")
        self.assertEqual(len(shapely.get_coordinates(geom)), 297)
        self.assertTrue(shapely.is_valid(geom))

        rwkd = footprint_facility.simplify(geom, tolerance=0.0,
                                           preserve_topology=True,
                                           tolerance_in_meter=False)
        self.assertEqual(len(shapely.get_coordinates(rwkd)), 5)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")

    def testSimplifySynergyAustralia(self):
        """
        Australia Syngery footprint has 295 point to be simplified
        :return:
        """
        index = 23
        geom = fp_to_geometry(self.footprints[index])
        print(geom)
        self.assertTrue("AUSTRALASIA" in self.footprints[index]['name'],
                        f"Wrong name {self.footprints[index]['name']}")
        self.assertEqual(len(shapely.get_coordinates(geom)), 295)
        self.assertTrue(shapely.is_valid(geom))

        rwkd = footprint_facility.simplify(geom, tolerance=0.0,
                                           preserve_topology=True,
                                           tolerance_in_meter=False)
        self.assertEqual(len(shapely.get_coordinates(rwkd)), 5)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")
        print(footprint_facility.to_geojson(rwkd))

    def test_print_geojson_all(self):
        for index, footprint in enumerate(self.footprints):
            method = footprint.get('method', None)
            if footprint.get('testable', True) and method:
                geom = fp_to_geometry(footprint)
                reworked = None
                try:
                    if method.lower() == 'polygon':
                        reworked = (footprint_facility.
                                    rework_to_polygon_geometry(geom))
                    elif method.lower() == 'linestring':
                        reworked = (footprint_facility.
                                    rework_to_linestring_geometry(geom))
                    print(
                        f"{index}-{footprint['name']}: "
                        f"{footprint_facility.to_geojson(reworked)}")
                except Exception as exception:
                    print(f"WARN: {index}-{footprint['name']} "
                          f"raised an exception ({repr(exception)})")
                    print(geom)

    def test_print_wkt_all(self):
        for index, footprint in enumerate(self.footprints):
            method = footprint.get('method', None)
            if footprint.get('testable', True) and method:
                geom = fp_to_geometry(footprint)
                reworked = None
                try:
                    if method.lower() == 'polygon':
                        reworked = (footprint_facility.
                                    rework_to_polygon_geometry(geom))
                    elif method.lower() == 'linestring':
                        reworked = (footprint_facility.
                                    rework_to_linestring_geometry(geom))
                    print(
                        f"{index}-{footprint['name']}: "
                        f"{footprint_facility.to_wkt(reworked)}")
                except Exception as exception:
                    print(f"WARN: {index}-{footprint['name']} "
                          f"raised an exception ({repr(exception)})")

    def test_S1A_WV_SLC__1SSV_no_antimeridian(self):
        """
        Manage imagette of Sentinel-1 wave mode.
        This Test use real manifest.safe file of S1A WV data.
        convex hull algortihm generates a polygon reducing points number
        from 470 to 53.
        """
        filename = ('S1A_WV_SLC__1SSV_20240408T072206_20240408T074451_053339_'
                    '0677B9_0282.manifest.safe')
        path = os.path.join(os.path.dirname(__file__), 'samples', filename)

        # Extract data from manifest
        import xml.etree.ElementTree as ET
        tree = ET.parse(path)
        root = tree.getroot()

        ns_safe = "{http://www.esa.int/safe/sentinel-1.0}"
        ns_gml = "{http://www.opengis.net/gml}"
        xpath = (f".//metadataObject[@ID='measurementFrameSet']/metadataWrap/"
                 f"xmlData/{ns_safe}frameSet/{ns_safe}frame/"
                 f"{ns_safe}footPrint/{ns_gml}coordinates")
        coordinates = root.findall(xpath)

        # build the python geometry
        polygons = []
        for coord in coordinates:
            footprint = dict(coord_order="lat lon", coords=coord.text)
            polygons.append(
                footprint_facility.
                rework_to_polygon_geometry(fp_to_geometry(footprint)))

        geometry = shapely.MultiPolygon(polygons)
        self.assertEqual(
            len(shapely.get_coordinates(geometry)), 470)
        self.assertEqual(len(
            shapely.get_coordinates(geometry.convex_hull)), 53)

    def test_S1A_WV_SLC__1SSV_crossing_antimeridian(self):
        """
        Manage imagette of Sentinel-1 wave mode.
        This Test use real manifest.safe file of S1A WV data. This data crosses
        the antimridian.
        Convex hull algortihm generates a polygon reducing points number
        from 470 to 53. But This algorithm does not support antimeridian
        singularity, it shall be split into 2 polygons before execution.
        :return:
        """
        filename = ('S1A_WV_SLC__1SSV_20240405T060850_20240405T062741_053294_'
                    '0675E8_157E.manifest.safe')
        path = os.path.join(os.path.dirname(__file__), 'samples', filename)

        # Extract data from manifest
        import xml.etree.ElementTree as ET
        tree = ET.parse(path)
        root = tree.getroot()

        ns_safe = "{http://www.esa.int/safe/sentinel-1.0}"
        ns_gml = "{http://www.opengis.net/gml}"
        xpath = (f".//metadataObject[@ID='measurementFrameSet']/metadataWrap/"
                 f"xmlData/{ns_safe}frameSet/{ns_safe}frame/"
                 f"{ns_safe}footPrint/{ns_gml}coordinates")
        coordinates = root.findall(xpath)

        # build the python geometry
        polygons = []
        for coord in coordinates:
            footprint = dict(coord_order="lat lon", coords=coord.text)
            polygons.append(
                footprint_facility.
                rework_to_polygon_geometry(fp_to_geometry(footprint)))
        geometry = shapely.MultiPolygon(polygons)

        east_geometry = geometry.intersection(shapely.box(-180, -90, 0, 90))
        west_geometry = geometry.intersection(shapely.box(0, -90, 180, 90))

        self.assertEqual(len(shapely.get_coordinates(geometry)), 390)
        self.assertEqual(
            len(shapely.get_coordinates(east_geometry.convex_hull)) +
            len(shapely.get_coordinates(west_geometry.convex_hull)), 49)

    def test_jan_07_06_2024_S1(self):
        """
        Issue reported by 07/06/2024,
        regarding product reported from https://datahub.creodias.eu/odata/v1
        "S1A_EW_OCN__2SDH_20240602T183043_20240602T183154_054148_0695B3_"
        "DC42.SAFE"

        Command line used:
        <code>
        #Sentinel-6
        product="S1A_EW_OCN__2SDH_20240602T183043_20240602T183154_054148_"
                "0695B3_DC42.SAFE"
        wget -qO - 'https://datahub.creodias.eu/odata/v1/Products?'
                                '$filter=((Name%20eq%20%27'$product'%27))' |
            jq '.value[] | .Footprint' |
            tr -d '"' |
            tr -d "'" |
            cut -f 2 -d ';' |
            xargs -I {} python3 -c '
              from footprint_facility import to_wkt,rework_to_polygon_geometry;
              from shapely import wkt;
              print(to_wkt(rework_to_polygon_geometry(wkt.loads("{}"))));'
        </code>
        """

        product = ("MULTIPOLYGON (((-174.036011 66.098473, -170.292542 "
                   "70.167793, -180 71.02345651890965, "
                   "-180 66.64955743876074, -174.036011 66.098473)), "
                   "((180 66.64955743876074, 180 71.02345651890965, "
                   "178.781082 71.130898, 176.806686 66.944626, "
                   "180 66.64955743876074)))")
        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_jan_07_06_2024_S2(self):
        """
        Issue reported 07/06/2024,
        regarding product reported from https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20240111T183749_N0510_R141_T01CDN_20240112T201221.SAFE"

        Command line used:
        <code>
        #Sentinel-6
        product="S2B_MSIL1C_20240111T183749_N0510_R141_T01CDN_"
                "20240112T201221.SAFE"
        wget -qO - 'https://datahub.creodias.eu/odata/v1/Products?'
                              '$filter=((Name%20eq%20%27'$product'%27))' |
           jq '.value[] | .Footprint' |
           tr -d '"' |
           tr -d "'" |
           cut -f 2 -d ';' |
           xargs -I {} python3 -c '
              from footprint_facility import to_wkt,rework_to_polygon_geometry;
              from shapely import wkt;
              print(to_wkt(rework_to_polygon_geometry(wkt.loads("{}"))));'
        </code>
        """
        product = ("POLYGON ((-179.508117526313 -79.16127199879642, -180 "
                   "-79.01692999138557, -180 -79.19944296655834, "
                   "-180 -79.19959581716972, -180 -79.19972960600606, "
                   "-180 -79.19988578232916, -180 -79.20007346017209, "
                   "-180 -79.20013436682478, -180 -79.20024126342099, "
                   "-180 -79.20029258993124, -180 -79.20049921536173, "
                   "-180 -79.20054631332516, -180 -79.20066396817484, "
                   "-180 -79.20077375877023, -180 -79.2008843839914, "
                   "-180 -79.21714918681978, -180 -79.21715630792468, "
                   "-180 -79.2175551235766, -180 -79.21773293229286, "
                   "-180 -79.21778003784787, -180 -79.2177900670303, "
                   "-180 -79.21779114542757, -180 -79.21779351757006, "
                   "-180 -79.21780296489362, -180 -79.21780421542903, "
                   "-180 -79.21780998189048, -180 -79.21827514353097, "
                   "-180 -79.21830910412172, -180 -79.33237518158053, "
                   "-178.9375581912928 -79.33974790172739, "
                   "-179.5490821971551 -79.1659353807717, -179.5463891574934 "
                   "-79.16562951391516, -179.5464126641663 "
                   "-79.16562282940411, -179.508117526313 "
                   "-79.16127199879642))")
        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_jan_07_06_2024_S3(self):
        """
        Issue reported 07/06/2024,
        regarding product reported from https://datahub.creodias.eu/odata/v1
        "S3A_SL_2_LST____20240601T075148_20240601T075448_20240601T102247_0180_
            113_078_1080_PS1_O_NR_004.SEN3"

        Command line used:
        <code>
        #Sentinel-6
        product="S3A_SL_2_LST____20240601T075148_20240601T075448_"
                "20240601T102247_0180_113_078_1080_PS1_O_NR_004.SEN3"
        wget -qO - 'https://datahub.creodias.eu/odata/v1/Products?'
                   '$filter=((Name%20eq%20%27'$product'%27))' |
           jq '.value[] | .Footprint' |
           tr -d '"' |
           tr -d "'" |
           cut -f 2 -d ';' |
           xargs -I {} python3 -c '
              from footprint_facility import to_wkt,rework_to_polygon_geometry;
              from shapely import wkt;
              print(to_wkt(rework_to_polygon_geometry(wkt.loads("{}"))));'
        </code>
        """
        product = ("MULTIPOLYGON (((180 65.68414879114478, 179.764 65.842, "
                   "175.686 68.0499, 170.896 70.1128, 171.256 70.2301, "
                   "172.291 70.5293, 173.355 70.8266, 174.424 71.108, "
                   "175.533 71.393, 176.703 71.6691, 177.869 71.9409, "
                   "179.088 72.1986, 180 72.38208313539192, "
                   "180 65.68414879114478)), ((-180 72.38208313539192, "
                   "-179.649 72.4527, -178.36 72.6974, -177.039 72.9329, "
                   "-175.694 73.1682, -174.288 73.3878, -172.854 73.5962, "
                   "-171.396 73.7949, -169.91 73.9844, -168.382 74.1639, "
                   "-166.798 74.3324, -165.214 74.4841, -163.563 74.6311, "
                   "-161.917 74.7626, -160.247 74.8843, -158.545 74.996, "
                   "-156.815 75.0909, -155.079 75.1715, -153.303 75.2416, "
                   "-151.49 75.2841, -149.712 75.3291, -147.895 75.3655, "
                   "-146.1 75.3717, -145.923 72.801, -145.686 70.1856, "
                   "-145.411 67.5691, -145.11 64.9601, -145.109 64.9514, "
                   "-146.171 64.9259, -147.266 64.8952, -148.33 64.8479, "
                   "-149.397 64.7954, -150.451 64.7395, -151.517 64.6709, "
                   "-152.57 64.5974, -153.604 64.5188, -154.67 64.4338, "
                   "-155.683 64.3383, -156.721 64.2411, -157.73 64.1281, "
                   "-158.74 64.0097, -159.743 63.8851, -160.753 63.7556, "
                   "-161.729 63.6187, -162.7 63.475, -163.671 63.3246, "
                   "-164.625 63.169, -165.557 62.9984, -166.489 62.8312, "
                   "-167.416 62.6562, -168.325 62.4771, -169.236 62.2889, "
                   "-170.112 62.094, -170.979 61.896, -171.853 61.6965, "
                   "-172.713 61.4854, -173.554 61.2618, -173.86 61.1864, "
                   "-173.885 61.1901, -176.803 63.5458, "
                   "-180 65.68414879114478, -180 72.38208313539192)))")
        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_jan_07_06_2024_S5P(self):
        """
        Issue reported 07/06/2024,
        regarding product reported from https://datahub.creodias.eu/odata/v1
        "S5P_OFFL_L1B_RA_BD8_20240601T002118_20240601T020248_34371_03_020100_"
        "20240601T035317.nc"

        Command line used:
        <code>
        #Sentinel-6
        product="S5P_OFFL_L1B_RA_BD8_20240601T002118_20240601T020248_34371_"
                "03_020100_20240601T035317.nc"
        wget -qO - 'https://datahub.creodias.eu/odata/v1/Products?'
                   '$filter=((Name%20eq%20%27'$product'%27))' |
           jq '.value[] | .Footprint' |
           tr -d '"' |
           tr -d "'" |
           cut -f 2 -d ';' |
           xargs -I {} python3 -c '
              from footprint_facility import to_wkt,rework_to_polygon_geometry;
              from shapely import wkt;
              print(to_wkt(rework_to_polygon_geometry(wkt.loads("{}"))));'
        </code>
        """
        product = ("MULTIPOLYGON (((-180 90, 0 90, 180 90, 180 "
                   "-41.86733642322825, 179.9763 -41.531116, 179.86395 "
                   "-40.08868, 179.74141 -38.645264, 179.60912 -37.200897, "
                   "179.46786 -35.75559, 179.31769 -34.30946, 179.15906 "
                   "-32.862434, 178.99269 -31.414688, 178.81853 -29.966076, "
                   "178.63658 -28.516865, 178.44719 -27.067, 178.25061 "
                   "-25.61658, 178.04707 -24.165606, 177.8364 -22.714108, "
                   "177.61887 -21.262264, 177.39426 -19.81008, 177.1631 "
                   "-18.357447, 176.925 -16.904694, 176.68001 -15.451712, "
                   "176.42805 -13.998643, 176.16916 -12.545524, 175.90312 "
                   "-11.092463, 175.63004 -9.639457, 175.3496 -8.186663, "
                   "175.06177 -6.734143, 174.76614 -5.281979, 174.46315 "
                   "-3.8302007, 174.15176 -2.378978, 173.8324 -0.9284125, "
                   "173.50458 0.5215158, 173.16786 1.9705427, 172.82219 "
                   "3.4187272, 172.46709 4.8658676, 172.10217 6.3118157, "
                   "171.7273 7.756614, 171.34175 9.199921, 170.94524 "
                   "10.641779, 170.53746 12.082073, 170.11725 13.520405, "
                   "169.68442 14.956774, 169.2385 16.391098, 168.77852 "
                   "17.823135, 168.3039 19.252695, 167.81377 20.679672, "
                   "167.30734 22.103739, 166.78372 23.524765, 166.24197 "
                   "24.942528, 165.68028 26.356531, 165.09837 27.766888, "
                   "164.4945 29.173054, 163.86742 30.57479, 163.21565 "
                   "31.971884, 162.53703 33.36365, 161.83011 34.749847, "
                   "161.09294 36.13012, 160.32303 37.503757, 159.51851 "
                   "38.87066, 158.67624 40.229736, 157.79373 41.58067, "
                   "156.86758 42.922604, 155.89424 44.254745, 154.87033 "
                   "45.576374, 153.79134 46.886234, 152.65265 48.1834, "
                   "151.44977 49.466858, 150.1766 50.734867, 148.82782 "
                   "51.986423, 147.3959 53.21909, 145.87462 54.431526, "
                   "144.25616 55.6216, 142.53186 56.786644, 140.6929 "
                   "57.92401, 138.73013 59.03079, 136.63399 60.103626, "
                   "134.3939 61.13849, 132.00021 62.131363, 129.44383 "
                   "63.077717, 126.71549 63.972107, 123.80851 64.80932, "
                   "120.71825 65.58352, 117.4435 66.28858, 113.9866 "
                   "66.91782, 110.35588 67.46508, 106.56541 67.92443, "
                   "102.63593 68.29027, 98.59393 68.55761, 94.47231 "
                   "68.723015, 90.30819 68.78379, 86.14067 68.73939, "
                   "82.00989 68.59008, 77.953156 68.338196, 74.004 67.98733, "
                   "70.19006 67.54217, 66.53354 67.00781, 63.048588 "
                   "66.390724, 59.74498 65.69689, 56.62577 64.93289, "
                   "53.69056 64.10463, 50.934845 63.218437, 48.35202 "
                   "62.279533, 45.933685 61.293293, 43.670315 60.264317, "
                   "41.552414 59.196846, 39.569862 58.094654, 37.71257 "
                   "56.961403, 35.971294 55.800068, 34.337177 54.613335, "
                   "32.801754 53.40378, 31.356928 52.17355, 29.996086 "
                   "50.924458, 28.712265 49.658478, 27.499353 48.377003, "
                   "26.351748 47.081535, 25.264315 45.773205, 23.509417 "
                   "46.187706, 22.387592 46.436874, 19.424397 47.043514, "
                   "18.469027 47.22568, 16.448671 47.595142, 15.751153 "
                   "47.719036, 13.117875 48.17936, 12.130072 48.35204, "
                   "9.9415 48.740776, 9.136205 48.886753, 7.1947713 "
                   "49.245853, 6.4209137 49.39178, 4.406008 49.77871, "
                   "3.5373578 49.94825, 1.0665072 50.43534, -0.1086481 "
                   "50.66653, -2.2045333 51.070694, -3.02813 51.2248, "
                   "-5.5050035 51.66518, -6.7307587 51.867783, -9.840376 "
                   "52.32859, -10.816945 52.456486, -11.346613 52.522366, "
                   "-11.343067 52.666473, -11.319423 54.106884, -11.315634 "
                   "55.54611, -11.333933 56.984184, -11.37619 58.420925, "
                   "-11.446254 59.856216, -11.548398 61.290066, -11.686891 "
                   "62.722286, -11.867555 64.152725, -12.096516 65.58102, "
                   "-12.384995 67.007065, -12.7416525 68.4305, -13.182033 "
                   "69.850876, -13.724232 71.26764, -14.393544 72.67994, "
                   "-15.221556 74.08696, -16.253458 75.48708, -17.554081 "
                   "76.87837, -19.21444 78.25778, -21.374022 79.62078, "
                   "-24.246838 80.96009, -28.17806 82.26377, -33.747017 "
                   "83.51025, -41.931393 84.65964, -54.259308 85.634834, "
                   "-72.295746 86.2957, -94.80977 86.46186, -115.950935 "
                   "86.07003, -131.49446 85.25663, -141.87256 84.19631, "
                   "-148.8116 83.00032, -153.60501 81.72725, -157.0416 "
                   "80.407684, -159.58424 79.058525, -161.51413 77.6892, "
                   "-163.01147 76.30584, -164.1911 74.91215, -165.13258 "
                   "73.51075, -165.89003 72.103264, -166.50316 70.69103, "
                   "-167.00111 69.27482, -167.40501 67.85531, -167.73248 "
                   "66.43314, -167.99614 65.00868, -168.20502 63.582, "
                   "-168.36803 62.153614, -168.49158 60.72353, -168.58104 "
                   "59.291912, -168.6403 57.859013, -168.6735 56.42478, "
                   "-168.6834 54.989403, -168.67216 53.55279, -168.64241 "
                   "52.11524, -168.59605 50.676617, -168.53398 49.23707, "
                   "-168.458 47.7965, -168.36926 46.35513, -168.26866 "
                   "44.912914, -168.15657 43.469837, -168.03493 42.02598, "
                   "-167.90309 40.58142, -167.76227 39.136147, -167.61287 "
                   "37.69012, -167.45518 36.243496, -167.28972 34.796215, "
                   "-167.11655 33.34833, -166.93604 31.899948, -166.7488 "
                   "30.450903, -166.55434 29.001495, -166.35318 27.551653, "
                   "-166.14563 26.10141, -165.93146 24.65076, -165.71072 "
                   "23.199873, -165.48364 21.748617, -165.25038 20.297253, "
                   "-165.01054 18.84571, -164.7642 17.394058, -164.51172 "
                   "15.942321, -164.25249 14.490606, -163.98685 13.039, "
                   "-163.71452 11.58754, -163.4353 10.136244, -163.1493 "
                   "8.685246, -162.85625 7.23458, -162.55586 5.7843776, "
                   "-162.24821 4.334724, -161.93277 2.885562, -161.60968 "
                   "1.4371812, -161.27832 -0.010504091, -160.93875 "
                   "-1.4573016, -160.59015 -2.9031165, -160.2327 -4.3478966, "
                   "-159.86583 -5.791431, -159.4894 -7.233785, -159.10248 "
                   "-8.674613, -158.70517 -10.113982, -158.29645 -11.551577, "
                   "-157.87637 -12.98747, -157.444 -14.421311, -156.99876 "
                   "-15.85309, -156.54001 -17.282581, -156.06744 -18.709654, "
                   "-155.57948 -20.13405, -155.07596 -21.555643, -154.5558 "
                   "-22.974205, -154.01758 -24.389427, -153.46085 "
                   "-25.801155, -152.8842 -27.209108, -152.28654 -28.612999, "
                   "-151.66628 -30.012564, -151.02205 -31.407356, -150.35246 "
                   "-32.79723, -149.65543 -34.181614, -148.9292 -35.56014, "
                   "-148.17175 -36.932407, -147.38063 -38.29769, -146.55342 "
                   "-39.6557, -145.68736 -41.00566, -144.7798 -42.347084, "
                   "-143.8269 -43.67897, -142.82521 -45.00064, -141.77133 "
                   "-46.31118, -140.66045 -47.60957, -139.4877 -48.894478, "
                   "-138.24828 -50.16494, -136.93637 -51.41941, -135.5458 "
                   "-52.656303, -134.0697 -53.87377, -132.5008 -55.069862, "
                   "-130.8311 -56.242336, -129.05223 -57.388638, -127.15525 "
                   "-58.506126, -125.13072 -59.59139, -122.968834 "
                   "-60.641064, -120.659386 -61.651016, -118.19338 "
                   "-62.61717, -115.5613 -63.534576, -112.755646 -64.39802, "
                   "-109.7707 -65.20218, -106.60273 -65.9407, -108.59956 "
                   "-66.93513, -109.949425 -67.55315, -113.80929 -69.11937, "
                   "-115.14966 -69.60426, -118.14668 -70.59907, -119.23415 "
                   "-70.933334, -123.59422 -72.15644, -125.33779 -72.600525, "
                   "-129.42595 -73.55694, -131.01332 -73.89894, -135.04094 "
                   "-74.698845, -136.73071 -75.00694, -141.37552 -75.7759, "
                   "-143.49399 -76.090675, -149.93294 -76.91839, -153.21971 "
                   "-77.26976, -159.44414 -77.81199, -162.01192 -77.991165, "
                   "-170.08966 -78.39724, -174.24023 -78.5178, "
                   "-180 -78.54299733461647, -180 -60.43489669869457, "
                   "-179.96748 -60.16659, -179.83322 -58.742584, -179.73184 "
                   "-57.316566, -179.65977 -55.888824, -179.6136 -54.45934, "
                   "-179.59041 -53.028225, -179.58913 -51.595722, -179.60602 "
                   "-50.161697, -179.64015 -48.726337, -179.69008 -47.2897, "
                   "-179.75443 -45.851803, -179.83203 -44.412685, -179.9221 "
                   "-42.972466, -180 -41.86733642322825, -180 90)), "
                   "((180 -78.54299733461647, 175.04135 -78.56469, 171.68889 "
                   "-78.500534, 169.88521 -78.44987, 170.11551 -78.31641, "
                   "172.13577 -76.97113, 173.73349 -75.609184, 175.0151 "
                   "-74.23472, 176.05489 -72.85067, 176.90472 -71.4589, "
                   "177.60373 -70.061005, 178.18103 -68.65796, 178.65848 "
                   "-67.25062, 179.05312 -65.83957, 179.37799 -64.42529, "
                   "179.6447 -63.00817, 179.86017 -61.588566, "
                   "180 -60.43489669869457, 180 -78.54299733461647)))")
        _wkt = wkt.loads(product)
        print(_wkt)
        print(footprint_facility.rework_to_polygon_geometry(_wkt))

    def test_jan_07_06_2024_S6(self):
        """
        Issue reported 07/06/2024,
        regarding product reported from https://datahub.creodias.eu/odata/v1
        "S6A_P4_2__LR______20240601T141934_20240601T151547_20240602T094057_"
        "3373_131_075_037_EUM__OPE_ST_F09.SEN6"

        Command line used:
        <code>
        #Sentinel-6
        product="S6A_P4_2__LR______20240601T141934_20240601T151547_"
                "20240602T094057_3373_131_075_037_EUM__OPE_ST_F09.SEN6"
        wget -qO - 'https://datahub.creodias.eu/odata/v1/Products?'
                   '$filter=((Name%20eq%20%27'$product'%27))' |
           jq '.value[] | .Footprint' |
           tr -d '"' |
           tr -d "'" |
           cut -f 2 -d ';' |
           xargs -I {} python3 -c '
              from footprint_facility import to_wkt,rework_to_polygon_geometry;
              from shapely import wkt;
              print(to_wkt(rework_to_polygon_geometry(wkt.loads("{}"))));'
        </code>
        """
        product = ("MULTIPOLYGON (((180 60.22980148474507, 168.417758 "
                   "56.243085, 155.691259 46.750119, 147.366563 36.111285, "
                   "141.341637 24.872868, 136.505741 13.306639, 132.205885 "
                   "1.583584, 127.965756 -10.173274, 123.326157 -21.849296, "
                   "116.541992 -35.271951, 108.459264 -46.166451, 96.228309 "
                   "-56.013986, 76.619961 -63.592298, 48.281191 -66.644914, "
                   "48.174683 -65.650602, 76.260516 -62.659132, 95.601983 "
                   "-55.234425, 107.656475 -45.570188, 115.649571 "
                   "-34.820747, 122.396845 -21.480001, 127.025064 -9.834011, "
                   "131.267059 1.927975, 135.583207 13.692556, 140.460574 "
                   "25.345868, 146.579813 36.728557, 155.094546 47.552574, "
                   "168.092904 57.188849, 180 61.27018968706418, "
                   "180 60.22980148474507)), ((-180 61.27018968706418, "
                   "-171.164341 64.298748, -145.987795 66.645419, "
                   "-145.894989 65.649735, -171.071535 63.303063, "
                   "-180 60.22980148474507, -180 61.27018968706418)))")

        _wkt = wkt.loads(product)
        print(wkt)
        print(footprint_facility.rework_to_polygon_geometry(_wkt))

    def test_marcin_10_06_2024_01(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2A_MSIL1C_20240409T224801_N0510_R058_T01RBN_20240410T013411.SAFE"

        """
        product = ("POLYGON ((-179.9876881381423 29.0291685491302, -180 "
                   "29.03155659510362, -180 28.98285094292218, "
                   "-180 28.98271563385081, -180 28.98267749312967, "
                   "-180 28.9826301658557, -180 28.98231907003779, "
                   "-180 28.98207088113581, -180 28.98199564557697, "
                   "-180 28.9818874012062, -180 28.98168445373044, "
                   "-180 28.98134004587741, -180 28.97287167365954, "
                   "-180 28.9724800982187, -180 28.97201308859933, "
                   "-180 28.92366753988982, -180 28.92345535520249, "
                   "-180 28.92154911321751, -180 28.92142927714886, "
                   "-180 28.92138566174452, -180 28.92124143543171, "
                   "-180 28.92122367544565, -180 28.92117129124892, "
                   "-180 28.92110801483784, -180 28.92107004450444, "
                   "-180 28.91396984852497, -180 28.91131882845719, "
                   "-180 28.91121448540229, -180 28.80581804559539, "
                   "-179.0350228270187 28.82378643806586, -179.1700409251341 "
                   "28.8545636014009, -179.2582015439308 28.87464057048835, "
                   "-179.258196659197 28.8746585624768, -179.2583009156745 "
                   "28.87468232757705, -179.2578661104106 28.87628285923174, "
                   "-179.2580148638191 28.87631698966688, -179.2579161794961 "
                   "28.87668033508817, -179.2579401870867 28.87668584831188, "
                   "-179.2579084557888 28.87680270425759, -179.2579329974328 "
                   "28.87680834562038, -179.2576853439967 28.87771959163993, "
                   "-179.5077117875585 28.93318662235096, -179.5083485813891 "
                   "28.93082221299412, -179.5105432199461 28.93128541800726, "
                   "-179.5106967946305 28.9307145946074, -179.7347382855255 "
                   "28.97795276579205, -179.7339339236061 28.98096695785088, "
                   "-179.9842953306247 29.03133422840303, -179.984597481629 "
                   "29.03019291548934, -179.9847308126944 29.03021870182818, "
                   "-179.9849148753883 29.02952269078926, -179.9850016555684 "
                   "29.02953951185671, -179.9851816359575 29.02885949683142, "
                   "-179.9876433795116 29.02933773510185, -179.9876881381423 "
                   "29.0291685491302))")

        _wkt = wkt.loads(product)
        print(wkt)
        print(footprint_facility.rework_to_polygon_geometry(_wkt))

    def test_marcin_10_06_2024_02(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2A_MSIL1C_20240521T030521_N0510_R075_T51VUC_20240521T064313.SAFE"

        """
        product = ("POLYGON ((119.797421348587 55.93819621688083, "
                   "119.807765253249 55.81589134146334, 121.5593013138845 "
                   "55.8488879777783, 121.5216424730097 56.83505986087058, "
                   "120.235983877957 56.81056346974395, 120.2024267920502 "
                   "56.74457214191219, 120.1305599624232 56.5994713836992, "
                   "120.0573029598348 56.45474361754042, 119.9844055829299 "
                   "56.30992972532578, 119.9114330022377 56.16513333356001, "
                   "119.8380448819553 56.02044430591336, 119.797421348587 "
                   "55.93819621688083))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_marcin_10_06_2024_03(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20240513T193859_N0510_R042_T15XVJ_20240513T214054.SAFE"
        """
        product = ("POLYGON ((-96.97673033238847 79.15042075633988, "
                   "-92.53422260052758 79.18123126796907, -92.49706194741519 "
                   "79.97506966116111, -92.58789246863891 79.96030467308965, "
                   "-93.2083285328792 79.85763391842576, -93.81362408192648 "
                   "79.75308071559806, -94.40926223137284 79.64796950837108, "
                   "-94.98949597744156 79.54095981795254, -95.55965621122536 "
                   "79.43332129931305, -96.1178586950274 79.324625086183, "
                   "-96.66449811670545 79.21488698029992, -96.97673033238847 "
                   "79.15042075633988))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_marcin_10_06_2024_04(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20231227T210529_N0510_R071_T60DWG_20231227T215209.SAFE"
        """
        product = ("POLYGON ((176.9994652359355 -70.41607942052394, "
                   "176.9994413608334 -71.29052981531568, 179.572179881629 "
                   "-71.26959996377886, 179.6721740780138 "
                   "-71.19803855312027, 179.8599573008396 "
                   "-71.06164728850977, 180 -70.95851167153866, "
                   "180 -70.92556822281612, 179.3942277030721 "
                   "-70.82312532219207, 179.4065959993365 "
                   "-70.81423576046868, 178.7525658093475 "
                   "-70.70538682886387, 178.7478324461233 "
                   "-70.70871718019387, 178.747493319118 -70.70865970914443, "
                   "178.7466712566637 -70.70923776863077, 178.7465004516869 "
                   "-70.70920879475975, 178.7447941071134 "
                   "-70.71040875515017, 178.7446136307058 "
                   "-70.71037810545408, 178.7440344859275 "
                   "-70.71078525996892, 178.7439023131008 "
                   "-70.71076277629899, 178.7430910034338 "
                   "-70.71133296014627, 178.7427845577315 "
                   "-70.71128077984781, 178.7417806732775 "
                   "-70.71198628518216, 178.7416517931338 "
                   "-70.71196431792183, 178.7400909685969 "
                   "-70.71306235743884, 178.739977349168 -70.71304295238998, "
                   "178.7393022707546 -70.71351730865861, 178.739129461579 "
                   "-70.71348776470606, 178.7382493908013 "
                   "-70.71410575542254, 178.170783554921 -70.61698669068961, "
                   "178.1828204293513 -70.60869796010728, 177.5542359158372 "
                   "-70.50195289083793, 177.5472162020975 "
                   "-70.50669177750456, 177.5469060049969 "
                   "-70.50663830899008, 177.5456972851142 "
                   "-70.50745367297019, 177.545666713415 -70.50744839713443, "
                   "177.5440119349725 -70.5085657739295, 177.5433628801525 "
                   "-70.50845362202493, 177.5428597657197 "
                   "-70.50879341424859, 177.5428557244273 "
                   "-70.50879271644239, 177.5421181273214 "
                   "-70.50929034494347, 177.5420059497903 "
                   "-70.50927096526664, 177.5413168288432 "
                   "-70.50973549338948, 176.9994652359355 "
                   "-70.41607942052394))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_marcin_10_06_2024_05(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20240111T183749_N0510_R141_T01CDN_20240112T201221.SAFE"
        """
        product = ("POLYGON ((-179.508117526313 -79.16127199879642, -180 "
                   "-79.01692999138557, -180 -79.19944296655834, "
                   "-180 -79.19959581716972, -180 -79.19972960600606, "
                   "-180 -79.19988578232916, -180 -79.20007346017209, "
                   "-180 -79.20013436682478, -180 -79.20024126342099, "
                   "-180 -79.20029258993124, -180 -79.20049921536173, "
                   "-180 -79.20054631332516, -180 -79.20066396817484, "
                   "-180 -79.20077375877023, -180 -79.2008843839914, "
                   "-180 -79.21714918681978, -180 -79.21715630792468, "
                   "-180 -79.2175551235766, -180 -79.21773293229286, "
                   "-180 -79.21778003784787, -180 -79.2177900670303, "
                   "-180 -79.21779114542757, -180 -79.21779351757006, "
                   "-180 -79.21780296489362, -180 -79.21780421542903, "
                   "-180 -79.21780998189048, -180 -79.21827514353097, "
                   "-180 -79.21830910412172, -180 -79.33237518158053, "
                   "-178.9375581912928 -79.33974790172739, "
                   "-179.5490821971551 -79.1659353807717, -179.5463891574934 "
                   "-79.16562951391516, -179.5464126641663 "
                   "-79.16562282940411, -179.508117526313 "
                   "-79.16127199879642))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_marcin_10_06_2024_06(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20240326T210529_N0510_R071_T60DWG_20240326T233250.SAFE"
        """
        product = ("POLYGON ((176.9994651544594 -70.41906356609854, "
                   "176.9994413608334 -71.29052981531568, 179.5827002480463 "
                   "-71.26951437804776, 179.6779330353536 "
                   "-71.20164541504658, 179.8660471915699 "
                   "-71.06541455826518, 180 -70.96702620900645, "
                   "180 -70.92851075764088, 179.399173113056 "
                   "-70.8269190325428, 179.4118052503909 -70.81786127781933, "
                   "178.7583023614406 -70.70911422211499, 178.753397288728 "
                   "-70.71254820043357, 178.7529355395073 "
                   "-70.71246995820101, 178.7521208760483 "
                   "-70.71304130653343, 178.7520537809051 "
                   "-70.71302992651998, 178.7503158259021 "
                   "-70.71424701992557, 178.7499498520174 "
                   "-70.71418487616172, 178.749350023558 -70.71460490928753, "
                   "178.7489397011358 -70.71453511892662, 178.7481155498963 "
                   "-70.7151126523084, 178.7480502042567 -70.71510152684793, "
                   "178.7461968290528 -70.71639954174172, 178.7460486272359 "
                   "-70.7163742596462, 178.7452945166694 -70.71690180963448, "
                   "178.7447921469283 -70.71681602157507, 178.7440933445718 "
                   "-70.71730500907283, 178.7438949980914 "
                   "-70.71727110341526, 178.7430226810598 "
                   "-70.71788223813657, 178.1753788459815 -70.6207447884229, "
                   "178.1876847818419 -70.6122901476094, 177.5596526106852 "
                   "-70.50565079699012, 177.5524359693655 "
                   "-70.51050296081975, 177.5517761838235 "
                   "-70.51038924711861, 177.5488326974667 -70.5123663560824, "
                   "177.5482939024504 -70.51227326695077, 177.547791959252 "
                   "-70.5126104218932, 177.5474041860378 -70.51254347329198, "
                   "177.5466434074202 -70.51305453487579, 177.5464329171782 "
                   "-70.5130181746587, 177.5457517781493 -70.51347629162153, "
                   "176.9994651544594 -70.41906356609854))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_marcin_10_06_2024_07(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20240121T183749_N0510_R141_T60CWT_20240121T212726.SAFE"
        """
        product = ("POLYGON ((-179.3389758084033 -79.14242545505675, -180 "
                   "-78.9493443207847, -180 -79.20060232223966, "
                   "-180 -79.20070247954938, -180 -79.2007670522849, "
                   "-180 -79.20090023310787, -180 -79.20112235414808, "
                   "-180 -79.2011867192771, -180 -79.20126215418246, "
                   "-180 -79.20128995185189, -180 -79.20148337743043, "
                   "-180 -79.20159443848705, -180 -79.20162579974793, "
                   "-180 -79.2017268386863, -180 -79.20187103282393, "
                   "-180 -79.21844315586061, -180 -79.21847170744411, "
                   "-180 -79.21866164111945, -180 -79.21874225983464, "
                   "-180 -79.21879659217447, -180 -79.21882990235626, "
                   "-180 -79.21894420996992, -180 -79.2189473244755, "
                   "-180 -79.21895573254695, -180 -79.21896107649158, "
                   "-180 -79.21904024752864, -180 -79.21946330316014, "
                   "-180 -79.21956056932171, -180 -79.33150649003348, "
                   "-178.7662167742809 -79.3210939569312, -179.3807034712833 "
                   "-79.14724286926662, -179.3779715745694 "
                   "-79.14692878413946, -179.3780146197653 "
                   "-79.14691659976745, -179.3389758084033 "
                   "-79.14242545505675))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_marcin_10_06_2024_08(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20240220T183749_N0510_R141_T01CDN_20240220T210409.SAFE"
        """
        product = ("POLYGON ((-179.472327088384 -79.16489209680499, -180 "
                   "-79.01033649528226, -180 -79.20654449983061, "
                   "-180 -79.20669504227244, -180 -79.20693310677962, "
                   "-180 -79.20718312069948, -180 -79.2073122331582, "
                   "-180 -79.2073313990563, -180 -79.20743070381685, "
                   "-180 -79.20754999893539, -180 -79.20778768373577, "
                   "-180 -79.20794579617595, -180 -79.20802562547372, "
                   "-180 -79.20810912784819, -180 -79.20823965873238, "
                   "-180 -79.2251377184389, -180 -79.22522241611811, "
                   "-180 -79.22542394599088, -180 -79.22546978496251, "
                   "-180 -79.2255205128762, -180 -79.22552750405887, "
                   "-180 -79.22566046972585, -180 -79.22567891628702, "
                   "-180 -79.22574971160533, -180 -79.22578693311603, "
                   "-180 -79.22586581935971, -180 -79.2261620322246, "
                   "-180 -79.22636934723057, -180 -79.33237518158053, "
                   "-178.9119796167795 -79.33992540196326, "
                   "-179.5126923714637 -79.16950069337689, -179.472327088384 "
                   "-79.16489209680499))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_marcin_10_06_2024_09(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20240305T224759_N0510_R058_T01RBN_20240305T235933.SAFE"
        """
        product = ("POLYGON ((-179.9726084221875 29.02774848883664, -180 "
                   "29.03305602630523, -180 28.92405745940028, "
                   "-180 28.92365348425323, -180 28.92328471061849, "
                   "-180 28.92315587836184, -180 28.92314589214138, "
                   "-180 28.92292509977204, -180 28.92273860727704, "
                   "-180 28.92243478502562, -180 28.92237840518189, "
                   "-180 28.92220714165031, -180 28.92186336567974, "
                   "-180 28.92169255434653, -180 28.92085916576632, "
                   "-180 28.86398419969101, -180 28.86376235439207, "
                   "-180 28.8625135403597, -180 28.86182198296167, "
                   "-180 28.86177263800117, -180 28.86175922384905, "
                   "-180 28.86165239704172, -180 28.86149088447868, "
                   "-180 28.86135465610515, -180 28.86133582415095, "
                   "-180 28.86118049530125, -180 28.86037359613003, "
                   "-180 28.85994914523384, -180 28.80581804559539, "
                   "-179.0254117042065 28.82396540232699, -179.2435796149245 "
                   "28.87359710319079, -179.2430548092013 28.87553905809875, "
                   "-179.2431117461943 28.87555210696329, -179.2431042081035 "
                   "28.87558000214502, -179.2432616114054 28.87561598611941, "
                   "-179.2429118700997 28.87690997130177, -179.4757171569616 "
                   "28.92847840039094, -179.4947763392047 28.93268856785107, "
                   "-179.4953826090487 28.93042364036135, -179.495640129408 "
                   "28.93047785137913, -179.4958976032855 28.92951710251109, "
                   "-179.7197759107133 28.97665152957523, -179.7189008661309 "
                   "28.9799434948634, -179.9711246134191 29.03057401142689, "
                   "-179.9714021451395 29.02951950260552, -179.9716112261731 "
                   "29.02955986208121, -179.9717934808075 29.02886735888065, "
                   "-179.9718527488075 29.0288788126164, -179.9720421969321 "
                   "29.0281585335533, -179.9723587419275 29.02821982865962, "
                   "-179.9723720061434 29.02816940680941, -179.9724134730059 "
                   "29.0281774310333, -179.9724833152255 29.02791186877477, "
                   "-179.9725614487616 29.02792699987426, -179.9726084221875 "
                   "29.02774848883664))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_marcin_10_06_2024_10(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20240101T183749_N0510_R141_T01CDN_20240101T195545.SAFE"
        """
        product = ("POLYGON ((-179.4659439421087 -79.16266030819288, -180 "
                   "-79.00627513455187, -180 -79.20560704191595, "
                   "-180 -79.20577500811633, -180 -79.2058573211517, "
                   "-180 -79.20601309051693, -180 -79.20619753454719, "
                   "-180 -79.20627015670875, -180 -79.20636618450428, "
                   "-180 -79.20638553333532, -180 -79.20661872315614, "
                   "-180 -79.20666765230693, -180 -79.20674674351788, "
                   "-180 -79.20688163422483, -180 -79.20695561042487, "
                   "-180 -79.22381700866191, -180 -79.223885625627, "
                   "-180 -79.22397372241886, -180 -79.22398771828203, "
                   "-180 -79.22409385588804, -180 -79.22414307640015, "
                   "-180 -79.22424054310756, -180 -79.22426808766679, "
                   "-180 -79.2243423088464, -180 -79.22435942662918, "
                   "-180 -79.22440118374973, -180 -79.2248432559935, "
                   "-180 -79.22490396784302, -180 -79.33237518158053, "
                   "-178.8989106382028 -79.34001609297415, "
                   "-179.5073846646551 -79.16744079084668, "
                   "-179.5046365996067 -79.16712591214419, "
                   "-179.5047238949631 -79.16710114155836, "
                   "-179.4659439421087 -79.16266030819288))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_24_07_2024_Linestring_two_coords(self):
        # Case Sentinel-1 WV_RAW_0A, WV_RAW_0C, WV_RAW_0N, WV_RAW_0S
        # -> The Linestring crosses the antimeridian returns a multilistring,
        # otherwise it returns same polygon
        count = 0
        for (dirpath, dirnames, filenames) in walk(
                'samples/jan-24.07.2024/SENTINEL-1'):
            for file in filenames:
                with open(os.path.join(dirpath, file), "r") as f:
                    _wkt = f.readline()
                count += 1

                geometry = wkt.loads(_wkt)
                rwrk = footprint_facility.rework_to_polygon_geometry(geometry)
                if not footprint_facility.check_cross_antimeridian(geometry):
                    self.assertEqual(rwrk, geometry)
                else:
                    self.assertIsInstance(rwrk,
                                          shapely.geometry.MultiLineString)
        print(f"Successfully checked {count} samples")

    def test_24_07_2024_Linestring_simplify(self):
        # Case Sentinel-1 contains only 2 points
        # The simplify call shall return same geometry.
        _wkt = "LINESTRING (-178.3024 -43.489, 172.2148 -62.4779)"
        rwrk = footprint_facility.rework_to_polygon_geometry(wkt.loads(_wkt))
        # Also here test set_precision over linestring
        spfy = footprint_facility.simplify(rwrk, tolerance_in_meter=False)
        self.assertEqual(rwrk, spfy)

    def test_24_07_2024_Linestring_simplify_meter(self):
        # Case Sentinel-1 contains only 2 points
        # The simplify call shall return same geometry.
        _wkt = "LINESTRING (-178.3024 -43.489, 172.2148 -62.4779)"
        rwrk = footprint_facility.rework_to_polygon_geometry(wkt.loads(_wkt))
        # Also here test set_precision over linestring
        spfy = footprint_facility.simplify(rwrk, tolerance=10000,
                                           tolerance_in_meter=True)
        self.assertTrue(shapely.equals_exact(rwrk, spfy, tolerance=1))

    def test_24_07_2024_Linestring_two_coords_cross_antimeridian(self):
        # Case Sentinel-1 WV_RAW_0A, WV_RAW_0C, WV_RAW_0N, WV_RAW_0S
        # -> The Linestring crosses the antimeridian shall return
        # multilinestring.
        _wkt = "LINESTRING (-178.3024 -43.489, 172.2148 -62.4779)"
        rwrk = footprint_facility.rework_to_polygon_geometry(wkt.loads(_wkt))
        print(footprint_facility.to_wkt(rwrk))
        expected = ("MULTILINESTRING ((-180 -46.89999999999998, "
                    "-178.3 -43.5), (172.2 -62.5, 180 -46.89999999999998))")
        # Also here test set_precision over linestring
        self.assertEqual(footprint_facility.to_wkt(rwrk), expected)

    def test_24_07_2024_Linestring_two_coords_use_precision(self):
        # Case Sentinel-1 WV_RAW_0A, WV_RAW_0C, WV_RAW_0N, WV_RAW_0S
        # -> The Linestring crosses the antimeridian shall return
        # multilinestring.
        _wkt = "LINESTRING (-178.3024 -43.489, 172.2148 -62.4779)"
        rwrk = footprint_facility.rework_to_polygon_geometry(wkt.loads(_wkt))
        print(footprint_facility.to_wkt(rwrk))
        expected = ("MULTILINESTRING ("
                    "(-180 -46.9, -178.3 -43.5), "
                    "(172.2 -62.5, 180 -46.9))")
        # Also here test set_precision over linestring
        self.assertEqual(footprint_facility.to_wkt(
            shapely.set_precision(rwrk, 0.01)), expected)

    def test_24_07_2024_sentinel_2(self):
        # These S2 sample products has footprint exactly aligned on the
        # antimeridian that generate problem to compute intersection with it...
        # This issue shall be analysed.
        count = 0
        total = 0
        for (dirpath, dirnames, filenames) in walk(
                'samples/jan-24.07.2024/SENTINEL-2'):
            for file in filenames:
                path = os.path.join(dirpath, file)
                with open(path, "r") as f:
                    _wkt = f.readline()
                total += 1

                geometry = wkt.loads(_wkt)
                try:
                    rwrk = footprint_facility.rework_to_polygon_geometry(
                        geometry)
                except AlreadyReworkedPolygon as e:
                    print(f"{str(e)}: already rwrkd {path}")
                    continue
                except Exception as e:
                    print(f"{str(e)}: something wrong {path}")
                    continue

                count += 1

                if not footprint_facility.check_cross_antimeridian(geometry):
                    self.assertEqual(rwrk, geometry)
                else:
                    self.assertIsInstance(rwrk, shapely.geometry.MultiPolygon)
        print(f"Successfully checked {count}/{total} samples")

    @skip(reason="Test too long")
    def test_24_07_2024_sentinel_3(self):
        # These S3 seems to be already reworked.
        # An issue regarding the crossing antimeridian shall be fixed.
        count = 0
        total = 0
        for (dirpath, dirnames, filenames) in walk(
                'samples/jan-24.07.2024/SENTINEL-3'):
            for file in filenames:
                path = os.path.join(dirpath, file)
                with open(path, "r") as f:
                    try:
                        _wkt = f.readline()
                    except Exception as e:
                        print(f"{str(e)}: cannot read footprint file({path}).")
                        continue
                total += 1

                geometry = wkt.loads(_wkt)
                try:
                    rwrk = footprint_facility.rework_to_polygon_geometry(
                        geometry)
                except Exception as e:
                    '''
                    they are up to 77000 samples in error
                    print(f"`{str(e)}`: Problem handling footprint of {path}")
                    '''
                    continue
                count += 1
                if not footprint_facility.check_cross_antimeridian(geometry):
                    self.assertEqual(rwrk, geometry)
                else:
                    self.assertIsInstance(rwrk,
                                          shapely.geometry.MultiPolygon)
        print(f"Successfully checked {count}/{total} samples")

    def test_24_07_2024_sentinel_3_already_reworked_north_pole(self):
        _wkt = ("POLYGON ((-128.226 83.7901, -122.55 83.7642, -116.892"
                " 83.6781, -111.514 83.5353, -106.359 83.3365, -101.582"
                " 83.0902, -97.1308 82.7976, -93.044 82.4659, -89.3377"
                " 82.1005, -85.9486 81.7028, -82.8501 81.2809, -80.097"
                " 80.8392, -77.5688 80.3765, -75.2979 79.8955, -73.2257"
                " 79.4019, -71.3502 78.8948, -69.6196 78.3792, -68.0404"
                " 77.853, -66.5831 77.3153, -65.2563 76.7739, -51.4913"
                " 77.9735, -35.7645 78.3998, -35.7546 79.0266, -35.7509"
                " 79.6414, -35.7469 80.2601, -35.7536 80.8774, -35.7301"
                " 81.494, -35.7218 82.1125, -35.6982 82.7319, -35.7033 83.35,"
                " -35.6837 83.9708, -35.7015 84.5908, -35.6797 85.2102,"
                " -35.6513 85.8276, -35.633 86.4479, -35.5921 87.0638,"
                " -35.5279 87.6838, -35.4154 88.3056, -35.175 88.9212, -34.284"
                " 89.5393, 139.081 89.8402, 180 89.8023747, 180 90, -180 90,"
                " -180 89.8023747, -129.234 86.8954, -128.226 83.7901)))")
        with self.assertRaises(AlreadyReworkedPolygon):
            rwrk = footprint_facility.rework_to_polygon_geometry(
                wkt.loads(_wkt))
            print(rwrk)

    @skip(reason="Test too long")
    def test_24_07_2024_sentinel_6(self):
        # These S6 seems to be already reworked.
        # Issue regarding the computation of the intersection with antimeridian
        count = 0
        total = 0
        for (dirpath, dirnames, filenames) in walk(
                'samples/jan-24.07.2024/SENTINEL-6'):
            for file in filenames:
                with open(os.path.join(dirpath, file), "r") as f:
                    _wkt = f.readline()
                    total += 1

                    geometry = wkt.loads(_wkt)
                    try:
                        rwrk = footprint_facility.rework_to_polygon_geometry(
                            geometry)
                    except Exception as e:
                        continue
                    count += 1
                    if not footprint_facility.check_cross_antimeridian(
                            geometry):
                        self.assertEqual(rwrk, geometry)
                    else:
                        self.assertIsInstance(rwrk,
                                              shapely.geometry.MultiPolygon)
        print(f"Successfully checked {count}/{total} samples")

    def test__24_07_2024_sentinel_6_thin_malfocrossing(self):
        _wkt = ("POLYGON ((-140.176 29.9923, -144.644 20.4233, -148.486 "
                "10.7008, -152.037 0.906387, -155.565 -8.89357, -159.331 "
                "-18.6338, -163.652 -28.237, -168.977 -37.5936, -176.028 "
                "-46.5229, 173.982 -54.6891, 159.162 -61.4295, 137.886 "
                "-65.5398, 112.839 -65.6531, 91.2392 -61.7212, 76.1072 "
                "-55.0823, 65.9181 -46.9691, 58.7492 -38.0683, 53.354 "
                "-28.7273, 48.9931 -19.1323, 45.2061 -9.39557, 41.6723 "
                "0.404495, 38.1278 10.2023, 34.3064 19.9317, 29.8792 29.5123,"
                "24.3688 38.8276, 17.003 47.682, 6.47951 55.7076, -9.16948 "
                "62.1774, -31.2825 65.8134, -56.2909 65.3326, -56.2898 "
                "65.3308, -31.2815 65.8117, -9.17018 62.1757, 6.47782 55.7061,"
                "17.001 47.6808, 24.3669 38.8266, 29.8774 29.5115, 34.3046 "
                "19.931, 38.1261 10.2016, 41.6706 0.403881, 45.2044 -9.39617, "
                "48.9913 -19.1329, 53.3521 -28.7279, 58.7471 -38.069, 65.9158 "
                "-46.97, 76.1046 -55.0833, 91.2365 -61.7224, 112.836 -65.6546,"
                "137.885 -65.5416, 159.163 -61.4312, 173.984 -54.6906, "
                "-176.026 -46.5241, -168.976 -37.5946, -163.65 -28.2379, "
                "-159.329 -18.6346, -155.563 -8.89422, -152.036 0.905776, "
                "-148.485 10.7002, -144.642 20.4227, -140.174 29.9917, "
                "-140.176 29.9923))")
        geometry = wkt.loads(_wkt)
        rwrk = footprint_facility.rework_to_polygon_geometry(geometry)
        print(footprint_facility.to_geojson(rwrk))

    def test_24_07_2024_sentinel_6_crossing_antimeridian(self):
        _wkt = ("MULTIPOLYGON (((-180 86.263647169221, -149.52 85.52, -130.65"
                " 83.87, -120.25 81.86, -113.95 79.7, -109.76 77.47, -106.74"
                " 75.2, -104.45 72.9, -102.62 70.58, -101.11 68.26, -99.83"
                " 65.92, -98.72 63.58, -97.74 61.23, -96.85 58.88, -96.04"
                " 56.53, -95.3 54.17, -94.6 51.81, -93.94 49.45, -93.31 47.09,"
                " -92.71 44.72, -92.14 42.35, -91.58 39.98, -91.04 37.61,"
                " -90.51 35.23, -90 32.86, -89.49 30.48, -88.99 28.1, -88.49"
                " 25.73, -88 23.35, -87.51 20.96, -87.02 18.58, -86.53 16.2,"
                " -86.04 13.82, -85.55 11.44, -85.05 9.05, -84.55 6.67, -84.05"
                " 4.29, -83.54 1.91, -83.02 -0.47, -82.5 -2.85, -81.96 -5.23,"
                " -81.41 -7.61, -80.86 -9.98, -80.28 -12.36, -79.69 -14.73,"
                " -79.09 -17.1, -78.46 -19.46, -77.81 -21.83, -77.14 -24.19,"
                " -76.43 -26.54, -75.7 -28.89, -74.93 -31.24, -74.12 -33.58,"
                " -73.26 -35.91, -72.36 -38.24, -71.39 -40.56, -70.36 -42.87,"
                " -69.25 -45.16, -68.04 -47.45, -66.74 -49.72, -65.3 -51.98,"
                " -63.73 -54.22, -61.97 -56.44, -60.01 -58.63, -57.8 -60.78,"
                " -55.27 -62.9, -52.37 -64.96, -49.01 -66.97, -45.06 -68.89,"
                " -40.4 -70.7, -34.86 -72.38, -28.28 -73.88, -20.52 -75.14,"
                " -11.55 -76.11, -1.55 -76.71, 9.05 -76.89, 19.6 -76.65, 29.48"
                " -75.99, 38.29 -74.98, 45.88 -73.68, 51.56 -72.36, 52.04"
                " -72.23, 82.23 -77.8, 78.47 -79.75, 72.15 -81.89, 61.73"
                " -83.89, 42.86 -85.53, 10.86 -86.3, -22.61 -85.71, -43.14"
                " -84.15, -54.4 -82.18, -61.13 -80.05, -65.57 -77.83, -68.72"
                " -75.58, -71.11 -73.29, -72.99 -70.99, -74.54 -68.67, -75.85"
                " -66.35, -76.99 -64.02, -77.99 -61.69, -78.89 -59.35, -79.71"
                " -57, -80.47 -54.65, -81.17 -52.3, -81.84 -49.95, -82.47"
                " -47.59, -83.07 -45.24, -83.65 -42.87, -84.21 -40.51, -84.75"
                " -38.15, -85.28 -35.78, -85.8 -33.41, -86.31 -31.04, -86.81"
                " -28.67, -87.31 -26.29, -87.8 -23.92, -88.29 -21.54, -88.78"
                " -19.17, -89.27 -16.79, -89.76 -14.41, -90.25 -12.03, -90.74"
                " -9.65, -91.24 -7.27, -91.74 -4.88, -92.25 -2.5, -92.77"
                " -0.12, -93.29 2.26, -93.82 4.64, -94.37 7.02, -94.92 9.4,"
                " -95.49 11.77, -96.08 14.15, -96.68 16.52, -97.3 18.89,"
                " -97.95 21.26, -98.62 23.62, -99.31 25.98, -100.04 28.34,"
                " -100.8 30.69, -101.61 33.04, -102.45 35.38, -103.35 37.72,"
                " -104.3 40.04, -105.32 42.36, -106.42 44.67, -107.61 46.97,"
                " -108.89 49.25, -110.3 51.52, -111.86 53.77, -113.58 56,"
                " -115.5 58.21, -117.67 60.38, -120.14 62.51, -122.98 64.6,"
                " -126.27 66.62, -130.12 68.57, -134.67 70.41, -140.08 72.12,"
                " -146.51 73.66, -154.11 74.97, -162.94 75.98, -172.86 76.64,"
                " -180 76.809034090909, -180 86.263647169221)), "
                "((180 76.809034090909, 176.58 76.89, 178.51 86.3,"
                " 180 86.263647169221, 180 76.809034090909)))")
        rwrk = footprint_facility.rework_to_polygon_geometry(wkt.loads(_wkt))
        print(footprint_facility.to_wkt(rwrk))

        # Also here test set_precision over linestring
        self.assertEqual(footprint_facility.to_wkt(rwrk), _wkt)

    def test_24_07_2024_smos_crossing_antimeridian(self, ):
        _wkt = ("MULTIPOLYGON (((-180 39.091237574483, -174.883 30.781,"
                " -170.343 21.2287, -166.461 11.5148, -162.896 1.72291,"
                " -159.375 -8.07972, -155.639 -17.8282, -151.378 -27.4468,"
                " -146.157 -36.8296, -139.285 -45.8041, -129.602 -54.0525,"
                " -115.264 -60.9482, -94.5159 -65.3338, -69.5194 -65.8074,"
                " -47.426 -62.1691, -31.7898 -55.7011, -21.2723 -47.6791,"
                " -13.9088 -38.8286, -8.3994 -29.517, -3.97256 -19.9395,"
                " -0.151216 -10.2125, 3.39329 -0.416293, 6.92709 9.38308,"
                " 10.714 19.1201, 15.0749 28.7161, 15.0768 28.7154, 10.7158"
                " 19.1194, 6.92881 9.38248, 3.39497 -0.416908, -0.149515"
                " -10.2132, -3.97081 -19.9403, -8.39757 -29.5178, -13.9069"
                " -38.8296, -21.2703 -47.6804, -31.7881 -55.7027, -47.4253"
                " -62.1708, -69.5205 -65.8091, -94.5183 -65.3353, -115.267"
                " -60.9494, -129.604 -54.0535, -139.288 -45.805, -146.159"
                " -36.8303, -151.38 -27.4475, -155.641 -17.8289, -159.377"
                " -8.08033, -162.897 1.72229, -166.463 11.5141, -170.345"
                " 21.228, -174.885 30.7802, -180 39.08701019979, -180"
                " 39.091237574483)), ((180 39.08701019979, 179.409 40.0468,"
                " 171.709 48.8162, 160.624 56.6854, 144.132 62.8604, 121.27"
                " 66.0003, 96.462 64.9398, 76.5963 60.1221, 63.0174 52.9838,"
                " 53.8089 44.6051, 53.8068 44.606, 63.0149 52.9847, 76.5936"
                " 60.1232, 96.4594 64.9412, 121.269 66.002, 144.132 62.8622,"
                " 160.625 56.6869, 171.711 48.8174, 179.411 40.0478, 180"
                " 39.091237574483, 180 39.08701019979)))")

        print(_wkt)
        rwrk = footprint_facility.rework_to_polygon_geometry(wkt.loads(_wkt))
        print(footprint_facility.to_wkt(rwrk))

        # Also here test set_precision over linestring
        self.assertEqual(footprint_facility.to_wkt(rwrk), _wkt)

    def test_handle_rework_exceptions(self):
        _wkt = ("POLYGON ((34.8393 42, 180 43, 180 90, -180 90, "
                "-180 43, -178.089 41, 34.8393 42))")
        geometry = wkt.loads(_wkt)
        import logging
        logging.basicConfig(level=logging.INFO)

        footprint_facility.check_time(True, True, True)
        with self.assertRaises(AlreadyReworkedPolygon):
            footprint_facility.rework_to_polygon_geometry(geometry)

        footprint_facility.set_raise_exception(False)
        rwrk = footprint_facility.rework_to_polygon_geometry(geometry)
        print(footprint_facility.to_geojson(rwrk))
        footprint_facility.set_raise_exception(True)

        footprint_facility.show_summary()

    def test_set_precision_error(self):
        with self.assertRaises(ValueError):
            footprint_facility.set_precision(-1)

    def test_set_precision(self):
        _wkt = ("POLYGON ((3.292 47.148, 5.651 46.967, 4.963 48.912, "
                "1.887 48.873, 1.137 46.395, 3.557 44.765, 3.292 47.148))")
        geometry = wkt.loads(_wkt)
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        self.assertEqual(footprint_facility.to_wkt(reworked), _wkt)

        precision = 1
        footprint_facility.set_precision(precision)
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        expected = wkt.loads(
            "POLYGON ((3 47, 6 47, 5 49, 2 49, 1 46, 4 45, 3 47))")
        self.assertTrue(
            reworked.difference(expected).is_empty,
            f'precision {precision} not properly handled {str(reworked)} '
            f'expected {str(expected)}')

        precision = 0.1
        footprint_facility.set_precision(precision)
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        expected = wkt.loads(
            "POLYGON ((3.3 47.1, 5.7 47.0, 5.0 48.9, 1.9 48.9, 1.1 46.4,"
            " 3.6 44.8, 3.3 47.1))")

        self.assertTrue(
            reworked.difference(expected).is_empty,
            f'precision {precision} not properly handled {str(reworked)} '
            f'expected {str(expected)}')

        # try to rollback to no precision setting (0)
        footprint_facility.set_precision(0)
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        self.assertEqual(footprint_facility.to_wkt(reworked), _wkt)

    def test_degree_to_meter_and_rev(self):
        point = Point(180, 90)
        new_point = footprint_facility.geodetic_to_cartesian(point)
        self.assertAlmostEqual(new_point.x, 20_037_508, delta=1)
        self.assertAlmostEqual(new_point.y, 10_018_754, delta=1)

        point = Point(20_037_508, 10_018_754)
        new_point = footprint_facility.cartesian_to_geodetic(point)
        self.assertAlmostEqual(new_point.x, 180, delta=1)
        self.assertAlmostEqual(new_point.y, 90, delta=1)

        point = Point(-180, 90)
        new_point = footprint_facility.geodetic_to_cartesian(point)
        self.assertAlmostEqual(new_point.x, -20_037_508, delta=1)
        self.assertAlmostEqual(new_point.y, 10_018_754, delta=1)

        point = Point(-20_037_508, 10_018_754)
        new_point = footprint_facility.cartesian_to_geodetic(point)
        self.assertAlmostEqual(new_point.x, -180, delta=1)
        self.assertAlmostEqual(new_point.y, 90, delta=1)

        point = Point(180, -90)
        new_point = footprint_facility.geodetic_to_cartesian(point)
        self.assertAlmostEqual(new_point.x, 20_037_508, delta=1)
        self.assertAlmostEqual(new_point.y, -10_018_754, delta=1)

        point = Point(20_037_508, -10_018_754)
        new_point = footprint_facility.cartesian_to_geodetic(point)
        self.assertAlmostEqual(new_point.x, 180, delta=1)
        self.assertAlmostEqual(new_point.y, -90, delta=1)

        point = Point(0, 0)
        new_point = footprint_facility.geodetic_to_cartesian(point)
        self.assertAlmostEqual(new_point.x, 0, delta=1)
        self.assertAlmostEqual(new_point.y, 0, delta=1)

        point = Point(0, 0)
        new_point = footprint_facility.cartesian_to_geodetic(point)
        self.assertAlmostEqual(new_point.x, 0, delta=1)
        self.assertAlmostEqual(new_point.y, 0, delta=1)

        point = Point(2, 48)
        new_point = footprint_facility.geodetic_to_cartesian(point)
        self.assertAlmostEqual(new_point.x, 222_639, delta=1)
        self.assertAlmostEqual(new_point.y, 5_343_336, delta=1)

        point = Point(222_639, 5_343_336)
        new_point = footprint_facility.cartesian_to_geodetic(point)
        self.assertAlmostEqual(new_point.x, 2, delta=1)
        self.assertAlmostEqual(new_point.y, 48, delta=1)

    def test_optimize_very_large_S5P(self):
        """
        Check verry long footptint crossing north & south polar area ans
        Antimeridian. This paricular usage case has been found in S3 datasets.
        It splits the footprint in north and south hemisphere to allow the
        usage of polar inclusion algorithm.
        Issue reported 07/01/2025 - Fixed since v1.10
        """
        _wkt = """POLYGON(( 131.1469 67.160164,134.64603 66.53697,137.96045
        65.83662,141.08707 65.06626,144.02696 64.2318,146.78499 63.33947,
        149.3682 62.394855,151.78534 61.40308,154.04622 60.36881,156.16086
        59.296402,158.13925 58.18946,159.99202 57.05182,161.7284 55.88636,
        163.35751 54.69573,164.88788 53.482563,166.32748 52.248913,167.68332
        50.996677,168.9624 49.727764,170.17073 48.443512,171.31366
        47.145306,172.39658 45.834454,173.42386 44.511814,174.40013
        43.178772,175.32895 41.83596,176.21387 40.484127,177.05809
        39.124138,177.86464 37.756573,178.63579 36.381874, 179.37445
        35.000885,-179.91759 33.613758, -179.23792 32.221195,-178.58492
        30.823515,-177.95688 29.421062,-177.35207 28.01428,-176.76932
        26.603268,-176.20717 25.18848,-175.66461 23.770105,-175.1401
        22.348572,-174.63301 20.923933,-174.14215 19.496479,-173.6668
        18.066378,-173.20602 16.633966,-172.75932 15.199154,-172.3259
        13.76221,-171.90495 12.323438,-171.49606 10.882896,-171.09871
        9.44065,-170.71211 7.997005,-170.33606 6.5520263,-169.97021
        5.1056833,-169.61389 3.658281,-169.26701 2.2098553,-168.92903
        0.7605694,-168.59976 -0.68957067,-168.27878 -2.1403482,-167.96606
        -3.5917692,-167.66136 -5.04376,-167.36395 -6.4960437,-167.0744
        -7.948791,-166.7919 -9.401701,-166.5166 -10.854807,-166.24854
        -12.308081,-165.98727 -13.761312,-165.73296 -15.214573,-165.48524
        -16.667652,-165.24431 -18.120611,-165.01006 -19.573303,-164.78252
        -21.025692,-164.56163 -22.477734,-164.34747 -23.929356,-164.14005
        -25.380476,-163.93942 -26.831076,-163.7461 -28.2812,-163.55972
        -29.730635,-163.38065 -31.179419,-163.20905 -32.6275,-163.0453
        -34.0748,-162.8894 -35.521328,-162.74182 -36.96694,-162.60306
        -38.411705,-162.47351 -39.85556,-162.3534 -41.298412,-162.24367
        -42.74023,-162.14517 -44.181076,-162.05806 -45.620777,-161.98373
        -47.05942,-161.923 -48.49681,-161.87724 -49.933033,-161.84761
        -51.367935,-161.83531 -52.80146,-161.84312 -54.23367,-161.87285
        -55.66443,-161.92648 -57.093544,-162.00793 -58.521,-162.11998
        -59.946686,-162.26761 -61.37046,-162.45544 -62.792118,-162.69069
        -64.21146,-162.98106 -65.62834,-163.33575 -67.042274,-163.76714
        -68.45288,-164.29143 -69.859634,-164.92822 -71.26191,-165.70526
        -72.658615,-166.65656 -74.0487,-167.8332 -75.43023,-169.30045
        -76.80091,-171.15746 -78.15696,-173.54726 -79.49304,-176.6876
        -80.800674,179.079 -82.0659,173.21472 -83.2653,164.86243 -84.35655,
        152.84338 -85.26478,136.23788 -85.86783,116.292046 -86.02437,
        97.23363 -85.68555,82.38748 -84.95029,71.906525 -83.96155,64.61662
        -82.82367,59.44964 -81.59658,55.680244 -80.314255,52.855778
        -78.99582,50.68698 -77.65298,48.991104 -76.29254,47.642315
        -74.919304,46.55744 -73.536354,45.67628 -72.14566,44.95468
        -70.74912,44.362564 -69.34756,43.874413 -67.941925,43.472404
        -66.532845,43.142944 -65.120705,42.87372 -63.70599,42.656162
        -62.288883,42.48286 -60.86981,42.348145 -59.44873,42.24664
        -58.025944,42.174953 -56.601532,42.129406 -55.17559,42.126205
        -55.03294,41.97427 -55.046413,39.185154 -55.25777,34.634563
        -55.45045,31.789438 -55.466427,29.250269 -55.403603,27.420107
        -55.30776,25.621023 -55.167843,24.222324 -55.02524,22.759287
        -54.84237,21.557997 -54.66517,20.3466 -54.460697,20.237915
        -54.441048,19.102398 -54.22259,17.797152 -53.94082,16.622656
        -53.65801,15.2079735 -53.27901,13.869392 -52.88062,12.162253
        -52.31542,10.433647 -51.677925,8.025516 -50.682514,5.26387
        -49.391403,2.9975026 -48.21471,1.7979982 -49.493137,0.5294303
        -50.756454,-0.8142948 -52.00312,-2.2393064 -53.231777,-3.7530673
        -54.440105,-5.363147 -55.626335,-7.0772276 -56.788067,-8.904466
        -57.922726,-10.854259 -59.027046,-12.935997 -60.098076,-15.159458
        -61.13198,-17.535229 -62.124485,-20.072094 -63.07139,-22.778967
        -63.967415,-25.66321 -64.807335,-28.72972 -65.5853,-31.980095
        -66.29536,-35.412533 -66.93118,-39.019417 -67.48627,-42.78771
        -67.95503,-46.698044 -68.331345,-50.723804 -68.61081,-54.83415
        -68.789024,-58.992157 -68.8641,-63.158737 -68.83441,-67.294525
        -68.7005,-71.36173 -68.46454,-75.326225 -68.1295,-79.159225
        -67.69996,-82.83878 -67.18137,-86.348694 -66.57933,-89.679436
        -65.90039,-92.82626 -65.15065,-95.78978 -64.33625,-98.573654
        -63.463356,-101.183464 -62.53699,-103.62837 -61.56301,-105.91712
        -60.545647,-108.05959 -59.489414,-110.0656 -58.398087,-111.945015
        -57.275227,-113.70738 -56.123848,-115.361176 -54.946712,-116.915955
        -53.746525,-118.37842 -52.525215,-119.7566 -51.284954,-121.05684
        -50.02733,-122.285194 -48.75396,-123.44766 -47.466236,-124.54916
        -46.16549,-125.59435 -44.852684,-126.58748 -43.528973,-127.532715
        -42.195194,-128.43346 -40.85215,-129.2928 -39.50057,-130.11357
        -38.141052,-130.89899 -36.77444,-131.65112 -35.400944,-132.37218
        -34.02129,-133.06442 -32.635868,-133.72968 -31.244947,-134.36969
        -29.84921,-134.986 -28.448847,-135.58011 -27.044147,-136.15329
        -25.63547,-136.70697 -24.223038,-137.24176 -22.807102,-137.75931
        -21.388006,-138.26021 -19.965841,-138.74564 -18.540913,-139.21616
        -17.113373,-139.67268 -15.683356,-140.11574 -14.251141,-140.54623
        -12.816804,-140.96466 -11.380524,-141.3715 -9.942434,-141.76732
        -8.5027075,-142.15276 -7.0615087,-142.52805 -5.618855,-142.8935
        -4.174853,-143.2499 -2.7297516,-143.59718 -1.2835804,-143.93591
        0.16357219,-144.26636 1.6115451,-144.58876 3.060406,-144.90343
        4.509823,-145.21043 5.959863,-145.51028 7.4104013,-145.80266
        8.861442,-146.08827 10.312798,-146.36702 11.764436,-146.63904
        13.216296,-146.90446 14.668324,-147.16338 16.120392,-147.41582
        17.572514,-147.66212 19.024536,-147.90187 20.47647,-148.13544
        21.928299,-148.36252 23.379938,-148.58336 24.831314,-148.7979
        26.28233,-149.00587 27.733017,-149.2073 29.183317,-149.40189
        30.633192,-149.58995 32.082634,-149.77095 33.531525,-149.94458
        34.97986,-150.11072 36.42764,-150.26903 37.874813,-150.41914
        39.321262,-150.56076 40.767162,-150.6933 42.21223,-150.81644
        43.656563,-150.92914 45.100143,-151.03064 46.542896,-151.12057
        47.984806,-151.19794 49.425816,-151.26094 50.865997,-151.30888
        52.305145,-151.34026 53.74333,-151.35222 55.180435,-151.3441
        56.6164,-151.31236 58.051247,-151.25456 59.484783,-151.16652
        60.916973,-151.04451 62.347614,-150.88228 63.77665,-150.6746
        65.203926,-150.41205 66.62913,-150.08498 68.05198,-149.68013
        69.47207,-149.18077 70.88893,-148.56462 72.301895,-147.80183
        73.71006,-146.85233 75.1123,-145.65822 76.50659,-144.1392 77.8906,
        -142.17181 79.26021,-139.56924 80.60941,-139.26428 80.74289,
        -139.71744 80.782845,-149.52025 81.44782,-166.19548 81.888435,
        -177.0563 81.77956,173.72198 81.42245, 167.61758 81.01948,162.17168
        80.51275,158.34344 80.04836,154.71835 79.50131,152.02135 79.0081,
        149.54279 78.47264,149.33173 78.42278,147.23262 77.884476,145.04593
        77.22712,143.26828 76.60097,141.34348 75.80367,139.7172 75.00619,
        137.88255 73.928764,136.25655 72.76941,134.30263 71.04028,132.39934
        68.891846,131.1469 67.160164))"""
        geometry = wkt.loads(_wkt)
        print(geometry)
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(reworked)
        self.assertFalse(shapely.difference(reworked, wkt.loads(
            """MULTIPOLYGON (((-180 81.66556557086965, -177.0563 81.77956,
        -166.19548 81.888435, -149.52025 81.44782, -139.71744 80.782845,
        -139.26428 80.74289, -139.56924 80.60941, -142.17181 79.26021,
        -144.1392 77.8906, -145.65822 76.50659, -146.85233 75.1123,
        -147.80183 73.71006, -148.56462 72.301895, -149.18077 70.88893,
        -149.68013 69.47207, -150.08498 68.05198, -150.41205 66.62913,
        -150.6746 65.203926, -150.88228 63.77665, -151.04451 62.347614,
        -151.16652 60.916973, -151.25456 59.484783, -151.31236 58.051247,
        -151.3441 56.6164, -151.35222 55.180435, -151.34026 53.74333,
        -151.30888 52.305145, -151.26094 50.865997, -151.19794 49.425816,
        -151.12057 47.984806, -151.03064 46.542896, -150.92914 45.100143,
        -150.81644 43.656563, -150.6933 42.21223, -150.56076 40.767162,
        -150.41914 39.321262, -150.26903 37.874813, -150.11072 36.42764,
        -149.94458 34.97986, -149.77095 33.531525, -149.58995 32.082634,
        -149.40189 30.633192, -149.2073 29.183317, -149.00587 27.733017,
        -148.7979 26.28233, -148.58336 24.831314, -148.36252 23.379938,
        -148.13544 21.928299, -147.90187 20.47647, -147.66212 19.024536,
        -147.41582 17.572514, -147.16338 16.120392, -146.90446 14.668324,
        -146.63904 13.216296, -146.36702 11.764436, -146.08827 10.312798,
        -145.80266 8.861442, -145.51028 7.4104013, -145.21043 5.959863,
        -144.90343 4.509823, -144.58876 3.060406, -144.26636 1.6115451,
        -143.93591 0.16357219, -143.89762322340053 0, -143.59718 -1.2835804,
        -143.2499 -2.7297516, -142.8935 -4.174853, -142.52805 -5.618855,
        -142.15276 -7.0615087, -141.76732 -8.5027075, -141.3715 -9.942434,
        -140.96466 -11.380524, -140.54623 -12.816804, -140.11574 -14.251141,
        -139.67268 -15.683356, -139.21616 -17.113373, -138.74564 -18.540913,
        -138.26021 -19.965841, -137.75931 -21.388006, -137.24176 -22.807102,
        -136.70697 -24.223038, -136.15329 -25.63547, -135.58011 -27.044147,
        -134.986 -28.448847, -134.36969 -29.84921, -133.72968 -31.244947,
        -133.06442 -32.635868, -132.37218 -34.02129, -131.65112 -35.400944,
        -130.89899 -36.77444, -130.11357 -38.141052, -129.2928 -39.50057,
        -128.43346 -40.85215, -127.532715 -42.195194, -126.58748 -43.528973,
        -125.59435 -44.852684, -124.54916 -46.16549, -123.44766 -47.466236,
        -122.285194 -48.75396, -121.05684 -50.02733, -119.7566 -51.284954,
        -118.37842 -52.525215, -116.915955 -53.746525, -115.361176
        -54.946712, -113.70738 -56.123848, -111.945015 -57.275227, -110.0656
        -58.398087, -108.05959 -59.489414, -105.91712 -60.545647, -103.62837
        -61.56301, -101.183464 -62.53699, -98.573654 -63.463356, -95.78978
        -64.33625, -92.82626 -65.15065, -89.679436 -65.90039, -86.348694
        -66.57933, -82.83878 -67.18137, -79.159225 -67.69996, -75.326225
        -68.1295, -71.36173 -68.46454, -67.294525 -68.7005, -63.158737
        -68.83441, -58.992157 -68.8641, -54.83415 -68.789024, -50.723804
        -68.61081, -46.698044 -68.331345, -42.78771 -67.95503, -39.019417
        -67.48627, -35.412533 -66.93118, -31.980095 -66.29536, -28.72972
        -65.5853, -25.66321 -64.807335, -22.778967 -63.967415, -20.072094
        -63.07139, -17.535229 -62.124485, -15.159458 -61.13198, -12.935997
        -60.098076, -10.854259 -59.027046, -8.904466 -57.922726, -7.0772276
        -56.788067, -5.363147 -55.626335, -3.7530673 -54.440105, -2.2393064
        -53.231777, -0.8142948 -52.00312, 0.5294303 -50.756454, 1.7979982
        -49.493137, 2.9975026 -48.21471, 5.26387 -49.391403, 8.025516
        -50.682514, 10.433647 -51.677925, 12.162253 -52.31542, 13.869392
        -52.88062, 15.2079735 -53.27901, 16.622656 -53.65801, 17.797152
        -53.94082, 19.102398 -54.22259, 20.237915 -54.441048, 20.3466
        -54.460697, 21.557997 -54.66517, 22.759287 -54.84237, 24.222324
        -55.02524, 25.621023 -55.167843, 27.420107 -55.30776, 29.250269
        -55.403603, 31.789438 -55.466427, 34.634563 -55.45045, 39.185154
        -55.25777, 41.97427 -55.046413, 42.126205 -55.03294, 42.129406
        -55.17559, 42.174953 -56.601532, 42.24664 -58.025944, 42.348145
        -59.44873, 42.48286 -60.86981, 42.656162 -62.288883, 42.87372
        -63.70599, 43.142944 -65.120705, 43.472404 -66.532845, 43.874413
        -67.941925, 44.362564 -69.34756, 44.95468 -70.74912, 45.67628
        -72.14566, 46.55744 -73.536354, 47.642315 -74.919304, 48.991104
        -76.29254, 50.68698 -77.65298, 52.855778 -78.99582, 55.680244
        -80.314255, 59.44964 -81.59658, 64.61662 -82.82367, 71.906525
        -83.96155, 82.38748 -84.95029, 97.23363 -85.68555, 116.292046
        -86.02437, 136.23788 -85.86783, 152.84338 -85.26478, 164.86243
        -84.35655, 173.21472 -83.2653, 179.079 -82.0659,
        180 -81.79064296168563, 180 -90, -180 -90, -180 -81.79064296168563,
        -176.6876 -80.800674, -173.54726 -79.49304, -171.15746 -78.15696,
        -169.30045 -76.80091, -167.8332 -75.43023, -166.65656 -74.0487,
        -165.70526 -72.658615, -164.92822 -71.26191, -164.29143 -69.859634,
        -163.76714 -68.45288, -163.33575 -67.042274, -162.98106 -65.62834,
        -162.69069 -64.21146, -162.45544 -62.792118, -162.26761 -61.37046,
        -162.11998 -59.946686, -162.00793 -58.521, -161.92648 -57.093544,
        -161.87285 -55.66443, -161.84312 -54.23367, -161.83531 -52.80146,
        -161.84761 -51.367935, -161.87724 -49.933033, -161.923 -48.49681,
        -161.98373 -47.05942, -162.05806 -45.620777, -162.14517 -44.181076,
        -162.24367 -42.74023, -162.3534 -41.298412, -162.47351 -39.85556,
        -162.60306 -38.411705, -162.74182 -36.96694, -162.8894 -35.521328,
        -163.0453 -34.0748, -163.20905 -32.6275, -163.38065 -31.179419,
        -163.55972 -29.730635, -163.7461 -28.2812, -163.93942 -26.831076,
        -164.14005 -25.380476, -164.34747 -23.929356, -164.56163 -22.477734,
        -164.78252 -21.025692, -165.01006 -19.573303, -165.24431 -18.120611,
        -165.48524 -16.667652, -165.73296 -15.214573, -165.98727 -13.761312,
        -166.24854 -12.308081, -166.5166 -10.854807, -166.7919 -9.401701,
        -167.0744 -7.948791, -167.36395 -6.4960437, -167.66136 -5.04376,
        -167.96606 -3.5917692, -168.27878 -2.1403482, -168.59976
        -0.68957067, -168.7563344849123 0, -168.92903 0.7605694, -169.26701
        2.2098553, -169.61389 3.658281, -169.97021 5.1056833, -170.33606
        6.5520263, -170.71211 7.997005, -171.09871 9.44065, -171.49606
        10.882896, -171.90495 12.323438, -172.3259 13.76221, -172.75932
        15.199154, -173.20602 16.633966, -173.6668 18.066378, -174.14215
        19.496479, -174.63301 20.923933, -175.1401 22.348572, -175.66461
        23.770105, -176.20717 25.18848, -176.76932 26.603268, -177.35207
        28.01428, -177.95688 29.421062, -178.58492 30.823515, -179.23792
        32.221195, -179.91759 33.613758, -180 33.775226354243216,
        -180 81.66556557086965)), ((180 33.775226354243216, 179.37445
        35.000885, 178.63579 36.381874, 177.86464 37.756573, 177.05809
        39.124138, 176.21387 40.484127, 175.32895 41.83596, 174.40013
        43.178772, 173.42386 44.511814, 172.39658 45.834454, 171.31366
        47.145306, 170.17073 48.443512, 168.9624 49.727764, 167.68332
        50.996677, 166.32748 52.248913, 164.88788 53.482563, 163.35751
        54.69573, 161.7284 55.88636, 159.99202 57.05182, 158.13925 58.18946,
        156.16086 59.296402, 154.04622 60.36881, 151.78534 61.40308,
        149.3682 62.394855, 146.78499 63.33947, 144.02696 64.2318, 141.08707
        65.06626, 137.96045 65.83662, 134.64603 66.53697, 131.1469
        67.160164, 132.39934 68.891846, 134.30263 71.04028, 136.25655
        72.76941, 137.88255 73.928764, 139.7172 75.00619, 141.34348
        75.80367, 143.26828 76.60097, 145.04593 77.22712, 147.23262
        77.884476, 149.33173 78.42278, 149.54279 78.47264, 152.02135
        79.0081, 154.71835 79.50131, 158.34344 80.04836, 162.17168 80.51275,
        167.61758 81.01948, 173.72198 81.42245, 180 81.66556557086965,
        180 33.775226354243216)))""")))

    def testVeryLongFootprintCrossingNorthSouthAntimeridian_1(self):
        """
        Check verry long footptint crossing north & south polar area ans
        Antimeridian. This paricular usage case has been fixed since v1.10.
        It splits the footprint in north and south hemisphere to allow the
        usage of polar inclusion algorithm.
        """
        index = 10
        geometry = fp_to_geometry(self.footprints[index])
        print(footprint_facility.to_geojson(geometry))
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(reworked)
        self.assertFalse(shapely.difference(reworked, wkt.loads(
            """POLYGON ((172.541 -1.66264, 171.947 -4.41159, 171.373
            -7.16139, 170.816 -9.91163, 170.276 -12.6619, 169.752 -15.4119,
            169.242 -18.1614, 168.745 -20.9099, 168.261 -23.6574, 167.79
            -26.4035, 167.33 -29.148, 166.881 -31.8909, 166.443 -34.6318,
            166.016 -37.3709, 165.6 -40.1078, 165.195 -42.8427, 164.802
            -45.5753, 164.421 -48.3058, 164.053 -51.034, 163.7 -53.7601,
            163.363 -56.484, 163.047 -59.2059, 162.755 -61.9256, 162.494
            -64.6434, 162.273 -67.3593, 162.109 -70.0733, 162.024 -72.7854,
            162.065 -75.4955, 162.313 -78.2033, 162.956 -80.9077, 164.486
            -83.6057, 168.83 -86.2853, 180 -87.36198338092518, 180 -90,
            -180 -90, -180 -87.36198338092518, -164.905 -88.817, -45.4789
            -88.0815, -32.8484 -85.456, -29.8241 -82.7679, -28.6634
            -80.0674, -28.1748 -77.3619, -28.0038 -74.6535, -28.0087
            -71.9429, -28.1215 -69.2304, -28.3058 -66.516, -28.5403
            -63.7998, -28.8118 -61.0816, -29.1119 -58.3615, -29.4348
            -55.6394, -29.7766 -52.9151, -30.1346 -50.1887, -30.5067
            -47.4601, -30.8917 -44.7294, -31.2887 -41.9965, -31.697
            -39.2614, -32.1163 -36.5243, -32.5465 -33.7851, -32.9876
            -31.044, -33.4397 -28.3011, -33.9032 -25.5566, -34.3785
            -22.8106, -34.8661 -20.0634, -35.3667 -17.3151, -35.881 -14.566,
            -36.4101 -11.8164, -36.9549 -9.06669, -37.5166 -6.31712,
            -38.0966 -3.56812, -38.6964 -0.820084, -38.88190842757092 0,
            -39.3177 1.92652, -39.9626 4.6712, -40.6333 7.4134, -41.3323
            10.1525, -42.0626 12.888, -42.8275 15.619, -43.6308 18.3447,
            -44.477 21.0643, -45.3711 23.7768, -46.3193 26.481, -47.3283
            29.1757, -48.4065 31.8592, -49.5633 34.5299, -50.8103 37.1857,
            -52.1612 39.8241, -53.6322 42.4422, -55.2434 45.0365, -57.0185
            47.6024, -58.987 50.1346, -61.1847 52.6263, -63.6555 55.0689,
            -66.4539 57.4515, -69.6455 59.7598, -73.3102 61.9759, -77.8972
            64.2412, -82.8603 66.1818, -88.6116 67.9344, -95.2394 69.4507,
            -102.774 70.6752, -111.141 71.5501, -112.8107414191941
            71.63817978956261, -118.109 71.2565, -126.174 70.2413, -133.363
            68.8982, -139.648 67.2853, -145.086 65.4556, -149.775 63.4536,
            -153.824 61.3154, -157.337 59.0691, -160.402 56.7364, -163.095
            54.3342, -165.478 51.8754, -167.602 49.3703, -169.509 46.827,
            -171.232 44.2516, -172.798 41.6494, -174.231 39.0244, -175.549
            36.38, -176.768 33.719, -177.899 31.0438, -178.956 28.3563,
            -179.946 25.6581, -180 25.50106498388834,
            -180 89.63275408880213, -180 90, 180 90, 180 89.63275408880213,
            180 25.50106498388834, 179.123 22.9507, 178.244 20.2355, 177.411
            17.5133, 176.62 14.7854, 175.866 12.0524, 175.146 9.31522,
            174.455 6.57451, 173.793 3.83093, 173.155 1.08503,
            172.91253696040647 0, 172.541 -1.66264), (-19.3611 -2.27227,
            -18.7138 -5.01639, -18.0408 -7.75738, -17.3397 -10.4947,
            -16.6075 -13.2276, -15.8408 -15.9555, -15.0358 -18.6776,
            -14.1879 -21.3929, -13.2922 -24.1006, -12.3427 -26.7995,
            -11.3322 -29.4882, -10.2528 -32.1654, -9.09463 -34.8293,
            -7.84626 -37.4779, -6.49405 -40.1088, -5.02146 -42.719, -3.40871
            -45.305, -1.6317 -47.8626, 0.33913 -50.3861, 2.53966 -52.8691,
            5.0143 -55.3028, 7.81747 -57.6765, 11.0155 -59.976, 14.6891
            -62.1832, 18.9326 -64.2747, 23.8522 -66.2201, 29.5575 -67.9808,
            36.1387 -69.5096, 43.6333 -70.7513, 51.9752 -71.6475, 60.9526
            -72.1465, 70.2102 -72.2146, 79.3184 -71.8472, 87.8882 -71.0696,
            95.6594 -69.9291, 102.525 -68.4834, 108.494 -66.7892, 113.647
            -64.8965, 118.089 -62.8467, 121.929 -60.6725, 125.266 -58.3993,
            128.184 -56.0468, 130.755 -53.6301, 133.036 -51.1612, 135.074
            -48.6491, 136.907 -46.1012, 138.569 -43.5231, 140.082 -40.9196,
            141.47 -38.2944, 142.749 -35.6506, 143.934 -32.9908, 145.037
            -30.3171, 146.068 -27.6312, 147.036 -24.9349, 147.948 -22.2293,
            148.81 -19.5157, 149.628 -16.795, 150.406 -14.0683, 151.148
            -11.3363, 151.859 -8.59969, 152.54 -5.8592, 153.195 -3.11541,
            153.826 -0.368877, 153.90772583407093 0, 154.435 2.3799, 155.024
            5.13045, 155.595 7.88235, 156.148 10.6352, 156.685 13.3886,
            157.208 16.1423, 157.717 18.8959, 158.214 21.6492, 158.698
            24.4019, 159.17 27.1538, 159.632 29.9047, 160.083 32.6544,
            160.524 35.4028, 160.955 38.1497, 161.376 40.895, 161.786
            43.6387, 162.187 46.3806, 162.576 49.1209, 162.953 51.8593,
            163.317 54.5961, 163.666 57.3311, 163.998 60.0643, 164.307
            62.796, 164.589 65.526, 164.834 68.2545, 165.028 70.9814,
            165.147 73.7069, 165.146 76.4308, 164.937 79.1527, 164.313
            81.8719, 162.653 84.5853, 156.879 87.2771, 73.4717 89.4102,
            72.66275828626124 89.42413766635043, 67.9659 89.3932,
            -15.4 88.2797, -27.2573 85.6202, -29.798 82.9117, -30.707
            80.1944, -31.0433 77.4736, -31.1124 74.7506, -31.035 72.026,
            -30.868 69.0802, -30.6368 66.3524, -30.3651 63.6231, -30.0634
            60.8922, -29.7384 58.1598, -29.3945 55.4256, -29.0348 52.6898,
            -28.6614 49.9522, -28.2758 47.2129, -27.8789 44.4718, -27.4715
            41.7291, -27.0538 38.9847, -26.6261 36.2388, -26.1884 33.4913,
            -25.7405 30.7425, -25.2821 27.9925, -24.8129 25.2414, -24.3325
            22.4895, -23.8401 19.7369, -23.3351 16.9839, -22.8166 14.2308,
            -22.2838 11.4778, -21.7355 8.7253, -21.1706 5.97365, -20.5876
            3.22322, -19.985 0.474428, -19.877235830367965 0, -19.3611
            -2.27227))""")))

    def testVeryLongFootprintCrossingNorthSouthAntimeridian_2(self):
        """
        Check verry long footptint crossing north & south polar area ans
        Antimeridian. This paricular usage case has been fixed since v1.10.
        It splits the footprint in north and south hemisphere to allow the
        usage of polar inclusion algorithm.
        """
        index = 11
        geometry = fp_to_geometry(self.footprints[index])
        print(geometry)
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(reworked)
        self.assertFalse(shapely.difference(reworked, wkt.loads(
            """POLYGON ((-177.727 -44.5233, -176.02 -47.0967, -174.13
            -49.6387, -172.024 -52.1432, -169.661 -54.6025, -166.989
            -57.0065, -163.945 -59.3425, -160.453 -61.5941, -156.42
            -63.7397, -151.741 -65.7515, -146.302 -67.5936, -139.996
            -69.2211, -132.758 -70.5802, -124.609 -71.6116,
            -119.00307227280112 -72.0187083791553, -116.494 -71.8798,
            -108.06 -70.9748, -100.5 -69.7213, -93.8784 -68.1795, -88.1522
            -66.4056, -83.225 -64.4476, -78.9828 -62.3444, -75.316 -60.1265,
            -72.1276 -57.8173, -69.3354 -55.435, -66.8724 -52.9934, -64.6832
            -50.5034, -62.7234 -47.9735, -60.9567 -45.4102, -59.3535
            -42.8189, -57.8897 -40.2038, -56.5455 -37.5685, -55.3044
            -34.9158, -54.1529 -32.2481, -53.0793 -29.5673, -52.074
            -26.8752, -51.129 -24.1732, -50.2373 -21.4625, -49.3929
            -18.7443, -48.5908 -16.0195, -47.8264 -13.2891, -47.096
            -10.5536, -46.3962 -7.81392, -45.7242 -5.07061, -45.0772
            -2.32425, -44.54950730431767 0, -44.4531 0.424631, -43.8499
            3.17554, -43.2658 5.92804, -42.6992 8.68171, -42.1488 11.4362,
            -41.6132 14.1911, -41.0914 16.9461, -40.5824 19.701, -40.0853
            22.4554, -39.5994 25.2092, -39.1239 27.9621, -38.6583 30.7139,
            -38.2021 33.4644, -37.7549 36.2136, -37.3164 38.9613, -36.8863
            41.7074, -36.4646 44.4518, -36.0514 47.1946, -35.6468 49.9356,
            -35.2513 52.6749, -34.8656 55.4125, -34.4909 58.1483, -34.1288
            60.8826, -33.782 63.6152, -33.4543 66.3464, -33.152 69.0762,
            -32.8851 71.8047, -32.6709 74.5319, -32.542 77.2579, -32.5662
            79.9826, -32.9134 82.7056, -34.1584 85.4254, -40.1998 88.1294,
            -180 88.99601144545146, -180 90, 180 90, 180 88.99601144545146,
            172.678 89.0414, 157.053 86.3687, 155.064 83.6366, 154.517
            80.9144, 154.411 78.1902, 154.498 75.4646, 154.688 72.7379,
            154.939 70.0099, 155.231 67.2806, 155.551 64.55, 155.892
            61.8179, 156.249 59.0842, 156.619 56.349, 157.002 53.6121,
            157.394 50.8734, 157.795 48.1331, 158.206 45.391, 158.624
            42.6472, 159.052 39.9017, 159.487 37.1547, 159.931 34.4061,
            160.385 31.656, 160.847 28.9047, 161.319 26.1523, 161.801
            23.3989, 162.294 20.6448, 162.799 17.8901, 163.316 15.1352,
            163.847 12.3803, 164.392 9.62572, 164.953 6.87183, 165.531
            4.11898, 166.128 1.36757, 166.4343869301774 0, 166.744 -1.38197,
            167.383 -4.12915, 168.046 -6.87348, 168.736 -9.61439, 169.456
            -12.3513, 170.208 -15.0835, 170.997 -17.8102, 171.826 -20.5307,
            172.701 -23.2439, 173.627 -25.949, 174.611 -28.6446, 175.66
            -31.3293, 176.783 -34.0017, 177.992 -36.6597, 179.299 -39.3012,
            180 -40.59481878958479, 180 -76.71046662724693, 178.367
            -75.7056, 175.333 -73.0583, 173.019 -70.3833, 171.17 -67.6901,
            169.636 -64.984, 168.327 -62.2682, 167.181 -59.5449, 166.157
            -56.8154, 165.228 -54.0806, 164.373 -51.3412, 163.576 -48.5977,
            162.825 -45.8505, 162.112 -43.0999, 161.43 -40.3461, 160.772
            -37.5894, 160.133 -34.8299, 159.511 -32.0679, 158.901 -29.3035,
            158.301 -26.5369, 157.708 -23.7683, 157.12 -20.998, 156.535
            -18.2261, 155.951 -15.4529, 155.366 -12.6787, 154.778 -9.90365,
            154.186 -7.12808, 153.588 -4.35228, 152.982 -1.57657,
            152.63206643630033 0, 152.366 1.19872, 151.739 3.97325, 151.097
            6.74663, 150.44 9.51847, 149.764 12.2883, 149.067 15.0558,
            148.346 17.8203, 147.596 20.5813, 146.815 23.3383, 145.997
            26.0906, 145.138 28.8373, 144.23 31.5778, 143.266 34.311,
            142.238 37.0358, 141.135 39.7508, 139.943 42.4544, 138.648
            45.1447, 137.229 47.8192, 135.662 50.4749, 133.916 53.108,
            131.951 55.7134, 129.717 58.2845, 127.148 60.8126, 124.156
            63.2858, 120.625 65.6876, 116.405 67.9951, 111.297 70.1754,
            105.056 72.1823, 97.4142 73.951, 88.1453 75.3946, 77.1743
            76.414, 65.0304 76.8979, 52.5399 76.7947, 40.7443 76.1175,
            30.3764 74.9436, 21.6809 73.3776, 14.5479 71.5188, 8.72482
            69.4463, 3.94564 67.218, -0.019286 64.8752, -3.35054 62.4467,
            -6.18666 59.953, -8.63261 57.409, -10.7675 54.8252, -12.6521
            52.2097, -14.333 49.5683, -15.8462 46.9057, -17.2205 44.2254,
            -18.4784 41.5302, -19.6381 38.8224, -20.7143 36.1039, -21.7193
            33.376, -22.6629 30.6401, -23.5536 27.8973, -24.3983 25.1484,
            -25.203 22.3944, -25.9729 19.6359, -26.7123 16.8735, -27.4251
            14.1078, -28.1145 11.3394, -28.7837 8.56872, -29.4352 5.79622,
            -30.0715 3.02231, -30.6948 0.247387, -30.749365543328622 0,
            -31.307 -2.52818, -31.9102 -5.30406, -32.5061 -8.0799, -33.0965
            -10.8554, -33.6832 -13.6303, -34.2678 -16.4043, -34.8521
            -19.1772, -35.438 -21.9486, -36.0274 -24.7185, -36.6225
            -27.4864, -37.2256 -30.2524, -37.8393 -33.0161, -38.4667
            -35.7774, -39.1113 -38.536, -39.7773 -41.2918, -40.4697
            -44.0446, -41.1947 -46.7942, -41.9601 -49.5402, -42.7757
            -52.2824, -43.6544 -55.0203, -44.6131 -57.7534, -45.6747
            -60.481, -46.8717 -63.2019, -48.2501 -65.9147, -49.8793
            -68.6169, -51.8673 -71.3046, -54.3918 -73.9715, -57.7662
            -76.6058, -62.5874 -79.1847, -70.111 -81.6578, -83.2276
            -83.8957, -106.25635166272522 -85.421628567467, -106.275
            -85.722, -106.203 -85.8938, -106.326 -85.9029,
            -116.32689773645563 -85.66133723816067, -131.404 -85.8939,
            -131.477 -85.7265, -131.3925393909133 -85.2974401058396,
            -140.432 -85.0791, -160.326 -83.1682, -171.021 -80.8255,
            -177.405 -78.3073, -180 -76.71046662724693,
            -180 -40.59481878958479, -179.28 -41.9235, -177.727
            -44.5233))""")))

    def test_optimize_very_large_2(self):
        _wkt = ("POLYGON((8.247026 44.96568, 9.292036 46.284668, 10.393683 "
                "47.59195, 11.557221 48.886055, 12.78799 50.165806, "
                "14.091579 51.429863, 15.4744215 52.67648, 16.943039 "
                "53.904106, 18.50546 55.110416, 20.169289 56.293453, "
                "21.94369 57.450485, 23.837675 58.57866, 25.861242 59.67476, "
                "28.023857 60.735462, 30.336597 61.756466, 32.809196 "
                "62.733437, 35.451427 63.66149, 38.271038 64.5355, 41.27522 "
                "65.34927, 44.466984 66.09703, 47.845764 66.77263, 51.40807 "
                "67.36881, 55.14158 67.88014, 59.03018 68.29987, 63.04915 "
                "68.62288, 67.16842 68.84511, 71.35221 68.96284, 75.560974 "
                "68.974655, 79.75362 68.88018, 83.8903 68.68093, 87.93421 "
                "68.379654, 91.853584 67.98095, 95.622826 67.489426, "
                "99.223595 66.91142, 102.64353 66.25296, 105.87664 "
                "65.520775, 108.92131 64.72095, 111.78139 63.860092, "
                "114.461975 62.943703, 116.971085 61.977257, 119.318115 "
                "60.965714, 121.51329 59.913857, 123.56667 58.825516, "
                "125.48834 57.70431, 127.288536 56.553715, 128.9763 "
                "55.376514, 130.56064 54.175446, 132.04942 52.952595, "
                "133.45097 51.71028, 134.77171 50.450123, 136.01862 "
                "49.174156, 137.1969 47.883236, 138.31248 46.579113, "
                "139.3699 45.262684, 140.37361 43.935055, 141.32816 "
                "42.597427, 142.23666 41.250244, 143.1028 39.894474, "
                "143.92972 38.530884, 144.71992 37.15987, 145.47612 "
                "35.78218, 146.20055 34.39821, 146.89532 33.008408, "
                "147.56252 31.61323, 148.20401 30.213243, 148.8212 "
                "28.808527, 149.41557 27.399542, 149.98871 25.986666, "
                "150.54189 24.570093, 151.07596 23.150103, 151.59236 "
                "21.726986, 152.09174 20.300774, 152.5753 18.871899, "
                "153.04364 17.440468, 153.49757 16.006605, 153.93802 "
                "14.570641, 154.36554 13.132637, 154.78091 11.692909, "
                "155.18428 10.251352, 155.57657 8.80826, 155.95801 7.36369, "
                "156.32918 5.917851, 156.69044 4.4708257, 157.042 3.0226383, "
                "157.38458 1.5735373, 157.7184 0.12363084, 158.04349 "
                "-1.3271537, 158.36049 -2.7784836, 158.66928 -4.2304, "
                "158.97043 -5.6828256, 159.26382 -7.13561, 159.54987 "
                "-8.588734, 159.8288 -10.042073, 160.10048 -11.495554, "
                "160.36508 -12.94912, 160.62296 -14.402592, 160.8739 "
                "-15.8561, 161.11809 -17.309488, 161.35585 -18.762575, "
                "161.5867 -20.215462, 161.81078 -21.667982, 162.02821 "
                "-23.120201, 162.2389 -24.571913, 162.4427 -26.023163, "
                "162.63988 -27.473816, 162.8298 -28.923828, 163.0122 "
                "-30.373413, 163.1876 -31.822153, 163.35529 -33.27017, "
                "163.51521 -34.71738, 163.66673 -36.163864, 163.80986 "
                "-37.609394, 163.94392 -39.054058, 164.06859 -40.49779, "
                "164.18329 -41.940495, 164.2874 -43.382195, 164.3803 "
                "-44.822784, 164.46121 -46.262253, 164.52843 -47.700706, "
                "164.58183 -49.137863, 164.62003 -50.573673, 164.64111 "
                "-52.008305, 164.64343 -53.441525, 164.62532 -54.873306, "
                "164.584 -56.303528, 164.51727 -57.732117, 164.421 "
                "-59.159084, 164.29218 -60.58416, 164.12558 -62.00721, "
                "163.91505 -63.42806, 163.65472 -64.846504, 163.3348 "
                "-66.26225, 162.94469 -67.67484, 162.47119 -69.08395, "
                "161.89597 -70.488846, 161.1968 -71.88883, 160.34218 "
                "-73.28272, 159.29146 -74.66909, 157.98883 -76.046005, "
                "156.35413 -77.41039, 156.10477 -77.59114, 156.5156 "
                "-77.60324, 164.10046 -77.71498, 176.23912 -77.46608, "
                "-176.60999 -77.066315, -170.61647 -76.57434, -166.53278 "
                "-76.15099, -162.70267 -75.684906, -159.84198 -75.29093, "
                "-156.94992 -74.8506, -154.64554 -74.46789, -152.38058 "
                "-74.06263, -152.18008 -74.025314, -150.11055 -73.625946, "
                "-147.78473 -73.14503, -145.73592 -72.6916, -143.31854 "
                "-72.118065, -141.0789 -71.545975, -138.28928 -70.771194, "
                "-135.54504 -69.93013, -131.87318 -68.653656, -127.9075 "
                "-67.02528, -124.86581 -65.54784, -127.920006 -64.763176, "
                "-130.79192 -63.917145, -133.48663 -63.015278, -136.01137 "
                "-62.06302, -138.37505 -61.06519, -140.58762 -60.02649, "
                "-142.65878 -58.950954, -144.59808 -57.84208, -146.41566 "
                "-56.703323, -148.1207 -55.537563, -149.72205 -54.347572, "
                "-151.22752 -53.135445, -152.64485 -51.903316, -153.98164 "
                "-50.65327, -155.24333 -49.386654, -156.43645 -48.105114, "
                "-157.5661 -46.8098, -158.63716 -45.50209, -159.65439 "
                "-44.183, -160.6217 -42.853344, -161.54248 -41.51403, "
                "-162.42058 -40.16588, -163.25906 -38.8096, -164.06055 "
                "-37.445766, -164.82784 -36.07498, -165.56284 -34.6977, "
                "-166.26814 -33.314495, -166.94563 -31.925747, -167.59695 "
                "-30.531786, -168.22366 -29.133085, -168.8277 -27.72995, "
                "-169.41013 -26.32266, -169.97227 -24.911488, -170.5154 "
                "-23.496784, -171.04057 -22.078714, -171.54878 -20.657534, "
                "-172.04097 -19.23349, -172.51797 -17.806734, -172.98041 "
                "-16.377419, -173.42934 -14.945875, -173.86526 -13.512076, "
                "-174.28874 -12.076349, -174.70055 -10.638694, -175.10107 "
                "-9.199341, -175.49081 -7.758427, -175.87038 -6.3160467, "
                "-176.23999 -4.872308, -176.6001 -3.4273303, -176.95105 "
                "-1.9813119, -177.29337 -0.5342251, -177.62723 0.9136972, "
                "-177.95294 2.3625014, -178.27055 3.811945, -178.58076 "
                "5.2620835, -178.88332 6.712753, -179.17883 8.163864, "
                "-179.46724 9.615332, -179.74846 11.067201, 179.97684 "
                "12.519292, 179.70895 13.971509, 179.44757 15.42387, "
                "179.19252 16.876207, 178.94403 18.328615, 178.7019 "
                "19.780912, 178.46605 21.233013, 178.23653 22.685009, "
                "178.01341 24.136726, 177.79677 25.588179, 177.58633 "
                "27.039263, 177.3824 28.49005, 177.18524 29.940344, "
                "176.99495 31.39018, 176.81151 32.839516, 176.63515 "
                "34.28835, 176.46623 35.736614, 176.30504 37.18413, "
                "176.15182 38.631187, 176.00703 40.077408, 175.87102 "
                "41.52302, 175.74452 42.9679, 175.62787 44.411922, 175.52211 "
                "45.855175, 175.4275 47.297634, 175.34534 48.73919, "
                "175.27692 50.179836, 175.223 51.619514, 175.1851 53.058167, "
                "175.16519 54.49585, 175.1652 55.93242, 175.1871 57.367794, "
                "175.23413 58.80187, 175.30946 60.234795, 175.41682 "
                "61.666172, 175.56177 63.095947, 175.74995 64.523926, "
                "175.98822 65.95004, 176.28685 67.37387, 176.65659 68.79514, "
                "177.11322 70.213394, 177.67519 71.62813, 178.36984 "
                "73.03834, 179.23201 74.443085, -179.69186 75.841, "
                "-178.33018 77.229645, -176.58134 78.60589, -174.29831 "
                "79.964905, -171.2369 81.29851, -167.00697 82.59319, "
                "-160.94902 83.8243, -151.94688 84.945564, -138.31126 "
                "85.86672, -118.715004 86.42909, -95.63204 86.45777, "
                "-75.484825 85.941154, -61.293423 85.04699, -51.918396 "
                "83.93992, -45.627518 82.71665, -41.25411 81.42622, "
                "-38.09722 80.09507, -35.748043 78.7374, -33.955788 "
                "77.36157, -32.56194 75.97284, -31.46073 74.57453, "
                "-30.580803 73.169044, -29.871939 71.7579, -29.298538 "
                "70.34209, -28.833363 68.92258, -28.455933 67.49984, "
                "-28.152029 66.074455, -27.908318 64.64674, -27.716707 "
                "63.216877, -27.568361 61.78526, -27.458477 60.35197, "
                "-27.380787 58.91714, -27.332062 57.480858, -27.308533 "
                "56.043343, -27.307472 54.604584, -27.326645 53.16469, "
                "-27.363619 51.72372, -27.369884 51.531498, -27.239649 "
                "51.51726, -24.664387 51.205338, -20.908089 50.65238, "
                "-18.576912 50.25901, -16.50009 49.88467, -14.99918 "
                "49.60503, -13.514714 49.32462, -12.350654 49.103886, "
                "-11.120221 48.870926, -10.0977125 48.678097, -9.053286 "
                "48.482067, -8.958856 48.464394, -7.964405 48.27881, "
                "-6.801798 48.063084, -5.7354417 47.86629, -4.422433 "
                "47.624893, -3.148441 47.39054, -1.4755751 47.079693, "
                "0.2758243 46.745552, 2.813852 46.23384, 5.864146 45.555958, "
                "8.247026 44.96568))")
        geometry = wkt.loads(_wkt)
        print(geometry)
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(reworked)
        self.assertFalse(shapely.difference(reworked, wkt.loads(
            """MULTIPOLYGON (((180 -77.2558308990909, 176.23912 -77.46608,
            164.10046 -77.71498, 156.5156 -77.60324, 156.10477 -77.59114,
            156.35413 -77.41039, 157.98883 -76.046005, 159.29146 -74.66909,
            160.34218 -73.28272, 161.1968 -71.88883, 161.89597 -70.488846,
            162.47119 -69.08395, 162.94469 -67.67484, 163.3348 -66.26225,
            163.65472 -64.846504, 163.91505 -63.42806, 164.12558 -62.00721,
            164.29218 -60.58416, 164.421 -59.159084, 164.51727 -57.732117,
            164.584 -56.303528, 164.62532 -54.873306, 164.64343 -53.441525,
            164.64111 -52.008305, 164.62003 -50.573673, 164.58183
            -49.137863, 164.52843 -47.700706, 164.46121 -46.262253, 164.3803
            -44.822784, 164.2874 -43.382195, 164.18329 -41.940495, 164.06859
            -40.49779, 163.94392 -39.054058, 163.80986 -37.609394, 163.66673
            -36.163864, 163.51521 -34.71738, 163.35529 -33.27017, 163.1876
            -31.822153, 163.0122 -30.373413, 162.8298 -28.923828, 162.63988
            -27.473816, 162.4427 -26.023163, 162.2389 -24.571913, 162.02821
            -23.120201, 161.81078 -21.667982, 161.5867 -20.215462, 161.35585
            -18.762575, 161.11809 -17.309488, 160.8739 -15.8561, 160.62296
            -14.402592, 160.36508 -12.94912, 160.10048 -11.495554, 159.8288
            -10.042073, 159.54987 -8.588734, 159.26382 -7.13561, 158.97043
            -5.6828256, 158.66928 -4.2304, 158.36049 -2.7784836, 158.04349
            -1.3271537, 157.746103045261 0, 157.7184 0.12363084, 157.38458
            1.5735373, 157.042 3.0226383, 156.69044 4.4708257, 156.32918
            5.917851, 155.95801 7.36369, 155.57657 8.80826, 155.18428
            10.251352, 154.78091 11.692909, 154.36554 13.132637, 153.93802
            14.570641, 153.49757 16.006605, 153.04364 17.440468, 152.5753
            18.871899, 152.09174 20.300774, 151.59236 21.726986, 151.07596
            23.150103, 150.54189 24.570093, 149.98871 25.986666, 149.41557
            27.399542, 148.8212 28.808527, 148.20401 30.213243, 147.56252
            31.61323, 146.89532 33.008408, 146.20055 34.39821, 145.47612
            35.78218, 144.71992 37.15987, 143.92972 38.530884, 143.1028
            39.894474, 142.23666 41.250244, 141.32816 42.597427, 140.37361
            43.935055, 139.3699 45.262684, 138.31248 46.579113, 137.1969
            47.883236, 136.01862 49.174156, 134.77171 50.450123, 133.45097
            51.71028, 132.04942 52.952595, 130.56064 54.175446, 128.9763
            55.376514, 127.288536 56.553715, 125.48834 57.70431, 123.56667
            58.825516, 121.51329 59.913857, 119.318115 60.965714, 116.971085
            61.977257, 114.461975 62.943703, 111.78139 63.860092, 108.92131
            64.72095, 105.87664 65.520775, 102.64353 66.25296, 99.223595
            66.91142, 95.622826 67.489426, 91.853584 67.98095, 87.93421
            68.379654, 83.8903 68.68093, 79.75362 68.88018, 75.560974
            68.974655, 71.35221 68.96284, 67.16842 68.84511, 63.04915
            68.62288, 59.03018 68.29987, 55.14158 67.88014, 51.40807
            67.36881, 47.845764 66.77263, 44.466984 66.09703, 41.27522
            65.34927, 38.271038 64.5355, 35.451427 63.66149, 32.809196
            62.733437, 30.336597 61.756466, 28.023857 60.735462, 25.861242
            59.67476, 23.837675 58.57866, 21.94369 57.450485, 20.169289
            56.293453, 18.50546 55.110416, 16.943039 53.904106, 15.4744215
            52.67648, 14.091579 51.429863, 12.78799 50.165806, 11.557221
            48.886055, 10.393683 47.59195, 9.292036 46.284668, 8.247026
            44.96568, 5.864146 45.555958, 2.813852 46.23384, 0.2758243
            46.745552, -1.4755751 47.079693, -3.148441 47.39054, -4.422433
            47.624893, -5.7354417 47.86629, -6.801798 48.063084, -7.964405
            48.27881, -8.958856 48.464394, -9.053286 48.482067, -10.0977125
            48.678097, -11.120221 48.870926, -12.350654 49.103886,
            -13.514714 49.32462, -14.99918 49.60503, -16.50009 49.88467,
            -18.576912 50.25901, -20.908089 50.65238, -24.664387 51.205338,
            -27.239649 51.51726, -27.369884 51.531498, -27.363619 51.72372,
            -27.326645 53.16469, -27.307472 54.604584, -27.308533 56.043343,
            -27.332062 57.480858, -27.380787 58.91714, -27.458477 60.35197,
            -27.568361 61.78526, -27.716707 63.216877, -27.908318 64.64674,
            -28.152029 66.074455, -28.455933 67.49984, -28.833363 68.92258,
            -29.298538 70.34209, -29.871939 71.7579, -30.580803 73.169044,
            -31.46073 74.57453, -32.56194 75.97284, -33.955788 77.36157,
            -35.748043 78.7374, -38.09722 80.09507, -41.25411 81.42622,
            -45.627518 82.71665, -51.918396 83.93992, -61.293423 85.04699,
            -75.484825 85.941154, -95.63204 86.45777, -118.715004 86.42909,
            -138.31126 85.86672, -151.94688 84.945564, -160.94902 83.8243,
            -167.00697 82.59319, -171.2369 81.29851, -174.29831 79.964905,
            -176.58134 78.60589, -178.33018 77.229645, -179.69186 75.841,
            -180 75.44071980327652, -180 90, 180 90, 180 75.44071980327652,
            179.23201 74.443085, 178.36984 73.03834, 177.67519 71.62813,
            177.11322 70.213394, 176.65659 68.79514, 176.28685 67.37387,
            175.98822 65.95004, 175.74995 64.523926, 175.56177 63.095947,
            175.41682 61.666172, 175.30946 60.234795, 175.23413 58.80187,
            175.1871 57.367794, 175.1652 55.93242, 175.16519 54.49585,
            175.1851 53.058167, 175.223 51.619514, 175.27692 50.179836,
            175.34534 48.73919, 175.4275 47.297634, 175.52211 45.855175,
            175.62787 44.411922, 175.74452 42.9679, 175.87102 41.52302,
            176.00703 40.077408, 176.15182 38.631187, 176.30504 37.18413,
            176.46623 35.736614, 176.63515 34.28835, 176.81151 32.839516,
            176.99495 31.39018, 177.18524 29.940344, 177.3824 28.49005,
            177.58633 27.039263, 177.79677 25.588179, 178.01341 24.136726,
            178.23653 22.685009, 178.46605 21.233013, 178.7019 19.780912,
            178.94403 18.328615, 179.19252 16.876207, 179.44757 15.42387,
            179.70895 13.971509, 179.97684 12.519292,
            180 12.396865980487746, 180 0, 180 -77.2558308990909)),
            ((-177.29337 -0.5342251, -176.95105 -1.9813119, -176.6001
            -3.4273303, -176.23999 -4.872308, -175.87038 -6.3160467,
            -175.49081 -7.758427, -175.10107 -9.199341, -174.70055
            -10.638694, -174.28874 -12.076349, -173.86526 -13.512076,
            -173.42934 -14.945875, -172.98041 -16.377419, -172.51797
            -17.806734, -172.04097 -19.23349, -171.54878 -20.657534,
            -171.04057 -22.078714, -170.5154 -23.496784, -169.97227
            -24.911488, -169.41013 -26.32266, -168.8277 -27.72995,
            -168.22366 -29.133085, -167.59695 -30.531786, -166.94563
            -31.925747, -166.26814 -33.314495, -165.56284 -34.6977,
            -164.82784 -36.07498, -164.06055 -37.445766, -163.25906
            -38.8096, -162.42058 -40.16588, -161.54248 -41.51403, -160.6217
            -42.853344, -159.65439 -44.183, -158.63716 -45.50209, -157.5661
            -46.8098, -156.43645 -48.105114, -155.24333 -49.386654,
            -153.98164 -50.65327, -152.64485 -51.903316, -151.22752
            -53.135445, -149.72205 -54.347572, -148.1207 -55.537563,
            -146.41566 -56.703323, -144.59808 -57.84208, -142.65878
            -58.950954, -140.58762 -60.02649, -138.37505 -61.06519,
            -136.01137 -62.06302, -133.48663 -63.015278, -130.79192
            -63.917145, -127.920006 -64.763176, -124.86581 -65.54784,
            -127.9075 -67.02528, -131.87318 -68.653656, -135.54504
            -69.93013, -138.28928 -70.771194, -141.0789 -71.545975,
            -143.31854 -72.118065, -145.73592 -72.6916, -147.78473
            -73.14503, -150.11055 -73.625946, -152.18008 -74.025314,
            -152.38058 -74.06263, -154.64554 -74.46789, -156.94992 -74.8506,
            -159.84198 -75.29093, -162.70267 -75.684906, -166.53278
            -76.15099, -170.61647 -76.57434, -176.60999 -77.066315,
            -180 -77.2558308990909, -180 0, -180 12.396865980487746,
            -179.74846 11.067201, -179.46724 9.615332, -179.17883 8.163864,
            -178.88332 6.712753, -178.58076 5.2620835, -178.27055 3.811945,
            -177.95294 2.3625014, -177.62723 0.9136972, -177.41655091370373
            0, -177.29337 -0.5342251)))""")))

    def test_error_13_01_2025(self):
        filename = 'errors_13.01.2025.txt'
        path = os.path.join(os.path.dirname(__file__), 'samples', filename)
        count = 0
        with (open(path, "r") as error_file):
            for _wkt in error_file:
                count += 1
                print(count)
                # Bypass footprint managed below with identified problems.
                invalid_single_forms = [19, 20, 39, 53, 107, 160, 161, 162,
                                        176, 177, 178, 180, 182, 204, 207]

                unsupported_huge = [26, 78, 102, 109, 124, 128, 130, 137,
                                    131, 142, 151, 152, 167, 169, 181, 185,
                                    186, 187, 203]
                cancel_list = unsupported_huge
                if count in cancel_list:
                    continue

                geometry = wkt.loads(_wkt)
                # Rework handle only polygons
                if not isinstance(geometry, Polygon):
                    continue
                print(geometry)
                if count in invalid_single_forms:
                    geometry = shapely.buffer(geometry, 0)

                reworked = footprint_facility.rework_to_polygon_geometry(
                    geometry)
                print(reworked)
                self.assertTrue(reworked.is_valid,
                                "Reworked geometry in not valid")

    @skip(reason="Not supported footprint")
    def test_error_13_01_2025_extracted_26(self):
        """
        Test Case of file "errors_13.01.2025.txt" - line 26
        This footprint has a very strange longitude coordiabtes around +/-180
        We can see:
            [-179.788113, 70.38057], [-180, 70.263906],
            [180, 72.400232], [179.999585, 72.400023], [180,72.399944],
            [180, 72.399405], [180, 72.399376], [180, 72.399276],
            [180, 72.399238], [180, 72.399183], [180, 72.399177],
            [180, 72.399156], [180, 72.399043], [180, 72.399011],
            [180, 72.39901 ], [180, 72.008172], [180, 72.008128],
            [180, 72.007871], [180, 72.007801
            ],
            ...98 times ...
            [180, 70.706422], [180, 70.263906], [179.978412, 70.25202],

            How to handle these oscillation around -/-180 ?
        :return:
        """
        _wkt = ("POLYGON ((173.178943557667 66.0797123341538, "
                "173.166466541377 66.0825070911793, 173.167638446395 "
                "66.0835015365078, 173.155093724009 66.0861059340778, "
                "172.699690104443 66.1812564087197, 172.698628797359 "
                "66.1803515625922, 172.670015081833 66.1861503819815, "
                "172.183317963261 66.2851695669719, 172.184358925825 "
                "66.2860873694679, 172.117845899888 66.2987901724398, "
                "171.720391706168 66.3750281284062, 171.719668395664 "
                "66.3743870741416, 171.200847791537 66.4703780395886, "
                "171.201556284896 66.4710181559133, 171.201105213216 "
                "66.4710975595147, 171.201253779353 66.4712320166911, "
                "171.201085038404 66.4712617244256, 171.201565370658 "
                "66.4716957022992, 170.736573429057 66.5534906625172, "
                "170.736163192412 66.5531136692527, 170.735970536396 "
                "66.5531475873612, 170.734807076494 66.5520769258592, "
                "170.205520970329 66.6405558744859, 170.206880101161 "
                "66.6418284967014, 170.205872366493 66.6419899997226, "
                "170.206242775507 66.6423362063488, 169.729340347538 "
                "66.7189893518001, 169.728124965748 66.7178337894717, "
                "169.37819285015 66.7703465560095, 169.183559658666 "
                "66.799672198641, 169.184554510133 66.8006476338793, "
                "169.181914216269 66.8010307147028, 169.18193766702 "
                "66.8010536675891, 168.686062443195 66.873551908363, "
                "168.684904532241 66.8724007791064, 168.116078586976 "
                "66.9481282915954, 168.117538753501 66.9496628406835, "
                "167.569029776395 67.0208498752846, 167.614315320137 "
                "67.069821360749, 167.749876639173 67.2102362782465, "
                "167.88553171917 67.3508761135617, 168.025859010395 "
                "67.4907991812971, 168.165616163355 67.6310756877018, "
                "168.308228666529 67.7709725674874, 168.451363814565 "
                "67.9109031449033, 168.593658374299 68.0511461651383, "
                "168.740362437631 68.1906253855857, 168.887390130253 "
                "68.3302441012353, 169.034883976415 68.4700161650924, "
                "169.185332776187 68.6094641279213, 169.336552003421 "
                "68.7490349100657, 169.490770327129 68.8882844150176, "
                "169.64723103454 69.027399188439, 169.805685628937 "
                "69.1663658178513, 169.965997992946 69.3052193265669, "
                "170.128424350726 69.4439055121378, 170.293010032053 "
                "69.582382201218, 170.458549511951 69.7208131242997, "
                "170.625706218627 69.8590762865631, 170.796774082479 "
                "69.9968114131594, 170.966055558098 70.1351635229934, "
                "171.139273747174 70.2729897592466, 171.314879957096 "
                "70.4106549688933, 171.493037449906 70.5481950498627, "
                "171.673723239664 70.6855778058914, 171.857033193866 "
                "70.8227979117422, 172.042869826756 70.9598611348833, "
                "172.231279080456 71.096763216138, 172.42215616069 "
                "71.2334527338256, 172.615227074519 71.3699843872912, "
                "172.810179511676 71.5063510329209, 173.007536981459 "
                "71.6425133903702, 173.20766477064 71.7784964351769, "
                "173.410519496948 71.914287468601, 173.616056026904 "
                "72.049881420192, 173.82493681268 72.1852561114213, "
                "174.037094651103 72.3204428920094, 174.252258254909 "
                "72.4554482085086, 174.470369827821 72.5902889795812, "
                "174.691898768581 72.7248843190542, 174.916924137385 "
                "72.859214564039, 175.144812702521 72.993328612308, "
                "175.372817875452 73.1256980111639, 175.719413852668 "
                "73.0794175488397, 176.070593804003 73.0323730436158, "
                "176.126743557826 73.0247583739739, 176.125939147035 "
                "73.0243023068753, 176.126029378935 73.024289678953, "
                "176.125678564517 73.0240908744391, 176.125994402766 "
                "73.0240467324265, 176.125722119183 73.0238923716704, "
                "176.125857253842 73.0238735107923, 176.125413996176 "
                "73.0236222586792, 176.125655628845 73.0235886011152, "
                "176.123742574642 73.0225066358993, 176.123946518922 "
                "73.0224784848947, 176.123718072984 73.0223493492346, "
                "176.774916948456 72.9323289111566, 176.776104272966 "
                "72.9329861305943, 176.776300259179 72.932958831229, "
                "176.776439913518 72.9330363327441, 176.777431380728 "
                "72.9328990839929, 176.779122499141 72.9338366019165, "
                "176.906495125108 72.9148238061541, 177.434715937013 "
                "72.8358235967977, 177.485400620919 72.8282151162738, "
                "177.48106667896 72.8258688695922, 178.094289743457 "
                "72.7307715982902, 178.094527362053 72.7308978304347, "
                "178.094637308454 72.7308807656724, 178.095774280769 "
                "72.7314849802838, 178.096629410045 72.7313521251643, "
                "178.098600840253 72.7324013663706, 178.28004827008 "
                "72.7023779341494, 178.76987277188 72.621186934419, "
                "178.766037388192 72.6191894624565, 179.351664482518 "
                "72.5179870139464, 179.351767580277 72.5180398192058, "
                "179.351915824335 72.5180141969412, 179.352588574239 "
                "72.5183588464927, 179.352885489756 72.5183075234883, "
                "179.355712470034 72.5197579269193, 179.356433643128 "
                "72.5196267295036, 180 72.402520348718, "
                "-180 72.399943708852, -179.433567591026 72.2915057505803, "
                "-179.4334017611 72.2915879009557, -179.433216905602 "
                "72.2915525227762, -179.432161427766 72.2920754697419, "
                "-179.431643642586 72.2919763304925, -179.431181031037 "
                "72.2922058581382, -179.431062961591 72.2921832858116, "
                "-179.429354534341 72.2930316175066, -179.289195590423 "
                "72.2651830546692, -179.241161037745 72.2556214462895, "
                "-178.796888019267 72.1670684401265, -178.800503528193 "
                "72.1653069935153, -178.244506998086 72.0477430481196, "
                "-178.244116621055 72.0479306113899, -178.243861008228 "
                "72.0478766067306, -178.242483819759 72.048538167036, "
                "-178.24218840385 72.0484759335801, -178.24182550574 "
                "72.0486504834644, -178.241730254979 72.0486304322945, "
                "-178.241395269498 72.0487916761131, -178.241297499028 "
                "72.0487711233462, -178.240649832429 72.0490829660098, "
                "-178.240509905851 72.0490535701961, -178.240161127107 "
                "72.0492214554655, -178.239750651321 72.0491352831568, "
                "-178.239725633649 72.0491473304027, -177.953707035954 "
                "71.9871931575548, -177.613374429004 71.9130171941952, "
                "-177.616703009812 71.9114427025655, -177.02068519836 "
                "71.7725023555932, -177.283834544638 71.6495697858135, "
                "-177.548091618983 71.5241188519904, -177.809259257633 "
                "71.3982965137616, -178.067516082976 71.2721351733463, "
                "-178.323528942182 71.1457799298299, -178.57583187952 "
                "71.0190204961358, -178.824626662048 70.8918735137983, "
                "-179.070416657873 70.7644889661896, -179.312806939943 "
                "70.6367778074043, -179.491824841048 70.5408743731896, "
                "-179.553881350293 70.5077061737108, -179.651091802825 "
                "70.4548890352188, -179.788113198731 70.3805698537077, "
                "-180 70.2639064327383, 180 72.4002315670167, "
                "179.999585490822 72.40002306259, 180 72.399943708852, "
                "180 72.3994053855274, 180 72.3993758138989, "
                "180 72.3992759944464, 180 72.399238241267, "
                "180 72.3991830657875, 180 72.3991768743652, "
                "180 72.3991560732622, 180 72.3990425664072, "
                "180 72.3990109734242, 180 72.3990101450161, "
                "180 72.0081720551638, 180 72.0081282726702, "
                "180 72.0078711620651, 180 72.0078006371219, "
                "180 72.0077764685578, 180 72.0077320089398, "
                "180 72.0076390897528, 180 72.0075520367943, "
                "180 72.0074980530538, 180 72.0074784037357, "
                "180 72.0074410303287, 180 72.0073550216106, "
                "180 72.007052037654, 180 71.9804573575485, "
                "180 71.9804091146431, 180 71.9802782870143, "
                "180 71.9800761302895, 180 71.9799694727057, "
                "180 71.9799233963198, 180 71.9797937898402, "
                "180 71.9797465099468, 180 71.9795914361277, "
                "180 71.9792388605987, 180 71.979232650663, "
                "180 71.979035405635, 180 71.9786659198905, "
                "180 71.5861377075283, 180 71.5859632167555, "
                "180 71.5859184673455, 180 71.5852190932166, "
                "180 71.5852006830471, 180 71.5847601526462, "
                "180 71.5846570909909, 180 71.5845061723652, "
                "180 71.5844199543863, 180 71.5840599115516, "
                "180 71.5836714381749, 180 71.5835671648161, "
                "180 71.5832746434326, 180 71.5638556858814, "
                "180 71.5638128317349, 180 71.5631064339829, "
                "180 71.5627680105871, 180 71.5627159880544, "
                "180 71.5624760874694, 180 71.5624683987581, "
                "180 71.5623212363625, 180 71.5622462454195, "
                "180 71.5621419653818, 180 71.5620345114973, "
                "180 71.561691783652, 180 71.5615995410981, "
                "180 71.1660821214902, 180 71.1660356121718, "
                "180 71.1659663061546, 180 71.1658698050471, "
                "180 71.1658408704234, 180 71.1658388726626, "
                "180 71.1658317840094, 180 71.1656076303597, "
                "180 71.1654683885365, 180 71.1653680827875, "
                "180 71.1653336389238, 180 71.1651998775651, "
                "180 71.164908951435, 180 71.1367162733956, "
                "180 71.136511270036, 180 71.1363222225006, "
                "180 71.1358420806914, 180 71.135309441336, "
                "180 71.1350716659728, 180 71.134554469774, "
                "180 71.1345057051436, 180 71.134495016381, "
                "180 71.1340307366507, 180 71.1338644643717, "
                "180 71.1337254624721, 180 71.1336067044562, "
                "180 70.7312512858118, 180 70.7309346659295, "
                "180 70.7306237074077, 180 70.7300529485724, "
                "180 70.7297599579229, 180 70.7292753715202, "
                "180 70.729086829137, 180 70.7288746470038, "
                "180 70.728335562687, 180 70.7278351644147, "
                "180 70.7278012907213, 180 70.727376920608, "
                "180 70.7268332354281, 180 70.7088746106886, "
                "180 70.7088551908284, 180 70.7084197642089, "
                "180 70.7079828071151, 180 70.7076939379703, "
                "180 70.7076289578831, 180 70.7076150615695, "
                "180 70.7074398795603, 180 70.7073125713518, "
                "180 70.7071244864194, 180 70.706725948709, "
                "180 70.7064992283325, 180 70.7064222482744, "
                "180 70.2639064327383, 179.978411564457 70.2520199880485, "
                "179.747833336901 70.1231777212651, 179.519940516925 "
                "69.9940724023889, 179.294439104736 69.8646964272666, "
                "179.071261155723 69.7350013655226, 178.850615731101 "
                "69.6050105532002, 178.632244333313 69.4748222567787, "
                "178.416534070498 69.3444154797658, 178.203014460907 "
                "69.2138139075997, 177.991206132554 69.0832228171423, "
                "177.782664609425 68.9523078230468, 177.577405913053 "
                "68.8210413930669, 177.374992615468 68.6894016046383, "
                "177.173202573693 68.5579335639573, 176.977505013186 "
                "68.4253479930724, 176.780460068505 68.2932900490974, "
                "176.586091291965 68.1607723573916, 176.392996938665 "
                "68.0281350587919, 176.202498454471 67.8951717316767, "
                "176.014306511468 67.7619489878355, 175.82835859166 "
                "67.6285173895888, 175.64438926187 67.4949277251335, "
                "175.461875522055 67.3613544950878, 175.281939450228 "
                "67.2275115934523, 175.103887933799 67.0935343384847, "
                "175.103370012082 67.093136677261, 175.102493993049 "
                "67.0924786495699, 175.095066337393 67.0867611009235, "
                "174.928842347864 66.959134023277, 174.754965189393 "
                "66.8247247002011, 174.583040930803 66.690068975239, "
                "174.412047887002 66.5553075029863, 174.242394174605 "
                "66.4203770481, 174.074427760776 66.2852495676271, "
                "173.908214486864 66.1499550766515, 173.743653834255 "
                "66.0145048974778, 173.685988036008 65.9664899837528, "
                "173.484153418351 66.011469877183, 173.178943557667 "
                "66.0797123341538))")
        geometry = wkt.loads(_wkt)
        print(geometry)
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(reworked)

    def test_error_13_01_2025_extracted_203(self):
        """
        Test Case of file "errors_13.01.2025.txt" - line 203
        This footprint, cross the antimeridian 3 times in north hemisphere
        but also pass over the south pole WITHOUT crossing +-180 longitude
        line in south hemisphere.

        Currently don't know how the reworked footprint should looks like.
        :return:
        """
        geometry = wkt.loads("POLYGON ((92.84236 67.44667, 96.46887 66.898636, 99.92162 66.2687, 103.1927 65.563446, 106.27939 64.78889, 109.18294 63.951305, 111.908264 63.05665, 114.46231 62.1104, 116.85347 61.11742, 119.09164 60.082855, 121.18622 59.01019, 123.14731 57.903454, 124.98479 56.766296, 126.70804 55.60149, 128.32564 54.411713, 129.84589 53.199425, 131.27698 51.96696, 132.6253 50.715828, 133.8979 49.448067, 135.10062 48.165047, 136.23874 46.868073, 137.31769 45.55864, 138.34123 44.23722, 139.31444 42.905468, 140.2405 41.563824, 141.12303 40.21324, 141.96523 38.854404, 142.76984 37.487965, 143.53984 36.114643, 144.27692 34.734634, 144.98392 33.34869, 145.66246 31.957176, 146.31471 30.560556, 146.94208 29.159204, 147.54588 27.753235, 148.12787 26.343128, 148.68958 24.929317, 149.23149 23.51184, 149.75525 22.091017, 150.262 20.667257, 150.75223 19.240482, 151.22702 17.811127, 151.68709 16.379313, 152.13316 14.945163, 152.5662 13.508923, 152.98653 12.07077, 153.39465 10.6307535, 153.79141 9.18915, 154.17726 7.7459583, 154.55247 6.301434, 154.91756 4.8556204, 155.27274 3.4086094, 155.61882 1.9606375, 155.95578 0.51169825, 156.28377 -0.93806124, 156.60368 -2.388514, 156.91502 -3.8396685, 157.21846 -5.2912936, 157.51414 -6.74338, 157.80238 -8.195809, 158.0831 -9.64852, 158.35654 -11.101406, 158.6227 -12.554484, 158.88208 -14.007494, 159.13411 -15.460579, 159.37955 -16.9135, 159.618 -18.366287, 159.84978 -19.818819, 160.0746 -21.27101, 160.29224 -22.722921, 160.50343 -24.174385, 160.70718 -25.625391, 160.90434 -27.075804, 161.0941 -28.525698, 161.27647 -29.974989, 161.4511 -31.423624, 161.61816 -32.871475, 161.77713 -34.31851, 161.92772 -35.76482, 162.06969 -37.210167, 162.20213 -38.65473, 162.3254 -40.09821, 162.43831 -41.54078, 162.54054 -42.982265, 162.63101 -44.42269, 162.70921 -45.86198, 162.77415 -47.30009, 162.82483 -48.736916, 162.85966 -50.17248, 162.87764 -51.60666, 162.87642 -53.039406, 162.85469 -54.470753, 162.80957 -55.900455, 162.7385 -57.328465, 162.63782 -58.754757, 162.50452 -60.17907, 162.33313 -61.60131, 162.11882 -63.02128, 161.85387 -64.438644, 161.53035 -65.85331, 161.13692 -67.26468, 160.66116 -68.67244, 160.08572 -70.07586, 159.38777 -71.4742, 158.53973 -72.8664, 157.50226 -74.251, 156.22198 -75.625946, 154.62552 -76.98846, 152.60495 -78.3343, 150.00749 -79.65731, 146.59592 -80.94759, 142.0041 -82.18926, 135.6623 -83.35514, 126.71312 -84.3979, 114.09335 -85.236496, 97.28751 -85.74858, 78.052536 -85.81277, 60.305435 -85.410286, 46.56523 -84.64568, 36.74957 -83.64792, 29.813765 -82.50995, 24.823318 -81.28649, 21.139164 -80.00891, 18.354044 -78.69511, 16.197372 -77.35682, 14.500261 -76.00055, 13.143473 -74.6312, 12.047251 -73.251755, 11.152132 -71.864456, 10.416725 -70.47101, 9.809853 -69.07241, 9.308249 -67.669464, 8.893127 -66.26299, 8.550886 -64.853325, 8.269844 -63.44095, 8.041124 -62.02624, 7.8574495 -60.609287, 7.712854 -59.19043, 7.6027646 -57.769726, 7.5223646 -56.34729, 7.515874 -56.204998, 6.8805385 -56.273827, 5.7050796 -56.391716, 1.9216778 -56.68637, 0.41244018 -56.766552, -2.6650984 -56.859093, -3.6949198 -56.86731, -6.322378 -56.83123, -7.7945843 -56.772038, -10.86659 -56.547005, -11.933296 -56.433914, -14.368162 -56.102283, -15.285791 -55.949387, -17.537115 -55.504967, -18.447449 -55.29575, -20.845005 -54.657192, -21.889198 -54.337482, -24.559238 -53.400692, -25.240215 -53.134125, -27.156214 -52.32434, -28.035183 -51.92368, -30.664263 -50.61766, -31.625053 -50.100536, -33.093864 -49.2689, -34.352318 -50.533707, -35.685234 -51.781975, -37.098473 -53.012344, -38.59912 -54.222843, -40.19451 -55.411427, -41.892902 -56.57584, -43.702873 -57.71348, -45.633743 -58.821274, -47.694633 -59.89627, -49.8957 -60.934635, -52.246883 -61.932213, -54.757153 -62.884895, -57.43579 -63.787632, -60.289906 -64.63496, -63.32492 -65.42135, -66.54307 -66.14061, -69.9427 -66.78683, -73.517395 -67.35323, -77.25477 -67.834366, -81.13637 -68.22411, -85.137405 -68.517715, -89.22716 -68.711, -93.36986 -68.80149, -97.52731 -68.787575, -101.65986 -68.66959, -105.72975 -68.44918, -109.70283 -68.129845, -113.5491 -67.71496, -117.2461 -67.2104, -120.77621 -66.621605, -124.12932 -65.95512, -127.30013 -65.216896, -130.28792 -64.41312, -133.0961 -63.549793, -135.73006 -62.63231, -138.19804 -61.66615, -140.5091 -60.656143, -142.67247 -59.60646, -144.69832 -58.52093, -146.59659 -57.403503, -148.37654 -56.257065, -150.04683 -55.08427, -151.61671 -53.888096, -153.0933 -52.67038, -154.48457 -51.43335, -155.79686 -50.178684, -157.03685 -48.908016, -158.20955 -47.622757, -159.3209 -46.324165, -160.37514 -45.013462, -161.37672 -43.691467, -162.32974 -42.359425, -163.2374 -41.01778, -164.10355 -39.667564, -164.93085 -38.30941, -165.72188 -36.94391, -166.47943 -35.57142, -167.20569 -34.192677, -167.9026 -32.808155, -168.57236 -31.418112, -169.21646 -30.023113, -169.83652 -28.623425, -170.43408 -27.2193, -171.01051 -25.811216, -171.56711 -24.39926, -172.10498 -22.983883, -172.62515 -21.565266, -173.12859 -20.143461, -173.61653 -18.719028, -174.08897 -17.291819, -174.54759 -15.862256, -174.99277 -14.430373, -175.42488 -12.9964485, -175.84496 -11.560459, -176.25317 -10.122684, -176.65047 -8.683286, -177.03705 -7.2423816, -177.41354 -5.800113, -177.78027 -4.3564677, -178.13748 -2.9116538, -178.48557 -1.46584, -178.82529 -0.019001152, -179.15652 1.4286697, -179.47935 2.8770704, -179.79446 4.3262277, 179.89786 5.775884, 179.59787 7.226062, 179.30495 8.676717, 179.01921 10.127641, 178.7403 11.578847, 178.46806 13.030323, 178.20268 14.481788, 177.94377 15.933465, 177.69127 17.385069, 177.44533 18.836609, 177.2058 20.288082, 176.97264 21.739407, 176.74565 23.190508, 176.52545 24.641298, 176.31142 26.091803, 176.10382 27.541882, 175.90327 28.991611, 175.70901 30.440912, 175.52196 31.889624, 175.3417 33.337906, 175.16895 34.785606, 175.0038 36.232655, 174.84639 37.679134, 174.69731 39.12493, 174.55692 40.57007, 174.4256 42.01437, 174.30424 43.45798, 174.19255 44.900814, 174.09216 46.34285, 174.00381 47.783916, 173.92827 49.224163, 173.86702 50.6635, 173.82077 52.101818, 173.79146 53.539146, 173.78111 54.97538, 173.79124 56.410492, 173.82515 57.844414, 173.88498 59.277023, 173.97514 60.708263, 174.09917 62.13807, 174.26279 63.566204, 174.47261 64.992386, 174.73648 66.4166, 175.06464 67.838356, 175.46959 69.25746, 175.96869 70.67324, 176.58209 72.0852, 177.34033 73.49217, 178.28102 74.89328, 179.46054 76.28659, -179.0424 77.669464, -177.11446 79.038376, -174.57556 80.38709, -171.14789 81.70636, -170.74136 81.836105, -172.71097 82.0207, -176.59584 82.335846, 168.85146 83.06716, 162.33987 83.21439, 148.62306 83.21949, 144.11824 83.13015, 133.35873 82.70291, 127.96553 82.34722, 118.41695 81.37115, 115.6331 80.966736, 110.20478 79.93317, 108.46025 79.50666, 104.78052 78.379875, 103.507904 77.892525, 100.65821 76.52166, 99.614914 75.88457, 97.38589 74.142876, 96.901924 73.67248, 95.686 72.29117, 95.18924 71.62867, 93.87908 69.53611, 93.452675 68.72845, 92.84236 67.44667))")
        expected = wkt.loads("MULTIPOLYGON (((180 -90, -180 -90, -180 5.294644093337297, -179.79446 4.3262277, -179.47935 2.8770704, -179.15652 1.4286697, -178.82529 -0.019001152, -178.48557 -1.46584, -178.13748 -2.9116538, -177.78027 -4.3564677, -177.41354 -5.800113, -177.03705 -7.2423816, -176.65047 -8.683286, -176.25317 -10.122684, -175.84496 -11.560459, -175.42488 -12.9964485, -174.99277 -14.430373, -174.54759 -15.862256, -174.08897 -17.291819, -173.61653 -18.719028, -173.12859 -20.143461, -172.62515 -21.565266, -172.10498 -22.983883, -171.56711 -24.39926, -171.01051 -25.811216, -170.43408 -27.2193, -169.83652 -28.623425, -169.21646 -30.023113, -168.57236 -31.418112, -167.9026 -32.808155, -167.20569 -34.192677, -166.47943 -35.57142, -165.72188 -36.94391, -164.93085 -38.30941, -164.10355 -39.667564, -163.2374 -41.01778, -162.32974 -42.359425, -161.37672 -43.691467, -160.37514 -45.013462, -159.3209 -46.324165, -158.20955 -47.622757, -157.03685 -48.908016, -155.79686 -50.178684, -154.48457 -51.43335, -153.0933 -52.67038, -151.61671 -53.888096, -150.04683 -55.08427, -148.37654 -56.257065, -146.59659 -57.403503, -144.69832 -58.52093, -142.67247 -59.60646, -140.5091 -60.656143, -138.19804 -61.66615, -135.73006 -62.63231, -133.0961 -63.549793, -130.28792 -64.41312, -127.30013 -65.216896, -124.12932 -65.95512, -120.77621 -66.621605, -117.2461 -67.2104, -113.5491 -67.71496, -109.70283 -68.129845, -105.72975 -68.44918, -101.65986 -68.66959, -97.52731 -68.787575, -93.36986 -68.80149, -89.22716 -68.711, -85.137405 -68.517715, -81.13637 -68.22411, -77.25477 -67.834366, -73.517395 -67.35323, -69.9427 -66.78683, -66.54307 -66.14061, -63.32492 -65.42135, -60.289906 -64.63496, -57.43579 -63.787632, -54.757153 -62.884895, -52.246883 -61.932213, -49.8957 -60.934635, -47.694633 -59.89627, -45.633743 -58.821274, -43.702873 -57.71348, -41.892902 -56.57584, -40.19451 -55.411427, -38.59912 -54.222843, -37.098473 -53.012344, -35.685234 -51.781975, -34.352318 -50.533707, -33.093864 -49.2689, -31.625053 -50.100536, -30.664263 -50.61766, -28.035183 -51.92368, -27.156214 -52.32434, -25.240215 -53.134125, -24.559238 -53.400692, -21.889198 -54.337482, -20.845005 -54.657192, -18.447449 -55.29575, -17.537115 -55.504967, -15.285791 -55.949387, -14.368162 -56.102283, -11.933296 -56.433914, -10.86659 -56.547005, -7.7945843 -56.772038, -6.322378 -56.83123, -3.6949198 -56.86731, -2.6650984 -56.859093, 0.41244018 -56.766552, 1.9216778 -56.68637, 5.7050796 -56.391716, 6.8805385 -56.273827, 7.515874 -56.204998, 7.5223646 -56.34729, 7.6027646 -57.769726, 7.712854 -59.19043, 7.8574495 -60.609287, 8.041124 -62.02624, 8.269844 -63.44095, 8.550886 -64.853325, 8.893127 -66.26299, 9.308249 -67.669464, 9.809853 -69.07241, 10.416725 -70.47101, 11.152132 -71.864456, 12.047251 -73.251755, 13.143473 -74.6312, 14.500261 -76.00055, 16.197372 -77.35682, 18.354044 -78.69511, 21.139164 -80.00891, 24.823318 -81.28649, 29.813765 -82.50995, 36.74957 -83.64792, 46.56523 -84.64568, 60.305435 -85.410286, 78.052536 -85.81277, 97.28751 -85.74858, 114.09335 -85.236496, 126.71312 -84.3979, 135.6623 -83.35514, 142.0041 -82.18926, 146.59592 -80.94759, 150.00749 -79.65731, 152.60495 -78.3343, 154.62552 -76.98846, 156.22198 -75.625946, 157.50226 -74.251, 158.53973 -72.8664, 159.38777 -71.4742, 160.08572 -70.07586, 160.66116 -68.67244, 161.13692 -67.26468, 161.53035 -65.85331, 161.85387 -64.438644, 162.11882 -63.02128, 162.33313 -61.60131, 162.50452 -60.17907, 162.63782 -58.754757, 162.7385 -57.328465, 162.80957 -55.900455, 162.85469 -54.470753, 162.87642 -53.039406, 162.87764 -51.60666, 162.85966 -50.17248, 162.82483 -48.736916, 162.77415 -47.30009, 162.70921 -45.86198, 162.63101 -44.42269, 162.54054 -42.982265, 162.43831 -41.54078, 162.3254 -40.09821, 162.20213 -38.65473, 162.06969 -37.210167, 161.92772 -35.76482, 161.77713 -34.31851, 161.61816 -32.871475, 161.4511 -31.423624, 161.27647 -29.974989, 161.0941 -28.525698, 160.90434 -27.075804, 160.70718 -25.625391, 160.50343 -24.174385, 160.29224 -22.722921, 160.0746 -21.27101, 159.84978 -19.818819, 159.618 -18.366287, 159.37955 -16.9135, 159.13411 -15.460579, 158.88208 -14.007494, 158.6227 -12.554484, 158.35654 -11.101406, 158.0831 -9.64852, 157.80238 -8.195809, 157.51414 -6.74338, 157.21846 -5.2912936, 156.91502 -3.8396685, 156.60368 -2.388514, 156.28377 -0.93806124, 155.95578 0.51169825, 155.61882 1.9606375, 155.27274 3.4086094, 154.91756 4.8556204, 154.55247 6.301434, 154.17726 7.7459583, 153.79141 9.18915, 153.39465 10.6307535, 152.98653 12.07077, 152.5662 13.508923, 152.13316 14.945163, 151.68709 16.379313, 151.22702 17.811127, 150.75223 19.240482, 150.262 20.667257, 149.75525 22.091017, 149.23149 23.51184, 148.68958 24.929317, 148.12787 26.343128, 147.54588 27.753235, 146.94208 29.159204, 146.31471 30.560556, 145.66246 31.957176, 144.98392 33.34869, 144.27692 34.734634, 143.53984 36.114643, 142.76984 37.487965, 141.96523 38.854404, 141.12303 40.21324, 140.2405 41.563824, 139.31444 42.905468, 138.34123 44.23722, 137.31769 45.55864, 136.23874 46.868073, 135.10062 48.165047, 133.8979 49.448067, 132.6253 50.715828, 131.27698 51.96696, 129.84589 53.199425, 128.32564 54.411713, 126.70804 55.60149, 124.98479 56.766296, 123.14731 57.903454, 121.18622 59.01019, 119.09164 60.082855, 116.85347 61.11742, 114.46231 62.1104, 111.908264 63.05665, 109.18294 63.951305, 106.27939 64.78889, 103.1927 65.563446, 99.92162 66.2687, 96.46887 66.898636, 92.84236 67.44667, 93.452675 68.72845, 93.87908 69.53611, 95.18924 71.62867, 95.686 72.29117, 96.901924 73.67248, 97.38589 74.142876, 99.614914 75.88457, 100.65821 76.52166, 103.507904 77.892525, 104.78052 78.379875, 108.46025 79.50666, 110.20478 79.93317, 115.6331 80.966736, 118.41695 81.37115, 127.96553 82.34722, 133.35873 82.70291, 144.11824 83.13015, 148.62306 83.21949, 162.33987 83.21439, 168.85146 83.06716, 180 82.50691458976273, 180 76.78490349981963, 179.46054 76.28659, 178.28102 74.89328, 177.34033 73.49217, 176.58209 72.0852, 175.96869 70.67324, 175.46959 69.25746, 175.06464 67.838356, 174.73648 66.4166, 174.47261 64.992386, 174.26279 63.566204, 174.09917 62.13807, 173.97514 60.708263, 173.88498 59.277023, 173.82515 57.844414, 173.79124 56.410492, 173.78111 54.97538, 173.79146 53.539146, 173.82077 52.101818, 173.86702 50.6635, 173.92827 49.224163, 174.00381 47.783916, 174.09216 46.34285, 174.19255 44.900814, 174.30424 43.45798, 174.4256 42.01437, 174.55692 40.57007, 174.69731 39.12493, 174.84639 37.679134, 175.0038 36.232655, 175.16895 34.785606, 175.3417 33.337906, 175.52196 31.889624, 175.70901 30.440912, 175.90327 28.991611, 176.10382 27.541882, 176.31142 26.091803, 176.52545 24.641298, 176.74565 23.190508, 176.97264 21.739407, 177.2058 20.288082, 177.44533 18.836609, 177.69127 17.385069, 177.94377 15.933465, 178.20268 14.481788, 178.46806 13.030323, 178.7403 11.578847, 179.01921 10.127641, 179.30495 8.676717, 179.59787 7.226062, 179.89786 5.775884, 180 5.294644093337297, 180 -90)), ((-180 82.50691458976273, -176.59584 82.335846, -172.71097 82.0207, -170.74136 81.836105, -171.14789 81.70636, -174.57556 80.38709, -177.11446 79.038376, -179.0424 77.669464, -180 76.78490349981963, -180 82.50691458976273)))")
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(geometry)
        print(reworked)
        self.assertTrue(geometry_compare(reworked, expected, 0.0),
                        "Reworked geometry is not equivalent to the expected")

    def test_error_13_01_2025_extracted_187(self):
        geometry = wkt.loads("POLYGON ((90.1772 68.25776, 95.14527 67.70738, 99.85219 67.00865, 104.26683 66.17488, 108.374596 65.219505, 112.174286 64.15598, 115.67488 62.99702, 118.89214 61.754562, 121.84533 60.438896, 124.55564 59.059242, 127.04492 57.62396, 129.33426 56.140106, 131.4426 54.613567, 133.38858 53.049805, 135.18843 51.453068, 136.857 49.827454, 138.4075 48.176212, 139.85223 46.502453, 141.20096 44.80844, 142.46341 43.09636, 143.64766 41.368267, 144.76118 39.625725, 145.8106 37.87022, 146.8011 36.10291, 147.73846 34.325127, 148.62688 32.537716, 149.47069 30.741678, 150.27315 28.937721, 151.03793 27.126616, 151.76752 25.30891, 152.46507 23.485395, 153.13246 21.656473, 153.77208 19.822557, 154.38576 17.98428, 154.9752 16.141935, 155.54178 14.295823, 156.08737 12.446474, 156.61282 10.594082, 157.11946 8.738977, 157.60835 6.881488, 158.08047 5.0219603, 158.53633 3.1604156, 158.97707 1.2972205, 159.40337 -0.5672917, 159.8154 -2.433111, 160.21437 -4.2998776, 160.60027 -6.167485, 160.97365 -8.035686, 161.33482 -9.904361, 161.68446 -11.773263, 162.0223 -13.642363, 162.34875 -15.511422, 162.66417 -17.380238, 162.9682 -19.24886, 163.26134 -21.116896, 163.54324 -22.984383, 163.81384 -24.851252, 164.07326 -26.717255, 164.32085 -28.58234, 164.55687 -30.44625, 164.78021 -32.309246, 164.99103 -34.170902, 165.18808 -36.031254, 165.37112 -37.890224, 165.53925 -39.747597, 165.69159 -41.603294, 165.82591 -43.457497, 165.94156 -45.309788, 166.03648 -47.160217, 166.10869 -49.008656, 166.15521 -50.85504, 166.17297 -52.69919, 166.1585 -54.54093, 166.1063 -56.380196, 166.01114 -58.21675, 165.86533 -60.050365, 165.65977 -61.880676, 165.38315 -63.7073, 165.01938 -65.52983, 164.54851 -67.34741, 163.94405 -69.15922, 163.16902 -70.963974, 162.17049 -72.759834, 160.87265 -74.544044, 159.1632 -76.31257, 156.86652 -78.0588, 153.69585 -79.77189, 149.16064 -81.4323, 142.39316 -83.00315, 131.83551 -84.40898, 115.14202 -85.49319, 91.42939 -85.986916, 66.594154 -85.682724, 48.06925 -84.71674, 36.227932 -83.3727, 28.701477 -81.8349, 23.715187 -80.19415, 20.263403 -78.49403, 17.780928 -76.75754, 15.94494 -74.99694, 14.557287 -73.21964, 13.491226 -71.43029, 12.664737 -69.63179, 12.020607 -67.82619, 11.518195 -66.01487, 11.128144 -64.198845, 10.829888 -62.378735, 10.606004 -60.55516, 10.444462 -58.72849, 10.422952 -58.423866, 9.761401 -58.494614, 5.0050554 -58.890965, 0.6366686 -59.074184, -1.8356657 -59.09392, -4.4969897 -59.0391, -6.173509 -58.95987, -8.1214695 -58.82012, -9.42831 -58.695538, -11.028412 -58.507076, -12.153689 -58.349674, -13.59151 -58.11717, -14.644389 -57.923553, -16.042934 -57.634186, -17.107199 -57.388107, -18.57733 -57.009285, -19.742823 -56.67536, -21.426998 -56.138054, -22.831749 -55.639027, -24.992495 -54.779778, -26.942928 -53.908604, -30.319275 -52.186672, -31.779776 -51.357315, -33.561485 -52.950565, -35.486412 -54.511757, -37.570477 -56.036545, -39.83189 -57.519855, -42.28939 -58.955853, -44.96413 -60.33765, -47.87706 -61.657448, -51.04984 -62.90613, -54.502235 -64.073586, -58.2506 -65.14816, -62.30526 -66.11773, -66.666954 -66.96884, -71.324036 -67.68787, -76.24807 -68.262215, -81.39375 -68.67948, -86.69771 -68.93078, -92.08265 -69.01003, -97.46407 -68.915405, -102.7575 -68.64885, -107.8867 -68.217026, -112.78989 -67.62904, -117.42286 -66.897224, -121.75896 -66.03444, -125.787544 -65.05423, -129.51004 -63.96967, -132.9383 -62.79364, -136.08807 -61.53681, -138.97986 -60.209713, -141.63516 -58.821182, -144.07483 -57.37886, -146.3201 -55.88979, -148.38954 -54.3595, -150.30128 -52.793175, -152.07095 -51.19496, -153.7133 -49.5688, -155.24075 -47.917778, -156.66507 -46.244568, -157.99625 -44.55179, -159.24358 -42.84148, -160.41476 -41.115387, -161.51686 -39.375153, -162.55635 -37.62212, -163.53882 -35.85755, -164.46927 -34.082623, -165.35194 -32.298176, -166.19102 -30.505262, -166.98994 -28.704391, -167.75177 -26.896488, -168.47966 -25.082136, -169.17589 -23.26179, -169.84276 -21.436085, -170.48254 -19.605461, -171.09695 -17.770355, -171.68794 -15.931217, -172.25658 -14.088236, -172.80466 -12.241981, -173.33336 -10.392684, -173.84357 -8.540604, -174.33662 -6.6860437, -174.81335 -4.829263, -175.27452 -2.9704692, -175.72101 -1.1099843, -176.15355 0.75200826, -176.57245 2.6154046, -176.97868 4.479869, -177.3725 6.3453283, -177.75433 8.2115555, -178.12486 10.078349, -178.48396 11.945658, -178.83226 13.813248, -179.16994 15.681012, -179.49709 17.548853, -179.81374 19.416548, 179.87976 21.284052, 179.58353 23.15127, 179.29749 25.018028, 179.02188 26.884314, 178.75667 28.749971, 178.50201 30.614939, 178.25873 32.47905, 178.02667 34.342358, 177.80647 36.20477, 177.5987 38.066154, 177.40405 39.926437, 177.22354 41.785618, 177.05803 43.643578, 176.90924 45.50033, 176.77817 47.35572, 176.66666 49.209736, 176.57715 51.062244, 176.5121 52.9133, 176.47565 54.76272, 176.47127 56.610374, 176.50378 58.456142, 176.57991 60.29984, 176.70735 62.141506, 176.89658 63.98046, 177.16151 65.8166, 177.5192 67.6494, 177.99457 69.47819, 178.6219 71.30187, 179.44717 73.11938, -179.45706 74.928345, -177.98526 76.72577, -175.96466 78.506454, -173.10318 80.2613, -168.88095 81.97387, -162.28577 83.61007, -160.83353 83.87085, -163.14969 84.08159, 174.93349 85.21502, 148.74185 85.37458, 134.78844 85.02311, 122.51355 84.34458, 116.367455 83.79221, 110.5861 83.055534, 107.40367 82.51325, 104.13882 81.80357, 102.19616 81.276855, 100.07129 80.57259, 98.73456 80.03521, 97.20445 79.29313, 96.20396 78.706406, 95.0228 77.86346, 94.23036 77.16723, 93.27482 76.11509, 92.6206 75.19376, 91.811806 73.69444, 91.23512 72.25064, 90.45813 69.530334, 90.1772 68.25776, 90.1772 68.25776))")
        expected = wkt.loads("MULTIPOLYGON (((180 -90, -180 -90, -180 20.551429876149996, -179.81374 19.416548, -179.49709 17.548853, -179.16994 15.681012, -178.83226 13.813248, -178.48396 11.945658, -178.12486 10.078349, -177.75433 8.2115555, -177.3725 6.3453283, -176.97868 4.479869, -176.57245 2.6154046, -176.15355 0.75200826, -175.72101 -1.1099843, -175.27452 -2.9704692, -174.81335 -4.829263, -174.33662 -6.6860437, -173.84357 -8.540604, -173.33336 -10.392684, -172.80466 -12.241981, -172.25658 -14.088236, -171.68794 -15.931217, -171.09695 -17.770355, -170.48254 -19.605461, -169.84276 -21.436085, -169.17589 -23.26179, -168.47966 -25.082136, -167.75177 -26.896488, -166.98994 -28.704391, -166.19102 -30.505262, -165.35194 -32.298176, -164.46927 -34.082623, -163.53882 -35.85755, -162.55635 -37.62212, -161.51686 -39.375153, -160.41476 -41.115387, -159.24358 -42.84148, -157.99625 -44.55179, -156.66507 -46.244568, -155.24075 -47.917778, -153.7133 -49.5688, -152.07095 -51.19496, -150.30128 -52.793175, -148.38954 -54.3595, -146.3201 -55.88979, -144.07483 -57.37886, -141.63516 -58.821182, -138.97986 -60.209713, -136.08807 -61.53681, -132.9383 -62.79364, -129.51004 -63.96967, -125.787544 -65.05423, -121.75896 -66.03444, -117.42286 -66.897224, -112.78989 -67.62904, -107.8867 -68.217026, -102.7575 -68.64885, -97.46407 -68.915405, -92.08265 -69.01003, -86.69771 -68.93078, -81.39375 -68.67948, -76.24807 -68.262215, -71.324036 -67.68787, -66.666954 -66.96884, -62.30526 -66.11773, -58.2506 -65.14816, -54.502235 -64.073586, -51.04984 -62.90613, -47.87706 -61.657448, -44.96413 -60.33765, -42.28939 -58.955853, -39.83189 -57.519855, -37.570477 -56.036545, -35.486412 -54.511757, -33.561485 -52.950565, -31.779776 -51.357315, -30.319275 -52.186672, -26.942928 -53.908604, -24.992495 -54.779778, -22.831749 -55.639027, -21.426998 -56.138054, -19.742823 -56.67536, -18.57733 -57.009285, -17.107199 -57.388107, -16.042934 -57.634186, -14.644389 -57.923553, -13.59151 -58.11717, -12.153689 -58.349674, -11.028412 -58.507076, -9.42831 -58.695538, -8.1214695 -58.82012, -6.173509 -58.95987, -4.4969897 -59.0391, -1.8356657 -59.09392, 0.6366686 -59.074184, 5.0050554 -58.890965, 9.761401 -58.494614, 10.422952 -58.423866, 10.444462 -58.72849, 10.606004 -60.55516, 10.829888 -62.378735, 11.128144 -64.198845, 11.518195 -66.01487, 12.020607 -67.82619, 12.664737 -69.63179, 13.491226 -71.43029, 14.557287 -73.21964, 15.94494 -74.99694, 17.780928 -76.75754, 20.263403 -78.49403, 23.715187 -80.19415, 28.701477 -81.8349, 36.227932 -83.3727, 48.06925 -84.71674, 66.594154 -85.682724, 91.42939 -85.986916, 115.14202 -85.49319, 131.83551 -84.40898, 142.39316 -83.00315, 149.16064 -81.4323, 153.69585 -79.77189, 156.86652 -78.0588, 159.1632 -76.31257, 160.87265 -74.544044, 162.17049 -72.759834, 163.16902 -70.963974, 163.94405 -69.15922, 164.54851 -67.34741, 165.01938 -65.52983, 165.38315 -63.7073, 165.65977 -61.880676, 165.86533 -60.050365, 166.01114 -58.21675, 166.1063 -56.380196, 166.1585 -54.54093, 166.17297 -52.69919, 166.15521 -50.85504, 166.10869 -49.008656, 166.03648 -47.160217, 165.94156 -45.309788, 165.82591 -43.457497, 165.69159 -41.603294, 165.53925 -39.747597, 165.37112 -37.890224, 165.18808 -36.031254, 164.99103 -34.170902, 164.78021 -32.309246, 164.55687 -30.44625, 164.32085 -28.58234, 164.07326 -26.717255, 163.81384 -24.851252, 163.54324 -22.984383, 163.26134 -21.116896, 162.9682 -19.24886, 162.66417 -17.380238, 162.34875 -15.511422, 162.0223 -13.642363, 161.68446 -11.773263, 161.33482 -9.904361, 160.97365 -8.035686, 160.60027 -6.167485, 160.21437 -4.2998776, 159.8154 -2.433111, 159.40337 -0.5672917, 158.97707 1.2972205, 158.53633 3.1604156, 158.08047 5.0219603, 157.60835 6.881488, 157.11946 8.738977, 156.61282 10.594082, 156.08737 12.446474, 155.54178 14.295823, 154.9752 16.141935, 154.38576 17.98428, 153.77208 19.822557, 153.13246 21.656473, 152.46507 23.485395, 151.76752 25.30891, 151.03793 27.126616, 150.27315 28.937721, 149.47069 30.741678, 148.62688 32.537716, 147.73846 34.325127, 146.8011 36.10291, 145.8106 37.87022, 144.76118 39.625725, 143.64766 41.368267, 142.46341 43.09636, 141.20096 44.80844, 139.85223 46.502453, 138.4075 48.176212, 136.857 49.827454, 135.18843 51.453068, 133.38858 53.049805, 131.4426 54.613567, 129.33426 56.140106, 127.04492 57.62396, 124.55564 59.059242, 121.84533 60.438896, 118.89214 61.754562, 115.67488 62.99702, 112.174286 64.15598, 108.374596 65.219505, 104.26683 66.17488, 99.85219 67.00865, 95.14527 67.70738, 90.1772 68.25776, 90.45813 69.530334, 91.23512 72.25064, 91.811806 73.69444, 92.6206 75.19376, 93.27482 76.11509, 94.23036 77.16723, 95.0228 77.86346, 96.20396 78.706406, 97.20445 79.29313, 98.73456 80.03521, 100.07129 80.57259, 102.19616 81.276855, 104.13882 81.80357, 107.40367 82.51325, 110.5861 83.055534, 116.367455 83.79221, 122.51355 84.34458, 134.78844 85.02311, 148.74185 85.37458, 174.93349 85.21502, 180 84.95300505306427, 180 74.03202601234753, 179.44717 73.11938, 178.6219 71.30187, 177.99457 69.47819, 177.5192 67.6494, 177.16151 65.8166, 176.89658 63.98046, 176.70735 62.141506, 176.57991 60.29984, 176.50378 58.456142, 176.47127 56.610374, 176.47565 54.76272, 176.5121 52.9133, 176.57715 51.062244, 176.66666 49.209736, 176.77817 47.35572, 176.90924 45.50033, 177.05803 43.643578, 177.22354 41.785618, 177.40405 39.926437, 177.5987 38.066154, 177.80647 36.20477, 178.02667 34.342358, 178.25873 32.47905, 178.50201 30.614939, 178.75667 28.749971, 179.02188 26.884314, 179.29749 25.018028, 179.58353 23.15127, 179.87976 21.284052, 180 20.551429876149996, 180 -90)), ((-180 84.95300505306427, -163.14969 84.08159, -160.83353 83.87085, -162.28577 83.61007, -168.88095 81.97387, -173.10318 80.2613, -175.96466 78.506454, -177.98526 76.72577, -179.45706 74.928345, -180 74.03202601234753, -180 84.95300505306427)))")
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(geometry)
        print(reworked)
        self.assertTrue(geometry_compare(reworked, expected, 0.0),
                        "Reworked geometry is not equivalent to the expected")

    @skip(reason="The reference footprint is malformed.")
    def test_error_13_01_2025_extracted_186(self):
        geometry = wkt.loads(
            "POLYGON ((-79.50155841 -53.23966919, -54.22624101 0, "
            "0 -79.4660493, -77.7839382 -54.19306622, -53.20766284 0, "
            "0 -77.85826952, -79.50155841 -53.23966919, -53.23966919 0, "
            "0 -79.50155841, -79.50155841 -53.23966919))")
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(geometry)
        print(reworked)

    def test_error_13_01_2025_extracted_185(self):
        geometry = wkt.loads("POLYGON ((45.9538 89.5934, -45.7285 89.7822, -96.6138 88.9696, -99.7496 88.5185, -101.423 88.0649, -104.81 84.8745, -105.914 78.9394, -106.061 76.9333, -97.9692 76.7818, -86.2176 76.081, -75.9171 74.8873, -67.2909 73.306, -60.2191 71.4359, -54.4472 69.3547, -49.7078 67.1201, -45.7745 64.7724, -42.4681 62.3402, -39.6515 59.8436, -37.2213 57.2972, -35.0991 54.7115, -33.2247 52.0944, -31.5525 49.4517, -30.0463 46.788, -28.6781 44.1067, -27.4253 41.4108, -26.27 38.7023, -25.1975 35.9831, -24.1958 33.2548, -23.255 30.5185, -22.3668 27.7754, -21.5243 25.0263, -20.7215 22.2721, -19.9533 19.5135, -19.2155 16.751, -18.5041 13.9853, -17.8158 11.217, -17.1478 8.44637, -16.4957 5.66767, -15.8603 2.89394, -15.2379 0.119231, -14.6263 -2.65608, -14.0238 -5.43166, -13.4284 -8.20717, -12.8385 -10.9823, -12.2523 -13.7568, -11.668 -16.5304, -11.0839 -19.3028, -10.4982 -22.0738, -9.90889 -24.8431, -9.31381 -27.6105, -8.71064 -30.3759, -8.0967 -33.1391, -7.46898 -35.8998, -6.82392 -38.6578, -6.15731 -41.413, -5.46407 -44.1652, -4.73794 -46.9141, -3.97112 -49.6595, -3.15367 -52.401, -2.27261 -55.1383, -1.31084 -57.8707, -0.245008 -60.5976, 0.957549 -63.3178, 2.34374 -66.0298, 3.98405 -68.731, 5.98849 -71.4177, 8.53849 -74.0832, 11.9554 -76.7155, 16.8527 -79.2913, 24.5282 -81.7581, 37.9743 -83.9815, 63.2834 -85.579, 100.518 -85.7692, 129.196 -84.4071, 144.619 -82.274, 153.211 -79.8441, 158.57 -77.2861, 162.244 -74.6634, 164.95 -72.0038, 167.055 -69.3209, 168.764 -66.6223, 170.198 -63.9122, 171.437 -61.1934, 172.529 -58.4677, 173.512 -55.7361, 174.409 -52.9996, 175.239 -50.2587, 176.016 -47.5138, 176.75 -44.7653, 177.45 -42.0134, 178.122 -39.2585, 178.772 -36.5007, 179.403 -33.7401, -179.981 -30.9771, -179.375 -28.2117, -178.778 -25.4442, -178.188 -22.6748, -177.602 -19.9037, -177.017 -17.1312, -176.433 -14.3573, -175.847 -11.5825, -175.258 -8.807, -174.664 -6.03105, -174.063 -3.25496, -173.454 -0.479071, -172.834 2.29629, -172.201 5.07076, -171.554 7.84394, -170.89 10.6154, -170.206 13.3848, -169.5 16.1516, -168.768 18.9152, -168.007 21.6752, -167.212 24.4308, -166.378 27.1815, -165.501 29.9264, -164.572 32.6646, -163.584 35.3952, -162.527 38.1168, -161.391 40.828, -160.16 43.5272, -158.819 46.2121, -157.344 48.8801, -155.71 51.5279, -153.883 54.1512, -151.818 56.7445, -149.46 59.3003, -146.734 61.8088, -143.543 64.2565, -139.757 66.6245, -135.209 68.8865, -129.679 71.0047, -122.91 72.926, -114.635 74.577, -104.689 75.8628, -93.2061 76.6777, -80.7939 76.9331, -80.7823 77.1123, -79.8296 83.9616, -79.6838 84.418, -79.3063 85.3306, -78.3508 86.6987, -77.8289 87.1544, -77.1057 87.6097, 70.6272 89.5914, 179.949 87.4362, -176.326 84.7244, -175.408 82.0031, -175.163 79.2791, -175.183 76.5537, -175.335 73.8269, -175.563 71.0989, -175.838 68.3697, -176.146 65.6391, -176.478 62.9071, -176.828 60.1736, -177.193 57.4384, -177.57 54.7017, -177.957 51.9632, -178.355 49.223, -178.761 46.4811, -179.176 43.7375, -179.6 40.9922, 179.968 38.2453, 179.528 35.4968, 179.079 32.7468, 178.62 29.9956, 178.153 27.2431, 177.675 24.4896, 177.186 21.7353, 176.686 18.9804, 176.174 16.2252, 175.649 13.4699, 175.11 10.7148, 174.556 7.96022, 173.985 5.20659, 173.396 2.45425, 172.788 -0.296366, 172.158 -3.0448, 171.505 -5.79057, 170.826 -8.53313, 170.119 -11.2719, 169.38 -14.0062, 168.606 -16.7353, 167.794 -19.4585, 166.938 -22.1749, 166.033 -24.8834, 165.073 -27.5829, 164.051 -30.2722, 162.958 -32.9497, 161.785 -35.6137, 160.518 -38.262, 159.145 -40.8922, 157.647 -43.5013, 156.004 -46.0857, 154.19 -48.6407, 152.175 -51.1608, 149.919 -53.6389, 147.376 -56.066, 144.488 -58.4306, 141.184 -60.7178, 137.378 -62.9082, 132.968 -64.9767, 127.844 -66.8908, 121.893 -68.6093, 115.028 -70.0816, 107.229 -71.2501, 98.5958 -72.0552, 89.388 -72.4473, 80.0045 -72.3986, 70.8927 -71.9126, 62.4262 -71.023, 54.8286 -69.7828, 48.1688 -68.2518, 42.4076 -66.4866, 37.4502 -64.5355, 33.1825 -62.4379, 29.4943 -60.2246, 26.2882 -57.9191, 23.4815 -55.5398, 21.0064 -53.1009, 18.8072 -50.6131, 16.8389 -48.0851, 15.0651 -45.5235, 13.4559 -42.9337, 11.987 -40.32, 10.6385 -37.686, 9.39361 -35.0344, 8.23873 -32.3677, 7.16229 -29.6879, 6.15456 -26.9966, 5.2074 -24.2954, 4.31376 -21.5856, 3.46767 -18.8681, 2.66401 -16.144, 1.8983 -13.4141, 1.16672 -10.6793, 0.465889 -7.94012, -0.207138 -5.19731, -0.854917 -2.4514, -1.47974 0.297061, -2.08362 3.04759, -2.66832 5.79976, -3.23544 8.55313, -3.78761 11.3136, -4.32355 14.0683, -4.84568 16.8232, -5.35497 19.5779, -5.8523 22.3322, -6.33845 25.0859, -6.81409 27.8388, -7.27981 30.5906, -7.7361 33.3411, -8.18336 36.0904, -8.62191 38.8382, -9.05196 41.5844, -9.47358 44.329, -9.88674 47.0719, -10.2912 49.8131, -10.6865 52.5527, -11.072 55.2905, -11.4465 58.0266, -11.8083 60.7612, -12.1548 63.4942, -12.4821 66.2257, -12.7841 68.9558, -13.0508 71.6847, -13.265 74.4123, -13.3948 77.1387, -13.3736 79.8638, -13.0365 82.5873, -11.8367 85.3075, -6.23691 88.0132, 45.9538 89.5934))")
        expected = wkt.loads("POLYGON ((178.772 -36.5007, 178.122 -39.2585, 177.45 -42.0134, 176.75 -44.7653, 176.016 -47.5138, 175.239 -50.2587, 174.409 -52.9996, 173.512 -55.7361, 172.529 -58.4677, 171.437 -61.1934, 170.198 -63.9122, 168.764 -66.6223, 167.055 -69.3209, 164.95 -72.0038, 162.244 -74.6634, 158.57 -77.2861, 153.211 -79.8441, 144.619 -82.274, 129.196 -84.4071, 100.518 -85.7692, 63.2834 -85.579, 37.9743 -83.9815, 24.5282 -81.7581, 16.8527 -79.2913, 11.9554 -76.7155, 8.53849 -74.0832, 5.98849 -71.4177, 3.98405 -68.731, 2.34374 -66.0298, 0.957549 -63.3178, -0.245008 -60.5976, -1.31084 -57.8707, -2.27261 -55.1383, -3.15367 -52.401, -3.97112 -49.6595, -4.73794 -46.9141, -5.46407 -44.1652, -6.15731 -41.413, -6.82392 -38.6578, -7.46898 -35.8998, -8.0967 -33.1391, -8.71064 -30.3759, -9.31381 -27.6105, -9.90889 -24.8431, -10.4982 -22.0738, -11.0839 -19.3028, -11.668 -16.5304, -12.2523 -13.7568, -12.8385 -10.9823, -13.4284 -8.20717, -14.0238 -5.43166, -14.6263 -2.65608, -15.211624861970392 0, -15.2379 0.119231, -15.8603 2.89394, -16.4957 5.66767, -17.1478 8.44637, -17.8158 11.217, -18.5041 13.9853, -19.2155 16.751, -19.9533 19.5135, -20.7215 22.2721, -21.5243 25.0263, -22.3668 27.7754, -23.255 30.5185, -24.1958 33.2548, -25.1975 35.9831, -26.27 38.7023, -27.4253 41.4108, -28.6781 44.1067, -30.0463 46.788, -31.5525 49.4517, -33.2247 52.0944, -35.0991 54.7115, -37.2213 57.2972, -39.6515 59.8436, -42.4681 62.3402, -45.7745 64.7724, -49.7078 67.1201, -54.4472 69.3547, -60.2191 71.4359, -67.2909 73.306, -75.9171 74.8873, -86.2176 76.081, -94.58392257445294 76.57992090099873, -104.689 75.8628, -114.635 74.577, -122.91 72.926, -129.679 71.0047, -135.209 68.8865, -139.757 66.6245, -143.543 64.2565, -146.734 61.8088, -149.46 59.3003, -151.818 56.7445, -153.883 54.1512, -155.71 51.5279, -157.344 48.8801, -158.819 46.2121, -160.16 43.5272, -161.391 40.828, -162.527 38.1168, -163.584 35.3952, -164.572 32.6646, -165.501 29.9264, -166.378 27.1815, -167.212 24.4308, -168.007 21.6752, -168.768 18.9152, -169.5 16.1516, -170.206 13.3848, -170.89 10.6154, -171.554 7.84394, -172.201 5.07076, -172.834 2.29629, -173.34697823958757 0, -173.454 -0.479071, -174.063 -3.25496, -174.664 -6.03105, -175.258 -8.807, -175.847 -11.5825, -176.433 -14.3573, -177.017 -17.1312, -177.602 -19.9037, -178.188 -22.6748, -178.778 -25.4442, -179.375 -28.2117, -179.981 -30.9771, -180 -31.062322402597374, -180 0, -180 38.44877407407398, -179.6 40.9922, -179.176 43.7375, -178.761 46.4811, -178.355 49.223, -177.957 51.9632, -177.57 54.7017, -177.193 57.4384, -176.828 60.1736, -176.478 62.9071, -176.146 65.6391, -175.838 68.3697, -175.563 71.0989, -175.335 73.8269, -175.183 76.5537, -175.163 79.2791, -175.408 82.0031, -176.326 84.7244, -180 87.39907200000002, -180 90, 180 90, 180 87.39907200000002, 179.949 87.4362, 70.6272 89.5914, 26.208559924889755 88.99556509093881, -6.23691 88.0132, -11.8367 85.3075, -13.0365 82.5873, -13.3736 79.8638, -13.3948 77.1387, -13.265 74.4123, -13.0508 71.6847, -12.7841 68.9558, -12.4821 66.2257, -12.1548 63.4942, -11.8083 60.7612, -11.4465 58.0266, -11.072 55.2905, -10.6865 52.5527, -10.2912 49.8131, -9.88674 47.0719, -9.47358 44.329, -9.05196 41.5844, -8.62191 38.8382, -8.18336 36.0904, -7.7361 33.3411, -7.27981 30.5906, -6.81409 27.8388, -6.33845 25.0859, -5.8523 22.3322, -5.35497 19.5779, -4.84568 16.8232, -4.32355 14.0683, -3.78761 11.3136, -3.23544 8.55313, -2.66832 5.79976, -2.08362 3.04759, -1.47974 0.297061, -1.4122074626261565 0, -0.854917 -2.4514, -0.207138 -5.19731, 0.465889 -7.94012, 1.16672 -10.6793, 1.8983 -13.4141, 2.66401 -16.144, 3.46767 -18.8681, 4.31376 -21.5856, 5.2074 -24.2954, 6.15456 -26.9966, 7.16229 -29.6879, 8.23873 -32.3677, 9.39361 -35.0344, 10.6385 -37.686, 11.987 -40.32, 13.4559 -42.9337, 15.0651 -45.5235, 16.8389 -48.0851, 18.8072 -50.6131, 21.0064 -53.1009, 23.4815 -55.5398, 26.2882 -57.9191, 29.4943 -60.2246, 33.1825 -62.4379, 37.4502 -64.5355, 42.4076 -66.4866, 48.1688 -68.2518, 54.8286 -69.7828, 62.4262 -71.023, 70.8927 -71.9126, 80.0045 -72.3986, 89.388 -72.4473, 98.5958 -72.0552, 107.229 -71.2501, 115.028 -70.0816, 121.893 -68.6093, 127.844 -66.8908, 132.968 -64.9767, 137.378 -62.9082, 141.184 -60.7178, 144.488 -58.4306, 147.376 -56.066, 149.919 -53.6389, 152.175 -51.1608, 154.19 -48.6407, 156.004 -46.0857, 157.647 -43.5013, 159.145 -40.8922, 160.518 -38.262, 161.785 -35.6137, 162.958 -32.9497, 164.051 -30.2722, 165.073 -27.5829, 166.033 -24.8834, 166.938 -22.1749, 167.794 -19.4585, 168.606 -16.7353, 169.38 -14.0062, 170.119 -11.2719, 170.826 -8.53313, 171.505 -5.79057, 172.158 -3.0448, 172.788 -0.296366, 172.8535091543131 0, 173.396 2.45425, 173.985 5.20659, 174.556 7.96022, 175.11 10.7148, 175.649 13.4699, 176.174 16.2252, 176.686 18.9804, 177.186 21.7353, 177.675 24.4896, 178.153 27.2431, 178.62 29.9956, 179.079 32.7468, 179.528 35.4968, 179.968 38.2453, 180 38.44877407407398, 180 0, 180 -31.062322402597374, 179.403 -33.7401, 178.772 -36.5007))")
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(geometry)
        print(reworked)
        self.assertTrue(geometry_compare(reworked, expected, 0.0),
                        "Reworked geometry is not equivalent to the expected")

    def test_error_13_01_2025_extracted_181(self):
        geometry = wkt.loads("POLYGON ((69.8315 89.6433, -61.0148 89.8656, -94.9287 89.4269, -97.081 88.9753, -98.0626 88.5221, -98.6025 88.0658, -98.9363 87.6094, -99.1629 87.153, -99.3263 86.6965, -99.4786 86.2331, -99.5709 85.78, -99.728 85.3196, -99.7398 84.8655, -99.7434 84.4136, -99.789 83.957, -99.8543 83.4941, -99.887 83.0391, -99.9278 82.5814, -99.9553 82.1299, -99.9828 81.6724, -100.013 81.2161, -99.9853 80.7586, -100.014 80.2981, -100.049 79.8426, -100.03 79.3901, -100.066 78.9252, -100.061 78.4686, -100.067 78.0198, -100.1 77.5589, -100.128 77.0998, -100.091 76.927, -92.0306 76.7943, -80.2287 76.1202, -69.8521 74.9488, -61.1473 73.3846, -54.0058 71.5272, -48.1762 69.4555, -43.3915 67.2278, -39.4223 64.8853, -36.0879 62.4571, -33.2491 59.9636, -30.8011 57.4197, -28.6645 54.836, -26.7784 52.2205, -25.0965 49.5792, -23.5822 46.9166, -22.2071 44.2364, -20.9486 41.5412, -19.7883 38.8335, -18.7115 36.115, -17.7061 33.3872, -16.7621 30.6514, -15.871 27.9087, -15.026 25.16, -14.2209 22.4062, -13.4508 19.6478, -12.7112 16.8856, -11.9982 14.1202, -11.3085 11.3521, -10.6391 8.58164, -9.98802 5.81191, -9.35154 3.03832, -8.72811 0.26373, -8.11568 -2.51149, -7.51235 -5.28699, -6.9163 -8.06245, -6.32576 -10.8376, -5.73901 -13.612, -5.15432 -16.3856, -4.5699 -19.158, -3.98392 -21.929, -3.39441 -24.6984, -2.79926 -27.4659, -2.19611 -30.2313, -1.58233 -32.9945, -0.954897 -35.7553, -0.310296 -38.5134, 0.355667 -41.2688, 1.04801 -44.021, 1.77295 -46.7701, 2.5382 -49.5156, 3.35358 -52.2573, 4.23191 -54.9947, 5.19007 -57.7273, 6.25103 -60.4544, 7.44696 -63.1749, 8.82389 -65.8872, 10.4508 -68.5889, 12.4353 -71.2763, 14.9541 -73.9428, 18.3187 -76.577, 23.1215 -79.1561, 30.607 -81.63, 43.6368 -83.8709, 68.1488 -85.5162, 105.129 -85.7961, 134.576 -84.4982, 150.525 -82.3911, 159.367 -79.9719, 164.852 -77.4191, 168.597 -74.7994, 171.346 -72.1415, 173.479 -69.4599, 175.207 -66.7621, 176.656 -64.0527, 177.905 -61.3344, 179.005 -58.6091, 179.994 -55.8779, -179.104 -53.1417, -178.27 -50.401, -177.489 -47.6564, -176.752 -44.9081, -176.05 -42.1564, -175.376 -39.4017, -174.725 -36.644, -174.093 -33.8837, -173.475 -31.1208, -172.868 -28.3556, -172.271 -25.5882, -171.68 -22.819, -171.093 -20.048, -170.508 -17.2755, -169.923 -14.5018, -169.337 -11.727, -168.748 -8.95159, -168.154 -6.17569, -167.553 -3.39966, -166.944 -0.623796, -166.324 2.15155, -165.692 4.92601, -165.045 7.69922, -164.382 10.4707, -163.699 13.2402, -162.994 16.007, -162.263 18.7708, -161.503 21.5308, -160.709 24.2867, -159.877 27.0375, -159.001 29.7826, -158.075 32.5211, -157.09 35.2519, -156.037 37.9739, -154.904 40.6856, -153.679 43.3853, -152.342 46.0708, -150.875 48.7396, -149.249 51.3884, -147.432 54.0129, -145.38 56.6076, -143.038 59.1653, -140.333 61.6763, -137.168 64.1272, -133.416 66.4995, -128.911 68.7674, -123.439 70.8937, -116.741 72.8264, -108.551 74.4931, -98.6962 75.7999, -87.2878 76.6415, -74.9079 76.9274, -74.9051 77.1066, -74.9037 77.5564, -74.8896 78.0202, -74.9222 78.4686, -74.8956 78.934, -74.9027 79.3881, -74.869 79.8424, -74.8369 80.3014, -74.8645 80.7604, -74.8479 81.2168, -74.8196 81.6724, -74.7845 82.1292, -74.7679 82.5814, -74.7497 83.039, -74.7254 83.4937, -74.6929 83.9497, -74.6673 84.4061, -74.6477 84.8641, -74.5515 85.3272, -74.5214 85.7777, -74.5528 86.2338, -74.3226 86.6969, -74.2402 87.1498, -74.1047 87.6034, -73.9276 88.0634, -73.5957 88.5215, -72.9981 88.9773, -70.551 89.4329, -56.3874 89.8785, 97.4036 89.6423, -172.962 87.2962, -169.629 84.583, -168.793 81.8614, -168.58 79.1373, -168.617 76.4118, -168.779 73.685, -169.013 70.957, -169.294 68.2278, -169.605 65.4971, -169.94 62.7651, -170.292 60.0315, -170.659 57.2964, -171.038 54.5596, -171.427 51.8211, -171.826 49.0809, -172.233 46.339, -172.649 43.5953, -173.074 40.85, -173.507 38.103, -173.948 35.3545, -174.398 32.6045, -174.858 29.8532, -175.326 27.1008, -175.805 24.3473, -176.295 21.593, -176.796 18.8381, -177.309 16.0829, -177.835 13.3276, -178.375 10.5726, -178.931 7.81815, -179.503 5.06462, 179.907 2.31241, 179.297 -0.438054, 178.666 -3.18632, 178.012 -5.93188, 177.331 -8.6742, 176.622 -11.4127, 175.881 -14.1467, 175.105 -16.8755, 174.29 -19.5983, 173.431 -22.3142, 172.523 -25.0222, 171.56 -27.7212, 170.534 -30.4098, 169.437 -33.0865, 168.258 -35.7496, 166.986 -38.397, 165.606 -41.0261, 164.101 -43.6338, 162.449 -46.2166, 160.625 -48.7698, 158.597 -51.2877, 156.328 -53.7632, 153.768 -56.1872, 150.859 -58.5479, 147.531 -60.8302, 143.695 -63.0146, 139.251 -65.0756, 134.086 -66.9802, 128.089 -68.6866, 121.176 -70.1442, 113.332 -71.2948, 104.664 -72.0791, 95.4395 -72.4485, 86.0628 -72.3766, 76.9798 -71.8687, 68.557 -70.9598, 61.0095 -69.7032, 54.3992 -68.1591, 48.683 -66.3835, 43.7643 -64.4243, 39.5291 -62.3203, 35.868 -60.1019, 32.6841 -57.7925, 29.8956 -55.4101, 27.4356 -52.9685, 25.2489 -50.4787, 23.2911 -47.949, 21.526 -45.3859, 19.9242 -42.795, 18.4616 -40.1803, 17.1183 -37.5454, 15.878 -34.893, 14.7271 -32.2257, 13.654 -29.5454, 12.6492 -26.8537, 11.7046 -24.1521, 10.8132 -21.4419, 9.96912 -18.7241, 9.16718 -15.9998, 8.40299 -13.2697, 7.67274 -10.5347, 6.97309 -7.79543, 6.3011 -5.05252, 5.65423 -2.30654, 5.0302 0.441978, 4.42702 3.19254, 3.84293 5.94471, 3.27634 8.69807, 2.72635 11.4498, 2.19074 14.2044, 1.66888 16.9592, 1.1598 19.7139, 0.662631 22.4681, 0.176588 25.2217, -0.298991 27.9744, -0.764703 30.7261, -1.22104 33.4765, -1.6684 36.2257, -2.1071 38.9733, -2.53734 41.7194, -2.95923 44.4638, -3.37271 47.2066, -3.77756 49.9477, -4.17335 52.6871, -4.55937 55.4247, -4.93449 58.1607, -5.297 60.8952, -5.64435 63.628, -5.97261 66.3594, -6.27567 69.0894, -6.54349 71.8181, -6.75882 74.5456, -6.88935 77.2719, -6.86721 79.997, -6.52295 82.7204, -5.28149 85.4406, 0.793633 88.145, 69.8315 89.6433))")
        expected = wkt.loads("POLYGON ((179.005 -58.6091, 177.905 -61.3344, 176.656 -64.0527, 175.207 -66.7621, 173.479 -69.4599, 171.346 -72.1415, 168.597 -74.7994, 164.852 -77.4191, 159.367 -79.9719, 150.525 -82.3911, 134.576 -84.4982, 105.129 -85.7961, 68.1488 -85.5162, 43.6368 -83.8709, 30.607 -81.63, 23.1215 -79.1561, 18.3187 -76.577, 14.9541 -73.9428, 12.4353 -71.2763, 10.4508 -68.5889, 8.82389 -65.8872, 7.44696 -63.1749, 6.25103 -60.4544, 5.19007 -57.7273, 4.23191 -54.9947, 3.35358 -52.2573, 2.5382 -49.5156, 1.77295 -46.7701, 1.04801 -44.021, 0.355667 -41.2688, -0.310296 -38.5134, -0.954897 -35.7553, -1.58233 -32.9945, -2.19611 -30.2313, -2.79926 -27.4659, -3.39441 -24.6984, -3.98392 -21.929, -4.5699 -19.158, -5.15432 -16.3856, -5.73901 -13.612, -6.32576 -10.8376, -6.9163 -8.06245, -7.51235 -5.28699, -8.11568 -2.51149, -8.66991059098018 0, -8.72811 0.26373, -9.35154 3.03832, -9.98802 5.81191, -10.6391 8.58164, -11.3085 11.3521, -11.9982 14.1202, -12.7112 16.8856, -13.4508 19.6478, -14.2209 22.4062, -15.026 25.16, -15.871 27.9087, -16.7621 30.6514, -17.7061 33.3872, -18.7115 36.115, -19.7883 38.8335, -20.9486 41.5412, -22.2071 44.2364, -23.5822 46.9166, -25.0965 49.5792, -26.7784 52.2205, -28.6645 54.836, -30.8011 57.4197, -33.2491 59.9636, -36.0879 62.4571, -39.4223 64.8853, -43.3915 67.2278, -48.1762 69.4555, -54.0058 71.5272, -61.1473 73.3846, -69.8521 74.9488, -80.2287 76.1202, -88.19008871412365 76.57493797712155, -98.6962 75.7999, -108.551 74.4931, -116.741 72.8264, -123.439 70.8937, -128.911 68.7674, -133.416 66.4995, -137.168 64.1272, -140.333 61.6763, -143.038 59.1653, -145.38 56.6076, -147.432 54.0129, -149.249 51.3884, -150.875 48.7396, -152.342 46.0708, -153.679 43.3853, -154.904 40.6856, -156.037 37.9739, -157.09 35.2519, -158.075 32.5211, -159.001 29.7826, -159.877 27.0375, -160.709 24.2867, -161.503 21.5308, -162.263 18.7708, -162.994 16.007, -163.699 13.2402, -164.382 10.4707, -165.045 7.69922, -165.692 4.92601, -166.324 2.15155, -166.80464673737976 0, -166.944 -0.623796, -167.553 -3.39966, -168.154 -6.17569, -168.748 -8.95159, -169.337 -11.727, -169.923 -14.5018, -170.508 -17.2755, -171.093 -20.048, -171.68 -22.819, -172.271 -25.5882, -172.868 -28.3556, -173.475 -31.1208, -174.093 -33.8837, -174.725 -36.644, -175.376 -39.4017, -176.05 -42.1564, -176.752 -44.9081, -177.489 -47.6564, -178.27 -50.401, -179.104 -53.1417, -180 -55.859699113082, -180 0, -180 2.74623293220327, -179.503 5.06462, -178.931 7.81815, -178.375 10.5726, -177.835 13.3276, -177.309 16.0829, -176.796 18.8381, -176.295 21.593, -175.805 24.3473, -175.326 27.1008, -174.858 29.8532, -174.398 32.6045, -173.948 35.3545, -173.507 38.103, -173.074 40.85, -172.649 43.5953, -172.233 46.339, -171.826 49.0809, -171.427 51.8211, -171.038 54.5596, -170.659 57.2964, -170.292 60.0315, -169.94 62.7651, -169.605 65.4971, -169.294 68.2278, -169.013 70.957, -168.779 73.685, -168.617 76.4118, -168.58 79.1373, -168.793 81.8614, -169.629 84.583, -172.962 87.2962, -180 87.48041333550512, -180 90, 180 90, 180 87.48041333550512, 97.4036 89.6423, -56.3874 89.8785, -57.0135084800737 89.85880204618029, 69.8315 89.6433, 0.793633 88.145, -5.28149 85.4406, -6.52295 82.7204, -6.86721 79.997, -6.88935 77.2719, -6.75882 74.5456, -6.54349 71.8181, -6.27567 69.0894, -5.97261 66.3594, -5.64435 63.628, -5.297 60.8952, -4.93449 58.1607, -4.55937 55.4247, -4.17335 52.6871, -3.77756 49.9477, -3.37271 47.2066, -2.95923 44.4638, -2.53734 41.7194, -2.1071 38.9733, -1.6684 36.2257, -1.22104 33.4765, -0.764703 30.7261, -0.298991 27.9744, 0.176588 25.2217, 0.662631 22.4681, 1.1598 19.7139, 1.66888 16.9592, 2.19074 14.2044, 2.72635 11.4498, 3.27634 8.69807, 3.84293 5.94471, 4.42702 3.19254, 5.0302 0.441978, 5.130547726061826 0, 5.65423 -2.30654, 6.3011 -5.05252, 6.97309 -7.79543, 7.67274 -10.5347, 8.40299 -13.2697, 9.16718 -15.9998, 9.96912 -18.7241, 10.8132 -21.4419, 11.7046 -24.1521, 12.6492 -26.8537, 13.654 -29.5454, 14.7271 -32.2257, 15.878 -34.893, 17.1183 -37.5454, 18.4616 -40.1803, 19.9242 -42.795, 21.526 -45.3859, 23.2911 -47.949, 25.2489 -50.4787, 27.4356 -52.9685, 29.8956 -55.4101, 32.6841 -57.7925, 35.868 -60.1019, 39.5291 -62.3203, 43.7643 -64.4243, 48.683 -66.3835, 54.3992 -68.1591, 61.0095 -69.7032, 68.557 -70.9598, 76.9798 -71.8687, 86.0628 -72.3766, 95.4395 -72.4485, 104.664 -72.0791, 113.332 -71.2948, 121.176 -70.1442, 128.089 -68.6866, 134.086 -66.9802, 139.251 -65.0756, 143.695 -63.0146, 147.531 -60.8302, 150.859 -58.5479, 153.768 -56.1872, 156.328 -53.7632, 158.597 -51.2877, 160.625 -48.7698, 162.449 -46.2166, 164.101 -43.6338, 165.606 -41.0261, 166.986 -38.397, 168.258 -35.7496, 169.437 -33.0865, 170.534 -30.4098, 171.56 -27.7212, 172.523 -25.0222, 173.431 -22.3142, 174.29 -19.5983, 175.105 -16.8755, 175.881 -14.1467, 176.622 -11.4127, 177.331 -8.6742, 178.012 -5.93188, 178.666 -3.18632, 179.297 -0.438054, 179.39415194963468 0, 179.907 2.31241, 180 2.74623293220327, 180 0, 180 -55.859699113082, 179.994 -55.8779, 179.005 -58.6091))")
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(geometry)
        print(reworked)
        self.assertTrue(geometry_compare(reworked, expected, 0.0),
                        "Reworked geometry is not equivalent to the expected")

    def test_error_13_01_2025_extracted_169(self):
        geometry = wkt.loads("POLYGON ((35.595528 54.756752, 37.230648 55.9462, 38.97297 57.110523, 40.83226 58.246887, 42.81822 59.3521, 44.94088 60.422703, 47.210064 61.454967, 49.636314 62.4444, 52.228897 63.38651, 54.99682 64.27598, 57.947166 65.106964, 61.08403 65.873695, 64.40903 66.56978, 67.917885 67.18894, 71.60204 67.72454, 75.44605 68.170525, 79.42787 68.521324, 83.51888 68.77223, 87.68465 68.91974, 91.88698 68.961685, 96.08485 68.89741, 100.2379 68.727745, 104.30818 68.455345, 108.263 68.08404, 112.074615 67.61878, 115.72262 67.06512, 119.19295 66.429344, 122.47811 65.717896, 125.57521 64.93728, 128.4863 64.093575, 131.21649 63.192844, 133.77318 62.24053, 136.16531 61.241955, 138.40262 60.20145, 140.49557 59.123463, 142.4539 58.01166, 144.28821 56.86957, 146.0074 55.70003, 147.6208 54.505875, 149.13652 53.289257, 150.56274 52.05265, 151.90651 50.797832, 153.17435 49.52635, 154.3722 48.239796, 155.50562 46.939545, 156.57962 45.626717, 157.59901 44.302437, 158.56778 42.967773, 159.4897 41.623466, 160.36835 40.270374, 161.20645 38.908974, 162.0073 37.540154, 162.77356 36.164482, 163.50737 34.78236, 164.21103 33.39439, 164.88661 32.000935, 165.53563 30.6023, 166.1602 29.199144, 166.76149 27.791496, 167.3411 26.379812, 167.90019 24.964298, 168.44008 23.545347, 168.962 22.123251, 169.46678 20.698153, 169.95508 19.269974, 170.42822 17.839388, 170.88683 16.406391, 171.33151 14.971169, 171.763 13.533704, 172.18233 12.094584, 172.58954 10.65362, 172.98534 9.211061, 173.3702 7.766964, 173.74467 6.321581, 174.10918 4.874893, 174.46417 3.4272132, 174.80968 1.9784602, 175.1462 0.52879375, 175.4743 -0.9215697, 175.79417 -2.3726044, 176.1058 -3.8242507, 176.40955 -5.276472, 176.70554 -6.7291107, 176.9943 -8.182019, 177.2757 -9.6351385, 177.54991 -11.088513, 177.81718 -12.541862, 178.07732 -13.995426, 178.33083 -15.448771, 178.57753 -16.902042, 178.8174 -18.355146, 179.0507 -19.80799, 179.27744 -21.260487, 179.49733 -22.712708, 179.71045 -24.164448, 179.91692 -25.615683, -179.88353 -27.066431, -179.69084 -28.516548, -179.50565 -29.966072, -179.32748 -31.414967, -179.15688 -32.863056, -178.99403 -34.31039, -178.83928 -35.756992, -178.69287 -37.202663, -178.5556 -38.647476, -178.42746 -40.091362, -178.3089 -41.53424, -178.20058 -42.976128, -178.10374 -44.41695, -178.01868 -45.856716, -177.94627 -47.29532, -177.8875 -48.732697, -177.84396 -50.16885, -177.81677 -51.60373, -177.80748 -53.03724, -177.818 -54.469315, -177.85109 -55.899937, -177.9088 -57.32897, -177.99428 -58.75635, -178.11176 -60.18192, -178.26524 -61.605495, -178.46011 -63.027008, -178.70311 -64.44611, -179.00287 -65.862724, -179.36832 -67.27623, -179.81323 -68.686424, 179.6463 -70.09271, 178.98912 -71.494316, 178.1871 -72.890236, 177.20335 -74.27921, 175.98602 -75.65941, 174.46321 -77.02811, 172.53185 -78.38161, 170.03717 -79.713936, 166.74629 -81.01603, 162.28969 -82.272736, 156.08195 -83.458176, 147.2112 -84.52608, 134.46266 -85.39409, 117.1074 -85.93262, 115.80803 -85.953026, 116.26059 -86.03657, 129.64954 -87.4893, -153.30655 -88.49546, -116.9236 -87.42685, -104.74276 -86.13558, -99.896164 -85.14788, -96.552086 -84.15173, -94.51047 -83.36311, -92.70713 -82.52511, -91.40472 -81.82634, -90.21072 -81.11096, -90.10842 -81.04621, -89.07934 -80.36378, -87.97148 -79.56483, -87.02828 -78.83113, -85.94574 -77.92664, -84.966866 -77.04764, -83.77711 -75.89042, -82.639694 -74.67346, -81.17525 -72.89574, -79.67728 -70.729744, -78.5924 -68.843254, -82.73444 -68.72322, -86.81283 -68.50076, -90.79302 -68.178955, -94.64508 -67.76162, -98.34641 -67.25476, -101.87992 -66.66364, -105.23501 -65.99461, -108.40666 -65.25391, -111.3949 -64.44792, -114.202095 -63.582268, -116.83514 -62.662838, -119.301895 -61.695004, -121.61082 -60.68292, -123.7726 -59.6317, -125.796425 -58.54483, -127.692245 -57.425865, -129.46979 -56.278065, -131.1378 -55.104145, -132.70544 -53.906807, -134.17982 -52.688053, -135.56882 -51.450073, -136.8791 -50.194614, -138.11699 -48.92313, -139.28809 -47.637165, -140.39755 -46.337975, -141.45004 -45.02664, -142.44995 -43.70421, -143.40146 -42.37159, -144.30768 -41.029488, -145.17256 -39.678913, -145.99864 -38.320374, -146.78862 -36.954426, -147.54518 -35.581703, -148.27026 -34.202606, -148.96654 -32.817795, -149.63538 -31.4276, -150.27855 -30.032259, -150.89806 -28.632252, -151.49512 -27.227987, -152.07095 -25.819605, -152.62712 -24.407454, -153.16466 -22.991846, -153.68431 -21.572897, -154.1876 -20.151018, -154.67496 -18.7262, -155.14755 -17.298807, -155.60593 -15.868964, -156.05089 -14.436843, -156.48311 -13.002554, -156.9033 -11.566382, -157.31155 -10.1283455, -157.709 -8.68863, -158.09573 -7.2473993, -158.47227 -5.8046412, -158.83934 -4.3606687, -159.19698 -2.9155498, -159.54555 -1.4693215, -159.8855 -0.022132674, -160.21715 1.426021, -160.54066 2.8748736, -160.85643 4.324457, -161.16446 5.7746267, -161.46516 7.225311, -161.7589 8.676456, -162.04529 10.127999, -162.32512 11.579775, -162.59814 13.031761, -162.86435 14.483994, -163.1242 15.936228, -163.37779 17.388494, -163.62468 18.840834, -163.8655 20.29292, -164.0999 21.744953, -164.32803 23.196735, -164.54971 24.648327, -164.76517 26.099632, -164.97394 27.550524, -165.17628 29.001064, -165.37201 30.451176, -165.56099 31.900833, -165.74303 33.34994, -165.91757 34.79851, -166.0849 36.24653, -166.24461 37.69387, -166.39575 39.14071, -166.53859 40.58668, -166.67245 42.032, -166.79681 43.476604, -166.91103 44.92043, -167.01453 46.36345, -167.10605 47.805626, -167.18509 49.24688, -167.25017 50.687256, -167.30025 52.12668, -167.33395 53.565083, -167.34895 55.002434, -167.34355 56.43868, -167.31538 57.873802, -167.26122 59.307606, -167.17757 60.740005, -167.06042 62.17104, -166.90416 63.600426, -166.70282 65.02797, -166.4478 66.453514, -166.13007 67.876755, -165.736 69.29731, -165.25058 70.71475, -164.65117 72.12834, -163.91008 73.5373, -162.9869 74.9404, -161.82907 76.33596, -160.35593 77.7214, -158.45456 79.093254, -155.94714 80.44569, -152.5481 81.76902, -147.79276 83.04698, -140.87978 84.24924, -130.47337 85.31732, -114.75465 86.13817, -93.210396 86.53137, -70.28859 86.35627, -52.111206 85.68094, -39.816265 84.69307, -31.714396 83.53428, -26.224075 82.28098, -22.357887 80.972466, -19.538637 79.62938, -17.422136 78.263565, -15.796961 76.88183, -14.525395 75.48877, -13.51709 74.08725, -12.709658 72.6791, -12.058041 71.26573, -11.530527 69.84825, -11.103324 68.42722, -10.757891 67.00321, -10.480039 65.57669, -10.259367 64.14798, -10.086856 62.717354, -10.076881 62.621876, -9.898351 62.613148, -6.3701777 62.39382, -1.2486025 61.91999, 1.9023303 61.542458, 4.685423 61.16102, 6.6808248 60.863976, 8.640442 60.556355, 10.167176 60.30742, 11.771366 60.038166, 13.096925 59.810158, 14.44379 59.57355, 14.56521 59.55198, 15.840309 59.323048, 17.322708 59.051373, 18.674467 58.798332, 20.328392 58.481285, 21.921867 58.166897, 23.996696 57.741226, 26.146374 57.275333, 29.21735 56.552467, 32.832726 55.590607, 35.595528 54.756752, 35.595528 54.756752))")
        expected = wkt.loads("MULTIPOLYGON (((-180 90, 180 90, 180 -26.219682718566673, 179.91692 -25.615683, 179.71045 -24.164448, 179.49733 -22.712708, 179.27744 -21.260487, 179.0507 -19.80799, 178.8174 -18.355146, 178.57753 -16.902042, 178.33083 -15.448771, 178.07732 -13.995426, 177.81718 -12.541862, 177.54991 -11.088513, 177.2757 -9.6351385, 176.9943 -8.182019, 176.70554 -6.7291107, 176.40955 -5.276472, 176.1058 -3.8242507, 175.79417 -2.3726044, 175.4743 -0.9215697, 175.1462 0.52879375, 174.80968 1.9784602, 174.46417 3.4272132, 174.10918 4.874893, 173.74467 6.321581, 173.3702 7.766964, 172.98534 9.211061, 172.58954 10.65362, 172.18233 12.094584, 171.763 13.533704, 171.33151 14.971169, 170.88683 16.406391, 170.42822 17.839388, 169.95508 19.269974, 169.46678 20.698153, 168.962 22.123251, 168.44008 23.545347, 167.90019 24.964298, 167.3411 26.379812, 166.76149 27.791496, 166.1602 29.199144, 165.53563 30.6023, 164.88661 32.000935, 164.21103 33.39439, 163.50737 34.78236, 162.77356 36.164482, 162.0073 37.540154, 161.20645 38.908974, 160.36835 40.270374, 159.4897 41.623466, 158.56778 42.967773, 157.59901 44.302437, 156.57962 45.626717, 155.50562 46.939545, 154.3722 48.239796, 153.17435 49.52635, 151.90651 50.797832, 150.56274 52.05265, 149.13652 53.289257, 147.6208 54.505875, 146.0074 55.70003, 144.28821 56.86957, 142.4539 58.01166, 140.49557 59.123463, 138.40262 60.20145, 136.16531 61.241955, 133.77318 62.24053, 131.21649 63.192844, 128.4863 64.093575, 125.57521 64.93728, 122.47811 65.717896, 119.19295 66.429344, 115.72262 67.06512, 112.074615 67.61878, 108.263 68.08404, 104.30818 68.455345, 100.2379 68.727745, 96.08485 68.89741, 91.88698 68.961685, 87.68465 68.91974, 83.51888 68.77223, 79.42787 68.521324, 75.44605 68.170525, 71.60204 67.72454, 67.917885 67.18894, 64.40903 66.56978, 61.08403 65.873695, 57.947166 65.106964, 54.99682 64.27598, 52.228897 63.38651, 49.636314 62.4444, 47.210064 61.454967, 44.94088 60.422703, 42.81822 59.3521, 40.83226 58.246887, 38.97297 57.110523, 37.230648 55.9462, 35.595528 54.756752, 32.832726 55.590607, 29.21735 56.552467, 26.146374 57.275333, 23.996696 57.741226, 21.921867 58.166897, 20.328392 58.481285, 18.674467 58.798332, 17.322708 59.051373, 15.840309 59.323048, 14.56521 59.55198, 14.44379 59.57355, 13.096925 59.810158, 11.771366 60.038166, 10.167176 60.30742, 8.640442 60.556355, 6.6808248 60.863976, 4.685423 61.16102, 1.9023303 61.542458, -1.2486025 61.91999, -6.3701777 62.39382, -9.898351 62.613148, -10.076881 62.621876, -10.086856 62.717354, -10.259367 64.14798, -10.480039 65.57669, -10.757891 67.00321, -11.103324 68.42722, -11.530527 69.84825, -12.058041 71.26573, -12.709658 72.6791, -13.51709 74.08725, -14.525395 75.48877, -15.796961 76.88183, -17.422136 78.263565, -19.538637 79.62938, -22.357887 80.972466, -26.224075 82.28098, -31.714396 83.53428, -39.816265 84.69307, -52.111206 85.68094, -70.28859 86.35627, -93.210396 86.53137, -114.75465 86.13817, -130.47337 85.31732, -140.87978 84.24924, -147.79276 83.04698, -152.5481 81.76902, -155.94714 80.44569, -158.45456 79.093254, -160.35593 77.7214, -161.82907 76.33596, -162.9869 74.9404, -163.91008 73.5373, -164.65117 72.12834, -165.25058 70.71475, -165.736 69.29731, -166.13007 67.876755, -166.4478 66.453514, -166.70282 65.02797, -166.90416 63.600426, -167.06042 62.17104, -167.17757 60.740005, -167.26122 59.307606, -167.31538 57.873802, -167.34355 56.43868, -167.34895 55.002434, -167.33395 53.565083, -167.30025 52.12668, -167.25017 50.687256, -167.18509 49.24688, -167.10605 47.805626, -167.01453 46.36345, -166.91103 44.92043, -166.79681 43.476604, -166.67245 42.032, -166.53859 40.58668, -166.39575 39.14071, -166.24461 37.69387, -166.0849 36.24653, -165.91757 34.79851, -165.74303 33.34994, -165.56099 31.900833, -165.37201 30.451176, -165.17628 29.001064, -164.97394 27.550524, -164.76517 26.099632, -164.54971 24.648327, -164.32803 23.196735, -164.0999 21.744953, -163.8655 20.29292, -163.62468 18.840834, -163.37779 17.388494, -163.1242 15.936228, -162.86435 14.483994, -162.59814 13.031761, -162.32512 11.579775, -162.04529 10.127999, -161.7589 8.676456, -161.46516 7.225311, -161.16446 5.7746267, -160.85643 4.324457, -160.54066 2.8748736, -160.21715 1.426021, -159.8855 -0.022132674, -159.54555 -1.4693215, -159.19698 -2.9155498, -158.83934 -4.3606687, -158.47227 -5.8046412, -158.09573 -7.2473993, -157.709 -8.68863, -157.31155 -10.1283455, -156.9033 -11.566382, -156.48311 -13.002554, -156.05089 -14.436843, -155.60593 -15.868964, -155.14755 -17.298807, -154.67496 -18.7262, -154.1876 -20.151018, -153.68431 -21.572897, -153.16466 -22.991846, -152.62712 -24.407454, -152.07095 -25.819605, -151.49512 -27.227987, -150.89806 -28.632252, -150.27855 -30.032259, -149.63538 -31.4276, -148.96654 -32.817795, -148.27026 -34.202606, -147.54518 -35.581703, -146.78862 -36.954426, -145.99864 -38.320374, -145.17256 -39.678913, -144.30768 -41.029488, -143.40146 -42.37159, -142.44995 -43.70421, -141.45004 -45.02664, -140.39755 -46.337975, -139.28809 -47.637165, -138.11699 -48.92313, -136.8791 -50.194614, -135.56882 -51.450073, -134.17982 -52.688053, -132.70544 -53.906807, -131.1378 -55.104145, -129.46979 -56.278065, -127.692245 -57.425865, -125.796425 -58.54483, -123.7726 -59.6317, -121.61082 -60.68292, -119.301895 -61.695004, -116.83514 -62.662838, -114.202095 -63.582268, -111.3949 -64.44792, -108.40666 -65.25391, -105.23501 -65.99461, -101.87992 -66.66364, -98.34641 -67.25476, -94.64508 -67.76162, -90.79302 -68.178955, -86.81283 -68.50076, -82.73444 -68.72322, -78.5924 -68.843254, -79.67728 -70.729744, -81.17525 -72.89574, -82.639694 -74.67346, -83.77711 -75.89042, -84.966866 -77.04764, -85.94574 -77.92664, -87.02828 -78.83113, -87.97148 -79.56483, -89.07934 -80.36378, -90.10842 -81.04621, -90.21072 -81.11096, -91.40472 -81.82634, -92.70713 -82.52511, -94.51047 -83.36311, -96.552086 -84.15173, -99.896164 -85.14788, -104.74276 -86.13558, -116.9236 -87.42685, -153.30655 -88.49546, -180 -88.14685513750015, -180 -69.17239368605101, -179.81323 -68.686424, -179.36832 -67.27623, -179.00287 -65.862724, -178.70311 -64.44611, -178.46011 -63.027008, -178.26524 -61.605495, -178.11176 -60.18192, -177.99428 -58.75635, -177.9088 -57.32897, -177.85109 -55.899937, -177.818 -54.469315, -177.80748 -53.03724, -177.81677 -51.60373, -177.84396 -50.16885, -177.8875 -48.732697, -177.94627 -47.29532, -178.01868 -45.856716, -178.10374 -44.41695, -178.20058 -42.976128, -178.3089 -41.53424, -178.42746 -40.091362, -178.5556 -38.647476, -178.69287 -37.202663, -178.83928 -35.756992, -178.99403 -34.31039, -179.15688 -32.863056, -179.32748 -31.414967, -179.50565 -29.966072, -179.69084 -28.516548, -179.88353 -27.066431, -180 -26.219682718566673, -180 90)), ((180 -88.14685513750015, 129.64954 -87.4893, 116.26059 -86.03657, 115.80803 -85.953026, 117.1074 -85.93262, 134.46266 -85.39409, 147.2112 -84.52608, 156.08195 -83.458176, 162.28969 -82.272736, 166.74629 -81.01603, 170.03717 -79.713936, 172.53185 -78.38161, 174.46321 -77.02811, 175.98602 -75.65941, 177.20335 -74.27921, 178.1871 -72.890236, 178.98912 -71.494316, 179.6463 -70.09271, 180 -69.17239368605101, 180 -88.14685513750015)))")
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(geometry)
        print(reworked)
        self.assertTrue(geometry_compare(reworked, expected, 0.0),
                        "Reworked geometry is not equivalent to the expected")

    def test_error_13_01_2025_extracted_167(self):
        geometry = wkt.loads("POLYGON ((105.74557 66.254135, 109.00099 65.52762, 112.59142 64.61104, 115.43313 63.74599, 118.096756 62.825893, 120.59032 61.856216, 122.92317 60.842052, 125.10519 59.78767, 127.146545 58.697098, 129.05759 57.574127, 130.84796 56.421906, 132.52689 55.243336, 134.10352 54.04113, 135.58536 52.81722, 136.98056 51.57413, 138.29568 50.313217, 139.53723 49.036373, 140.71092 47.744907, 141.82233 46.440224, 142.87608 45.12344, 143.8766 43.795452, 144.82791 42.457363, 145.73392 41.110027, 146.59766 39.75401, 147.42244 38.390232, 148.21053 37.01904, 148.96497 35.64115, 149.68779 34.25703, 150.38129 32.867153, 151.04733 31.472034, 151.68758 30.071924, 152.30376 28.667192, 152.8975 27.25832, 153.46976 25.845346, 154.0221 24.4287, 154.55571 23.008783, 155.07138 21.585634, 155.5706 20.159569, 156.05367 18.730711, 156.52179 17.299358, 156.97545 15.865599, 157.41576 14.429719, 157.84322 12.991862, 158.25835 11.552102, 158.66176 10.110686, 159.05386 8.667624, 159.4354 7.223157, 159.80661 5.7774687, 160.1678 4.3304806, 160.5197 2.8824794, 160.86241 1.4334992, 161.19638 -0.01628945, 161.52174 -1.4668884, 161.83891 -2.9181278, 162.14793 -4.369978, 162.4493 -5.8221884, 162.7431 -7.2748823, 163.02968 -8.7278, 163.30882 -10.180975, 163.5809 -11.634278, 163.84608 -13.087646, 164.1042 -14.541095, 164.3555 -15.994454, 164.60023 -17.447609, 164.83823 -18.900581, 165.06987 -20.353146, 165.29451 -21.805595, 165.51244 -23.257618, 165.7237 -24.70919, 165.92812 -26.160275, 166.12553 -27.610806, 166.31615 -29.06066, 166.49948 -30.51001, 166.67546 -31.958588, 166.84367 -33.4065, 167.0042 -34.853577, 167.15663 -36.2998, 167.30038 -37.745205, 167.43536 -39.18965, 167.56071 -40.633205, 167.67635 -42.075855, 167.78143 -43.517303, 167.87505 -44.957813, 167.95633 -46.397198, 168.02504 -47.83538, 168.07909 -49.272404, 168.118 -50.70814, 168.13991 -52.14263, 168.14319 -53.575726, 168.1257 -55.00735, 168.08524 -56.437477, 168.01927 -57.866077, 167.92372 -59.292915, 167.79517 -60.717865, 167.62914 -62.14089, 167.41957 -63.56169, 167.15837 -64.98005, 166.83841 -66.39575, 166.44777 -67.80837, 165.97253 -69.21742, 165.39435 -70.62226, 164.6915 -72.02228, 163.83116 -73.41615, 162.77194 -74.80254, 161.45717 -76.17928, 159.80331 -77.543434, 157.6904 -78.89058, 154.94016 -80.213806, 151.27742 -81.50235, 146.26201 -82.73779, 139.19296 -83.88814, 129.0147 -84.895744, 114.509254 -85.660095, 95.613945 -86.03849, 75.44 -85.92198, 58.40321 -85.34745, 46.01727 -84.45585, 37.423153 -83.37386, 31.408236 -82.179955, 27.082176 -80.91824, 23.882092 -79.61331, 21.452692 -78.27942, 19.569103 -76.92543, 18.082212 -75.55688, 16.893393 -74.17738, 16.387003 -73.484436, 16.091139 -73.51392, 10.52718 -73.97524, 1.0409191 -74.3848, -5.0020194 -74.40936, -10.356827 -74.270966, -14.143765 -74.07332, -17.773182 -73.796524, -20.513874 -73.523705, -23.292042 -73.1838, -25.498487 -72.86281, -27.650528 -72.50075, -27.839903 -72.46638, -29.781057 -72.08865, -31.926468 -71.61225, -33.777134 -71.14468, -35.905495 -70.53226, -37.819164 -69.90321, -40.122948 -69.03172, -42.30811 -68.071915, -45.126965 -66.60981, -48.077286 -64.76126, -50.306465 -63.11076, -53.022873 -64.0035, -55.916775 -64.83967, -58.993168 -65.61357, -62.252872 -66.31915, -65.69404 -66.95029, -69.30899 -67.50034, -73.084045 -67.963455, -76.99957 -68.334335, -81.02909 -68.60787, -85.1405 -68.78019, -89.297424 -68.84898, -93.46067 -68.81348, -97.59104 -68.67376, -101.650764 -68.43214, -105.60626 -68.09183, -109.42938 -67.65737, -113.097855 -67.13395, -116.59662 -66.52778, -119.91555 -65.84479, -123.05122 -65.09155, -126.003746 -64.27404, -128.77664 -63.397907, -131.37704 -62.469223, -133.81264 -61.49279, -136.0927 -60.473328, -138.2274 -59.41529, -140.226 -58.322166, -142.09874 -57.197792, -143.85518 -56.045124, -145.50377 -54.86679, -147.05293 -53.66532, -148.51103 -52.44305, -149.88501 -51.2018, -151.18166 -49.943356, -152.40663 -48.669186, -153.56595 -47.380795, -154.66443 -46.079216, -155.70718 -44.76593, -156.698 -43.441574, -157.64117 -42.10724, -158.53972 -40.763634, -159.39737 -39.411564, -160.21649 -38.051647, -161.00032 -36.684456, -161.75107 -35.310547, -162.47098 -33.930523, -163.16225 -32.544712, -163.82642 -31.1535, -164.46535 -29.757374, -165.08072 -28.356602, -165.67412 -26.951567, -166.24658 -25.54258, -166.79933 -24.1298, -167.33362 -22.713535, -167.85051 -21.294117, -168.35103 -19.87168, -168.83595 -18.446459, -169.30595 -17.018635, -169.76212 -15.588327, -170.20496 -14.155889, -170.63516 -12.721281, -171.05324 -11.284764, -171.45992 -9.846537, -171.85536 -8.40653, -172.24065 -6.9650407, -172.61551 -5.5221357, -172.98112 -4.078021, -173.3372 -2.6326625, -173.68456 -1.1863033, -174.02312 0.26105678, -174.35352 1.7092742, -174.67584 3.1582577, -174.99043 4.607855, -175.2975 6.058112, -175.59712 7.5088553, -175.88965 8.960021, -176.17525 10.411494, -176.45401 11.863294, -176.72597 13.315283, -176.99144 14.767451, -177.25037 16.21965, -177.5029 17.671873, -177.74916 19.124037, -177.98895 20.576172, -178.2226 22.028057, -178.44965 23.479782, -178.67058 24.93127, -178.88516 26.382347, -179.09325 27.833158, -179.29471 29.283527, -179.48956 30.733498, -179.67746 32.182938, -179.85854 33.631966, 179.96765 35.080334, 179.80139 36.528152, 179.6429 37.97532, 179.49254 39.421864, 179.351 40.86767, 179.21829 42.312794, 179.09512 43.75718, 178.98236 45.200775, 178.88039 46.64356, 178.79065 48.08549, 178.7137 49.526505, 178.6506 50.966618, 178.60269 52.40578, 178.5717 53.84393, 178.5594 55.28103, 178.56784 56.716976, 178.60002 58.151714, 178.6583 59.585228, 178.74675 61.017357, 178.86963 62.448055, 179.0326 63.87702, 179.242 65.30415, 179.50601 66.729324, 179.83536 68.15205, -179.75676 69.57204, -179.25371 70.98879, -178.6322 72.40166, -177.86296 73.80962, -176.90376 75.21151, -175.71512 76.59335, -174.60269 77.74566, -173.72314 78.434265, -174.09918 78.46921, 177.97311 79.05627, 165.00467 79.49289, 156.54063 79.466324, 149.11119 79.23249, 143.98003 78.93907, 139.20581 78.54958, 135.7142 78.179, 132.28746 77.72969, 129.65262 77.314964, 127.16014 76.85606, 126.94455 76.81292, 124.77004 76.34314, 122.44261 75.76053, 120.499626 75.19773, 118.339424 74.47172, 116.46455 73.73669, 114.290184 72.73223, 112.30748 71.6398, 109.85455 69.99389, 107.39563 67.92929, 105.74557 66.254135, 105.74557 66.254135))")
        expected = wkt.loads("MULTIPOLYGON (((180 -90, -180 -90, -180 34.810759724641684, -179.85854 33.631966, -179.67746 32.182938, -179.48956 30.733498, -179.29471 29.283527, -179.09325 27.833158, -178.88516 26.382347, -178.67058 24.93127, -178.44965 23.479782, -178.2226 22.028057, -177.98895 20.576172, -177.74916 19.124037, -177.5029 17.671873, -177.25037 16.21965, -176.99144 14.767451, -176.72597 13.315283, -176.45401 11.863294, -176.17525 10.411494, -175.88965 8.960021, -175.59712 7.5088553, -175.2975 6.058112, -174.99043 4.607855, -174.67584 3.1582577, -174.35352 1.7092742, -174.02312 0.26105678, -173.68456 -1.1863033, -173.3372 -2.6326625, -172.98112 -4.078021, -172.61551 -5.5221357, -172.24065 -6.9650407, -171.85536 -8.40653, -171.45992 -9.846537, -171.05324 -11.284764, -170.63516 -12.721281, -170.20496 -14.155889, -169.76212 -15.588327, -169.30595 -17.018635, -168.83595 -18.446459, -168.35103 -19.87168, -167.85051 -21.294117, -167.33362 -22.713535, -166.79933 -24.1298, -166.24658 -25.54258, -165.67412 -26.951567, -165.08072 -28.356602, -164.46535 -29.757374, -163.82642 -31.1535, -163.16225 -32.544712, -162.47098 -33.930523, -161.75107 -35.310547, -161.00032 -36.684456, -160.21649 -38.051647, -159.39737 -39.411564, -158.53972 -40.763634, -157.64117 -42.10724, -156.698 -43.441574, -155.70718 -44.76593, -154.66443 -46.079216, -153.56595 -47.380795, -152.40663 -48.669186, -151.18166 -49.943356, -149.88501 -51.2018, -148.51103 -52.44305, -147.05293 -53.66532, -145.50377 -54.86679, -143.85518 -56.045124, -142.09874 -57.197792, -140.226 -58.322166, -138.2274 -59.41529, -136.0927 -60.473328, -133.81264 -61.49279, -131.37704 -62.469223, -128.77664 -63.397907, -126.003746 -64.27404, -123.05122 -65.09155, -119.91555 -65.84479, -116.59662 -66.52778, -113.097855 -67.13395, -109.42938 -67.65737, -105.60626 -68.09183, -101.650764 -68.43214, -97.59104 -68.67376, -93.46067 -68.81348, -89.297424 -68.84898, -85.1405 -68.78019, -81.02909 -68.60787, -76.99957 -68.334335, -73.084045 -67.963455, -69.30899 -67.50034, -65.69404 -66.95029, -62.252872 -66.31915, -58.993168 -65.61357, -55.916775 -64.83967, -53.022873 -64.0035, -50.306465 -63.11076, -48.077286 -64.76126, -45.126965 -66.60981, -42.30811 -68.071915, -40.122948 -69.03172, -37.819164 -69.90321, -35.905495 -70.53226, -33.777134 -71.14468, -31.926468 -71.61225, -29.781057 -72.08865, -27.839903 -72.46638, -27.650528 -72.50075, -25.498487 -72.86281, -23.292042 -73.1838, -20.513874 -73.523705, -17.773182 -73.796524, -14.143765 -74.07332, -10.356827 -74.270966, -5.0020194 -74.40936, 1.0409191 -74.3848, 10.52718 -73.97524, 16.091139 -73.51392, 16.387003 -73.484436, 16.893393 -74.17738, 18.082212 -75.55688, 19.569103 -76.92543, 21.452692 -78.27942, 23.882092 -79.61331, 27.082176 -80.91824, 31.408236 -82.179955, 37.423153 -83.37386, 46.01727 -84.45585, 58.40321 -85.34745, 75.44 -85.92198, 95.613945 -86.03849, 114.509254 -85.660095, 129.0147 -84.895744, 139.19296 -83.88814, 146.26201 -82.73779, 151.27742 -81.50235, 154.94016 -80.213806, 157.6904 -78.89058, 159.80331 -77.543434, 161.45717 -76.17928, 162.77194 -74.80254, 163.83116 -73.41615, 164.6915 -72.02228, 165.39435 -70.62226, 165.97253 -69.21742, 166.44777 -67.80837, 166.83841 -66.39575, 167.15837 -64.98005, 167.41957 -63.56169, 167.62914 -62.14089, 167.79517 -60.717865, 167.92372 -59.292915, 168.01927 -57.866077, 168.08524 -56.437477, 168.1257 -55.00735, 168.14319 -53.575726, 168.13991 -52.14263, 168.118 -50.70814, 168.07909 -49.272404, 168.02504 -47.83538, 167.95633 -46.397198, 167.87505 -44.957813, 167.78143 -43.517303, 167.67635 -42.075855, 167.56071 -40.633205, 167.43536 -39.18965, 167.30038 -37.745205, 167.15663 -36.2998, 167.0042 -34.853577, 166.84367 -33.4065, 166.67546 -31.958588, 166.49948 -30.51001, 166.31615 -29.06066, 166.12553 -27.610806, 165.92812 -26.160275, 165.7237 -24.70919, 165.51244 -23.257618, 165.29451 -21.805595, 165.06987 -20.353146, 164.83823 -18.900581, 164.60023 -17.447609, 164.3555 -15.994454, 164.1042 -14.541095, 163.84608 -13.087646, 163.5809 -11.634278, 163.30882 -10.180975, 163.02968 -8.7278, 162.7431 -7.2748823, 162.4493 -5.8221884, 162.14793 -4.369978, 161.83891 -2.9181278, 161.52174 -1.4668884, 161.19638 -0.01628945, 160.86241 1.4334992, 160.5197 2.8824794, 160.1678 4.3304806, 159.80661 5.7774687, 159.4354 7.223157, 159.05386 8.667624, 158.66176 10.110686, 158.25835 11.552102, 157.84322 12.991862, 157.41576 14.429719, 156.97545 15.865599, 156.52179 17.299358, 156.05367 18.730711, 155.5706 20.159569, 155.07138 21.585634, 154.55571 23.008783, 154.0221 24.4287, 153.46976 25.845346, 152.8975 27.25832, 152.30376 28.667192, 151.68758 30.071924, 151.04733 31.472034, 150.38129 32.867153, 149.68779 34.25703, 148.96497 35.64115, 148.21053 37.01904, 147.42244 38.390232, 146.59766 39.75401, 145.73392 41.110027, 144.82791 42.457363, 143.8766 43.795452, 142.87608 45.12344, 141.82233 46.440224, 140.71092 47.744907, 139.53723 49.036373, 138.29568 50.313217, 136.98056 51.57413, 135.58536 52.81722, 134.10352 54.04113, 132.52689 55.243336, 130.84796 56.421906, 129.05759 57.574127, 127.146545 58.697098, 125.10519 59.78767, 122.92317 60.842052, 120.59032 61.856216, 118.096756 62.825893, 115.43313 63.74599, 112.59142 64.61104, 109.00099 65.52762, 105.74557 66.254135, 107.39563 67.92929, 109.85455 69.99389, 112.30748 71.6398, 114.290184 72.73223, 116.46455 73.73669, 118.339424 74.47172, 120.499626 75.19773, 122.44261 75.76053, 124.77004 76.34314, 126.94455 76.81292, 127.16014 76.85606, 129.65262 77.314964, 132.28746 77.72969, 135.7142 78.179, 139.20581 78.54958, 143.98003 78.93907, 149.11119 79.23249, 156.54063 79.466324, 165.00467 79.49289, 177.97311 79.05627, 180 78.90617545272215, 180 68.72522631067955, 179.83536 68.15205, 179.50601 66.729324, 179.242 65.30415, 179.0326 63.87702, 178.86963 62.448055, 178.74675 61.017357, 178.6583 59.585228, 178.60002 58.151714, 178.56784 56.716976, 178.5594 55.28103, 178.5717 53.84393, 178.60269 52.40578, 178.6506 50.966618, 178.7137 49.526505, 178.79065 48.08549, 178.88039 46.64356, 178.98236 45.200775, 179.09512 43.75718, 179.21829 42.312794, 179.351 40.86767, 179.49254 39.421864, 179.6429 37.97532, 179.80139 36.528152, 179.96765 35.080334, 180 34.810759724641684, 180 -90)), ((-180 78.90617545272215, -174.09918 78.46921, -173.72314 78.434265, -174.60269 77.74566, -175.71512 76.59335, -176.90376 75.21151, -177.86296 73.80962, -178.6322 72.40166, -179.25371 70.98879, -179.75676 69.57204, -180 68.72522631067955, -180 78.90617545272215)))")
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(geometry)
        print(reworked)
        self.assertTrue(geometry_compare(reworked, expected, 0.0),
                        "Reworked geometry is not equivalent to the expected")

    def test_error_13_01_2025_extracted_152(self):
        geometry = wkt.loads("POLYGON ((67.611946 67.620964, 69.55126 67.63703, 74.102264 68.14614, 79.24173 68.5702, 84.54143 68.82732, 89.92418 68.91143, 95.30511 68.82053, 100.599785 68.5567, 105.73135 68.12645, 110.63774 67.53919, 115.273964 66.80675, 119.61333 65.94242, 123.6448 64.959984, 127.369934 63.87251, 130.79953 62.69261, 133.95053 61.43183, 136.84285 60.100258, 139.49763 58.706726, 141.9365 57.259327, 144.18027 55.76484, 146.24821 54.22926, 148.15749 52.657223, 149.92455 51.053417, 151.56392 49.42162, 153.08812 47.764915, 154.50897 46.086155, 155.83656 44.387844, 157.07971 42.671867, 158.24681 40.940357, 159.34459 39.194645, 160.37952 37.436264, 161.35732 35.666515, 162.28279 33.88638, 163.16052 32.096977, 163.99423 30.298933, 164.78781 28.493303, 165.54417 26.680645, 166.26624 24.86156, 166.95653 23.03669, 167.61723 21.206472, 168.25095 19.371626, 168.85876 17.532246, 169.44308 15.689066, 170.00496 13.842198, 170.54572 11.992046, 171.06705 10.139046, 171.56969 8.283398, 172.05473 6.4253807, 172.5231 4.5653176, 172.97563 2.703328, 173.41325 0.8398602, 173.83638 -1.0250238, 174.24568 -2.8910284, 174.64171 -4.7580853, 175.02501 -6.625802, 175.3959 -8.49417, 175.75455 -10.362971, 176.10158 -12.231959, 176.43723 -14.101047, 176.76122 -15.97011, 177.0742 -17.838964, 177.37613 -19.707424, 177.6669 -21.57542, 177.94643 -23.442871, 178.21501 -25.309486, 178.47198 -27.175322, 178.71727 -29.040207, 178.9507 -30.903973, 179.17152 -32.76669, 179.3794 -34.628113, 179.57405 -36.488113, 179.75401 -38.346764, 179.91888 -40.203857, -179.93239 -42.0593, -179.80164 -43.913048, -179.69028 -45.765015, -179.59972 -47.615005, -179.53285 -49.463036, -179.49208 -51.308964, -179.48085 -53.15262, -179.50325 -54.99391, -179.56421 -56.83267, -179.66959 -58.66859, -179.82741 -60.5015, 179.95255 -62.331112, 179.6578 -64.15693, 179.27176 -65.97848, 178.7736 -67.794945, 178.13342 -69.605385, 177.31218 -71.40838, 176.25133 -73.20199, 174.86954 -74.98315, 173.04066 -76.74734, 170.56767 -78.48728, 167.12549 -80.19033, 162.15256 -81.834175, 154.64195 -83.37502, 144.7279 -84.55932, 147.87727 -84.76315, 176.63318 -85.613716, -154.86484 -85.24839, -142.12057 -84.63063, -131.57169 -83.75412, -126.27637 -83.12481, -121.103424 -82.338776, -118.09298 -81.784004, -114.79927 -81.07807, -112.694145 -80.564865, -110.21112 -79.88916, -108.51638 -79.37989, -106.39901 -78.68369, -104.87405 -78.13797, -102.86966 -77.35974, -101.35278 -76.721, -99.25899 -75.76059, -97.59446 -74.92247, -95.17511 -73.56066, -93.139626 -72.24896, -89.954926 -69.77536, -88.70899 -68.61981, -93.82531 -68.17936, -98.71342 -67.58363, -103.329346 -66.84457, -107.64777 -65.97522, -111.65883 -64.98935, -115.36498 -63.90002, -118.77718 -62.719467, -121.91246 -61.459023, -124.79088 -60.12859, -127.433846 -58.73712, -129.8629 -57.29244, -132.09856 -55.801224, -134.15909 -54.268982, -136.06317 -52.700985, -137.826 -51.101414, -139.4622 -49.47397, -140.98438 -47.82187, -142.40369 -46.14774, -143.7305 -44.45406, -144.97392 -42.74294, -146.1417 -41.01621, -147.2405 -39.275246, -148.27737 -37.521683, -149.25725 -35.75662, -150.18544 -33.981266, -151.06596 -32.196404, -151.90314 -30.403013, -152.70035 -28.60187, -153.46068 -26.79358, -154.18709 -24.978943, -154.88208 -23.158375, -155.54778 -21.332386, -156.18658 -19.501566, -156.8001 -17.66624, -157.39008 -15.826865, -157.95796 -13.983808, -158.50531 -12.137402, -159.03322 -10.287876, -159.5429 -8.435685, -160.03542 -6.5810122, -160.51154 -4.724098, -160.97221 -2.8652656, -161.41823 -1.0046209, -161.85027 0.85744154, -162.26892 2.720867, -162.67479 4.585449, -163.06828 6.450932, -163.44998 8.317161, -163.81992 10.184044, -164.17899 12.051425, -164.52705 13.919017, -164.86444 15.786825, -165.19142 17.654627, -165.50798 19.52236, -165.81438 21.389902, -166.1106 23.25707, -166.39641 25.123867, -166.6719 26.990112, -166.93706 28.85577, -167.19136 30.72072, -167.43478 32.584854, -167.66664 34.44814, -167.88675 36.310474, -168.09453 38.171818, -168.28879 40.032066, -168.46935 41.891205, -168.63454 43.74917, -168.78322 45.605835, -168.91405 47.461185, -169.02513 49.31514, -169.11421 51.16768, -169.17836 53.018658, -169.21436 54.868008, -169.21837 56.71562, -169.1848 58.561344, -169.10767 60.40507, -168.97876 62.246506, -168.78714 64.085464, -168.51987 65.92153, -168.15805 67.75424, -167.6778 69.58287, -167.04463 71.406525, -166.20952 73.223724, -165.10138 75.032486, -163.60982 76.82945, -161.55782 78.60936, -158.64719 80.36306, -154.33542 82.073204, -147.57275 83.70465, -136.22194 85.17693, -116.46326 86.29537, -86.87543 86.68074, -58.85632 86.10838, -41.199852 84.89047, -31.061022 83.37371, -24.301153 81.37524, -19.707224 78.885216, -18.071928 78.95246, -5.9031534 79.17343, 5.3210716 78.968895, 11.434472 78.69203, 17.71754 78.278366, 21.50251 77.96226, 25.734262 77.54574, 28.478449 77.238235, 31.74248 76.83192, 33.979298 76.52661, 36.772896 76.112686, 38.77653 75.79223, 41.388664 75.34304, 43.342735 74.98245, 45.99992 74.456, 48.075264 74.013565, 51.02843 73.33114, 53.44927 72.718864, 57.087612 71.69066, 60.266293 70.66141, 65.48132 68.619194, 67.611946 67.620964, 67.611946 67.620964))")
        expected = wkt.loads('MULTIPOLYGON (((-180 90, 180 90, 180 -41.21584877139776, 179.91888 -40.203857, 179.75401 -38.346764, 179.57405 -36.488113, 179.3794 -34.628113, 179.17152 -32.76669, 178.9507 -30.903973, 178.71727 -29.040207, 178.47198 -27.175322, 178.21501 -25.309486, 177.94643 -23.442871, 177.6669 -21.57542, 177.37613 -19.707424, 177.0742 -17.838964, 176.76122 -15.97011, 176.43723 -14.101047, 176.10158 -12.231959, 175.75455 -10.362971, 175.3959 -8.49417, 175.02501 -6.625802, 174.64171 -4.7580853, 174.24568 -2.8910284, 173.83638 -1.0250238, 173.41325 0.8398602, 172.97563 2.703328, 172.5231 4.5653176, 172.05473 6.4253807, 171.56969 8.283398, 171.06705 10.139046, 170.54572 11.992046, 170.00496 13.842198, 169.44308 15.689066, 168.85876 17.532246, 168.25095 19.371626, 167.61723 21.206472, 166.95653 23.03669, 166.26624 24.86156, 165.54417 26.680645, 164.78781 28.493303, 163.99423 30.298933, 163.16052 32.096977, 162.28279 33.88638, 161.35732 35.666515, 160.37952 37.436264, 159.34459 39.194645, 158.24681 40.940357, 157.07971 42.671867, 155.83656 44.387844, 154.50897 46.086155, 153.08812 47.764915, 151.56392 49.42162, 149.92455 51.053417, 148.15749 52.657223, 146.24821 54.22926, 144.18027 55.76484, 141.9365 57.259327, 139.49763 58.706726, 136.84285 60.100258, 133.95053 61.43183, 130.79953 62.69261, 127.369934 63.87251, 123.6448 64.959984, 119.61333 65.94242, 115.273964 66.80675, 110.63774 67.53919, 105.73135 68.12645, 100.599785 68.5567, 95.30511 68.82053, 89.92418 68.91143, 84.54143 68.82732, 79.24173 68.5702, 74.102264 68.14614, 69.55126 67.63703, 67.611946 67.620964, 65.48132 68.619194, 60.266293 70.66141, 57.087612 71.69066, 53.44927 72.718864, 51.02843 73.33114, 48.075264 74.013565, 45.99992 74.456, 43.342735 74.98245, 41.388664 75.34304, 38.77653 75.79223, 36.772896 76.112686, 33.979298 76.52661, 31.74248 76.83192, 28.478449 77.238235, 25.734262 77.54574, 21.50251 77.96226, 17.71754 78.278366, 11.434472 78.69203, 5.3210716 78.968895, -5.9031534 79.17343, -18.071928 78.95246, -19.707224 78.885216, -24.301153 81.37524, -31.061022 83.37371, -41.199852 84.89047, -58.85632 86.10838, -86.87543 86.68074, -116.46326 86.29537, -136.22194 85.17693, -147.57275 83.70465, -154.33542 82.073204, -158.64719 80.36306, -161.55782 78.60936, -163.60982 76.82945, -165.10138 75.032486, -166.20952 73.223724, -167.04463 71.406525, -167.6778 69.58287, -168.15805 67.75424, -168.51987 65.92153, -168.78714 64.085464, -168.97876 62.246506, -169.10767 60.40507, -169.1848 58.561344, -169.21837 56.71562, -169.21436 54.868008, -169.17836 53.018658, -169.11421 51.16768, -169.02513 49.31514, -168.91405 47.461185, -168.78322 45.605835, -168.63454 43.74917, -168.46935 41.891205, -168.28879 40.032066, -168.09453 38.171818, -167.88675 36.310474, -167.66664 34.44814, -167.43478 32.584854, -167.19136 30.72072, -166.93706 28.85577, -166.6719 26.990112, -166.39641 25.123867, -166.1106 23.25707, -165.81438 21.389902, -165.50798 19.52236, -165.19142 17.654627, -164.86444 15.786825, -164.52705 13.919017, -164.17899 12.051425, -163.81992 10.184044, -163.44998 8.317161, -163.06828 6.450932, -162.67479 4.585449, -162.26892 2.720867, -161.85027 0.85744154, -161.41823 -1.0046209, -160.97221 -2.8652656, -160.51154 -4.724098, -160.03542 -6.5810122, -159.5429 -8.435685, -159.03322 -10.287876, -158.50531 -12.137402, -157.95796 -13.983808, -157.39008 -15.826865, -156.8001 -17.66624, -156.18658 -19.501566, -155.54778 -21.332386, -154.88208 -23.158375, -154.18709 -24.978943, -153.46068 -26.79358, -152.70035 -28.60187, -151.90314 -30.403013, -151.06596 -32.196404, -150.18544 -33.981266, -149.25725 -35.75662, -148.27737 -37.521683, -147.2405 -39.275246, -146.1417 -41.01621, -144.97392 -42.74294, -143.7305 -44.45406, -142.40369 -46.14774, -140.98438 -47.82187, -139.4622 -49.47397, -137.826 -51.101414, -136.06317 -52.700985, -134.15909 -54.268982, -132.09856 -55.801224, -129.8629 -57.29244, -127.433846 -58.73712, -124.79088 -60.12859, -121.91246 -61.459023, -118.77718 -62.719467, -115.36498 -63.90002, -111.65883 -64.98935, -107.64777 -65.97522, -103.329346 -66.84457, -98.71342 -67.58363, -93.82531 -68.17936, -88.70899 -68.61981, -89.954926 -69.77536, -93.139626 -72.24896, -95.17511 -73.56066, -97.59446 -74.92247, -99.25899 -75.76059, -101.35278 -76.721, -102.86966 -77.35974, -104.87405 -78.13797, -106.39901 -78.68369, -108.51638 -79.37989, -110.21112 -79.88916, -112.694145 -80.564865, -114.79927 -81.07807, -118.09298 -81.784004, -121.103424 -82.338776, -126.27637 -83.12481, -131.57169 -83.75412, -142.12057 -84.63063, -154.86484 -85.24839, -180 -85.57056156359523, -180 -61.93656969223798, -179.82741 -60.5015, -179.66959 -58.66859, -179.56421 -56.83267, -179.50325 -54.99391, -179.48085 -53.15262, -179.49208 -51.308964, -179.53285 -49.463036, -179.59972 -47.615005, -179.69028 -45.765015, -179.80164 -43.913048, -179.93239 -42.0593, -180 -41.21584877139776, -180 90)), ((180 -85.57056156359523, 176.63318 -85.613716, 147.87727 -84.76315, 144.7279 -84.55932, 154.64195 -83.37502, 162.15256 -81.834175, 167.12549 -80.19033, 170.56767 -78.48728, 173.04066 -76.74734, 174.86954 -74.98315, 176.25133 -73.20199, 177.31218 -71.40838, 178.13342 -69.605385, 178.7736 -67.794945, 179.27176 -65.97848, 179.6578 -64.15693, 179.95255 -62.331112, 180 -61.93656969223798, 180 -85.57056156359523)))')
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(geometry)
        print(reworked)
        self.assertTrue(geometry_compare(reworked, expected, 0.0),
                        "Reworked geometry is not equivalent to the expected")

    def test_error_13_01_2025_extracted_151(self):
        geometry = wkt.loads("POLYGON ((76.88914 68.64518, 78.93809 68.63362, 81.72632 68.71964, 85.88138 68.87019, 90.07393 68.915215, 94.26332 68.85433, 98.409515 68.68821, 102.47468 68.419464, 106.425644 68.05197, 110.235085 67.59041, 113.88244 67.04042, 117.3534 66.40821, 120.64011 65.700264, 123.73969 64.92285, 126.65419 64.08253, 129.3881 63.18475, 131.94855 62.235294, 134.34503 61.239372, 136.58653 60.20134, 138.6838 59.125797, 140.64645 58.01617, 142.4847 56.87607, 144.208 55.70848, 145.82529 54.51612, 147.34497 53.30132, 148.77483 52.06632, 150.12178 50.81274, 151.39287 49.54274, 152.59375 48.257507, 153.73033 46.958534, 154.80739 45.64696, 155.82924 44.32374, 156.80057 42.9901, 157.72475 41.646732, 158.60562 40.29449, 159.44589 38.93398, 160.24908 37.566113, 161.01698 36.19108, 161.75264 34.80969, 162.45813 33.422443, 163.13538 32.02966, 163.78618 30.631767, 164.41193 29.228966, 165.01479 27.82194, 165.59561 26.410728, 166.15602 24.995703, 166.69731 23.577229, 167.22034 22.155548, 167.726 20.730642, 168.21558 19.303009, 168.68976 17.872734, 169.14935 16.440023, 169.59494 15.005026, 170.02736 13.567901, 170.4475 12.129021, 170.8553 10.688119, 171.25192 9.245683, 171.6375 7.8017554, 172.01273 6.356489, 172.37784 4.909944, 172.7335 3.4622974, 173.07948 2.0135546, 173.41663 0.56390923, 173.74538 -0.8864741, 174.06554 -2.337641, 174.37749 -3.7894127, 174.68173 -5.2416587, 174.97821 -6.6943426, 175.26718 -8.147412, 175.54883 -9.60076, 175.82327 -11.054236, 176.09068 -12.507865, 176.35124 -13.96155, 176.60478 -15.415192, 176.85168 -16.868736, 177.09175 -18.322088, 177.32498 -19.775291, 177.5518 -21.228035, 177.77177 -22.68051, 177.9848 -24.1326, 178.19112 -25.584208, 178.39056 -27.035255, 178.58292 -28.485806, 178.76804 -29.935709, 178.94603 -31.384838, 179.1161 -32.833435, 179.27853 -34.281147, 179.43265 -35.728107, 179.5784 -37.1742, 179.71545 -38.61937, 179.84296 -40.06363, 179.96086 -41.506897, -179.93198 -42.94918, -179.83582 -44.390366, -179.7515 -45.830444, -179.68013 -47.269405, -179.62254 -48.707058, -179.5806 -50.143642, -179.55447 -51.578777, -179.54697 -53.012566, -179.55954 -54.44495, -179.59421 -55.875835, -179.65408 -57.305054, -179.74231 -58.73263, -179.86182 -60.15833, 179.982 -61.582058, 179.78395 -63.003635, 179.5375 -64.42278, 179.2341 -65.83929, 178.86432 -67.25281, 178.41437 -68.6628, 177.86842 -70.06891, 177.20549 -71.47018, 176.3964 -72.865715, 175.40492 -74.254166, 174.17879 -75.63367, 172.64624 -77.00155, 170.7032 -78.3539, 168.19714 -79.68494, 164.89444 -80.98532, 160.43106 -82.24005, 154.22266 -83.422844, 145.37703 -84.48782, 132.7121 -85.35355, 115.52265 -85.89217, 105.64115 -85.99406, 106.93918 -86.34042, 134.5757 -88.62898, -123.13585 -88.452, -106.50273 -87.31666, -99.325836 -86.00093, -96.62457 -85.15335, -94.26903 -84.15463, -92.96539 -83.47568, -91.55787 -82.63291, -90.655045 -82.03146, -89.57531 -81.2506, -88.82377 -80.66877, -87.862335 -79.88084, -87.15132 -79.26823, -86.189804 -78.40094, -85.44061 -77.69391, -84.376465 -76.637955, -83.50793 -75.72291, -82.21712 -74.24795, -81.11329 -72.840065, -79.373535 -70.21473, -78.69416 -68.99951, -82.87765 -68.9186, -87.0105 -68.73375, -91.055954 -68.44743, -94.98206 -68.063576, -98.76285 -67.58741, -102.37863 -67.02437, -105.81696 -66.38087, -109.07029 -65.663, -112.13739 -64.87743, -115.01989 -64.02993, -117.72392 -63.12671, -120.256355 -62.17275, -122.62628 -61.173286, -124.843925 -60.132874, -126.919205 -59.055588, -128.86221 -57.94518, -130.68225 -56.80466, -132.38947 -55.63733, -133.99194 -54.445534, -135.49886 -53.23192, -136.9169 -51.998257, -138.25401 -50.746628, -139.51608 -49.478546, -140.70915 -48.195534, -141.8389 -46.89906, -142.90991 -45.59, -143.92694 -44.26958, -144.8937 -42.938667, -145.8144 -41.598248, -146.69223 -40.248947, -147.53024 -38.891594, -148.33131 -37.52667, -149.09805 -36.15481, -149.83287 -34.776573, -150.53761 -33.39235, -151.21475 -32.002724, -151.86586 -30.607882, -152.49252 -29.208296, -153.09619 -27.804325, -153.67853 -26.396284, -154.24054 -24.984303, -154.78381 -23.568888, -155.30873 -22.150038, -155.81686 -20.728178, -156.3092 -19.303482, -156.7862 -17.876038, -157.24895 -16.446169, -157.6981 -15.0139265, -158.13432 -13.579596, -158.5581 -12.143314, -158.97032 -10.705104, -159.37134 -9.265225, -159.7616 -7.823775, -160.14157 -6.380929, -160.5119 -4.9367003, -160.8728 -3.4912984, -161.22461 -2.0448196, -161.5678 -0.5973707, -161.90257 0.85099286, -162.22931 2.3002055, -162.5481 3.7500393, -162.85938 5.200532, -163.16322 6.651596, -163.45993 8.103073, -163.74976 9.55489, -164.03265 11.007093, -164.30888 12.459461, -164.57861 13.912013, -164.8419 15.364676, -165.0987 16.817398, -165.3493 18.270048, -165.5938 19.72258, -165.83173 21.17504, -166.06374 22.627321, -166.28963 24.079334, -166.50911 25.5311, -166.72243 26.982544, -166.9294 28.433592, -167.12997 29.884232, -167.32387 31.334402, -167.51111 32.78408, -167.69142 34.233265, -167.86456 35.68189, -168.0302 37.12989, -168.18831 38.577225, -168.33803 40.02396, -168.4794 41.470016, -168.61186 42.91533, -168.73468 44.359947, -168.84729 45.803738, -168.9487 47.246746, -169.03862 48.688873, -169.11559 50.130203, -169.17836 51.57061, -169.22574 53.010063, -169.25626 54.448547, -169.26762 55.885983, -169.25818 57.322273, -169.2249 58.757504, -169.16447 60.191444, -169.07349 61.62407, -168.94751 63.055233, -168.77975 64.48471, -168.5642 65.91247, -168.29185 67.33813, -167.95148 68.7615, -167.52893 70.18207, -167.00563 71.5994, -166.35648 73.01275, -165.5487 74.42116, -164.53537 75.82322, -163.25175 77.217064, -161.59889 78.599594, -159.43214 79.96641, -156.51906 81.31017, -152.47577 82.61826, -146.64899 83.868195, -137.89146 85.015884, -124.36339 85.97286, -104.34557 86.575615, -80.160576 86.62825, -59.05918 86.10842, -44.394722 85.18761, -30.737564 83.08694, -27.671694 82.30806, -25.401226 82.419464, -7.568519 82.844345, 9.262352 82.61184, 18.03902 82.23403, 26.545952 81.66153, 31.38546 81.226364, 36.538754 80.65881, 39.739944 80.2444, 43.4114 79.70279, 45.846886 79.30015, 48.802784 78.75989, 50.867897 78.34582, 53.496426 77.771164, 55.418964 77.31437, 57.978027 76.65416, 59.935696 76.10509, 62.664005 75.26798, 64.853195 74.52661, 68.067505 73.30109, 70.8043 72.09679, 75.1573 69.76342, 76.88914 68.64518, 76.88914 68.64518))")
        expected = wkt.loads("MULTIPOLYGON (((-180 90, 180 90, 180 -42.033688308511046, 179.96086 -41.506897, 179.84296 -40.06363, 179.71545 -38.61937, 179.5784 -37.1742, 179.43265 -35.728107, 179.27853 -34.281147, 179.1161 -32.833435, 178.94603 -31.384838, 178.76804 -29.935709, 178.58292 -28.485806, 178.39056 -27.035255, 178.19112 -25.584208, 177.9848 -24.1326, 177.77177 -22.68051, 177.5518 -21.228035, 177.32498 -19.775291, 177.09175 -18.322088, 176.85168 -16.868736, 176.60478 -15.415192, 176.35124 -13.96155, 176.09068 -12.507865, 175.82327 -11.054236, 175.54883 -9.60076, 175.26718 -8.147412, 174.97821 -6.6943426, 174.68173 -5.2416587, 174.37749 -3.7894127, 174.06554 -2.337641, 173.74538 -0.8864741, 173.41663 0.56390923, 173.07948 2.0135546, 172.7335 3.4622974, 172.37784 4.909944, 172.01273 6.356489, 171.6375 7.8017554, 171.25192 9.245683, 170.8553 10.688119, 170.4475 12.129021, 170.02736 13.567901, 169.59494 15.005026, 169.14935 16.440023, 168.68976 17.872734, 168.21558 19.303009, 167.726 20.730642, 167.22034 22.155548, 166.69731 23.577229, 166.15602 24.995703, 165.59561 26.410728, 165.01479 27.82194, 164.41193 29.228966, 163.78618 30.631767, 163.13538 32.02966, 162.45813 33.422443, 161.75264 34.80969, 161.01698 36.19108, 160.24908 37.566113, 159.44589 38.93398, 158.60562 40.29449, 157.72475 41.646732, 156.80057 42.9901, 155.82924 44.32374, 154.80739 45.64696, 153.73033 46.958534, 152.59375 48.257507, 151.39287 49.54274, 150.12178 50.81274, 148.77483 52.06632, 147.34497 53.30132, 145.82529 54.51612, 144.208 55.70848, 142.4847 56.87607, 140.64645 58.01617, 138.6838 59.125797, 136.58653 60.20134, 134.34503 61.239372, 131.94855 62.235294, 129.3881 63.18475, 126.65419 64.08253, 123.73969 64.92285, 120.64011 65.700264, 117.3534 66.40821, 113.88244 67.04042, 110.235085 67.59041, 106.425644 68.05197, 102.47468 68.419464, 98.409515 68.68821, 94.26332 68.85433, 90.07393 68.915215, 85.88138 68.87019, 81.72632 68.71964, 78.93809 68.63362, 76.88914 68.64518, 75.1573 69.76342, 70.8043 72.09679, 68.067505 73.30109, 64.853195 74.52661, 62.664005 75.26798, 59.935696 76.10509, 57.978027 76.65416, 55.418964 77.31437, 53.496426 77.771164, 50.867897 78.34582, 48.802784 78.75989, 45.846886 79.30015, 43.4114 79.70279, 39.739944 80.2444, 36.538754 80.65881, 31.38546 81.226364, 26.545952 81.66153, 18.03902 82.23403, 9.262352 82.61184, -7.568519 82.844345, -25.401226 82.419464, -27.671694 82.30806, -30.737564 83.08694, -44.394722 85.18761, -59.05918 86.10842, -80.160576 86.62825, -104.34557 86.575615, -124.36339 85.97286, -137.89146 85.015884, -146.64899 83.868195, -152.47577 82.61826, -156.51906 81.31017, -159.43214 79.96641, -161.59889 78.599594, -163.25175 77.217064, -164.53537 75.82322, -165.5487 74.42116, -166.35648 73.01275, -167.00563 71.5994, -167.52893 70.18207, -167.95148 68.7615, -168.29185 67.33813, -168.5642 65.91247, -168.77975 64.48471, -168.94751 63.055233, -169.07349 61.62407, -169.16447 60.191444, -169.2249 58.757504, -169.25818 57.322273, -169.26762 55.885983, -169.25626 54.448547, -169.22574 53.010063, -169.17836 51.57061, -169.11559 50.130203, -169.03862 48.688873, -168.9487 47.246746, -168.84729 45.803738, -168.73468 44.359947, -168.61186 42.91533, -168.4794 41.470016, -168.33803 40.02396, -168.18831 38.577225, -168.0302 37.12989, -167.86456 35.68189, -167.69142 34.233265, -167.51111 32.78408, -167.32387 31.334402, -167.12997 29.884232, -166.9294 28.433592, -166.72243 26.982544, -166.50911 25.5311, -166.28963 24.079334, -166.06374 22.627321, -165.83173 21.17504, -165.5938 19.72258, -165.3493 18.270048, -165.0987 16.817398, -164.8419 15.364676, -164.57861 13.912013, -164.30888 12.459461, -164.03265 11.007093, -163.74976 9.55489, -163.45993 8.103073, -163.16322 6.651596, -162.85938 5.200532, -162.5481 3.7500393, -162.22931 2.3002055, -161.90257 0.85099286, -161.5678 -0.5973707, -161.22461 -2.0448196, -160.8728 -3.4912984, -160.5119 -4.9367003, -160.14157 -6.380929, -159.7616 -7.823775, -159.37134 -9.265225, -158.97032 -10.705104, -158.5581 -12.143314, -158.13432 -13.579596, -157.6981 -15.0139265, -157.24895 -16.446169, -156.7862 -17.876038, -156.3092 -19.303482, -155.81686 -20.728178, -155.30873 -22.150038, -154.78381 -23.568888, -154.24054 -24.984303, -153.67853 -26.396284, -153.09619 -27.804325, -152.49252 -29.208296, -151.86586 -30.607882, -151.21475 -32.002724, -150.53761 -33.39235, -149.83287 -34.776573, -149.09805 -36.15481, -148.33131 -37.52667, -147.53024 -38.891594, -146.69223 -40.248947, -145.8144 -41.598248, -144.8937 -42.938667, -143.92694 -44.26958, -142.90991 -45.59, -141.8389 -46.89906, -140.70915 -48.195534, -139.51608 -49.478546, -138.25401 -50.746628, -136.9169 -51.998257, -135.49886 -53.23192, -133.99194 -54.445534, -132.38947 -55.63733, -130.68225 -56.80466, -128.86221 -57.94518, -126.919205 -59.055588, -124.843925 -60.132874, -122.62628 -61.173286, -120.256355 -62.17275, -117.72392 -63.12671, -115.01989 -64.02993, -112.13739 -64.87743, -109.07029 -65.663, -105.81696 -66.38087, -102.37863 -67.02437, -98.76285 -67.58741, -94.98206 -68.063576, -91.055954 -68.44743, -87.0105 -68.73375, -82.87765 -68.9186, -78.69416 -68.99951, -79.373535 -70.21473, -81.11329 -72.840065, -82.21712 -74.24795, -83.50793 -75.72291, -84.376465 -76.637955, -85.44061 -77.69391, -86.189804 -78.40094, -87.15132 -79.26823, -87.862335 -79.88084, -88.82377 -80.66877, -89.57531 -81.2506, -90.655045 -82.03146, -91.55787 -82.63291, -92.96539 -83.47568, -94.26903 -84.15463, -96.62457 -85.15335, -99.325836 -86.00093, -106.50273 -87.31666, -123.13585 -88.452, -180 -88.55038664352622, -180 -61.417971023434575, -179.86182 -60.15833, -179.74231 -58.73263, -179.65408 -57.305054, -179.59421 -55.875835, -179.55954 -54.44495, -179.54697 -53.012566, -179.55447 -51.578777, -179.5806 -50.143642, -179.62254 -48.707058, -179.68013 -47.269405, -179.7515 -45.830444, -179.83582 -44.390366, -179.93198 -42.94918, -180 -42.033688308511046, -180 90)), ((180 -88.55038664352622, 134.5757 -88.62898, 106.93918 -86.34042, 105.64115 -85.99406, 115.52265 -85.89217, 132.7121 -85.35355, 145.37703 -84.48782, 154.22266 -83.422844, 160.43106 -82.24005, 164.89444 -80.98532, 168.19714 -79.68494, 170.7032 -78.3539, 172.64624 -77.00155, 174.17879 -75.63367, 175.40492 -74.254166, 176.3964 -72.865715, 177.20549 -71.47018, 177.86842 -70.06891, 178.41437 -68.6628, 178.86432 -67.25281, 179.2341 -65.83929, 179.5375 -64.42278, 179.78395 -63.003635, 179.982 -61.582058, 180 -61.417971023434575, 180 -88.55038664352622)))")
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(geometry)
        print(reworked)
        self.assertTrue(geometry_compare(reworked, expected, 0.0),
                        "Reworked geometry is not equivalent to the expected")

    def test_error_13_01_2025_extracted_142(self):
        # This footprint does not pass over polar area, but cross antimeridian
        # close to south pole.
        geometry = wkt.loads("POLYGON ((92.76 78.64, 92.31 78.87, 86.96 81.07, 78.45 83.15, 63.47 84.97, 36.3 86.16, 0.58 86.08, -25.01 84.79, -39.02 82.92, -47.06 80.83, -52.18 78.62, -55.72 76.37, -58.35 74.08, -60.62 71.48, -62.23 69.16, -63.59 66.83, -64.76 64.49, -65.79 62.15, -66.71 59.8, -67.55 57.45, -68.32 55.09, -69.04 52.73, -69.71 50.37, -70.35 48.01, -71.03 45.34, -71.61 42.98, -72.17 40.61, -72.72 38.23, -73.25 35.86, -73.77 33.49, -74.28 31.11, -74.78 28.73, -75.28 26.35, -75.77 23.97, -76.27 21.59, -76.82 18.91, -77.3 16.53, -77.79 14.15, -78.28 11.77, -78.78 9.39, -79.28 7, -79.78 4.62, -80.29 2.24, -80.8 -0.14, -81.33 -2.52, -81.86 -4.9, -82.48 -7.58, -83.04 -9.95, -83.61 -12.32, -84.2 -14.7, -84.8 -17.07, -85.43 -19.43, -86.08 -21.79, -86.75 -24.15, -87.46 -26.51, -88.19 -28.86, -88.96 -31.2, -89.77 -33.54, -90.73 -36.17, -91.65 -38.5, -92.62 -40.81, -93.66 -43.12, -94.78 -45.42, -96 -47.7, -97.32 -49.98, -98.76 -52.23, -100.36 -54.47, -102.13 -56.68, -104.12 -58.87, -106.67 -61.29, -109.27 -63.39, -112.28 -65.44, -115.77 -67.43, -119.87 -69.33, -124.72 -71.11, -130.49 -72.75, -137.34 -74.2, -145.39 -75.4, -154.63 -76.28, -164.82 -76.79, -176.8 -76.85, 173.53 -76.49, 146.5 -85.11, 172.35 -86.17, -148.16 -85.96, -124.53 -84.57, -111.62 -82.67, -104.09 -80.56, -99.24 -78.36, -95.84 -76.11, -93.3 -73.83, -91.32 -71.53, -89.7 -69.22, -88.34 -66.9, -87.17 -64.57, -86.02 -61.94, -85.11 -59.61, -84.28 -57.26, -83.51 -54.91, -82.8 -52.56, -82.13 -50.21, -81.5 -47.86, -80.89 -45.5, -80.31 -43.14, -79.75 -40.77, -79.21 -38.41, -78.61 -35.75, -78.09 -33.38, -77.58 -31.01, -77.08 -28.64, -76.58 -26.26, -76.09 -23.89, -75.6 -21.51, -75.11 -19.13, -74.62 -16.75, -74.13 -14.37, -73.64 -11.99, -73.15 -9.61, -72.59 -6.94, -72.09 -4.55, -71.58 -2.17, -71.06 0.21, -70.54 2.59, -70 4.97, -69.46 7.35, -68.9 9.73, -68.33 12.1, -67.74 14.48, -67.13 16.85, -66.43 19.51, -65.78 21.88, -65.1 24.24, -64.4 26.6, -63.66 28.96, -62.89 31.31, -62.08 33.66, -61.22 36, -60.31 38.33, -59.34 40.66, -58.3 42.97, -57.03 45.57, -55.81 47.86, -54.47 50.14, -53.01 52.4, -51.4 54.64, -49.6 56.86, -47.59 59.06, -45.31 61.21, -42.7 63.33, -39.7 65.39, -36.21 67.39, -31.54 69.53, -26.57 71.31, -20.66 72.94, -13.64 74.36, -5.4 75.53, 4.02 76.37, 14.36 76.83, 25.07 76.85, 35.47 76.44, 45.02 75.64, 53.4 74.51, 60.55 73.1, 92.76 78.64))")
        expected = wkt.loads("MULTIPOLYGON (((-180 -86.12931881488984, -180 -76.73086866597725, -176.8 -76.85, -164.82 -76.79, -154.63 -76.28, -145.39 -75.4, -137.34 -74.2, -130.49 -72.75, -124.72 -71.11, -119.87 -69.33, -115.77 -67.43, -112.28 -65.44, -109.27 -63.39, -106.67 -61.29, -104.12 -58.87, -102.13 -56.68, -100.36 -54.47, -98.76 -52.23, -97.32 -49.98, -96 -47.7, -94.78 -45.42, -93.66 -43.12, -92.62 -40.81, -91.65 -38.5, -90.73 -36.17, -89.77 -33.54, -88.96 -31.2, -88.19 -28.86, -87.46 -26.51, -86.75 -24.15, -86.08 -21.79, -85.43 -19.43, -84.8 -17.07, -84.2 -14.7, -83.61 -12.32, -83.04 -9.95, -82.48 -7.58, -81.86 -4.9, -81.33 -2.52, -80.8 -0.14, -80.29 2.24, -79.78 4.62, -79.28 7, -78.78 9.39, -78.28 11.77, -77.79 14.15, -77.3 16.53, -76.82 18.91, -76.27 21.59, -75.77 23.97, -75.28 26.35, -74.78 28.73, -74.28 31.11, -73.77 33.49, -73.25 35.86, -72.72 38.23, -72.17 40.61, -71.61 42.98, -71.03 45.34, -70.35 48.01, -69.71 50.37, -69.04 52.73, -68.32 55.09, -67.55 57.45, -66.71 59.8, -65.79 62.15, -64.76 64.49, -63.59 66.83, -62.23 69.16, -60.62 71.48, -58.35 74.08, -55.72 76.37, -52.18 78.62, -47.06 80.83, -39.02 82.92, -25.01 84.79, 0.58 86.08, 36.3 86.16, 63.47 84.97, 78.45 83.15, 86.96 81.07, 92.31 78.87, 92.76 78.64, 60.55 73.1, 53.4 74.51, 45.02 75.64, 35.47 76.44, 25.07 76.85, 14.36 76.83, 4.02 76.37, -5.4 75.53, -13.64 74.36, -20.66 72.94, -26.57 71.31, -31.54 69.53, -36.21 67.39, -39.7 65.39, -42.7 63.33, -45.31 61.21, -47.59 59.06, -49.6 56.86, -51.4 54.64, -53.01 52.4, -54.47 50.14, -55.81 47.86, -57.03 45.57, -58.3 42.97, -59.34 40.66, -60.31 38.33, -61.22 36, -62.08 33.66, -62.89 31.31, -63.66 28.96, -64.4 26.6, -65.1 24.24, -65.78 21.88, -66.43 19.51, -67.13 16.85, -67.74 14.48, -68.33 12.1, -68.9 9.73, -69.46 7.35, -70 4.97, -70.54 2.59, -71.06 0.21, -71.58 -2.17, -72.09 -4.55, -72.59 -6.94, -73.15 -9.61, -73.64 -11.99, -74.13 -14.37, -74.62 -16.75, -75.11 -19.13, -75.6 -21.51, -76.09 -23.89, -76.58 -26.26, -77.08 -28.64, -77.58 -31.01, -78.09 -33.38, -78.61 -35.75, -79.21 -38.41, -79.75 -40.77, -80.31 -43.14, -80.89 -45.5, -81.5 -47.86, -82.13 -50.21, -82.8 -52.56, -83.51 -54.91, -84.28 -57.26, -85.11 -59.61, -86.02 -61.94, -87.17 -64.57, -88.34 -66.9, -89.7 -69.22, -91.32 -71.53, -93.3 -73.83, -95.84 -76.11, -99.24 -78.36, -104.09 -80.56, -111.62 -82.67, -124.53 -84.57, -148.16 -85.96, -180 -86.12931881488984)), ((180 -86.12931881488984, 172.35 -86.17, 146.5 -85.11, 173.53 -76.49, 180 -76.73086866597725, 180 -86.12931881488984)))")
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(geometry)
        print(reworked)
        self.assertTrue(geometry_compare(reworked, expected, 0.0),
                        "Reworked geometry is not equivalent to the expected")


    def test_error_13_01_2025_extracted_131(self):
        geometry = wkt.loads("POLYGON ((180 -79.2380982347165, -179.68489 -79.3288471626108, 180 -79.3315064900335, 176.99902999007 -79.3568332240301, 176.999080367788 -78.745458319278, 177.404588194791 -78.7028272504728, 178.056534211388 -78.6318395089797, 178.721279451068 -78.8388777040525, 178.707044670304 -78.84044170899, 178.707347779763 -78.8405333618639, 178.704881962724 -78.8408044813414, 178.705407944923 -78.8409633948802, 178.703063859609 -78.8412210490064, 178.703303629245 -78.8412934249978, 178.685784032187 -78.8432170655546, 178.685917453268 -78.8432571028287, 178.685221839156 -78.8433335076021, 179.290082609886 -79.0246590574883, 179.293656001187 -79.0242634483362, 179.30078682032 -79.0264027636166, 179.33127334589 -79.0230304949518, 180 -79.2218069420933, -179.99835 -79.2222963194723, 180 -79.2224799856686, 179.985775955281 -79.2240667949805, 179.985810870837 -79.2240768931646, 179.960946153513 -79.2268508632316, 180 -79.2380982347165))")
        expected = wkt.loads("MULTIPOLYGON (((180 -79.2380982347165, 180 -79.3315064900335, 176.99902999007 -79.3568332240301, 176.999080367788 -78.745458319278, 177.404588194791 -78.7028272504728, 178.056534211388 -78.6318395089797, 178.721279451068 -78.8388777040525, 178.707044670304 -78.84044170899, 178.707347779763 -78.8405333618639, 178.704881962724 -78.8408044813414, 178.705407944923 -78.8409633948802, 178.703063859609 -78.8412210490064, 178.703303629245 -78.8412934249978, 178.685784032187 -78.8432170655546, 178.685917453268 -78.8432571028287, 178.685221839156 -78.8433335076021, 179.290082609886 -79.0246590574883, 179.293656001187 -79.0242634483362, 179.30078682032 -79.0264027636166, 179.33127334589 -79.0230304949518, 180 -79.2218069420933, 180 -79.2224799856686, 179.985775955281 -79.2240667949805, 179.985810870837 -79.2240768931646, 179.960946153513 -79.2268508632316, 180 -79.2380982347165)), ((-180 -79.2380982347165, -179.68489 -79.3288471626108, -180 -79.3315064900335, -180 -79.2380982347165)), ((-180 -79.2224799856686, -180 -79.2218069420933, -179.99835 -79.2222963194723, -180 -79.2224799856686)))")
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(geometry)
        print(reworked)
        self.assertTrue(geometry_compare(reworked, expected, 0.0),
                        "Reworked geometry is not equivalent to the expected")


    def test_error_98(self):
        geometry = wkt.loads("POLYGON ((85.9213 -85.901, 85.9704 -85.7294, 85.8608 -85.2741, 85.8633 -84.8183, 85.847 -84.364, 85.8812 -83.9024, 85.8541 -83.4518, 85.8753 -82.991, 85.8324 -82.5373, 85.85 -82.079, 85.8032 -81.6239, 85.8166 -81.1606, 85.8197 -80.7056, 85.8243 -80.2474, 85.8245 -79.7922, 85.8085 -79.34, 85.7929 -78.8793, 85.8122 -78.4248, 85.8172 -77.9687, 85.776 -77.5082, 85.783 -77.0554, 85.7965 -76.5926, 85.763 -76.141, 85.7907 -75.6837, 85.8014 -75.2215, 85.7525 -74.7697, 85.7478 -74.313, 85.7854 -73.8505, 85.7425 -73.4013, 85.7874 -72.947, 85.7733 -72.4844, 91.7744 -72.3917, 100.871 -71.8907, 109.31 -70.9874, 116.876 -69.7356, 123.503 -68.1951, 129.234 -66.4221, 134.165 -64.4649, 138.41 -62.3624, 142.08 -60.145, 145.27 -57.8363, 148.064 -55.4544, 150.528 -53.0131, 152.718 -50.5235, 154.678 -47.9938, 156.446 -45.4307, 158.049 -42.8396, 159.513 -40.2247, 160.858 -37.5896, 162.099 -34.937, 163.251 -32.2694, 164.324 -29.5887, 165.33 -26.8966, 166.275 -24.1947, 167.166 -21.484, 168.011 -18.7659, 168.813 -16.0411, 169.577 -13.3105, 170.307 -10.575, 171.007 -7.83527, 171.679 -5.09186, 172.326 -2.34538, 172.949 0.403643, 173.552 3.15472, 174.136 5.90739, 174.703 8.66127, 175.253 11.416, 175.788 14.1711, 176.31 16.9264, 176.818 19.6815, 177.315 22.4363, 177.801 25.1903, 178.276 27.9435, 178.741 30.6957, 179.197 33.4466, 179.644 36.1961, -179.918 38.9442, -179.489 41.6907, -179.068 44.4355, -178.655 47.1787, -178.252 49.9201, -177.857 52.6598, -177.472 55.3978, -177.099 58.1341, -176.738 60.8687, -176.393 63.6018, -176.067 66.3334, -175.768 69.0636, -175.504 71.7925, -175.294 74.5201, -175.171 77.2465, -175.205 79.9716, -175.567 82.695, -176.843 85.4149, 177.015 88.1186, 30.7516 89.0467, 14.597 86.3765, 12.5511 83.6592, 11.9766 80.9367, 11.8561 78.2122, 11.9346 75.4864, 12.1186 72.7593, 12.3658 70.031, 12.6542 67.3014, 12.9733 64.5555, 13.3122 61.8231, 13.6678 59.0891, 14.037 56.3536, 14.4179 53.6164, 14.8091 50.8775, 15.2097 48.1369, 15.6192 45.3946, 16.0373 42.6506, 16.4638 39.905, 16.8987 37.1577, 17.3423 34.409, 17.7948 31.6588, 18.2566 28.9074, 18.7281 26.1549, 19.2099 23.4014, 19.7027 20.6472, 20.207 17.8925, 20.7239 15.1376, 21.2542 12.3827, 21.7989 9.62817, 22.3594 6.87432, 22.9369 4.12152, 23.5329 1.37018, 24.1492 -1.37927, 24.7876 -4.12636, 25.4503 -6.87058, 26.1398 -9.61137, 26.8588 -12.3481, 27.6106 -15.0802, 28.3988 -17.8068, 29.2276 -20.5271, 30.1018 -23.2402, 31.0272 -25.9451, 32.0102 -28.6405, 33.0585 -31.3251, 34.1814 -33.9973, 35.3894 -36.6552, 36.6955 -39.2966, 38.1151 -41.9188, 39.6667 -44.5186, 41.3729 -47.0919, 43.2612 -49.634, 45.3652 -52.1385, 47.7267 -54.5979, 50.3966 -57.0021, 53.4377 -59.3385, 56.9272 -61.5905, 60.9565 -63.7367, 65.6318 -65.7493, 71.0672 -67.5925, 77.3686 -69.2214, 84.6032 -70.5822, 92.7503 -71.6154, 101.65 -72.2642, 110.952 -72.4853, 110.981 -72.4853, 110.98 -72.9439, 110.997 -73.3982, 110.983 -73.8567, 111.001 -74.3111, 111.006 -74.7673, 110.998 -75.2276, 110.97 -75.6826, 110.964 -76.1447, 110.991 -76.6008, 111.004 -77.0525, 110.976 -77.5109, 110.981 -77.9691, 110.972 -78.4252, 111.002 -78.8783, 111.003 -79.341, 110.971 -79.7922, 111.015 -80.2565, 111.016 -80.7059, 110.999 -81.1618, 110.983 -81.6252, 110.967 -82.0808, 111.004 -82.5388, 110.977 -82.9933, 111.015 -83.4535, 110.964 -83.9052, 110.994 -84.3651, 111 -84.8187, 111.035 -85.2787, 110.994 -85.7314, 111.012 -85.9018, 110.889 -85.9108, 76.7857 -85.0789, 56.9603 -83.1628, 46.3028 -80.8179, 39.9412 -78.2987, 35.7272 -75.6965, 32.7019 -73.049, 30.3944 -70.374, 28.5499 -67.6808, 27.02 -64.9749, 25.7132 -62.2593, 24.5693 -59.5362, 23.5479 -56.8069, 22.6206 -54.0723, 21.7666 -51.3332, 20.9707 -48.59, 20.2212 -45.843, 19.509 -43.0927, 18.8272 -40.3391, 18.1698 -37.5827, 17.5323 -34.8234, 16.9106 -32.0616, 16.3014 -29.2974, 15.702 -26.5311, 15.1096 -23.7627, 14.5221 -20.9926, 13.9375 -18.2209, 13.3538 -15.4479, 12.7691 -12.6738, 12.1818 -9.8989, 11.5902 -7.12346, 10.9924 -4.34776, 10.3867 -1.57213, 9.7713 1.20309, 9.1442 3.97758, 8.50334 6.75094, 7.84645 9.52277, 7.17103 12.2927, 6.47434 15.0601, 5.75326 17.8247, 5.00429 20.5859, 4.22343 23.343, 3.40601 26.0954, 2.5467 28.8423, 1.63918 31.583, 0.676 34.3164, -0.351687 37.0414, -1.45459 39.7567, -2.64563 42.4606, -3.94061 45.1512, -5.35925 47.8261, -6.92591 50.4822, -8.67154 53.1156, -10.6357 55.7214, -12.8691 58.293, -15.4385 60.8216, -18.4488 63.3086, -21.9832 65.7105, -26.2095 68.0178, -31.3259 70.1977, -37.5767 72.2039, -45.2339 73.9711, -54.5204 75.4125, -65.4466 76.4244, -77.6021 76.9065, -90.1009 76.8012, -101.901 76.1218, -112.267 74.9453, -120.96 73.3772, -128.089 71.5165, -133.907 69.4424, -138.682 67.2127, -142.643 64.8686, -145.972 62.439, -148.805 59.9445, -151.249 57.3995, -153.381 54.815, -155.264 52.1987, -156.944 49.5566, -158.455 46.8934, -159.828 44.2125, -161.085 41.5167, -162.244 38.8084, -163.319 36.0893, -164.323 33.3609, -165.266 30.6245, -166.156 27.8813, -167 25.132, -167.804 22.3776, -168.574 19.6187, -169.312 16.8559, -170.025 14.0899, -170.714 11.3212, -171.382 8.55024, -172.033 5.77747, -172.669 3.00332, -173.292 0.228173, -173.904 -2.54759, -174.507 -5.32364, -175.102 -8.09963, -175.692 -10.8753, -176.279 -13.6503, -176.863 -16.4244, -177.447 -19.1973, -178.032 -21.9688, -178.621 -24.7386, -179.216 -27.5066, -179.819 -30.2725, 179.568 -33.0362, 178.941 -35.7973, 178.297 -38.5559, 177.631 -41.3116, 176.939 -44.0643, 176.215 -46.8137, 175.45 -49.5596, 174.635 -52.3016, 173.757 -55.0393, 172.799 -57.7722, 171.738 -60.4996, 170.541 -63.2204, 169.163 -65.9329, 167.535 -68.6349, 165.547 -71.3224, 163.022 -73.9891, 159.646 -76.6233, 154.821 -79.202, 147.283 -81.6747, 134.135 -83.9118, 109.351 -85.5439, 85.9213 -85.901))")
        expected = wkt.loads("POLYGON ((24.7876 -4.12636, 25.4503 -6.87058, 26.1398 -9.61137, 26.8588 -12.3481, 27.6106 -15.0802, 28.3988 -17.8068, 29.2276 -20.5271, 30.1018 -23.2402, 31.0272 -25.9451, 32.0102 -28.6405, 33.0585 -31.3251, 34.1814 -33.9973, 35.3894 -36.6552, 36.6955 -39.2966, 38.1151 -41.9188, 39.6667 -44.5186, 41.3729 -47.0919, 43.2612 -49.634, 45.3652 -52.1385, 47.7267 -54.5979, 50.3966 -57.0021, 53.4377 -59.3385, 56.9272 -61.5905, 60.9565 -63.7367, 65.6318 -65.7493, 71.0672 -67.5925, 77.3686 -69.2214, 84.6032 -70.5822, 92.7503 -71.6154, 98.39625675556861 -72.0269977777917, 100.871 -71.8907, 109.31 -70.9874, 116.876 -69.7356, 123.503 -68.1951, 129.234 -66.4221, 134.165 -64.4649, 138.41 -62.3624, 142.08 -60.145, 145.27 -57.8363, 148.064 -55.4544, 150.528 -53.0131, 152.718 -50.5235, 154.678 -47.9938, 156.446 -45.4307, 158.049 -42.8396, 159.513 -40.2247, 160.858 -37.5896, 162.099 -34.937, 163.251 -32.2694, 164.324 -29.5887, 165.33 -26.8966, 166.275 -24.1947, 167.166 -21.484, 168.011 -18.7659, 168.813 -16.0411, 169.577 -13.3105, 170.307 -10.575, 171.007 -7.83527, 171.679 -5.09186, 172.326 -2.34538, 172.85752401416795 0, 172.949 0.403643, 173.552 3.15472, 174.136 5.90739, 174.703 8.66127, 175.253 11.416, 175.788 14.1711, 176.31 16.9264, 176.818 19.6815, 177.315 22.4363, 177.801 25.1903, 178.276 27.9435, 178.741 30.6957, 179.197 33.4466, 179.644 36.1961, 180 38.42971552511426, 180 0, 180 -31.0885353996739, 179.568 -33.0362, 178.941 -35.7973, 178.297 -38.5559, 177.631 -41.3116, 176.939 -44.0643, 176.215 -46.8137, 175.45 -49.5596, 174.635 -52.3016, 173.757 -55.0393, 172.799 -57.7722, 171.738 -60.4996, 170.541 -63.2204, 169.163 -65.9329, 167.535 -68.6349, 165.547 -71.3224, 163.022 -73.9891, 159.646 -76.6233, 154.821 -79.202, 147.283 -81.6747, 134.135 -83.9118, 111.02094122852029 -85.43392941094787, 110.994 -85.7314, 111.012 -85.9018, 110.889 -85.9108, 101.04057228229651 -85.67056204594988, 85.9213 -85.901, 85.9704 -85.7294, 85.86713777320473 -85.30042835894265, 76.7857 -85.0789, 56.9603 -83.1628, 46.3028 -80.8179, 39.9412 -78.2987, 35.7272 -75.6965, 32.7019 -73.049, 30.3944 -70.374, 28.5499 -67.6808, 27.02 -64.9749, 25.7132 -62.2593, 24.5693 -59.5362, 23.5479 -56.8069, 22.6206 -54.0723, 21.7666 -51.3332, 20.9707 -48.59, 20.2212 -45.843, 19.509 -43.0927, 18.8272 -40.3391, 18.1698 -37.5827, 17.5323 -34.8234, 16.9106 -32.0616, 16.3014 -29.2974, 15.702 -26.5311, 15.1096 -23.7627, 14.5221 -20.9926, 13.9375 -18.2209, 13.3538 -15.4479, 12.7691 -12.6738, 12.1818 -9.8989, 11.5902 -7.12346, 10.9924 -4.34776, 10.3867 -1.57213, 10.038083024769207 0, 9.7713 1.20309, 9.1442 3.97758, 8.50334 6.75094, 7.84645 9.52277, 7.17103 12.2927, 6.47434 15.0601, 5.75326 17.8247, 5.00429 20.5859, 4.22343 23.343, 3.40601 26.0954, 2.5467 28.8423, 1.63918 31.583, 0.676 34.3164, -0.351687 37.0414, -1.45459 39.7567, -2.64563 42.4606, -3.94061 45.1512, -5.35925 47.8261, -6.92591 50.4822, -8.67154 53.1156, -10.6357 55.7214, -12.8691 58.293, -15.4385 60.8216, -18.4488 63.3086, -21.9832 65.7105, -26.2095 68.0178, -31.3259 70.1977, -37.5767 72.2039, -45.2339 73.9711, -54.5204 75.4125, -65.4466 76.4244, -77.6021 76.9065, -90.1009 76.8012, -101.901 76.1218, -112.267 74.9453, -120.96 73.3772, -128.089 71.5165, -133.907 69.4424, -138.682 67.2127, -142.643 64.8686, -145.972 62.439, -148.805 59.9445, -151.249 57.3995, -153.381 54.815, -155.264 52.1987, -156.944 49.5566, -158.455 46.8934, -159.828 44.2125, -161.085 41.5167, -162.244 38.8084, -163.319 36.0893, -164.323 33.3609, -165.266 30.6245, -166.156 27.8813, -167 25.132, -167.804 22.3776, -168.574 19.6187, -169.312 16.8559, -170.025 14.0899, -170.714 11.3212, -171.382 8.55024, -172.033 5.77747, -172.669 3.00332, -173.292 0.228173, -173.34230756444262 0, -173.904 -2.54759, -174.507 -5.32364, -175.102 -8.09963, -175.692 -10.8753, -176.279 -13.6503, -176.863 -16.4244, -177.447 -19.1973, -178.032 -21.9688, -178.621 -24.7386, -179.216 -27.5066, -179.819 -30.2725, -180 -31.0885353996739, -180 0, -180 38.42971552511426, -179.918 38.9442, -179.489 41.6907, -179.068 44.4355, -178.655 47.1787, -178.252 49.9201, -177.857 52.6598, -177.472 55.3978, -177.099 58.1341, -176.738 60.8687, -176.393 63.6018, -176.067 66.3334, -175.768 69.0636, -175.504 71.7925, -175.294 74.5201, -175.171 77.2465, -175.205 79.9716, -175.567 82.695, -176.843 85.4149, -180 86.8046070823836, -180 90, 180 90, 180 86.8046070823836, 177.015 88.1186, 30.7516 89.0467, 14.597 86.3765, 12.5511 83.6592, 11.9766 80.9367, 11.8561 78.2122, 11.9346 75.4864, 12.1186 72.7593, 12.3658 70.031, 12.6542 67.3014, 12.9733 64.5555, 13.3122 61.8231, 13.6678 59.0891, 14.037 56.3536, 14.4179 53.6164, 14.8091 50.8775, 15.2097 48.1369, 15.6192 45.3946, 16.0373 42.6506, 16.4638 39.905, 16.8987 37.1577, 17.3423 34.409, 17.7948 31.6588, 18.2566 28.9074, 18.7281 26.1549, 19.2099 23.4014, 19.7027 20.6472, 20.207 17.8925, 20.7239 15.1376, 21.2542 12.3827, 21.7989 9.62817, 22.3594 6.87432, 22.9369 4.12152, 23.5329 1.37018, 23.840031220425903 0, 24.1492 -1.37927, 24.7876 -4.12636))")
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(geometry)
        print(reworked)
        self.assertTrue(geometry_compare(reworked, expected, 0.0),
                        "Reworked geometry is not equivalent to the expected")


    def test_error_100(self):
        geometry = wkt.loads("POLYGON ((76.88914 68.64518, 78.93809 68.63362, 81.72632 68.71964, 85.88138 68.87019, 90.07393 68.915215, 94.26332 68.85433, 98.409515 68.68821, 102.47468 68.419464, 106.425644 68.05197, 110.235085 67.59041, 113.88244 67.04042, 117.3534 66.40821, 120.64011 65.700264, 123.73969 64.92285, 126.65419 64.08253, 129.3881 63.18475, 131.94855 62.235294, 134.34503 61.239372, 136.58653 60.20134, 138.6838 59.125797, 140.64645 58.01617, 142.4847 56.87607, 144.208 55.70848, 145.82529 54.51612, 147.34497 53.30132, 148.77483 52.06632, 150.12178 50.81274, 151.39287 49.54274, 152.59375 48.257507, 153.73033 46.958534, 154.80739 45.64696, 155.82924 44.32374, 156.80057 42.9901, 157.72475 41.646732, 158.60562 40.29449, 159.44589 38.93398, 160.24908 37.566113, 161.01698 36.19108, 161.75264 34.80969, 162.45813 33.422443, 163.13538 32.02966, 163.78618 30.631767, 164.41193 29.228966, 165.01479 27.82194, 165.59561 26.410728, 166.15602 24.995703, 166.69731 23.577229, 167.22034 22.155548, 167.726 20.730642, 168.21558 19.303009, 168.68976 17.872734, 169.14935 16.440023, 169.59494 15.005026, 170.02736 13.567901, 170.4475 12.129021, 170.8553 10.688119, 171.25192 9.245683, 171.6375 7.8017554, 172.01273 6.356489, 172.37784 4.909944, 172.7335 3.4622974, 173.07948 2.0135546, 173.41663 0.56390923, 173.74538 -0.8864741, 174.06554 -2.337641, 174.37749 -3.7894127, 174.68173 -5.2416587, 174.97821 -6.6943426, 175.26718 -8.147412, 175.54883 -9.60076, 175.82327 -11.054236, 176.09068 -12.507865, 176.35124 -13.96155, 176.60478 -15.415192, 176.85168 -16.868736, 177.09175 -18.322088, 177.32498 -19.775291, 177.5518 -21.228035, 177.77177 -22.68051, 177.9848 -24.1326, 178.19112 -25.584208, 178.39056 -27.035255, 178.58292 -28.485806, 178.76804 -29.935709, 178.94603 -31.384838, 179.1161 -32.833435, 179.27853 -34.281147, 179.43265 -35.728107, 179.5784 -37.1742, 179.71545 -38.61937, 179.84296 -40.06363, 179.96086 -41.506897, -179.93198 -42.94918, -179.83582 -44.390366, -179.7515 -45.830444, -179.68013 -47.269405, -179.62254 -48.707058, -179.5806 -50.143642, -179.55447 -51.578777, -179.54697 -53.012566, -179.55954 -54.44495, -179.59421 -55.875835, -179.65408 -57.305054, -179.74231 -58.73263, -179.86182 -60.15833, 179.982 -61.582058, 179.78395 -63.003635, 179.5375 -64.42278, 179.2341 -65.83929, 178.86432 -67.25281, 178.41437 -68.6628, 177.86842 -70.06891, 177.20549 -71.47018, 176.3964 -72.865715, 175.40492 -74.254166, 174.17879 -75.63367, 172.64624 -77.00155, 170.7032 -78.3539, 168.19714 -79.68494, 164.89444 -80.98532, 160.43106 -82.24005, 154.22266 -83.422844, 145.37703 -84.48782, 132.7121 -85.35355, 115.52265 -85.89217, 105.64115 -85.99406, 106.93918 -86.34042, 134.5757 -88.62898, -123.13585 -88.452, -106.50273 -87.31666, -99.325836 -86.00093, -96.62457 -85.15335, -94.26903 -84.15463, -92.96539 -83.47568, -91.55787 -82.63291, -90.655045 -82.03146, -89.57531 -81.2506, -88.82377 -80.66877, -87.862335 -79.88084, -87.15132 -79.26823, -86.189804 -78.40094, -85.44061 -77.69391, -84.376465 -76.637955, -83.50793 -75.72291, -82.21712 -74.24795, -81.11329 -72.840065, -79.373535 -70.21473, -78.69416 -68.99951, -82.87765 -68.9186, -87.0105 -68.73375, -91.055954 -68.44743, -94.98206 -68.063576, -98.76285 -67.58741, -102.37863 -67.02437, -105.81696 -66.38087, -109.07029 -65.663, -112.13739 -64.87743, -115.01989 -64.02993, -117.72392 -63.12671, -120.256355 -62.17275, -122.62628 -61.173286, -124.843925 -60.132874, -126.919205 -59.055588, -128.86221 -57.94518, -130.68225 -56.80466, -132.38947 -55.63733, -133.99194 -54.445534, -135.49886 -53.23192, -136.9169 -51.998257, -138.25401 -50.746628, -139.51608 -49.478546, -140.70915 -48.195534, -141.8389 -46.89906, -142.90991 -45.59, -143.92694 -44.26958, -144.8937 -42.938667, -145.8144 -41.598248, -146.69223 -40.248947, -147.53024 -38.891594, -148.33131 -37.52667, -149.09805 -36.15481, -149.83287 -34.776573, -150.53761 -33.39235, -151.21475 -32.002724, -151.86586 -30.607882, -152.49252 -29.208296, -153.09619 -27.804325, -153.67853 -26.396284, -154.24054 -24.984303, -154.78381 -23.568888, -155.30873 -22.150038, -155.81686 -20.728178, -156.3092 -19.303482, -156.7862 -17.876038, -157.24895 -16.446169, -157.6981 -15.0139265, -158.13432 -13.579596, -158.5581 -12.143314, -158.97032 -10.705104, -159.37134 -9.265225, -159.7616 -7.823775, -160.14157 -6.380929, -160.5119 -4.9367003, -160.8728 -3.4912984, -161.22461 -2.0448196, -161.5678 -0.5973707, -161.90257 0.85099286, -162.22931 2.3002055, -162.5481 3.7500393, -162.85938 5.200532, -163.16322 6.651596, -163.45993 8.103073, -163.74976 9.55489, -164.03265 11.007093, -164.30888 12.459461, -164.57861 13.912013, -164.8419 15.364676, -165.0987 16.817398, -165.3493 18.270048, -165.5938 19.72258, -165.83173 21.17504, -166.06374 22.627321, -166.28963 24.079334, -166.50911 25.5311, -166.72243 26.982544, -166.9294 28.433592, -167.12997 29.884232, -167.32387 31.334402, -167.51111 32.78408, -167.69142 34.233265, -167.86456 35.68189, -168.0302 37.12989, -168.18831 38.577225, -168.33803 40.02396, -168.4794 41.470016, -168.61186 42.91533, -168.73468 44.359947, -168.84729 45.803738, -168.9487 47.246746, -169.03862 48.688873, -169.11559 50.130203, -169.17836 51.57061, -169.22574 53.010063, -169.25626 54.448547, -169.26762 55.885983, -169.25818 57.322273, -169.2249 58.757504, -169.16447 60.191444, -169.07349 61.62407, -168.94751 63.055233, -168.77975 64.48471, -168.5642 65.91247, -168.29185 67.33813, -167.95148 68.7615, -167.52893 70.18207, -167.00563 71.5994, -166.35648 73.01275, -165.5487 74.42116, -164.53537 75.82322, -163.25175 77.217064, -161.59889 78.599594, -159.43214 79.96641, -156.51906 81.31017, -152.47577 82.61826, -146.64899 83.868195, -137.89146 85.015884, -124.36339 85.97286, -104.34557 86.575615, -80.160576 86.62825, -59.05918 86.10842, -44.394722 85.18761, -30.737564 83.08694, -27.671694 82.30806, -25.401226 82.419464, -7.568519 82.844345, 9.262352 82.61184, 18.03902 82.23403, 26.545952 81.66153, 31.38546 81.226364, 36.538754 80.65881, 39.739944 80.2444, 43.4114 79.70279, 45.846886 79.30015, 48.802784 78.75989, 50.867897 78.34582, 53.496426 77.771164, 55.418964 77.31437, 57.978027 76.65416, 59.935696 76.10509, 62.664005 75.26798, 64.853195 74.52661, 68.067505 73.30109, 70.8043 72.09679, 75.1573 69.76342, 76.88914 68.64518, 76.88914 68.64518))")
        expected = wkt.loads("MULTIPOLYGON (((180 -88.55038664352622, 134.5757 -88.62898, 106.93918 -86.34042, 105.64115 -85.99406, 115.52265 -85.89217, 132.7121 -85.35355, 145.37703 -84.48782, 154.22266 -83.422844, 160.43106 -82.24005, 164.89444 -80.98532, 168.19714 -79.68494, 170.7032 -78.3539, 172.64624 -77.00155, 174.17879 -75.63367, 175.40492 -74.254166, 176.3964 -72.865715, 177.20549 -71.47018, 177.86842 -70.06891, 178.41437 -68.6628, 178.86432 -67.25281, 179.2341 -65.83929, 179.5375 -64.42278, 179.78395 -63.003635, 179.982 -61.582058, 180 -61.417971023434575, 180 -88.55038664352622)), ((-180 90, 180 90, 180 -42.033688308511046, 179.96086 -41.506897, 179.84296 -40.06363, 179.71545 -38.61937, 179.5784 -37.1742, 179.43265 -35.728107, 179.27853 -34.281147, 179.1161 -32.833435, 178.94603 -31.384838, 178.76804 -29.935709, 178.58292 -28.485806, 178.39056 -27.035255, 178.19112 -25.584208, 177.9848 -24.1326, 177.77177 -22.68051, 177.5518 -21.228035, 177.32498 -19.775291, 177.09175 -18.322088, 176.85168 -16.868736, 176.60478 -15.415192, 176.35124 -13.96155, 176.09068 -12.507865, 175.82327 -11.054236, 175.54883 -9.60076, 175.26718 -8.147412, 174.97821 -6.6943426, 174.68173 -5.2416587, 174.37749 -3.7894127, 174.06554 -2.337641, 173.74538 -0.8864741, 173.41663 0.56390923, 173.07948 2.0135546, 172.7335 3.4622974, 172.37784 4.909944, 172.01273 6.356489, 171.6375 7.8017554, 171.25192 9.245683, 170.8553 10.688119, 170.4475 12.129021, 170.02736 13.567901, 169.59494 15.005026, 169.14935 16.440023, 168.68976 17.872734, 168.21558 19.303009, 167.726 20.730642, 167.22034 22.155548, 166.69731 23.577229, 166.15602 24.995703, 165.59561 26.410728, 165.01479 27.82194, 164.41193 29.228966, 163.78618 30.631767, 163.13538 32.02966, 162.45813 33.422443, 161.75264 34.80969, 161.01698 36.19108, 160.24908 37.566113, 159.44589 38.93398, 158.60562 40.29449, 157.72475 41.646732, 156.80057 42.9901, 155.82924 44.32374, 154.80739 45.64696, 153.73033 46.958534, 152.59375 48.257507, 151.39287 49.54274, 150.12178 50.81274, 148.77483 52.06632, 147.34497 53.30132, 145.82529 54.51612, 144.208 55.70848, 142.4847 56.87607, 140.64645 58.01617, 138.6838 59.125797, 136.58653 60.20134, 134.34503 61.239372, 131.94855 62.235294, 129.3881 63.18475, 126.65419 64.08253, 123.73969 64.92285, 120.64011 65.700264, 117.3534 66.40821, 113.88244 67.04042, 110.235085 67.59041, 106.425644 68.05197, 102.47468 68.419464, 98.409515 68.68821, 94.26332 68.85433, 90.07393 68.915215, 85.88138 68.87019, 81.72632 68.71964, 78.93809 68.63362, 76.88914 68.64518, 75.1573 69.76342, 70.8043 72.09679, 68.067505 73.30109, 64.853195 74.52661, 62.664005 75.26798, 59.935696 76.10509, 57.978027 76.65416, 55.418964 77.31437, 53.496426 77.771164, 50.867897 78.34582, 48.802784 78.75989, 45.846886 79.30015, 43.4114 79.70279, 39.739944 80.2444, 36.538754 80.65881, 31.38546 81.226364, 26.545952 81.66153, 18.03902 82.23403, 9.262352 82.61184, -7.568519 82.844345, -25.401226 82.419464, -27.671694 82.30806, -30.737564 83.08694, -44.394722 85.18761, -59.05918 86.10842, -80.160576 86.62825, -104.34557 86.575615, -124.36339 85.97286, -137.89146 85.015884, -146.64899 83.868195, -152.47577 82.61826, -156.51906 81.31017, -159.43214 79.96641, -161.59889 78.599594, -163.25175 77.217064, -164.53537 75.82322, -165.5487 74.42116, -166.35648 73.01275, -167.00563 71.5994, -167.52893 70.18207, -167.95148 68.7615, -168.29185 67.33813, -168.5642 65.91247, -168.77975 64.48471, -168.94751 63.055233, -169.07349 61.62407, -169.16447 60.191444, -169.2249 58.757504, -169.25818 57.322273, -169.26762 55.885983, -169.25626 54.448547, -169.22574 53.010063, -169.17836 51.57061, -169.11559 50.130203, -169.03862 48.688873, -168.9487 47.246746, -168.84729 45.803738, -168.73468 44.359947, -168.61186 42.91533, -168.4794 41.470016, -168.33803 40.02396, -168.18831 38.577225, -168.0302 37.12989, -167.86456 35.68189, -167.69142 34.233265, -167.51111 32.78408, -167.32387 31.334402, -167.12997 29.884232, -166.9294 28.433592, -166.72243 26.982544, -166.50911 25.5311, -166.28963 24.079334, -166.06374 22.627321, -165.83173 21.17504, -165.5938 19.72258, -165.3493 18.270048, -165.0987 16.817398, -164.8419 15.364676, -164.57861 13.912013, -164.30888 12.459461, -164.03265 11.007093, -163.74976 9.55489, -163.45993 8.103073, -163.16322 6.651596, -162.85938 5.200532, -162.5481 3.7500393, -162.22931 2.3002055, -161.90257 0.85099286, -161.5678 -0.5973707, -161.22461 -2.0448196, -160.8728 -3.4912984, -160.5119 -4.9367003, -160.14157 -6.380929, -159.7616 -7.823775, -159.37134 -9.265225, -158.97032 -10.705104, -158.5581 -12.143314, -158.13432 -13.579596, -157.6981 -15.0139265, -157.24895 -16.446169, -156.7862 -17.876038, -156.3092 -19.303482, -155.81686 -20.728178, -155.30873 -22.150038, -154.78381 -23.568888, -154.24054 -24.984303, -153.67853 -26.396284, -153.09619 -27.804325, -152.49252 -29.208296, -151.86586 -30.607882, -151.21475 -32.002724, -150.53761 -33.39235, -149.83287 -34.776573, -149.09805 -36.15481, -148.33131 -37.52667, -147.53024 -38.891594, -146.69223 -40.248947, -145.8144 -41.598248, -144.8937 -42.938667, -143.92694 -44.26958, -142.90991 -45.59, -141.8389 -46.89906, -140.70915 -48.195534, -139.51608 -49.478546, -138.25401 -50.746628, -136.9169 -51.998257, -135.49886 -53.23192, -133.99194 -54.445534, -132.38947 -55.63733, -130.68225 -56.80466, -128.86221 -57.94518, -126.919205 -59.055588, -124.843925 -60.132874, -122.62628 -61.173286, -120.256355 -62.17275, -117.72392 -63.12671, -115.01989 -64.02993, -112.13739 -64.87743, -109.07029 -65.663, -105.81696 -66.38087, -102.37863 -67.02437, -98.76285 -67.58741, -94.98206 -68.063576, -91.055954 -68.44743, -87.0105 -68.73375, -82.87765 -68.9186, -78.69416 -68.99951, -79.373535 -70.21473, -81.11329 -72.840065, -82.21712 -74.24795, -83.50793 -75.72291, -84.376465 -76.637955, -85.44061 -77.69391, -86.189804 -78.40094, -87.15132 -79.26823, -87.862335 -79.88084, -88.82377 -80.66877, -89.57531 -81.2506, -90.655045 -82.03146, -91.55787 -82.63291, -92.96539 -83.47568, -94.26903 -84.15463, -96.62457 -85.15335, -99.325836 -86.00093, -106.50273 -87.31666, -123.13585 -88.452, -180 -88.55038664352622, -180 -61.417971023434575, -179.86182 -60.15833, -179.74231 -58.73263, -179.65408 -57.305054, -179.59421 -55.875835, -179.55954 -54.44495, -179.54697 -53.012566, -179.55447 -51.578777, -179.5806 -50.143642, -179.62254 -48.707058, -179.68013 -47.269405, -179.7515 -45.830444, -179.83582 -44.390366, -179.93198 -42.94918, -180 -42.033688308511046, -180 90)))")
        reworked = footprint_facility.rework_to_polygon_geometry(geometry)
        print(geometry)
        print(reworked)
        self.assertTrue(geometry_compare(reworked, expected, 0.0),
                        "Reworked geometry is not equivalent to the expected")

