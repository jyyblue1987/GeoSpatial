import rasterio
from rasterio.warp import transform
import os
import numpy as np
import math


# read GeoTiff Data using rasterio
dataset = rasterio.open('TroutPassAerial.tiff')
print(dataset.profile)

r = dataset.read(1)
g = dataset.read(2)
b = dataset.read(3)
# print(r)
# print(g)
# print(b)

ny, nx = dataset.height, dataset.width

bounds = dataset.bounds
xr = np.linspace(bounds.left, bounds.right, dataset.width)
yr = np.linspace(bounds.top, bounds.bottom, dataset.height)
x, y = np.meshgrid(xr, yr)

lon, lat = transform(dataset.crs, {'init': 'EPSG:4326'},
                     x.flatten(), y.flatten())

lon = np.asarray(lon).reshape((ny, nx))
lat = np.asarray(lat).reshape((ny, nx))

print(lon)
print(lat)



# read hgt data
fn = 'N38W079.hgt'

siz = os.path.getsize(fn)
dim = int(math.sqrt(siz/2))

assert dim*dim*2 == siz, 'Invalid file size'

hgt_data = np.fromfile(fn, np.dtype('>i2'), dim*dim).reshape((dim, dim))
# print(hgt_data)
