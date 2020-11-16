import arcpy
from arcpy.sa import *

fault_line = arcpy.GetParameterAsText(0) # major fault lines
minor_fault = arcpy.GetParameterAsText(1) # minor fault lines
census = arcpy.GetParameterAsText(2) # census tracts
DEM = arcpy.GetParameterAsText(3) # DEM used for slope calculation
hospital_school = arcpy.GetParameterAsText(4) # hospital/school shapefile
remapTxt = arcpy.GetParameterAsText(5) # remap textfile
folder = arcpy.GetParameterAsText(6) # putput folder

arcpy.env.workspace = folder
arcpy.env.overwriteOutput = True

# check for spatial license, if not present, end program immediately
try:
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")

    # grab remap textfile if given
    if remapTxt and remapTxt != "#":
        with open(remapTxt) as txt:
            line = txt.readline()
            cnt = 1
            # grab lines 2, 5, 8, etc., save the remap, turn it into a list and then tuple, and then feed to 
            while line:
                if cnt == 2:
                    range1 = line.strip()
                    range1 = tuple(eval(range1))
                if cnt == 5:
                    range2 = line.strip()
                    range2 = tuple(eval(range2))
                if cnt == 8:
                    range3 = line.strip()
                    range3 = tuple(eval(range3))
                if cnt == 11:
                    range4 = line.strip()
                    range4 = tuple(eval(range4))
                if cnt == 14:
                    range5 = line.strip()
                    range5 = tuple(eval(range5))
                if cnt == 17:
                    range6 = line.strip()
                    range6 = tuple(eval(range6))
                line = txt.readline()
                cnt += 1
    # if no remap is supplied, set ranges to default values
    else:
        range1 = [[0,10,5], [10,25,4], [25,50,3], [50,100,2], [100,200,1], [200,1000000,0]]
        range2 = [[0,3,15], [3,10,13], [10,25,11], [25,1000000,10]]
        range3 = [[0,.1,9], [.1,1000000,10]]
        range4 = [[0,500,0], [500, 10000, 1], [10000, 25000, 2], [25000, 1000000, 3]]
        range5 = [[0,10,10], [10, 20, 11], [20, 35, 12], [35, 60, 13], [60, 90, 14]]
        range6 = [[0,1,0], [1,3,1], [3,7,2], [7,10,3], [10,13,4], [13,16000000,5]]
                
    # set extent so euclidean distance raster is size of polygon shapefile
    arcpy.env.extent = arcpy.Describe(census).extent

    # constant raster that allows for raster math to turn distance raster from meters into miles
    outConstRaster = CreateConstantRaster(1609.344, "FLOAT")

    # raster used to allow categorical rasters to have decimal values for calculation in the final index
    outConstRaster2 = CreateConstantRaster(10.0, "FLOAT")

    ### MAJOR FAULT LINE DISTANCE CATEGORICAL RASTER

    # distance raster for major fault line, reproject to meters
    new_fault_line = arcpy.Project_management(fault_line, folder + "\Fault_Line_Project.shp", out_coor_system="PROJCS['NAD_1983_Contiguous_USA_Albers',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-96.0],PARAMETER['Standard_Parallel_1',29.5],PARAMETER['Standard_Parallel_2',45.5],PARAMETER['Latitude_Of_Origin',23.0],UNIT['Meter',1.0]]", transform_method="WGS_1984_(ITRF00)_To_NAD_1983", in_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")
    dist = arcpy.gp.EucDistance_sa(new_fault_line, folder + "\EucDist1.tif", "", "", "", "PLANAR")
    newDist = dist / outConstRaster

    # remap raster and save
    distRemap = RemapRange(range1)
    distCat = Reclassify(newDist, "VALUE", distRemap)
    distCat.save("distCat.tif")

    ### MINOR FAULT LINE DISTANCE CATEGORICAL RASTER
    if minor_fault and minor_fault != "#":
        
        # reproject minor line into meters distance projection, then make distance raster and convert to miles
        new_minor_line = arcpy.Project_management(minor_fault, folder + "\Minor_Fault_Project.shp", out_coor_system="PROJCS['NAD_1983_Contiguous_USA_Albers',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-96.0],PARAMETER['Standard_Parallel_1',29.5],PARAMETER['Standard_Parallel_2',45.5],PARAMETER['Latitude_Of_Origin',23.0],UNIT['Meter',1.0]]", transform_method="WGS_1984_(ITRF00)_To_NAD_1983", in_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")
        distMinor = arcpy.gp.EucDistance_sa(new_minor_line, folder + "\EucDist2.tif", "", "", "", "PLANAR")
        newDistMinor = distMinor / outConstRaster

        # remap raster and save
        minorDistRemap = RemapRange(range2)
        minorDistCat = Reclassify(newDistMinor, "VALUE", minorDistRemap)
        minorDistCat = Float(minorDistCat/outConstRaster2)
        minorDistCat.save("minorDistCat.tif")

    # if not, raster is constant 1.0 in order to not affect index calculation
    else:
        minorDistCat = CreateConstantRaster(1.0, "FLOAT")
        
    ### HOSPITAL/SCHOOL DISTANCE CATEGORICAL RASTER    
    if hospital_school and hospital_school != "#":

        # reproject hospital and school shapefile into meters distance projection, then make distance raster and convert to miles
        new_hospital_school = arcpy.Project_management(hospital_school, folder + "\hospital_school_project.shp", out_coor_system="PROJCS['NAD_1983_2011_Contiguous_USA_Albers',GEOGCS['GCS_NAD_1983_2011',DATUM['D_NAD_1983_2011',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-96.0],PARAMETER['Standard_Parallel_1',29.5],PARAMETER['Standard_Parallel_2',45.5],PARAMETER['Latitude_Of_Origin',23.0],UNIT['Meter',1.0]]", transform_method="'WGS_1984_(ITRF00)_To_NAD_1983 + WGS_1984_(ITRF08)_To_NAD_1983_2011'", in_coor_system="PROJCS['NAD_1983_StatePlane_California_V_FIPS_0405_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',6561666.666666666],PARAMETER['False_Northing',1640416.666666667],PARAMETER['Central_Meridian',-118.0],PARAMETER['Standard_Parallel_1',34.03333333333333],PARAMETER['Standard_Parallel_2',35.46666666666667],PARAMETER['Latitude_Of_Origin',33.5],UNIT['Foot_US',0.3048006096012192]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")
        distEvac = arcpy.gp.EucDistance_sa(new_hospital_school, folder + "\EucDist3.tif", "", "", "", "PLANAR")
        newDistEvac = distEvac / outConstRaster

        # remap raster and save
        distEvacRemap = RemapRange(range3)
        distEvacCat = Reclassify(newDistEvac, "VALUE", distEvacRemap)
        distEvacCat = Float(distEvacCat/outConstRaster2)
        distEvacCat.save("distEvacCat.tif")

    else:
        distEvacCat = CreateConstantRaster(1.0, "FLOAT")

    ### POPULATION DENSITY CATEGORICAL RASTER

    # create density field from census tract
    censusCopy = arcpy.CopyFeatures_management(census, "CensusCopy.shp")
    arcpy.AddField_management(censusCopy, "Density", "DOUBLE")
    arcpy.CalculateField_management(censusCopy, "Density", "[POPULATION] / [SQMI]")

    # population density raster
    density = arcpy.PolygonToRaster_conversion(censusCopy, "Density", "C:/Users/haeso/Documents/ArcGIS/Default.gdb/Density")

    # population density categorical raster
    densMap = RemapRange(range4)
    densCat = Reclassify(density, "VALUE", densMap)
    densCat.save("densCat.tif")

    ### SLOPE DENSITY CATEGORICAL RASTER

    if minor_fault and minor_fault != "#":
        slope = Slope(DEM)

        # slope categorical raster
        slopeMap = RemapRange(range5)
        slopeCat = Reclassify(slope, "VALUE", slopeMap)

        # divide by constant raster to turn into multiple
        slopeCat = Float(slopeCat/outConstRaster2)
        slopeCat.save("slopeCat.tif")

    # if not, raster is constant 1.0 in order to not affect index calculation
    else:
        slopeCat = CreateConstantRaster(1.0, "FLOAT")

    ### FINAL INDEX RASTER

    ### set such that if the density or distance rasters are 0, the entire cell for the index is 0. The other values are modifiers such as 1.2 or 0.7 that either lower or raise the index
    index = (densCat * distCat) * slopeCat * minorDistCat * distEvacCat
    index.save("index.tif")

    # remap and save
    indexRemap = RemapRange(range6)
    index = Reclassify(index, "VALUE", indexRemap)
    index.save("indexCategorical.tif")

    # Delete tertiary shapefiles, check extension back in
    arcpy.Delete_management(folder + "\CensusCopy.shp")
    arcpy.Delete_management(folder + "\densCat.tif")
    arcpy.Delete_management(folder + "\distCat.tif")
    arcpy.Delete_management(folder + "\EucDist1.tif")
    arcpy.Delete_management(folder + "\EucDist2.tif")
    arcpy.Delete_management(folder + "\EucDist3.tif")
    arcpy.Delete_management(folder + "\minorDistCat.tif")
    arcpy.Delete_management(folder + "\slopeCat.tif")
    arcpy.Delete_management(folder + "\distEvacCat.tif")
    arcpy.Delete_management(folder + "\Fault_Line_Project.shp")
    arcpy.Delete_management(folder + "\Minor_Fault_Project.shp")
    arcpy.Delete_management(folder + "\hospital_school_project.shp")

    arcpy.CheckInExtension("Spatial")

except:
    print("The spatial analyst license is required to run this tool.")
