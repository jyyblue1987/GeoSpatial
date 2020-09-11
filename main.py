import rasterio
import os
import numpy
import math

# read GeoTiff Data using rasterio
dataset = rasterio.open('TroutPassAerial.tiff')

print(dataset.width, dataset.height)
print(dataset.bounds)
print(dataset.transform)

print(dataset.transform * (0, 0))
print(dataset.transform * (dataset.width, dataset.height))

# crs = CRS.from_epsg(3005)
# print(crs)
print(dataset.crs)

r = dataset.read(1)
g = dataset.read(2)
b = dataset.read(3)
# print(r)
# print(g)
# print(b)


# read hgt data
fn = 'N38W079.hgt'

siz = os.path.getsize(fn)
dim = int(math.sqrt(siz/2))

assert dim*dim*2 == siz, 'Invalid file size'

hgt_data = numpy.fromfile(fn, numpy.dtype('>i2'), dim*dim).reshape((dim, dim))
print(hgt_data)