import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines


import pandas as pd
from cartopy.feature import ShapelyFeature
from shapely.geometry import Point, LineString, Polygon


# %matplotlib notebook #not sure if this is required for the work that I am doing

plt.ion() # make the plotting interactive

# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles


# create a scale bar of length 40 km in the lower right corner of the map
def scale_bar(ax, location=(0.9, 0.05)):
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]

    tmc = ccrs.TransverseMercator(sbllx, sblly)
    x0, x1, y0, y1 = ax.get_extent(tmc)
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    plt.plot([sbx, sbx - 40000], [sby, sby], color='k', linewidth=9, transform=tmc)
    plt.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=6, transform=tmc)
    plt.plot([sbx - 20000, sbx - 40000], [sby, sby], color='w', linewidth=6, transform=tmc)

    plt.text(sbx, sby - 8000, '40 km', transform=tmc, fontsize=6)
    plt.text(sbx - 25000, sby - 8000, '20 km', transform=tmc, fontsize=6)
    plt.text(sbx - 50000, sby - 8000, '0 km', transform=tmc, fontsize=6)


# load the outline of Northern Ireland and Ireland
outline = gpd.read_file('data_files/Ireland.shp')
outline = outline.to_crs(epsg=2158)

#load datasets for display on map
#water = gpd.read_file('data_files/Ire_Water.shp')
#water = water.to_crs(epsg=2158)

counties = gpd.read_file('data_files/Ire_Counties.shp')
counties = counties.to_crs(epsg=2158)




# create a figure of size 20x60 (representing the page size in inches)
myFig = plt.figure(figsize=(10, 30))

myCRS = ccrs.UTM(29)  # create a Universal Transverse Mercator reference system to transform our data.
ax = plt.axes(projection=ccrs.Mercator())  # finally, create an axes object in the figure, using a Mercator
# projection, where we can actually plot our data.

# first, we just add the outline of Northern Ireland using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor='w')
xmin, ymin, xmax, ymax = outline.total_bounds
ax.add_feature(outline_feature)  # add the features we've created to the map.

ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS) # set the extent to the boundaries of the NI outline

gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-10.5, -10, -9.5, -9, -8.5, -8, -7.5, -7, -6.5, -6, -5.5],
                         ylocs=[51, 51.5, 52, 52.5, 53, 53.5, 54, 54.5, 55])
gridlines.left_labels = False # turn off the left-side labels
gridlines.bottom_labels = False # turn off the bottom labels

#add datafiles to map
Counties = ShapelyFeature(counties['geometry'], myCRS,
                            edgecolor='k',
                            facecolor='w',
                            linewidth=1)
ax.add_feature(Counties)
""" Adding Water bodies to the map
Waterbodies = ShapelyFeature(water['geometry'], myCRS,
                            edgecolor='mediumblue',
                            facecolor='mediumblue',
                            linewidth=1)
ax.add_feature(Waterbodies)

"""


scale_bar(ax) #Add scale bar to map

ax. set(title='Island of Ireland with Towns and Shipwreck Locations') # Apply Title to Map of Ireland with Towns

myFig.savefig('map.png', bbox_inches='tight', dpi=300) #Save Map of Ireland as png file
