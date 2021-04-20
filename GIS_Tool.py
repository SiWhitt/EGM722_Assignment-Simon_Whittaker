import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import pandas as pd
from cartopy.feature import ShapelyFeature
from shapely.geometry import Point, LineString, Polygon

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

    tmc = ccrs.Mercator(sbllx, sblly)
    x0, x1, y0, y1 = ax.get_extent(tmc)
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    plt.plot([sbx, sbx - 40000], [sby, sby], color='k', linewidth=6, transform=tmc)
    plt.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=4, transform=tmc)
    plt.plot([sbx - 20000, sbx - 40000], [sby, sby], color='w', linewidth=4, transform=tmc)

    plt.text(sbx, sby - 8000, '40 km', transform=tmc, fontsize=5)
    plt.text(sbx - 25000, sby - 8000, '20 km', transform=tmc, fontsize=5)
    plt.text(sbx - 50000, sby - 8000, '0 km', transform=tmc, fontsize=5)



# load the outline of Northern Ireland and Ireland
outline = gpd.read_file('data_files/Simplified_Shapes/Ireland.shp')
outline = outline.to_crs(epsg=2158)



#load datasets for display on map
water = gpd.read_file('data_files/Files_for_analysis/Ire_Water.shp')
water = water.to_crs(epsg=2158)

counties = gpd.read_file('data_files/Files_for_analysis/Ire_Counties.shp')
counties = counties.to_crs(epsg=2158)

center_counties = gpd.read_file('data_files/Simplified_Shapes/Counties_Center_pts.shp')
center_counties = center_counties.to_crs(epsg=2158)

towns = gpd.read_file('data_files/Files_for_analysis/Ire_Places.shp')
towns = towns.to_crs(epsg=2158)


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
gridlines.right_labels = False # turn off the left-side labels
gridlines.top_labels = False # turn off the bottom labels

#add datafiles to map

""" Adding Ireland Counties to Map """
Counties = ShapelyFeature(counties['geometry'], myCRS,
                            edgecolor='k',
                            facecolor='w',
                            linewidth=0.25)
ax.add_feature(Counties)


# get a list of unique names for the county boundaries
#county_names = list(counties.name.unique())
#county_names.sort()  # sort the counties alphabetically by name



"""Adding Water bodies to the map"""
Waterbodies = ShapelyFeature(water['geometry'], myCRS,
                            edgecolor='mediumblue',
                            facecolor='mediumblue',
                            linewidth=1)
ax.add_feature(Waterbodies)

"""Adding Towns to the map"""
# ShapelyFeature creates a polygon, so for point data we can just use ax.plot()
# town_handle = ax.plot(towns.geometry.x, towns.geometry.y, 's', color='0.5', ms=6, transform=myCRS)

#town_handle = ax.plot(towns[towns['fclass'] == 'town'].geometry.x, towns[towns['fclass'] == 'town'].geometry.y, 's', color='0', ms=6, transform=myCRS)

city_handle = ax.plot(towns[towns['fclass'] == 'city'].geometry.x, towns[towns['fclass'] == 'city'].geometry.y, '*', color='r', ms=6, transform=myCRS)


"""
# add the text labels for the towns
for i, row in towns.iterrows():
    x, y = row.geometry.x, row.geometry.y
    plt.text(x, y, row['name'].title(), fontsize=8, transform=myCRS) # use plt.text to place a label at x,y
"""

"""
# add the text labels for the counties

##counties['coords'] = counties['geometry'].apply(lambda x: x.centroid.coords[:])
##counties['coords'] = [coords[0] for coords in counties['coords']]
"""
for i, row in center_counties.iterrows():
    x, y = row.geometry.x, row.geometry.y
    plt.text(x, y, row['name'].title(), fontsize=4, transform=myCRS) # use plt.text to place a label at x,y


# ax.legend() takes a list of handles and a list of labels corresponding to the objects you want to add to the legend
handles = city_handle
labels = ['Cities']

leg = ax.legend(handles, labels, title='Legend', title_fontsize=14,
                 fontsize=12, loc='upper left', frameon=True, framealpha=1)

"""
handles = county_handles + water_handle + river_handle + town_handle + city_handle
labels = nice_names + ['Lakes', 'Rivers', 'Towns', 'Cities']

leg = ax.legend(handles, labels, title='Legend', title_fontsize=14,
                 fontsize=12, loc='upper left', frameon=True, framealpha=1)


"""

scale_bar(ax) #Add scale bar to map

ax.set(title='Points of Interest within 20km of holiday day trip loction') # Apply Title to Map of Ireland with Towns

myFig.savefig('map.png', bbox_inches='tight', dpi=300) #Save Map of Ireland as png file