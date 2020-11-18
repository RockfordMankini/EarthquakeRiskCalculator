# Overview

This is a tool for ArcMap that can be used to analyze the potential threat levels of earthquakes. I do not claim any substantial domain knowledge about earthquakes, and this tool should NOT be used for serious analysis. With tweaks to the ranges/weights provided as a .txt file, however, it is possible that the tool could be used more effectively with more domain knowledge.

## ORGANIZATION OF THE FOLDER

* ## Non-Feature Classes/Data

  * **Earthquake.mxd** - MXD file that has the toolbox loaded in.

  * **Earthquake Kit** - Toolkit that creates the earthquake damage index. Has relative pathing to Final.py; they need to be in the same directory to work.

  * **Final.py** - Script for the Earthquake Kit tool.

Here are the sample data used as a demo for the tool. Their intended parameters when using the tool
are labelled.

* Feature Classes/Raster Data 

  * **Major and Minor Fault Line Inputs**
    * **Faults/San_An.shp** - San Andreas Faultline as it runs through Los Angeles county.
    * **Faults/Minor.shp** - Other minor faultlines as they run through Los Angeles county.

  **Census/Enriched_LA_County_Census_Tracts_2015.shp** - Census tracts shapefile with demographic data.

  * **DEM/DEM1.tif** - DEM of Los Angeles County.

  * **School_Hospitals/School_Hospitals.shp** - Point shapefile of public schools/hospitals in Los Angeles County.

  * **Ranges.txt** - Text file that has editable remap ranges for categorical rasters, in effect allowing one to alter the weights of each factor.
Has default values stored in text file.

  * **Index/** - Folder for the tool's output.
  
  * **Index/indexCategorical.tif** - raster dataset of output categorical raster. Overwritten when tool is run.
