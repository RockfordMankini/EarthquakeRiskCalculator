ORGANIZATION OF THE FOLDER

--- Non-Feature Classes/Data ---

Earthquake.mxd - MXD file that has the toolbox loaded in.

Earthquake Kit - Toolkit that creates the earthquake damage index. Has relative pathing to Final.py; they need to be in the same directory to work.

Final.py - Script for the Earthquake Kit tool.

Presentation.pptx - Powerpoint Presentation for the tool.

Report.pdf/Report.docx - Report for the tool.

--- Feature Classes/Raster Data --- 

Here are the sample data used as a proof of concept for the tool. Their intended parameters when using the tool
are labelled.

### Major and Minor Fault Line Inputs
Faults/San_An.shp - San Andreas Faultline as it runs through Los Angeles county.
Faults/Minor.shp - Other minor faultlines as they run through Los Angeles county.

# Census Tracts Input
Census/Enriched_LA_County_Census_Tracts_2015.shp - Census tracts shapefile with demographic data.

# DEM Input
DEM/DEM1.tif - DEM of Los Angeles County.

# School/Hospitals Input
School_Hospitals/School_Hospitals.shp - Point shapefile of public schools/hospitals in Los Angeles County.

# Remap Ranges
Ranges.txt - Text file that has editable remap ranges for categorical rasters, in effect allowing one to alter the weights of each factor.
Has default values stored in text file.

# Output Folder Input
Index/ - Folder for the tool's output.

# Output Rasters
Index/index.tif - raster dataset of output raster. Overwritten when tool is run.
Index/indexCategorical.tif - raster dataset of output categorical raster. Overwritten when tool is run.
