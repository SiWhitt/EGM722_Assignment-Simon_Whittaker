""" GIS_Tool - This script produces 3 outputs which assist in the planning process for a fly fishing
trip to Ireland.

First, a planning map in png format will be produced which details Irish counties, significant settlements,
large waterbodies and contains a scale and co-ordinate system to help determine distance and travel time.

The second part of the script computes the total length of rivers in each county on the Island of Ireland
and displays this as a bar graph.

Finally a choropleth map will be produced containing the area of inland waterbodies in sq km for each county
in Ireland.
"""

# import the required modules to ensue that the scrip runs as intended
import matplotlib.lines as mlines
import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import pandas as pd


# load the required datasets from data_files folder and standardise the CRS of each shapefile.
outline = gpd.read_file('data_files/Simplified_Shapes/Ireland.shp')
outline = outline.to_crs(epsg=2158)

water = gpd.read_file('data_files/Simplified_Shapes/Ire_Water_simplified.shp')
water = water.to_crs(epsg=2158)

rivers = gpd.read_file('data_files/Files_for_analysis/Ire_Rivers_Canals.shp')
rivers = rivers.to_crs(epsg=2158)

counties = gpd.read_file('data_files/Files_for_analysis/Ire_Counties.shp')
counties = counties.to_crs(epsg=2158)

center_counties = gpd.read_file('data_files/Simplified_Shapes/Counties_Center_pts.shp')
center_counties = center_counties.to_crs(epsg=2158)

towns = gpd.read_file('data_files/Simplified_Shapes/Ire_Places_simplified.shp')
towns = towns.to_crs(epsg=2158)

water_per_county = gpd.read_file('data_files/Files_for_analysis/water_per_county.shp')

myCRS = ccrs.UTM(29)  # create a Universal Transverse Mercator reference system to transform our data.

""" Output 1 - The following lines of code produce a map to assist with the trip planning process"""

# generate matplotlib handles for inclusion on the planning map legend highlighting significant features
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    i: int
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

# create a scale bar of length 40 km to be positioned in the lower right corner of the map
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


# create a figure of page size 10 inches x 30 inches
output1 = plt.figure(figsize=(10, 30))

# create an axes object in output 1 using the mercator projection to allow data to be plotted
ax = plt.axes(projection=ccrs.Mercator())


# define map outline and figure extent. Set outline colors and add outline of Ireland to the map
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor='w')
xmin, ymin, xmax, ymax = outline.total_bounds
ax.add_feature(outline_feature)

# set map extent to the boundaries the Ireland outline
ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS)

# add gridlines to the map and modify to show labels on left and bottom sides of map
gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-10.5, -10, -9.5, -9, -8.5, -8, -7.5, -7, -6.5, -6, -5.5],
                         ylocs=[51, 51.5, 52, 52.5, 53, 53.5, 54, 54.5, 55])
gridlines.right_labels = False
gridlines.top_labels = False

# adding irish counties to the planing map for formating to look nice

Counties = ShapelyFeature(counties['geometry'], myCRS,
                          edgecolor='k',
                          facecolor='w',
                          linewidth=0.25)
ax.add_feature(Counties)

# adding significant waterbodies to the planning map and formatting
Waterbodies = ShapelyFeature(water['geometry'], myCRS,
                             edgecolor='mediumblue',
                             facecolor='mediumblue',
                             linewidth=1)
ax.add_feature(Waterbodies)

# adding significant cities / towns and formatting shape and color of symbols
town_handle = ax.plot(towns[towns['fclass'] == 'town'].geometry.x, towns[towns['fclass'] == 'town'].geometry.y, 's',
                      color='y', ms=6, transform=myCRS)

city_handle = ax.plot(towns[towns['fclass'] == 'city'].geometry.x, towns[towns['fclass'] == 'city'].geometry.y, '*',
                      color='r', ms=6, transform=myCRS)

# adding waterbodies and setting colour of these features to medium blue
water_handle = generate_handles(['Waterbodies'], ['mediumblue'])

# add the text labels for the significant cities / towns
for i, row in towns.iterrows():
    x, y = row.geometry.x, row.geometry.y
    plt.text(x, y, row['name'].title(), fontsize=6, transform=myCRS)

