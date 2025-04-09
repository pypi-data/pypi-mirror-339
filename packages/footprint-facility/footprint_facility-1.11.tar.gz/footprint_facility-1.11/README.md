# Footprint facility
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![pipeline](https://gitlab.com/be-prototypes/geofootprint-prototype/badges/main/pipeline.svg)
![Coverage](https://gitlab.com/be-prototypes/geofootprint-prototype/badges/main/coverage.svg)

This set of functions provides facilities to manipulate footprints for display in Leaflet, OpenLayers, MapBox, and Cesium.

It manages:
- Splitting polygons into multi-polygons when crossing the anti-meridian
- Managing polar areas including polar points inside polygon boundaries
- Managing long footprints with overlays
- Managing thin footprints by collapsing polygons into a single LineString

# Preliminary information regrading dependencies
We recommend using a virtual environment to manage dependencies.
The dependencies are automatically installed during this module installation:
- pyproj
- numpy
- shapely
- geojson

Details can be found in the [requirements.txt](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/requirements.txt) file.

## Library usage
The `shapely` library provides a set of features that could be a solution to handle the footprints identified in this study. Unfortunately, the library is also affected by display issues. For example, intersection operations in shapely fail when a footprint contains the antimeridian or covers polar area. This library is mainly used to handle geometries types and format conversions. This issue arises due to discontinuities between the Cartesian reference system used in Shapely and the geospatial reference system using latitude and longitude in degrees in footprints.

`Numpy` is used to manipulate and crawl among the list of coordinates to fix the issues caused by lat/lon limits of the geometry.

## Installation
```python
pip install footprint-facility
```
The module is retrieved from pypi.org service.
# Available methods

The ```rework_to_polygon_geometry(geometry: Geometry) -> Geometry``` method reworks the geometry parameter to manage polar and antimeridian singularities. This process implements the **Polar inclusive algorithm**. The objective of this algorithm is to add the North/South Pole into the list of coordinates of the polygon at the antimeridian cross.

When the geometry contains the pole the single polygon geometry including the pole in its border point list is properly interpreted by displays systems. When the geometry does not contain the pole, the geometry is split among the antimeridian line.

```python
from shapely import wkt
from footprint_facility import rework_to_polygon_geometry

wkt_geometry='POLYGON((175.812988 -70.711365,-175.61055 -68.469902,-172.383392 -69.75074,178.803558 -72.136864,175.812988 -70.711365))'

geometry = wkt.loads(wkt_geometry)
reworked = rework_to_polygon_geometry(geometry)

print(reworked)
```

prints
```python
MULTIPOLYGON (((-180 -69.61708714060345, -175.61055 -68.469902, -172.383392 -69.75074, -180 -71.81292858935237, -180 -69.61708714060345)), 
              ((175.812988 -70.711365, 180 -69.61708714060345, 180 -71.81292858935237, 178.803558 -72.136864, 175.812988 -70.711365)))
```

This sample footprint is extracted from product `S1A_EW_SL1__1_DH_20240118T082036_20240118T082109_052158_064DFF_6639` not anymore accessible in data hub, but derived products are available such as `S1A_EW_OCN__2SDH_20240118T082040_20240118T082108_052158_064DFF_66CB.SAFE`. This data is accessible in the catalog [following this odata link](https://catalogue.dataspace.copernicus.eu/odata/v1/Products(ba5106b0-f9c4-490b-bc8e-2d7dbb829bf0))

View the output in Leaflet:  
![Leaflet](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_5.png)  
View the output in MapBox (https://geojson.io):  
![MapBox display](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img.png)  
View the output in OpenLayer:  
![OpenLayer Display](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_7.png)  
View the output in Cesium  
![Cesium display](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_6.png)  




The same method also manage footprint passing over pole area, for example product called `S3A_SL_1_RBT____20240101T234743_20240101T235043_20240103T092302_0179_107_230_1440_PS1_O_NT_004`
avaialble in catalog [following this odata link](https://catalogue.dataspace.copernicus.eu/odata/v1/Products(f189f02b-137f-4da4-b0d4-b9da66fcb5c8))  

![img_8.png](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_21.png)

```python
from shapely import wkt
from footprint_facility import rework_to_polygon_geometry

wkt_geometry='POLYGON((148.66 83.7852,152.864 83.7881,157.085 83.7477,161.246 83.6889,165.27 83.594,169.107 83.4668,172.868 83.3119,176.409 83.1294,179.768 82.9261,-177.09 82.6993,-174.112 82.4387,-171.356 82.1771,-168.826 81.8915,-166.413 81.5862,-164.187 81.2727,-162.124 80.9494,-160.207 80.6132,-158.378 80.271,-156.704 79.911,-155.155 79.5456,-153.715 79.1749,-152.364 78.797,-151.091 78.4225,-149.916 78.0337,-148.797 77.6345,-147.746 77.2423,-146.768 76.845,-145.838 76.4404,-144.979 76.034,-144.147 75.6258,-143.843 75.4683,-133.508 76.4059,-121.888 76.8854,-109.902 76.8263,-98.5116 76.2384,-98.4639 76.2441,-98.2252 76.4066,-97.6125 76.8338,-96.9351 77.2695,-96.2223 77.7014,-95.4704 78.1301,-94.67 78.554,-93.7717 78.9733,-92.7923 79.4003,-91.7963 79.8163,-90.6757 80.2289,-89.4578 80.6379,-88.1285 81.0437,-86.6584 81.4456,-85.117 81.8441,-83.3788 82.2296,-81.4475 82.6096,-79.3161 82.9811,-76.958 83.3328,-74.2774 83.6856,-71.3901 84.0125,-68.1774 84.3328,-64.59 84.6283,-60.5631 84.9038,-55.9807 85.139,-51.1282 85.3472,-45.8032 85.5231,-40.1262 85.6577,-34.1967 85.7497,-28.0603 85.8022,-21.787 85.7844,-21.7786 85.793,-14.5003 88.3719,133.773 88.9159,146.77 86.3469,148.66 83.7852))'
geometry = wkt.loads(wkt_geometry)
reworked = rework_to_polygon_geometry(geometry)

print(reworked)
```

returns

```
POLYGON ((148.66 83.7852, 152.864 83.7881, 157.085 83.7477, 161.246 83.6889, 165.27 83.594, 169.107 83.4668, 172.868 83.3119, 176.409 83.1294, 179.768 82.9261, 180 82.90935346912795, 180 90, -180 90, -180 82.90935346912795, -177.09 82.6993, -174.112 82.4387, -171.356 82.1771, -168.826 81.8915, -166.413 81.5862, -164.187 81.2727, -162.124 80.9494, -160.207 80.6132, -158.378 80.271, -156.704 79.911, -155.155 79.5456, -153.715 79.1749, -152.364 78.797, -151.091 78.4225, -149.916 78.0337, -148.797 77.6345, -147.746 77.2423, -146.768 76.845, -145.838 76.4404, -144.979 76.034, -144.147 75.6258, -143.843 75.4683, -133.508 76.4059, -121.888 76.8854, -109.902 76.8263, -98.5116 76.2384, -98.4639 76.2441, -98.2252 76.4066, -97.6125 76.8338, -96.9351 77.2695, -96.2223 77.7014, -95.4704 78.1301, -94.67 78.554, -93.7717 78.9733, -92.7923 79.4003, -91.7963 79.8163, -90.6757 80.2289, -89.4578 80.6379, -88.1285 81.0437, -86.6584 81.4456, -85.117 81.8441, -83.3788 82.2296, -81.4475 82.6096, -79.3161 82.9811, -76.958 83.3328, -74.2774 83.6856, -71.3901 84.0125, -68.1774 84.3328, -64.59 84.6283, -60.5631 84.9038, -55.9807 85.139, -51.1282 85.3472, -45.8032 85.5231, -40.1262 85.6577, -34.1967 85.7497, -28.0603 85.8022, -21.787 85.7844, -21.7786 85.793, -14.5003 88.3719, 133.773 88.9159, 146.77 86.3469, 148.66 83.7852))
```

View the output in Leaflet:  
![Leaflet display](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_8.png)  
View the output in MapBox (https://geojson.io)    
![MapBox 2D display](https://gitlab.com/be-prototypes/geofootprint-prototype/-/raw/main/img/img_9.png)
![MapBox 3D display](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_12.png)  
View the output in OpenLayer:  
![OpenLayer Display](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_10.png)  
View the output int Cesium   
![Cesium display](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_11.png)


A more complex footprint that includes overlapping can be retrieved from Sentinel-3 SLSTR products with name `S3A_SL_2_WST____20240224T211727_20240224T225826_20240226T033733_6059_109_228______MAR_O_NT_003.SEN3` also available in catalog [following this odata link](https://catalogue.dataspace.copernicus.eu/odata/v1/Products(67a2b237-50dc-4967-98ce-bad0fbc04ad3))    
![img_10.png](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_23.png)  


```python
from shapely import wkt
from footprint_facility import rework_to_polygon_geometry

wkt_geometry='POLYGON ((75.4813 -72.4831, 75.4641 -72.9385, 75.4825 -73.3926, 75.4667 -73.8533, 75.4859 -74.3095, 75.4892 -74.7668, 75.4863 -75.2255, 75.4766 -75.688, 75.5071 -76.138, 75.4855 -76.5976, 75.4994 -77.0502, 75.4912 -77.5039, 75.4804 -77.9674, 75.5255 -78.4229, 75.506 -78.8781, 75.5216 -79.339, 75.5372 -79.7913, 75.5373 -80.2465, 75.5329 -80.7048, 75.5299 -81.1598, 75.5171 -81.623, 75.5639 -82.078, 75.5458 -82.5362, 75.5075 -82.9892, 75.5671 -83.4508, 75.594 -83.9015, 75.5601 -84.3631, 75.5772 -84.8172, 75.5759 -85.2729, 75.6882 -85.7284, 75.6155 -85.8996, 99.0441 -85.5436, 123.827 -83.9119, 136.984 -81.6753, 144.524 -79.2029, 149.351 -76.6243, 152.729 -73.9903, 155.254 -71.3237, 157.243 -68.6363, 158.872 -65.9344, 160.25 -63.2219, 161.447 -60.5012, 162.509 -57.7739, 163.467 -55.0411, 164.345 -52.3034, 165.16 -49.5614, 165.925 -46.8156, 166.65 -44.0663, 167.342 -41.3137, 168.008 -38.558, 168.652 -35.7995, 169.279 -33.0384, 169.893 -30.2748, 170.495 -27.5089, 171.09 -24.741, 171.679 -21.9712, 172.265 -19.1997, 172.849 -16.4268, 173.433 -13.6528, 174.019 -10.8778, 174.61 -8.10221, 175.205 -5.32624, 175.808 -2.55022, 176.42 0.225521, 177.043 3.00064, 177.679 5.77478, 178.33 8.54753, 178.999 11.3185, 179.688 14.0872, -179.6 16.8532, -178.861 19.6159, -178.092 22.3748, -177.288 25.1292, -176.444 27.8785, -175.554 30.6218, -174.611 33.3581, -173.607 36.0865, -172.531 38.8056, -171.373 41.5139, -170.116 44.2097, -168.743 46.8906, -167.231 49.5539, -165.552 52.1959, -163.669 54.8122, -161.536 57.3968, -159.092 59.9417, -156.259 62.4363, -152.931 64.8659, -148.97 67.21, -144.196 69.4397, -138.378 71.514, -131.251 73.3747, -122.56 74.9431, -112.195 76.1196, -100.397 76.7995, -87.8992 76.9054, -75.7446 76.4234, -64.8174 75.4121, -55.5302 73.9711, -47.8722 72.2041, -41.6199 70.1983, -36.5031 68.0184, -32.2759 65.7113, -28.7407 63.3095, -25.7211 60.8146, -23.1527 58.2859, -20.9197 55.7142, -18.956 53.1084, -17.2107 50.4749, -15.6443 47.8187, -14.2259 45.1438, -12.931 42.4532, -11.7401 39.7492, -10.6373 37.0339, -9.60971 34.3089, -8.64659 31.5754, -7.73911 28.8348, -6.87981 26.0878, -6.06243 23.3354, -5.28156 20.5783, -4.53257 17.8171, -3.81149 15.0525, -3.11477 12.285, -2.43933 9.51511, -1.78241 6.74326, -1.14151 3.9699, -0.51437 1.19541, 0.101093 -1.57983, 0.706828 -4.35545, 1.30468 -7.13115, 1.89642 -9.90659, 2.48378 -12.6815, 3.0685 -15.4556, 3.65232 -18.2286, 4.23706 -21.0002, 4.82464 -23.7704, 5.41711 -26.5387, 6.01674 -29.305, 6.62603 -32.0692, 7.24788 -34.831, 7.88562 -37.5902, 8.54317 -40.3466, 9.22526 -43.1001, 9.93764 -45.8504, 10.6874 -48.5973, 11.4837 -51.3405, 12.3381 -54.0796, 13.266 -56.8141, 14.2879 -59.5433, 15.4325 -62.2664, 16.7404 -64.9819, 18.2714 -67.6878, 20.1175 -70.3808, 22.4275 -73.0557, 25.456 -75.7029, 29.6757 -78.3048, 36.0471 -80.8235, 46.7204 -83.1675, 66.5853 -85.0811, 100.702 -85.909, 100.825 -85.9, 100.8 -85.7265, 100.836 -85.2741, 100.835 -84.8184, 100.817 -84.3644, 100.753 -83.9016, 100.799 -83.4425, 100.759 -82.9905, 100.797 -82.5372, 100.743 -82.0785, 100.767 -81.6235, 100.78 -81.16, 100.732 -80.7044, 100.74 -80.2457, 100.733 -79.7918, 100.719 -79.34, 100.758 -78.8787, 100.726 -78.4261, 100.732 -77.9704, 100.741 -77.5078, 100.718 -77.0519, 100.734 -76.5887, 100.728 -76.1405, 100.756 -75.6831, 100.71 -75.2283, 100.717 -74.7686, 100.712 -74.3119, 100.75 -73.8494, 100.706 -73.4005, 100.75 -72.9462, 100.719 -72.4834, 100.689 -72.4834, 91.3873 -72.2634, 82.4869 -71.616, 74.3385 -70.5836, 67.1017 -69.2238, 60.7981 -67.5957, 55.3608 -65.7531, 50.6834 -63.7411, 46.6526 -61.5953, 43.1618 -59.3436, 40.1192 -57.0075, 37.4483 -54.6035, 35.086 -52.1444, 32.9811 -49.64, 31.0922 -47.0982, 29.3854 -44.5249, 27.8333 -41.9253, 26.4133 -39.3032, 25.1067 -36.6619, 23.8983 -34.0041, 22.7752 -31.332, 21.7265 -28.6474, 20.7433 -25.952, 19.8177 -23.2472, 18.9432 -20.5341, 18.1142 -17.8139, 17.3258 -15.0873, 16.5739 -12.3553, 15.8547 -9.61856, 15.165 -6.8778, 14.5022 -4.13359, 13.8636 -1.38652, 13.2472 1.36292, 12.6511 4.11426, 12.0734 6.86705, 11.5129 9.62091, 10.968 12.3755, 10.4375 15.1304, 9.92058 17.8853, 9.41609 20.64, 8.92326 23.3942, 8.44135 26.1477, 7.96971 28.9002, 7.5078 31.6517, 7.05516 34.4018, 6.61142 37.1506, 6.17631 39.8979, 5.74967 42.6435, 5.33147 45.3876, 4.92181 48.1299, 4.521 50.8705, 4.12959 53.6094, 3.74844 56.3466, 3.37891 59.0822, 3.02299 61.8161, 2.68373 64.5486, 2.36316 67.3032, 2.07425 70.0328, 1.82645 72.7612, 1.64156 75.4883, 1.56185 78.2142, 1.68051 80.9387, 2.25149 83.6613, 4.29171 86.3786, 20.3724 89.0493, 166.781 88.1169, 172.888 85.413, 174.157 82.693, 174.516 79.9695, 174.547 77.2444, 174.423 74.518, 174.213 71.7903, 173.948 69.0614, 173.648 66.3312, 173.322 63.5996, 172.977 60.8664, 172.616 58.1317, 172.242 55.3954, 171.857 52.6574, 171.462 49.9177, 171.058 47.1763, 170.646 44.4331, 170.224 41.6883, 169.795 38.9418, 169.357 36.1937, 168.91 33.4442, 168.454 30.6933, 167.989 27.9411, 167.514 25.1879, 167.028 22.4339, 166.531 19.6791, 166.022 16.924, 165.501 14.1687, 164.965 11.4136, 164.415 8.65892, 163.849 5.90507, 163.265 3.15242, 162.661 0.401369, 162.038 -2.34762, 161.391 -5.09407, 160.719 -7.83745, 160.019 -10.5772, 159.289 -13.3126, 158.524 -16.0431, 157.722 -18.7679, 156.878 -21.486, 155.986 -24.1966, 155.041 -26.8985, 154.035 -29.5905, 152.962 -32.2711, 151.81 -34.9387, 150.568 -37.5912, 149.224 -40.2263, 147.759 -42.841, 146.156 -45.4321, 144.388 -47.995, 142.428 -50.5246, 140.237 -53.0142, 137.773 -55.4553, 134.979 -57.8371, 131.788 -60.1457, 128.119 -62.3629, 123.873 -64.4652, 118.942 -66.4222, 113.21 -68.1949, 106.583 -69.7353, 99.0172 -70.9868, 90.5777 -71.8897, 81.482 -72.3907, 75.4813 -72.4831))'
geometry = wkt.loads(wkt_geometry)
reworked = rework_to_polygon_geometry(geometry)

print(reworked)
```

returns

```
POLYGON ((75.58244101140099 -85.29943099459616, 66.5853 -85.0811, 46.7204 -83.1675, 36.0471 -80.8235, 29.6757 -78.3048, 25.456 -75.7029, 22.4275 -73.0557, 20.1175 -70.3808, 18.2714 -67.6878, 16.7404 -64.9819, 15.4325 -62.2664, 14.2879 -59.5433, 13.266 -56.8141, 12.3381 -54.0796, 11.4837 -51.3405, 10.6874 -48.5973, 9.93764 -45.8504, 9.22526 -43.1001, 8.54317 -40.3466, 7.88562 -37.5902, 7.24788 -34.831, 6.62603 -32.0692, 6.01674 -29.305, 5.41711 -26.5387, 4.82464 -23.7704, 4.23706 -21.0002, 3.65232 -18.2286, 3.0685 -15.4556, 2.48378 -12.6815, 1.89642 -9.90659, 1.30468 -7.13115, 0.706828 -4.35545, 0.101093 -1.57983, -0.51437 1.19541, -1.14151 3.9699, -1.78241 6.74326, -2.43933 9.51511, -3.11477 12.285, -3.81149 15.0525, -4.53257 17.8171, -5.28156 20.5783, -6.06243 23.3354, -6.87981 26.0878, -7.73911 28.8348, -8.64659 31.5754, -9.60971 34.3089, -10.6373 37.0339, -11.7401 39.7492, -12.931 42.4532, -14.2259 45.1438, -15.6443 47.8187, -17.2107 50.4749, -18.956 53.1084, -20.9197 55.7142, -23.1527 58.2859, -25.7211 60.8146, -28.7407 63.3095, -32.2759 65.7113, -36.5031 68.0184, -41.6199 70.1983, -47.8722 72.2041, -55.5302 73.9711, -64.8174 75.4121, -75.7446 76.4234, -87.8992 76.9054, -100.397 76.7995, -112.195 76.1196, -122.56 74.9431, -131.251 73.3747, -138.378 71.514, -144.196 69.4397, -148.97 67.21, -152.931 64.8659, -156.259 62.4363, -159.092 59.9417, -161.536 57.3968, -163.669 54.8122, -165.552 52.1959, -167.231 49.5539, -168.743 46.8906, -170.116 44.2097, -171.373 41.5139, -172.531 38.8056, -173.607 36.0865, -174.611 33.3581, -175.554 30.6218, -176.444 27.8785, -177.288 25.1292, -178.092 22.3748, -178.861 19.6159, -179.6 16.8532, -180 15.299267415730355, -180 90, 180 90, 180 15.299267415730355, 179.688 14.0872, 178.999 11.3185, 178.33 8.54753, 177.679 5.77478, 177.043 3.00064, 176.42 0.225521, 175.808 -2.55022, 175.205 -5.32624, 174.61 -8.10221, 174.019 -10.8778, 173.433 -13.6528, 172.849 -16.4268, 172.265 -19.1997, 171.679 -21.9712, 171.09 -24.741, 170.495 -27.5089, 169.893 -30.2748, 169.279 -33.0384, 168.652 -35.7995, 168.008 -38.558, 167.342 -41.3137, 166.65 -44.0663, 165.925 -46.8156, 165.16 -49.5614, 164.345 -52.3034, 163.467 -55.0411, 162.509 -57.7739, 161.447 -60.5012, 160.25 -63.2219, 158.872 -65.9344, 157.243 -68.6363, 155.254 -71.3237, 152.729 -73.9903, 149.351 -76.6243, 144.524 -79.2029, 136.984 -81.6753, 123.827 -83.9119, 100.82387906202558 -85.42641978721186, 100.8 -85.7265, 100.825 -85.9, 100.702 -85.909, 90.8040265674998 -85.66880876800023, 75.6155 -85.8996, 75.6882 -85.7284, 75.58244101140099 -85.29943099459616), (88.11476108761217 -72.02536107007776, 90.5777 -71.8897, 99.0172 -70.9868, 106.583 -69.7353, 113.21 -68.1949, 118.942 -66.4222, 123.873 -64.4652, 128.119 -62.3629, 131.788 -60.1457, 134.979 -57.8371, 137.773 -55.4553, 140.237 -53.0142, 142.428 -50.5246, 144.388 -47.995, 146.156 -45.4321, 147.759 -42.841, 149.224 -40.2263, 150.568 -37.5912, 151.81 -34.9387, 152.962 -32.2711, 154.035 -29.5905, 155.041 -26.8985, 155.986 -24.1966, 156.878 -21.486, 157.722 -18.7679, 158.524 -16.0431, 159.289 -13.3126, 160.019 -10.5772, 160.719 -7.83745, 161.391 -5.09407, 162.038 -2.34762, 162.661 0.401369, 163.265 3.15242, 163.849 5.90507, 164.415 8.65892, 164.965 11.4136, 165.501 14.1687, 166.022 16.924, 166.531 19.6791, 167.028 22.4339, 167.514 25.1879, 167.989 27.9411, 168.454 30.6933, 168.91 33.4442, 169.357 36.1937, 169.795 38.9418, 170.224 41.6883, 170.646 44.4331, 171.058 47.1763, 171.462 49.9177, 171.857 52.6574, 172.242 55.3954, 172.616 58.1317, 172.977 60.8664, 173.322 63.5996, 173.648 66.3312, 173.948 69.0614, 174.213 71.7903, 174.423 74.518, 174.547 77.2444, 174.516 79.9695, 174.157 82.693, 172.888 85.413, 166.781 88.1169, 20.3724 89.0493, 4.29171 86.3786, 2.25149 83.6613, 1.68051 80.9387, 1.56185 78.2142, 1.64156 75.4883, 1.82645 72.7612, 2.07425 70.0328, 2.36316 67.3032, 2.68373 64.5486, 3.02299 61.8161, 3.37891 59.0822, 3.74844 56.3466, 4.12959 53.6094, 4.521 50.8705, 4.92181 48.1299, 5.33147 45.3876, 5.74967 42.6435, 6.17631 39.8979, 6.61142 37.1506, 7.05516 34.4018, 7.5078 31.6517, 7.96971 28.9002, 8.44135 26.1477, 8.92326 23.3942, 9.41609 20.64, 9.92058 17.8853, 10.4375 15.1304, 10.968 12.3755, 11.5129 9.62091, 12.0734 6.86705, 12.6511 4.11426, 13.2472 1.36292, 13.8636 -1.38652, 14.5022 -4.13359, 15.165 -6.8778, 15.8547 -9.61856, 16.5739 -12.3553, 17.3258 -15.0873, 18.1142 -17.8139, 18.9432 -20.5341, 19.8177 -23.2472, 20.7433 -25.952, 21.7265 -28.6474, 22.7752 -31.332, 23.8983 -34.0041, 25.1067 -36.6619, 26.4133 -39.3032, 27.8333 -41.9253, 29.3854 -44.5249, 31.0922 -47.0982, 32.9811 -49.64, 35.086 -52.1444, 37.4483 -54.6035, 40.1192 -57.0075, 43.1618 -59.3436, 46.6526 -61.5953, 50.6834 -63.7411, 55.3608 -65.7531, 60.7981 -67.5957, 67.1017 -69.2238, 74.3385 -70.5836, 82.4869 -71.616, 88.11476108761217 -72.02536107007776))
```
View the output in Leaflet:  
![Leaflet display](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_14.png)

View the output in MapBox (https://geojson.io):  
![MapBox 2D display](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_4.png)
![MapBox 3D display](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_13.png)

View the output in OpenLayer:
![OpenLayer Display](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_15.png)

View the output in Cesium  
![Cesium display](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_16.png)  



The ```rework_to_linestring_geometry(geometry: Geometry) -> Geometry``` elaborates more or less complex linestring geometry from thin polygon and manage the antimeridian cross. For example, the product named
`S3A_SR_2_LAN_LI_20240302T235923_20240303T001845_20240304T182116_1161_109_330______PS1_O_ST_005` is available in catalog and can be accessed [by following this odata link](https://catalogue.dataspace.copernicus.eu/odata/v1/Products(1a50ce1b-f630-46a5-917b-b35d1b265db1))  
![img_11.png](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_24.png)  

```python
from shapely import wkt
from footprint_facility import rework_to_linestring_geometry

wkt_geometry='POLYGON ((-44.6919 59.6012, -45.9328 61.3301, -47.303 63.0483, -48.8281 64.7538, -50.5403 66.4439, -52.4808 68.1153, -54.7026 69.7634, -57.2749 71.3821, -60.2887 72.9632, -63.8633 74.4954, -68.1552 75.9627, -73.3645 77.3427, -79.7337 78.6037, -87.5189 79.7021, -96.9041 80.5808, -107.835 81.1742, -119.831 81.4228, -131.996 81.2971, -143.357 80.8124, -153.278 80.0208, -161.581 78.9883, -168.392 77.7757, -173.958 76.431, -178.529 74.9898, 177.678 73.477, 174.493 71.9106, 171.786 70.3033, 169.456 68.6641, 167.429 66.9998, 165.646 65.3154, 164.063 63.6146, 162.645 61.9002, 161.363 60.1746, 160.197 58.4395, 159.129 56.6962, 158.144 54.946, 157.23 53.1896, 156.378 51.4279, 155.579 49.6615, 155.582 49.661, 156.38 51.4274, 157.233 53.1891, 158.146 54.9454, 159.132 56.6957, 160.201 58.4389, 161.367 60.174, 162.648 61.8996, 164.067 63.6139, 165.65 65.3147, 167.433 66.9991, 169.461 68.6633, 171.79 70.3024, 174.498 71.9097, 177.683 73.4761, -178.524 74.9887, -173.952 76.4299, -168.386 77.7744, -161.575 78.9869, -153.273 80.0193, -143.353 80.8107, -131.994 81.2953, -119.831 81.421, -107.837 81.1725, -96.9086 80.5792, -87.5244 79.7006, -79.7396 78.6023, -73.3705 77.3414, -68.1609 75.9616, -63.8688 74.4944, -60.2939 72.9623, -57.2799 71.3812, -54.7072 69.7626, -52.4851 68.1145, -50.5444 66.4432, -48.832 64.7531, -47.3067 63.0476, -45.9363 61.3295, -44.6952 59.6006, -44.6919 59.6012))'
geometry = wkt.loads(wkt_geometry)
reworked = rework_to_linestring_geometry(geometry)

print(reworked)
```

results the following multilinestring geometry:
```
MULTILINESTRING ((-180 74.40789473684211, -178.5 75, -174 76.4, -168.4 77.8, -161.6 79, -153.3 80, -143.4 80.8, -132 81.3, -119.8 81.4, -107.8 81.2, -96.9 80.6, -87.5 79.7, -79.7 78.6, -73.4 77.3, -68.2 76, -63.9 74.5, -60.3 73, -57.3 71.4, -54.7 69.8, -52.5 68.1, -50.5 66.4, -48.8 64.8, -47.3 63, -45.9 61.3, -44.7 59.6), (155.6 49.7, 156.4 51.4, 157.2 53.2, 158.1 54.9, 159.1 56.7, 160.2 58.4, 161.4 60.2, 162.6 61.9, 164.1 63.6, 165.6 65.3, 167.4 67, 169.5 68.7, 171.8 70.3, 174.5 71.9, 177.7 73.5, 180 74.40789473684211))
```
View the output in Leaflet:  
![Leaflet display](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_3.png)  

View the output in MapBox (https://geojson.io):  
![MapBox 2D display](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_2.png)
![MapBox 3D display](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_18.png)  

View the output in OpenLayer:  
![OpenLayer Display](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_19.png)  

View the output in Cesium  
![Cesium display](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_20.png)   



The ```check_cross_antimeridian(geometry: Geometry) -> bool``` method checks if the footprint pass over the antimeridian. The recognition of the antimeridian line is based on array list single comparison and can be considered fast.
```python
from shapely import wkt
from footprint_facility import check_cross_antimeridian

wkt_geometry='POLYGON((175.812988 -70.711365,-175.61055 -68.469902,-172.383392 -69.75074,178.803558 -72.136864,175.812988 -70.711365))'

geometry = wkt.loads(wkt_geometry)
print(check_cross_antimeridian(geometry))
```
returns

```python
True
```

## Export facilities
### GeoJSON Output 
The ```to_geojson(geometry: Geometry) -> str``` returns a geojson formatted string of the given geometry.
```python
from shapely import wkt
from footprint_facility import to_geojson, rework_to_polygon_geometry

wkt_geometry='POLYGON((175.812988 -70.711365,-175.61055 -68.469902,-172.383392 -69.75074,178.803558 -72.136864,175.812988 -70.711365))'

geometry = wkt.loads(wkt_geometry)
print(to_geojson(rework_to_polygon_geometry(geometry)))
```
returns

```json
{
  "features": [
    {
      "geometry": {
        "coordinates": [
          [
            [
              [
                -180,
                -69.617087
              ],
              [
                -175.61055,
                -68.469902
              ],
              [
                -172.383392,
                -69.75074
              ],
              [
                -180,
                -71.812929
              ],
              [
                -180,
                -69.617087
              ]
            ]
          ],
          [
            [
              [
                175.812988,
                -70.711365
              ],
              [
                180,
                -69.617087
              ],
              [
                180,
                -71.812929
              ],
              [
                178.803558,
                -72.136864
              ],
              [
                175.812988,
                -70.711365
              ]
            ]
          ]
        ],
        "type": "MultiPolygon"
      },
      "id": "15943947-67bd-4515-87c5-454fdc23db2e",
      "properties": {},
      "type": "Feature"
    }
  ],
  "type": "FeatureCollection"
}
```
### WKT Output
The ```to_wkt(geometry: Geometry) -> str``` returns a WKT formatted string of the given geometry. 
```python
from shapely import wkt
from footprint_facility import to_wkt, rework_to_polygon_geometry

wkt_geometry='POLYGON((175.812988 -70.711365,-175.61055 -68.469902,-172.383392 -69.75074,178.803558 -72.136864,175.812988 -70.711365))'

geometry = wkt.loads(wkt_geometry)
print(to_wkt(rework_to_polygon_geometry(geometry)))
```
returns

```python
MULTIPOLYGON (
   ((-180 -69.61708714060345, -175.61055 -68.469902, -172.383392 -69.75074, -180 -71.81292858935237, -180 -69.61708714060345)),
   ((175.812988 -70.711365, 180 -69.61708714060345, 180 -71.81292858935237, 178.803558 -72.136864, 175.812988 -70.711365)))
```

## Footprint simplification function
Products such as "S3 Synergy" contains up to 290 points whereas they footprints are single rectangles. Others huge along track acquisition also contains greate number of coordinates. The footprint containing many points could be simplify improve indexing and display services.   
This facility module decorates 2 identified algorithms to simplify these footprints:
- Douglas–Peucker algorithm that is implemented into the shapely geometry library wrapped here as `footprint_facility.simplify`.
- Convex hull algorithm can be used to reduce de number of points assembly footprint with many polygons. The algorithm is also already implemented in the shapely library.

### The Douglas-Peucker algorithm
The Douglas-Peucker algorithm is an algorithm that decimates a curve composed of line segments to a similar curve with fewer points. It was one of the earliest successful algorithms developed for cartographic generalization.  
The purpose of the algorithm is, given a curve composed of line segments, to find a similar curve with fewer points. The algorithm defines 'dissimilar' based on the maximum distance between the original curve and the simplified curve. The simplified curve consists of a subset of the points that defined the original curve.  
The shapely library used in the footprint_facility module implements this algorithm of simplification. The definition of the distance to be used for the simplification shall be carefully defined to minimize the surface change.

This later distance is also called tolerance. It is expressed in the unit of geometry (degrees for our footprints). As the size of degrees varies according to the latitude of the points, the choice of the tolerance is not trivial to define wrt the footprint is localised closed to the polar areas or the equator. To simplify this inaccuracy, version 1.7 of the library introduces the possibility to specify the tolerance in metres thanks to the `tolerance_in_metre` flag.

Code simplification snippet  
```python
from footprint_facility import rework_to_polygon_geometry, to_geojson, simplify
 
geometry = rework_to_polygon_geometry(origin_geometry)
geojson = to_geojson(simplify(geometry, tolerance=0.4, tolerance_in_meter=False))
 
print(geojson)
```

![img.png](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_25.png)
We observe the algorithm is quite efficient and reduced the larger the number of points between tolerance set between 0.005 and 0.5:

![img_1.png](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_26.png)
The variation of the surface regarding reduction of the number of point is not significant.

#### More Complex footprints

When the footprint crosses antimeridian or pass other the poles, the polygon is not anymore properly supported by the algortihm. it is recommended to systematically manage rework of polygon before performing the simplification.

Example of Footprints crossing antimeridian and pole. The Douglas-Peucker algorithm properly manages this use case when antimeridian case has been previously handled. The pole area (polar inclusion solution) is also well supported:

![img_2.png](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_27.png)

The Use case of single footprint crossing antimeridian managed as multi-polygon are also well supported:
![img_3.png](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_28.png)

Sentinel-3 Synergy Data sets identified in the footprint category can be simplified:
![img_4.png](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_29.png)
Here, the 295 points are well aligned and a distance 0 properly simplifies the polygon.

### The Convex Hull algorithm 

The convex hull is the smallest convex polygon that encloses all points of a geometry. The Sentinel-1 wave-mode images are organized in a list of polygons, and the previously analyzed "Douglas-Peucker" optimization cannot be considered efficient enough to simplify them. The following scheme shows the convex hull (in purple) simplifying the wave-mode images of the set of polygons (in yellow) into a single enclosed polygon.

![img_5.png](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_30.png)
The curvature of the Earth is visible using an algorithm that considers coordinates in a Euclidean reference frame. The algorithm will be improved to support spherical coordinates, but the 2D convex hull used here reduces the number of points by 90%. The convex hull created an envelope that contains all the points of the wave mode without fitting the entire huge envelope (green shape): This algorithm remains a good solution for reducing the number of points to optimize indexing systems.


When using the convex hull algorithm with a footprint that crosses the antimeridian, it must be managed before applying the implementation. In the following scheme, the antimeridian is materialized in red and the footprint hull is spread on each side of the red line:

![img_6.png](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/img_31.png)

Code snippet to manage the footprint
```python
import shapely
from footprint_facility import rework_to_polygon_geometry, to_geojson
 
geometry = rework_to_polygon_geometry(origin_geometry)
 
# split eastern/wester part of the polygon
west_geometry = geometry.intersection(shapely.box(-180, -90, 0, 90))
east_geometry = geometry.intersection(shapely.box(0, -90, 180, 90))
 
convex_hull = shapely.MultiPolygon([east_geometry.convex_hull, west_geometry.convex_hull])
print (to_geojson(convex_hull))
```
### `fpstat` tool
Starting from version 1.5, the distribution comes with a tool dedicated to help analysing the discrepancies introduced by the optimizations. It loads a footprint in WKT or GeoJSON format, and apply an optimization to make a before/after comparison and identify added and removed section into the footprints.

```commandline
fpstat --help
usage: fpstat [-h] -f orig_footprint [-ff {wkt,geojson}] [-o output] [-r]
              [-p precision] [-a {simplify,convex_hull}] [-t tolerance] [-m]

compare footprint optimization results

options:
  -h, --help            show this help message and exit
  -f orig_footprint     the footprint to be optimized
  -ff {wkt,geojson}     passed footprint format (default=wkt)
  -o output             output file name of the results. The output format is selected
                        according to the file extension, if ".htm." HTML interactive
                        map is generated, otherwise results are returned in GeoJSON
                        format
  -r                    rework the footprint before optimization
  -p precision          defines the optimized/reworked footprint precision (default=0
                        no precision defined).
  -a {simplify,convex_hull}
                        selection of the footprint simplification algorithm
  -t tolerance          the simplify tolerance value
  -m                    the tolerance unit is in meter. Overwise no unit conversion is
                        performed from the geometry input (usually degrees)
```

Usage example with the [polygon crossing antimeridian](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/polygon.wkt)

```commandline
fpstat -o output.html -r -f "$(cat polygon.wkt)" -t 1.0
```
When providing `-o filename`, a GeoJSON file is generated with 4 main features:
 - the original geometry, with area in m<sup>2</sup> and its number of points in properties.
 - the reworked geometry, with its area in m<sup>2</sup>, its reduced number of points, and the selected tolerance in properties.
 - If exists, the geometry of the area added by the optimization and its area in m<sup>2</sup>
 - If exists, the geometry of the area removed by the optimization and its area in m<sup>2</sup>
```json
{
  "type": "FeatureCollection",
  "features": 
     [{"type": "Feature", 
       "id": "0", 
       "geometry": 
       {
         "type": "MultiPolygon", 
         "coordinates": [[[[106.44, -71.4926], [107.179, -72.1035], [107.92, -72.6785], [108.711, -73.2507], [109.555, -73.8191], [110.46, -74.3847], [111.428, -74.9449], [112.471, -75.5014], [113.595, -76.0528], [114.808, -76.5984], [116.121, -77.1376], [117.547, -77.6698], [119.098, -78.1939], [120.79, -78.7088], [122.641, -79.2133], [124.668, -79.7059], [126.895, -80.1846], [129.344, -80.6474], [132.042, -81.0921], [135.065, -81.5223], [141.004, -80.3652], [146.557, -78.8572], [150.818, -77.2759], [154.178, -75.6455], [156.895, -73.9811], [159.142, -72.2919], [161.038, -70.5835], [162.666, -68.8619], [164.084, -67.1292], [165.336, -65.3872], [166.457, -63.6378], [167.466, -61.8825], [168.387, -60.1222], [169.233, -58.3574], [170.016, -56.5887], [170.746, -54.8167], [171.43, -53.0416], [172.075, -51.2638], [172.686, -49.4835], [173.268, -47.701], [173.825, -45.9162], [174.359, -44.1293], [174.873, -42.3412], [175.37, -40.5512], [175.852, -38.7588], [176.32, -36.9658], [176.777, -35.171], [177.223, -33.3749], [177.66, -31.5775], [178.088, -29.779], [178.51, -27.9793], [178.925, -26.1785], [179.336, -24.3769], [179.741, -22.5742], [180.0, -21.411921], [180.0, 39.74572], [179.927, 39.2897], [179.637, 37.5022], [179.344, 35.714], [179.048, 33.9253], [178.749, 32.136], [178.446, 30.3462], [178.139, 28.5557], [177.829, 26.7649], [177.515, 24.9732], [177.197, 23.1829], [176.874, 21.3902], [176.547, 19.5975], [176.215, 17.8055], [175.878, 16.0132], [175.535, 14.2207], [175.187, 12.428], [174.833, 10.6359], [174.473, 8.84373], [174.107, 7.05198], [173.733, 5.26056], [173.352, 3.46961], [172.963, 1.67973], [172.566, -0.109789], [172.16, -1.89834], [171.745, -3.68586], [171.319, -5.47231], [170.884, -7.25724], [170.437, -9.04089], [169.978, -10.8229], [169.506, -12.603], [169.02, -14.3815], [168.519, -16.1574], [168.003, -17.93], [167.47, -19.7018], [166.918, -21.4703], [166.347, -23.2349], [165.754, -24.9965], [165.138, -26.7543], [164.497, -28.508], [163.829, -30.2574], [163.132, -32.0018], [162.402, -33.7409], [161.637, -35.4739], [160.834, -37.2011], [159.989, -38.9207], [159.097, -40.6325], [158.153, -42.336], [157.154, -44.0299], [156.091, -45.7131], [154.959, -47.3846], [153.749, -49.0427], [152.452, -50.686], [151.058, -52.3129], [149.555, -53.9205], [147.93, -55.5066], [146.165, -57.068], [144.245, -58.6014], [142.146, -60.1027], [139.848, -61.5663], [137.324, -62.9855], [134.544, -64.3539], [131.476, -65.6648], [128.089, -66.9054], [124.351, -68.0648], [120.232, -69.1303], [115.711, -70.0864], [110.785, -70.9165], [106.44, -71.4926]]], [[[-180.0, -21.411921], [-179.857, -20.7702], [-179.458, -18.9665], [-179.062, -17.1616], [-178.668, -15.3557], [-178.275, -13.5496], [-177.883, -11.7429], [-177.492, -9.93579], [-177.1, -8.12844], [-176.707, -6.32075], [-176.313, -4.51289], [-175.917, -2.70497], [-175.519, -0.897023], [-175.118, 0.910718], [-174.714, 2.71852], [-174.306, 4.52588], [-173.893, 6.33294], [-173.476, 8.13948], [-173.052, 9.9454], [-172.623, 11.7509], [-172.185, 13.5553], [-171.741, 15.3589], [-171.287, 17.1613], [-170.824, 18.9629], [-170.351, 20.7634], [-169.865, 22.5615], [-169.367, 24.3589], [-168.855, 26.1542], [-168.328, 27.9478], [-167.783, 29.7392], [-167.22, 31.5282], [-166.637, 33.3148], [-166.031, 35.0986], [-165.4, 36.8793], [-164.741, 38.6567], [-164.052, 40.4305], [-163.328, 42.2001], [-162.565, 43.9653], [-161.76, 45.7255], [-160.907, 47.4802], [-160.0, 49.2286], [-159.03, 50.9696], [-157.991, 52.7036], [-156.872, 54.4279], [-155.661, 56.142], [-154.344, 57.8444], [-152.904, 59.5326], [-151.322, 61.2048], [-149.571, 62.859], [-147.622, 64.4891], [-145.437, 66.0924], [-142.972, 67.6634], [-140.171, 69.1934], [-141.62, 69.545], [-143.114, 69.8836], [-144.657, 70.2092], [-146.248, 70.5213], [-147.888, 70.819], [-149.577, 71.1018], [-151.313, 71.3688], [-153.097, 71.6194], [-154.927, 71.853], [-156.8, 72.0689], [-158.716, 72.2664], [-160.672, 72.445], [-162.665, 72.6038], [-164.69, 72.7427], [-166.745, 72.8609], [-168.826, 72.9582], [-170.927, 73.034], [-173.043, 73.0882], [-175.171, 73.1193], [-175.385, 71.3448], [-175.609, 69.5687], [-175.841, 67.7931], [-176.08, 66.0178], [-176.322, 64.2393], [-176.569, 62.4618], [-176.821, 60.6838], [-177.076, 58.9046], [-177.334, 57.1252], [-177.596, 55.3449], [-177.859, 53.5635], [-178.127, 51.7821], [-178.397, 49.9996], [-178.669, 48.2164], [-178.944, 46.4324], [-179.222, 44.6478], [-179.503, 42.8624], [-179.787, 41.0763], [-180.0, 39.74572], [-180.0, -21.411921]]]]
       },
       "properties": 
       {
         "name": "Origin",
         "point no": 216,
         "area_in_m": 23008319024088.113,
         "area": "23008319.02 km<sup>2"
       }
     },{
       "type": "Feature", 
       "id": "0", 
       "geometry": {
         "type": "MultiPolygon", 
         "coordinates": [[[[106.44, -71.4926], [117.547, -77.6698], [135.065, -81.5223], [154.178, -75.6455], [165.336, -65.3872], [172.686, -49.4835], [180.0, -21.411921], [180.0, 39.74572], [169.02, -14.3815], [163.132, -32.0018], [156.091, -45.7131], [147.93, -55.5066], [137.324, -62.9855], [124.351, -68.0648], [106.44, -71.4926]]], [[[-180.0, -21.411921], [-170.351, 20.7634], [-162.565, 43.9653], [-152.904, 59.5326], [-140.171, 69.1934], [-156.8, 72.0689], [-175.171, 73.1193], [-180.0, 39.74572], [-180.0, -21.411921]]]]
       },
       "properties": {
         "name": "Optimized", 
         "point no": 24,
         "area_in_m": 23947672064379.215,
         "area": "23947672.06 km<sup>2",
         "tolerance": 1.0
       }
     },
       {
         "type": "Feature",
         "id": "0",
         "geometry": {
           "type": "MultiPolygon",
           "coordinates": [[[[180.0, 39.74572], [179.927, 39.2897], [179.637, 37.5022], [179.344, 35.714], [179.048, 33.9253], [178.749, 32.136], [178.446, 30.3462], [178.139, 28.5557], [177.829, 26.7649], [177.515, 24.9732], [177.197, 23.1829], [176.874, 21.3902], [176.547, 19.5975], [176.215, 17.8055], [175.878, 16.0132], [175.535, 14.2207], [175.187, 12.428], [174.833, 10.6359], [174.473, 8.84373], [174.107, 7.05198], [173.733, 5.26056], [173.352, 3.46961], [172.963, 1.67973], [172.566, -0.109789], [172.16, -1.89834], [171.745, -3.68586], [171.319, -5.47231], [170.884, -7.25724], [170.437, -9.04089], [169.978, -10.8229], [169.506, -12.603], [169.02, -14.3815], [180.0, 39.74572]]], [[[169.02, -14.3815], [168.519, -16.1574], [168.003, -17.93], [167.47, -19.7018], [166.918, -21.4703], [166.347, -23.2349], [165.754, -24.9965], [165.138, -26.7543], [164.497, -28.508], [163.829, -30.2574], [163.132, -32.0018], [169.02, -14.3815]]], [[[163.132, -32.0018], [162.402, -33.7409], [161.637, -35.4739], [160.834, -37.2011], [159.989, -38.9207], [159.097, -40.6325], [158.153, -42.336], [157.154, -44.0299], [156.091, -45.7131], [163.132, -32.0018]]], [[[156.091, -45.7131], [154.959, -47.3846], [153.749, -49.0427], [152.452, -50.686], [151.058, -52.3129], [149.555, -53.9205], [147.93, -55.5066], [156.091, -45.7131]]], [[[147.93, -55.5066], [146.165, -57.068], [144.245, -58.6014], [142.146, -60.1027], [139.848, -61.5663], [137.324, -62.9855], [147.93, -55.5066]]], [[[137.324, -62.9855], [134.544, -64.3539], [131.476, -65.6648], [128.089, -66.9054], [124.351, -68.0648], [137.324, -62.9855]]], [[[124.351, -68.0648], [120.232, -69.1303], [115.711, -70.0864], [110.785, -70.9165], [106.44, -71.4926], [124.351, -68.0648]]], [[[-180.0, -21.411921], [-179.857, -20.7702], [-179.458, -18.9665], [-179.062, -17.1616], [-178.668, -15.3557], [-178.275, -13.5496], [-177.883, -11.7429], [-177.492, -9.93579], [-177.1, -8.12844], [-176.707, -6.32075], [-176.313, -4.51289], [-175.917, -2.70497], [-175.519, -0.897023], [-175.118, 0.910718], [-174.714, 2.71852], [-174.306, 4.52588], [-173.893, 6.33294], [-173.476, 8.13948], [-173.052, 9.9454], [-172.623, 11.7509], [-172.185, 13.5553], [-171.741, 15.3589], [-171.287, 17.1613], [-170.824, 18.9629], [-170.351, 20.7634], [-180.0, -21.411921]]], [[[-170.351, 20.7634], [-169.865, 22.5615], [-169.367, 24.3589], [-168.855, 26.1542], [-168.328, 27.9478], [-167.783, 29.7392], [-167.22, 31.5282], [-166.637, 33.3148], [-166.031, 35.0986], [-165.4, 36.8793], [-164.741, 38.6567], [-164.052, 40.4305], [-163.328, 42.2001], [-162.565, 43.9653], [-170.351, 20.7634]]], [[[-162.565, 43.9653], [-161.76, 45.7255], [-160.907, 47.4802], [-160.0, 49.2286], [-159.03, 50.9696], [-157.991, 52.7036], [-156.872, 54.4279], [-155.661, 56.142], [-154.344, 57.8444], [-152.904, 59.5326], [-162.565, 43.9653]]], [[[-152.904, 59.5326], [-151.322, 61.2048], [-149.571, 62.859], [-147.622, 64.4891], [-145.437, 66.0924], [-142.972, 67.6634], [-140.171, 69.1934], [-152.904, 59.5326]]], [[[-175.171, 73.1193], [-175.385, 71.3448], [-175.609, 69.5687], [-175.841, 67.7931], [-176.08, 66.0178], [-176.322, 64.2393], [-176.569, 62.4618], [-176.821, 60.6838], [-177.076, 58.9046], [-177.334, 57.1252], [-177.596, 55.3449], [-177.859, 53.5635], [-178.127, 51.7821], [-178.397, 49.9996], [-178.669, 48.2164], [-178.944, 46.4324], [-179.222, 44.6478], [-179.503, 42.8624], [-179.787, 41.0763], [-180.0, 39.74572], [-175.171, 73.1193]]]]},
         "properties": {
           "name": "Added Part",
           "area_in_m": 864096294971.3123,
           "area": "864096.29 km<sup>2"
         }
       },
       {
         "type": "Feature",
         "id": "0",
         "geometry": {
           "type": "MultiPolygon",
           "coordinates": [[[[116.121, -77.1376], [114.808, -76.5984], [113.595, -76.0528], [112.471, -75.5014], [111.428, -74.9449], [110.46, -74.3847], [109.555, -73.8191], [108.711, -73.2507], [107.92, -72.6785], [107.179, -72.1035], [106.44, -71.4926], [117.547, -77.6698], [116.121, -77.1376]]], [[[132.042, -81.0921], [129.344, -80.6474], [126.895, -80.1846], [124.668, -79.7059], [122.641, -79.2133], [120.79, -78.7088], [119.098, -78.1939], [117.547, -77.6698], [135.065, -81.5223], [132.042, -81.0921]]], [[[150.818, -77.2759], [146.557, -78.8572], [141.004, -80.3652], [135.065, -81.5223], [154.178, -75.6455], [150.818, -77.2759]]], [[[164.084, -67.1292], [162.666, -68.8619], [161.038, -70.5835], [159.142, -72.2919], [156.895, -73.9811], [154.178, -75.6455], [165.336, -65.3872], [164.084, -67.1292]]], [[[172.075, -51.2638], [171.43, -53.0416], [170.746, -54.8167], [170.016, -56.5887], [169.233, -58.3574], [168.387, -60.1222], [167.466, -61.8825], [166.457, -63.6378], [165.336, -65.3872], [172.686, -49.4835], [172.075, -51.2638]]], [[[179.741, -22.5742], [179.336, -24.3769], [178.925, -26.1785], [178.51, -27.9793], [178.088, -29.779], [177.66, -31.5775], [177.223, -33.3749], [176.777, -35.171], [176.32, -36.9658], [175.852, -38.7588], [175.37, -40.5512], [174.873, -42.3412], [174.359, -44.1293], [173.825, -45.9162], [173.268, -47.701], [172.686, -49.4835], [180.0, -21.411921], [179.741, -22.5742]]], [[[-154.927, 71.853], [-153.097, 71.6194], [-151.313, 71.3688], [-149.577, 71.1018], [-147.888, 70.819], [-146.248, 70.5213], [-144.657, 70.2092], [-143.114, 69.8836], [-141.62, 69.545], [-140.171, 69.1934], [-156.8, 72.0689], [-154.927, 71.853]]], [[[-173.043, 73.0882], [-170.927, 73.034], [-168.826, 72.9582], [-166.745, 72.8609], [-164.69, 72.7427], [-162.665, 72.6038], [-160.672, 72.445], [-158.716, 72.2664], [-156.8, 72.0689], [-175.171, 73.1193], [-173.043, 73.0882]]]]},
         "properties": {
           "name": "Removed Part",
           "area_in_m": 75256745319.78705,
           "area": "75256.75 km<sup>2"
         }
       }
     ]
}
```

When the output file ends with `.html` extension (with `-o` option), the command line generates an interactive map to navigate inside the results. The layer displays both sources and optimized footprints, and when difference exists, it includes dedicated layers to show them. More layers are present to view added and removed area.
Each trace on map raises a tooltip to see the area of each trace and tne number of points:

![sample output](https://gitlab.com/be-prototypes/geofootprint-prototype/raw/main/img/fpstats_sample.png)

Starting from version 1.7, the tolerance can be provided into meter activating the `-m` parameter flag. The library expects geometries in geographic projection and coordinates are expressed in degrees. When setting the tolerance in meter, the footprint is internally converted in metric projection (Plate Carée global pojection also called Equidistant Cylindrical) to manage the Douglas-Pucker  algorithm in meter based distances. Then, once processed, the geometry is back to latlon to be returned as result.

Usage [sample](img/polygon.wkt) using 150Km tolerance
```commandline
fpstat -r -o output.json -f "$(cat polygon.wkt)" -t 150000 -m
```

result (coordinates removed):
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "0",
      "geometry": {
        "type": "MultiPolygon",
        "coordinates": [
            ...
        ]
      },
      "properties": {
        "name": "Origin",
        "point no": 216,
        "area_in_m": 23008319024088.113,
        "area": "23008319.02 km<sup>2"
      }
    },
    {
      "type": "Feature",
      "id": "0",
      "geometry": {
        "type": "MultiPolygon",
        "coordinates": [
            ...
        ]
      },
      "properties": {
        "name": "Optimized",
        "point no": 22,
        "area_in_m": 23987084887986.29,
        "area": "23987084.89 km<sup>2",
        "tolerance": 150000
      }
    },
    {
      "type": "Feature",
      "id": "0",
      "geometry": {
        "type": "MultiPolygon",
        "coordinates": [
            ...
        ]
      },
      "properties": {
        "name": "Added Part",
        "area_in_m": 903525190763.8513,
        "area": "903525.19 km<sup>2"
      }
    },
    {
      "type": "Feature",
      "id": "0",
      "geometry": {
        "type": "MultiPolygon",
        "coordinates": [
            ...
        ]
      },
      "properties": {
        "name": "Removed Part",
        "area_in_m": 75240673134.3222,
        "area": "75240.67 km<sup>2"
      }
    }
  ]
}


```

### Footprint simplification conclusion
Reducing the number of points in the EO data footprint can have a positive effect by optimizing the display and faster indexing systems. However, it may introduce inaccuracies in these footprints. For example, using the convex hull algorithm on a Sentinel-1 wave mode can reduce the number of points to 90%, the counterpart is the footprint will cover a larger area than the data. The `fpstat` tool provided within the later distributions help to identify these differences. 
The use of the Douglas-Peucker algorithm is also very efficient and according to the tolerance parameter, the simplified result footprint surface may not shift more than 1%. For example, we demonstrate that S3 SYNERGY products can be completely simplified with 0 tolerance without any surface modification. Other products, in particular long footprints with many points along tracks, can also be simplified by controlling the deviations with the tolerance.

## Developers Corner
### Set the footprint precision
The library can handle footprint precision, reducing the number of decimals in the geometries. By default, no precision is defined, and the geometry decimal number is managed according to the input geometries.

To define the precision, use the method `footprint_facility.set_precision(precision: float)`. The precision value must be greater than or equal to 0. A value of 0 means no precision is set. The precision value represents the grid size.

example of precision for &#x3C0;= 3.1415926535897...

| precision | value   |
|-----------|---------|
| 0         | &#x3C0; |
| 1         | 3       |
| 0.1       | 3.1     |
| 0.01      | 3.14    |
| 0.001     | 3.142   |
| 0.0001    | 3.1416  |
| 0.00001   | 3.14159 |

Usage example:
```python
from shapely import wkt
import footprint_facility
_wkt = """
    POLYGON((1.1337565834818406  47.53419913245443,  
             0.48102854059970923 43.46590619424384, 
             5.684268403836398 45.25814101702673,
             7.629303288477502  48.23334218606277,
            1.1337565834818406 47.53419913245443))
    """

geometry = wkt.loads(_wkt)
footprint_facility.set_precision(1)
reworked = footprint_facility.rework_to_polygon_geometry(geometry)
# expected POLYGON((1 47, 0 43, 6 45, 8 48, 1 47))
```
The current configured precision can be retrieved with function `footprint_facility.get_raise_exception()`

### Avoiding exceptions
The version 1.4 comes with the possibility to not raise errors when 
performing footprint rework. Default exception are active, but thy can easily be deactivated with `footprint_facility.set_raise_exception(False)` method:

```python
corrupted_wkt = ("POLYGON ((34.8393 42, 180 43, 180 90, -180 90, "
                 "-180 43, -178.089 41, 34.8393 42))")

footprint_facility.set_raise_exception(False)
rwrk = footprint_facility.rework_to_polygon_geometry(
    wkt.loads(corrupted_wkt))
```
In this case a warning message is logged onto the standard output and the footprint provided in input will be returned without any modification.
```
WARNING:footprint_facility:rework_to_polygon_geometry Cannot manage footprint (Points are aligned onto the antimeridian)
```
The message can be modified with reconfiguring the standard python logger named 'footprint_facility'.
### Control Performances 
The methods are completed with embedded performances metrics capabilities. To activate them, use the following `check_time` method:

```python
import footprint_facility 
footprint_facility.check_time(enable=True,
                              incremental=False,
                              summary_time=True)
```
`enable` parameter to `False` fully deactivate the time management.  
`incremental` parameter to `True` displays metrics during the execution.  
`summary_time` parameter to `True` stores metrics for future display with `footprint_facility.show_summary()`

Sample Output:
 ```
check_cross_antimeridian:	    0.69 μs/point
rework_to_polygon_geometry:	    6.94 μs/point
simplify:	                    1.00 μs/point
rework_to_linestring_geometry:      2.99 μs/point
 ```

The output is logged onto the standard output using the python logger. If the output is not visible, the logger could be quickly configured as followed:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

The footprint library uses a named logger `footprint_facility` that could be configured by clients.

### Code Style and Best Practices
- Use consistent quotation marks (preferably double quotes) throughout the code
- Follow PEP 8 guidelines for Python code
- Document all public methods and classes
- Include type hints for better code maintainability

## Prerequisites
- Python 3.8 or higher
- Required packages: pyproj, numpy, shapely, geojson
- Basic understanding of geographic coordinate systems

# Known issues
## East/West swaths larger than 180
When eastern distance between consecutive coordinates is longer than 180 and coordinates longitude sign is reverted (e.g. longitudes sequentially -175 then +175), the algorithm uses the smallest area and consider the polygon crossing the antimeridian. This scenario should never occur with EO footprints. 

## Licenses
This software is under Apache 2.0 License.  
It includes dynamic dependencies to the following libraries:

| Library name | License       | URL |
|--------------|---------------| -- |
| pyproj       | MIT           | https://github.com/pyproj4/pyproj/blob/3.6.1/LICENSE |
| numpy        | Modified BSD  | https://numpy.org/doc/stable/license.html |
| shapely      | BSD 3-Clause | https://github.com/shapely/shapely/blob/2.0.3/LICENSE.txt |
| geojson      | BSD 3-Clause | https://github.com/jazzband/geojson/blob/3.1.0/LICENSE.rst |
