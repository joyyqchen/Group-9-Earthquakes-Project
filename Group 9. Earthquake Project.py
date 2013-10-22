# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import urllib
import json
import sys
import pandas as pd
import os

USE_CACHE = True
CACHE_NAME = 'geo_cache.csv'

url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson'

if USE_CACHE and not os.path.isfile(CACHE_NAME):
    print "Can't find Cache file. Using online version and creating one instead."
    USE_CACHE = False

if not USE_CACHE:
    d = json.loads(urllib.urlopen(url).read())
    data = pd.DataFrame(d.items()) # assuming you used json.load to get the data
    features = data[1].values[1] # since we don't care about metadata, bbox, etc.
    Src_list = []
    Eqid_list = []
    time_list = []
    nst_list = []
    region_list = []
    Lat_list = []
    Lon_list = []
    Depth_list = []
    Mag_list = []
    for quake in features:
        Src_list.append(quake['properties']['net'])
        Eqid_list.append(quake['properties']['code'])
        time_list.append(quake['properties']['time'])
        nst_list.append(quake['properties']['nst'])
        region_list.append(quake['properties']['place'])
        Mag_list.append(quake['properties']['mag'])
        Lon_list.append(quake['geometry']['coordinates'][0])
        Lat_list.append(quake['geometry']['coordinates'][1])
        Depth_list.append(quake['geometry']['coordinates'][2])
    data = pd.DataFrame({'Src':Src_list, 'Eqid':Eqid_list, 'time':time_list, 'nst':nst_list, 'region':region_list, 'Lat':Lat_list, 'Lon':Lon_list, 'Depth':Depth_list, 'Mag':Mag_list})
    #cleaned_data = data.dropna()
    clean_data = data
    clean_data.to_csv(CACHE_NAME, index = False)
else:
    clean_data = pd.read_csv(CACHE_NAME)

# <codecell>

# In the code above note that I saved the results of `data.dropna()` into a different variable `clean_data` rather than over-writing the old variable `data`. **Why?** Why not just re-use old variable names? And if we did re-use old variable names what extra danger do we have to keep in mind while using the IPython Notebook?
alaska = clean_data[clean_data.Src == 'ak']
print "ALASKA"
#print alaska[0:10]

def find_left_most(quakes):
    ll_lon = min(quakes.Lon)
    ll_lat = min(quakes.Lat)
    ur_lon = max(quakes.Lon)
    ur_lat = max(quakes.Lat)
    avg = quakes.Lon.mean()
    if avg < -150:
       ur_lon = -130
    return ll_lon, ll_lat, ur_lon, ur_lat
        
from mpl_toolkits.basemap import Basemap

def plot_quakes(quakes):
    ll_lon, ll_lat, ur_lon, ur_lat = find_left_most(quakes)
    print ll_lon
    print ll_lat
    print ur_lon
    print ur_lat
    m = Basemap(llcrnrlon=ll_lon,llcrnrlat=ll_lat,
                urcrnrlon=ur_lon,urcrnrlat=ur_lat,
                resolution='l',area_thresh=1000.,projection='merc',
                lat_0=62.9540,lon_0=-149.2697)
    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color='coral',lake_color='blue')
    m.drawmapboundary(fill_color='aqua')

    mags = quakes.Mag
    lons = quakes.Lon
    lats = quakes.Lat
    x, y = m(quakes.Lon, quakes.Lat)
    #Documentation from http://matplotlib.org/basemap/api/basemap_api.html#mpl_toolkits.basemap.Basemap.plot
    #Additional hints from http://stackoverflow.com/questions/8409095/matplotlib-set-markers-for-individual-points-on-a-line

    for key in x.keys(): #Note that an entry's data in the series share the same key.
        m.plot(x[key], y[key], marker='o', markersize=mags[key]*4, color='b', alpha = 0.5)
        #alpha is transparency
        #color is blue
        #marker size is magnitude * 4
        #marker is circular shaped
    #x, y = m(quakes.Lon, quakes.Lat)
    #m.plot(x, y, 'k.')
    return m

plot_quakes(alaska)
#plot_quakes(clean_data)

# <codecell>


# <codecell>


# <codecell>