# add the names of each of the Irish counties in the center of the county
for i, row in center_counties.iterrows():
    x, y = row.geometry.x, row.geometry.y
    plt.text(x, y, row['name'].title(), fontsize=4, transform=myCRS)

# define the handles corresponding to features that will be included in the planning map legend
handles = city_handle + town_handle + water_handle
labels = ['Cities', 'Towns', 'Waterbodies']

# create legend from handles, format for presentation and place in upper left corner
leg = ax.legend(handles, labels, title='Legend', title_fontsize=14,
                fontsize=12, loc='upper left', frameon=True, framealpha=1)

# add scale bar to map
scale_bar(ax)

# create and add title to the planning map
ax.set(title='Map for planning fishing trips in Ireland')

# save the planning map to the data_files folder within the repository at a suitable resolution/dpi
output1.savefig('data_files/Planning Map.png', bbox_inches='tight', dpi=300)

"""The following lines of code use the rivers shapefile alongwith the counties shaprfile to produce a barchart
depicting the total lenght of rivers in each county in ireland and Northern Ireland"""

for i, row in rivers.iterrows():  # iterate over each row in the GeoDataFrame
    rivers.loc[i, 'Length'] = row['geometry'].length  # assign the row's geometry length to a new column, Length

# print(rivers.head())  # print the updated GeoDataFrame to see the changes

join = gpd.sjoin(rivers, counties)  # , how='inner', lsuffix='left', rsuffix='right') # perform the spatial join

join_total = join['Length'].sum()  # find the total length of roads in the join GeoDataFrame

clipped = []  # initialize an empty list
for county in counties['name'].unique():
    tmp_clip = gpd.clip(rivers, counties[counties['name'] == county])  # clip the roads by county border
    for i, row in tmp_clip.iterrows():
        tmp_clip.loc[i, 'Length'] = row['geometry'].length  # we have to update the length for any clipped roads
        tmp_clip.loc[i, 'name'] = county  # set the county name for each road feature
    clipped.append(tmp_clip)  # add the clipped GeoDataFrame to the

# pandas has a function, concat, which will combine (concatenate) a list of DataFrames (or GeoDataFrames)
# we can then create a GeoDataFrame from the combined DataFrame, as the combined DataFrame will have a geometry column.
clipped_gdf = gpd.GeoDataFrame(pd.concat(clipped))
clip_total = clipped_gdf['Length'].sum()

# print (clipped_gdf.groupby('name') [['Length']].sum()/1000)

total_rivers_per_county = (clipped_gdf.groupby('name')[['Length']].sum() / 1000)

fig = total_rivers_per_county.plot(kind='bar', width=0.8, rot=90,
                                   title= "Total Length (in km) of Rivers in Irish Counties")

plt.style.use('seaborn-dark-palette')
plt.minorticks_on()
plt.grid(which='both', axis='y', linestyle='-', linewidth='0.5', color='black')
plt.xlabel('Counties')
plt.ylabel('Total Length of Rivers in km')

plt.subplots_adjust(bottom=0.25, left=0.2)

# plt.show

output2 = fig.get_figure()
output2.savefig('data_files/Total Length of rivers in Irish Counties.png', transparent=True, dpi=300)

"""The following lines of code create a chloropleth map of the inland water area of counties in ireland 
to determine which would be best to visit for a fishing trip"""

output3, ax = plt.subplots(1, figsize=(12, 18))
# to make a nice colorbar that stays in line with our map, use these lines:
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

ax = water_per_county.plot(column='sum_area_s', ax=ax, vmin=0, vmax=275, cmap='bone_r', edgecolor='k',
                           legend=True, cax=cax, legend_kwds={'label': 'Total Area of Waterbodies in sq km'})

# create and add title to choropleth map of Ireland waterbodies
ax.set(title='Map of Irish counties with total area of inland waterbodies in sq km')

# Switch off the bounding box drawn round the map so it looks a bit tidier
ax.axis('off')

output3.savefig('data_files/Total area of inland water per county in ireland.png', dpi=300, bbox_inches='tight')
