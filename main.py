import rasterio
from rasterio.warp import transform
import os
import numpy as np
import math
import scipy as sp
import scipy.ndimage

# read GeoTiff Data using rasterio
dataset = rasterio.open('TroutPassAerial.tiff')
print(dataset.profile)

r = dataset.read(1)
g = dataset.read(2)
b = dataset.read(3)
# print(r)
# print(g)
# print(b)

print(dataset.xy(0, 0))
print(dataset.xy(dataset.height, dataset.width))

bounds = dataset.bounds
xr = np.linspace(bounds.left, bounds.right, dataset.width)
yr = np.linspace(bounds.top, bounds.bottom, dataset.height)
x, y = np.meshgrid(xr, yr)

lon, lat = transform(dataset.crs, {'init': 'EPSG:4326'},
                     x.flatten(), y.flatten())

lon = np.asarray(lon).reshape((dataset.height, dataset.width))
lat = np.asarray(lat).reshape((dataset.height, dataset.width))

# print(lon)
# print(lat)

# read hgt data
fn = 'N38W079.hgt'
start_lon = -79
start_lat = 38

siz = os.path.getsize(fn)
dim = int(math.sqrt(siz/2))

assert dim*dim*2 == siz, 'Invalid file size'

hgt_data = np.fromfile(fn, np.dtype('>i2'), dim*dim).reshape((dim, dim))
# print(hgt_data)
sigma_y = 40.0
sigma_x = 40.0
sigma = [sigma_y, sigma_x]

# Smooth the elevation layer
hgt_smooth_data = sp.ndimage.filters.gaussian_filter(hgt_data, sigma, mode='constant')

idx = 0
idy = 0
for r1, g1, b1, x1, y1, lon1, lat1 in zip(r, g, b, x, y, lon, lat):
    idx = 0
    for r2, g2, b2, x2, y2, lon2, lat2 in zip(r1, g1, b1, x1, y1, lon1, lat1):
        gap_lon = lon2 - start_lon
        gap_lat = lat2 - start_lat

        hgt_x = int(gap_lon * 3600)
        hgt_y = int(gap_lat * 3600)

        z2 = hgt_smooth_data[hgt_y][hgt_x]
        idx += 1

        print(x2, y2, z2, r2, g2, b2)

    idy += 1

print(idx, idy)





