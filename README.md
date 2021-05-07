# EGM722_Assignment-Simon_Whittaker
EGM722 Assessment Part 2: The GitHub repository

# Set-up / Installation
The repository containing the Python script and associated datasets is stored within GitHub at the following web address:
	https://github.com/SiWhitt/EGM722_Assignment-Simon_Whittaker.git
  
To make use of this repository, three criteria must be met.
  1.	The script and data must be copied from the repository.
  2.	An environment must be created from the repository environment.yml file using a python environment manager such as Anaconda Navigator. 
  3.	A python interpreter, such as PyCharm, should be used to run the code and produce the required outputs.

Those users already familiar, and comfortable, with such programs should fork or copy the repository, create an environment from the yml file using their preferred python environment manager and open the GIS_Tool.py file to run the code and create the output files. They can then skip to the Methodology section of this How to Guide. Additional information concerning datasets and dependencies can be found in the following paragraphs.

Users who are unfamiliar with these steps should carry out the instructions in Figures 1 - 3 (below) to obtain the suitable software, copy the data, and run the GIS_Tool.py script.

Figure 1, below, describes the necessary steps to obtain a copy of the GIS tool and data required to produce the output files.

![image](https://user-images.githubusercontent.com/80222749/117508809-2dc78c80-af57-11eb-8f15-1873737165da.png)
![image](https://user-images.githubusercontent.com/80222749/117508840-3750f480-af57-11eb-9a46-dd577f24f97f.png)

# Preparation and use of data
On completion of the repository download and extraction process it is possible to examine the data sets and files used to run the script, conduct the necessary analysis, and produce the required outputs. The raw data used within this project has been obtained from the Open Street Maps (OSM) repository and is available from:

  	https://download.geofabrik.de/europe/ireland-and-northern-ireland.html
    
OSM was chosen as it is licensed under the Open Data Commons Open Database License (OSM, 2021) which makes it available at no cost under a license agreement which ensure data can be freely shared, modified and used (ODbL, 2021).

The data_files folder has been split into 2 further folders to delineate which shapefiles are for display purposes only and which have been used in the analysis process. Files which will not undergo any analysis have been saved into the Simplified_Shapes folder for use in displaying Output 1, the overview / orientation map of Ireland. These shapefiles have been modified using ArcGIS to remove database entries thus simplifying the files and reducing their physical size. The knock-on effect is that these shape files require less storage and process more quickly when the project script runs.

The second folder, named Files_For_Analysis, contains the original shapefiles which have been re-named to simplify and clarify the script writing and reading process. These files are used to compute Output 2, the total length of rivers in each county, and Output 3 displaying the total area of waterbodies in each county in Ireland.

# Dependencies
Within the repository an environment.yml file can be found containing the dependencies required to ensure the GIS_Tool.py script runs smoothly and creates the required outputs after processing the datasets. When opened the following dependencies can be observed:

  •	Python – v 3.8.8 
  •	geopandas – v 0.9.0   
  •	cartopy – v 0.18.0 
  •	matplotlib – v 3.4.1 
  •	pandas – v 1.2.4 

To make use of these dependencies an environment, in which the dependencies have been installed, must be created. Figure 2, below, describes the steps to download Anaconda Navigator and create a python environment from the repository environment.yml file. This will ensure the GIS_Tool.py script runs smoothly to process the project datafiles and create the output files for further analysis.

![image](https://user-images.githubusercontent.com/80222749/117509010-80a14400-af57-11eb-968a-941f3eae27fb.png)
![image](https://user-images.githubusercontent.com/80222749/117509032-87c85200-af57-11eb-81aa-9d1a4ef42fc1.png)

Now that the environment has been created the user is free to install a python IDE to explore and run the GIS_Tool script. Figure 3, below, describes the steps to download and install PyCharm Community Edition

![image](https://user-images.githubusercontent.com/80222749/117509070-944caa80-af57-11eb-9dae-295c72757c49.png)
![image](https://user-images.githubusercontent.com/80222749/117509077-9878c800-af57-11eb-9a29-6256a43ccc6d.png)



