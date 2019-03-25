#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Nov 9, 2016

@author: mike.sweet
'''

import csv
import json
import os
import sys
import collections
import arcpy
from provider import ZentraAPI_Old as meter
import util.ConnectSQL as connSQL
# from CalculateEndDate import row
# import datetime

#======================================================================================
gdbconn = connSQL.ConnectGDB()
mcoconn = gdbconn.create_connection()
mt_mesonet_path = str(mcoconn)+ "\\" + "MesonetSiteInfo"
print mt_mesonet_path
# Set workspace path to Mesonet geodatabase
# arcpy.env.workspace = r"\\cfcnas17a.gs.umt.edu\Resources$\Data\Mesonet\Master\Mesonet201704.gdb"
# arcpy.env.workspace = r"D:\Data\Mesonet201802.gdb"
arcpy.env.workspace = str(mcoconn)
# Set variable for parent Mesonet feture class in workspace
mesonetSiteInfo = "MesonetSiteInfo"
# Set variable for child Mesonet table for sensors associated with each site
mesonetSensorLineage = "MesonetSensorLineage"
# Declare output folder path
mesowestFilePath = r'\\cfcweb\ftp$\mesowest'
mcoFilePath = r'\\mcofiles\Resources$\Data\Mesonet\API-Output\ClimateOffice'
mcoURL = 'http://mco.cfc.umt.edu/mesonet'
jsonFilePath = r'\\cfcweb17\D$\wwwroot\mco.cfc.umt.edu\Stations.json'
webGraphFilePath = r'\\cfcweb17\D$\wwwroot\mco.cfc.umt.edu\mesonet'

#======================================================================================

def get_program_path(print_enabled=False):
    sys.path.append(os.path.dirname(sys.modules['__main__'].__file__))
    if print_enabled:
        print os.path.dirname(sys.modules['__main__'].__file__)
    return

def create_tableView_forAllSites(siteTable):
    siteView = arcpy.MakeTableView_management(siteTable)
    return siteView

def create_tableView_forActiveSites(siteTable):
    siteView = arcpy.MakeTableView_management(siteTable,"#", \
                                              """"Reporting_status" = 'yes'""")
    return siteView

def create_tableView_forActiveSensors(station,sensorTable):
    # Where clause for child table query
    whereClause = 'Primary_key = ' + "'" + station + "'" + " AND Station_state = 'active'"
    # Create table view from query of child table
    sensorView = arcpy.MakeTableView_management(sensorTable,"#",whereClause)
    return sensorView

def create_searchCursor_forSiteTable(siteView):
    siteCursor = arcpy.SearchCursor(siteView,
                                    fields="Primary_key; Active_status; Reporting_status; \
                                    MesoWest; Display_name", 
                                    sort_fields="Display_name A")
    return siteCursor

def create_searchCursor_forSensorTable(sensorView):
    sensorCursor = arcpy.SearchCursor(sensorView, 
                                      fields="Logger_username; Logger_password; Record_start_local_date", 
                                    sort_fields="Logger_username D")
    return sensorCursor

def build_dictionary_forStations(siteCursor):
    # To access the value of an entry in this dictionary use the following form:
    # stationDict[mesonetPrimaryKey].displayName
    stationTuple = collections.namedtuple('Station', \
                                     'activeStatus reportingStatus \
                                     mesoWest displayName')
    stationDict = {}
    for site in siteCursor:
        mesonetPrimaryKey =  site.getValue("Primary_key")
        stationDict[mesonetPrimaryKey] = stationTuple(activeStatus = site.getValue("Active_status"),\
                                               reportingStatus = site.getValue("Reporting_status"), \
                                               mesoWest = site.getValue("MesoWest"), \
                                               displayName = site.getValue("Display_name"))
    return stationDict

def build_dictionary_forSensors(stationKeys,stationDict,sensorLineage):
    # To access the value of an entry in this dictionary use the following form:
    # stationDict[mesonetPrimaryKey].displayName
    sensorTuple = collections.namedtuple('Sensor', \
                                    'loggerUserName loggerPassword \
                                     loggerLocalDate, displayName')
    sensorDict = {}
    for station in stationKeys:
        # Search cursor for table view finding latest active record
        # Note: return email error message if more than one record
        sensorView = create_tableView_forActiveSensors(station,sensorLineage)
        # Create a search cursor in for table view of active sites
        sensorCursor = create_searchCursor_forSensorTable(sensorView)
        for sensor in sensorCursor:
            sensorDict[station] = sensorTuple(loggerUserName = sensor.getValue("Logger_username"), \
                                              loggerPassword = sensor.getValue("Logger_password"), \
                                              loggerLocalDate = sensor.getValue("Record_start_local_date"), \
                                              displayName = stationDict[station].displayName)
        # Delete this table view
        arcpy.Delete_management("sensorView")
    return sensorDict

def create_listOfSortedKeys_fromDictionary(stationDict):
    # create sorted list of keys in dictionary
    # k represents the keys, and v represents the tuple
    # [3] is the forth element in the tuple which is the display name
    sorted_dict = sorted(stationDict.iteritems(), key=lambda (k,v): v[3])
    sorted_keys = [i[0] for i in sorted_dict]
    return sorted_keys

def create_outputCSV_forMesoWest01hr(station,filepath,maxUTC):
    datestr = "-"+meter.UTCms_to_localfilestring(maxUTC)
    # Declare output file name
    csvfilename = "MesoWest-" + station + datestr + ".csv"
    # Declare output file path
    csvpath = os.path.normpath(os.path.join(filepath,"Hourly"))
    csvpath = os.path.normpath(os.path.join(csvpath,csvfilename))
    return csvpath

def create_outputCSV_forMesoWest(station,filepath):
    # Declare output file name
    csvfilename = "MesoWest-" + station + ".csv"
    # Declare output file path
    csvpath = os.path.normpath(os.path.join(filepath,"Full"))
    csvpath = os.path.normpath(os.path.join(csvpath,csvfilename))
    return csvpath

def create_outputCSV_forClimateOffice(station,filepath):
    # Declare output file name
    smofilename = "MCORaw-" + station + ".csv"        
    # Declare output file path
    smopath = os.path.normpath(os.path.join(filepath,"Raw"))
    smopath = os.path.normpath(os.path.join(smopath,smofilename))  
    return smopath

def create_outputCSVlevel1_forClimateOffice(station,filepath):
    # Declare output file name
    smofilename = "MCOLevel1-" + station + ".csv"        
    # Declare output file path
    smopath = os.path.normpath(os.path.join(filepath,"Level1"))
    smopath = os.path.normpath(os.path.join(smopath,smofilename))  
    return smopath

def create_outputJSON_forMesoWest(station,filepath):
    # Declare output file name
    csvfilename = "MesoWest-" + station + ".json"
    # Declare output file path
    csvpath = os.path.normpath(os.path.join(filepath,"JSON"))
    csvpath = os.path.normpath(os.path.join(csvpath,csvfilename))
    return csvpath

def create_outputJSONsettings_forClimateOffice(station,filepath):
    # Declare output file name
    smofilename = "MCO-Settings-" + station + ".json"        
    # Declare output file path
    smopath = os.path.normpath(os.path.join(filepath,"Settings"))
    smopath = os.path.normpath(os.path.join(smopath,smofilename))  
    return smopath

def create_outputJSONreadings_forClimateOffice(station,filepath):
    # Declare output file name
    smofilename = "MCO-Readings-" + station + ".json"        
    # Declare output file path
    smopath = os.path.normpath(os.path.join(filepath,"Readings"))
    smopath = os.path.normpath(os.path.join(smopath,smofilename))  
    return smopath

def create_outputMeta_forMesoWest(station,filepath):
    # Declare output file name
    csvfilename = "MesoWest-Metadata-" + station + ".txt"
    # Declare output file path
    csvpath = os.path.normpath(os.path.join(filepath,"Metadata"))
    csvpath = os.path.normpath(os.path.join(csvpath,csvfilename))
    return csvpath

def create_outputMeta_forClimateOffice(station,filepath):
    # Declare output file name
    smofilename = "MCO-Metadata-" + station + ".txt"        
    # Declare output file path
    smopath = os.path.normpath(os.path.join(filepath,"Metadata"))
    smopath = os.path.normpath(os.path.join(smopath,smofilename))  
    return smopath

def write_as_MCO_JSON(settingsFile,settingsDict):
    # print "Size of dictionary in bytes is: ", sys.getsizeof(settingsDict)
    f = open(settingsFile,"w")
    f.write(json.dumps(settingsDict))
    # for chunk in json.JSONEncoder().iterencode(settingsDict):
    #    f.write(chunk)
    f.close
    return

def write_station_siteMetadata(metadataFile,settingsDict):
    # Set defaults
    stationLatitude = "unknown"
    stationLongitude = "unknown"
    stationElevation = "unknown"
    stationElevationAccuracy = "unknown"
    #
    if settingsDict["device"]["locations"]:
        stationLatitude = settingsDict["device"]["locations"][0]["latitude"]
        stationLongitude = settingsDict["device"]["locations"][0]["longitude"]
        stationElevation = (settingsDict["device"]["locations"][0]["altitude_mm"])*0.001
        stationElevationAccuracy = (settingsDict["device"]["locations"][0]["accuracyEstimate_mm"])*0.001   
    text_file = open(metadataFile, "w")
    text_file.write("Station latitude: %s\n" % stationLatitude)
    text_file.write("Station longitude: %s\n" % stationLongitude)
    text_file.write("Station elevation: %s\n" % stationElevation)
    text_file.write("Station elevation accuracy: %s\n" % stationElevationAccuracy)
    text_file.close()
    # print "Lat:",stationLatitude, "Long:",stationLongitude, \
    #      "Elev(m):",stationElevation, "Accuracy(m):",stationElevationAccuracy

def write_station_metadata(metadataFile,created="",version=""):
    text_file = open(metadataFile, "a")
    text_file.write("UTC date station was created: %s\n" % created)
    text_file.write("Station API version: %s\n" % version)
    text_file.close()
    return

def write_device_metadata(metadataFile,trait="",sn="",fw="",devType=""):
    text_file = open(metadataFile, "a")
    text_file.write("Device trait: %s\n" % trait)
    text_file.write("Device serial number: %s\n" % sn)
    text_file.write("Device firmware: %s\n" % fw)
    text_file.write("Device type: %s\n" % devType)
    text_file.close()
    return

def write_sensorConfig_metadata(metadataFile,validSince=""):
    text_file = open(metadataFile, "a")
    text_file.write("Sensor configuration valid since: %s\n" % validSince)
    text_file.close()
    return

def write_sensor_metadata(metadataFile,number="",port="",index=""):
    text_file = open(metadataFile, "a")
    text_file.write("Sensor number: %s" % number)
    text_file.write(" on port: %s" % port)
    text_file.write(" with port index: %s\n" % index)
    text_file.close()
    return

def write_measurement_metadata(metadataFile,sensorNumber,measurementList,sensorLabel):
    text_file = open(metadataFile, "a")
    listLen = len(measurementList)
    for indx in range(listLen) :
        label = "No label"
        if str(sensorNumber) in sensorLabel:
            label = sensorLabel[str(sensorNumber)][indx]
        # ele.encode('utf-8')
        text_file.write("Sensor element {0:02d}: {1} ({2})\n".format(indx,label,measurementList[indx].encode('utf-8').strip()))
    text_file.write("\n")
    text_file.close()
    return

def create_sensor_label_dict():
    labelDict = {}
    labelDict['93']  = ["solar radiation","precipitation","lightening strike counter", 
                        "lightening distance","wind direction","wind speed","wind gusts",
                        "air temperature","relative humidity","barometric pressure",
                        "x-axis tilt","y-axis tilt","maximum precipitation",
                        "humidity sensor temperature"]
    labelDict['114'] = ['reflected solar radiation 630 nm','reflected solar radiation 800 nm','orientation','α for NDVI']
    labelDict['115'] = ['incident solar radiation 630 nm','incident solar radiation 800 nm','orientation','α for NDVI']
    labelDict['119'] = ['soil volumetric water content','soil temperature','soil saturation extract']
    labelDict['133'] = ['battery percent','battery charge']
    labelDict['134'] = ["standard pressure","air temperature"]
    return labelDict

def write_list_to_file(outFile,outList=[]):
    text_file = open(outFile, "a")
    json.dump(outList, text_file)
    text_file.close()
    return

def parse_for_sensor(valueList,sensorNum,sensorPort,sensorNumDict,mcoDict,sensorMeas):
    # print "Parsing for: ", int(sensorNum), sensorPort, valueList
    if sensorNum == 93:
        mcoDict = parse_for_sensor093(valueList,sensorPort,sensorNumDict,mcoDict,sensorMeas)
    if sensorNum == 114:
        mcoDict = parse_for_sensor114(valueList,sensorPort,sensorNumDict,mcoDict,sensorMeas)
    if sensorNum == 115:
        mcoDict = parse_for_sensor115(valueList,sensorPort,sensorNumDict,mcoDict,sensorMeas)
    if sensorNum == 119:
        mcoDict = parse_for_sensor119(valueList,sensorPort,sensorNumDict,mcoDict,sensorMeas)
    if sensorNum == 133:
        mcoDict = parse_for_sensor133(valueList,sensorPort,sensorNumDict,mcoDict,sensorMeas)
    if sensorNum == 134:
        mcoDict = parse_for_sensor134(valueList,sensorPort,sensorNumDict,mcoDict,sensorMeas)
    return mcoDict

def parse_for_sensor093(valueList,sensorPort,sensorNumDict,mcoDict,sensorMeas):
    sensorMeas = sensorMeas
    sensorPort = sensorPort
    sensorNumDict = sensorNumDict
    if len(valueList)== 14:
        mcoDict['06:solrad'] = valueList[0]['value']
        mcoDict['07:precipitation'] = valueList[1]['value']
        mcoDict['08:hitnum'] = valueList[2]['value']
        mcoDict['09:hitdist'] = valueList[3]['value']
        mcoDict['10:winddir'] = valueList[4]['value']
        mcoDict['11:windspeed'] = valueList[5]['value']
        mcoDict['12:windgust'] = valueList[6]['value']
        mcoDict['13:temperature'] = valueList[7]['value']
        mcoDict['14:relhumidity'] = valueList[8]['value']
        mcoDict['15:pressure'] = valueList[9]['value']
        mcoDict['16:sensortiltx'] = valueList[10]['value']
        mcoDict['17:sensortilty'] = valueList[11]['value']
        mcoDict['18:maxprecip'] = valueList[12]['value']
        mcoDict['19:humiditytemp'] = valueList[13]['value']
    return mcoDict

def parse_for_sensor114(valueList,sensorPort,sensorNumDict,mcoDict,sensorMeas):
    sensorMeas = sensorMeas
    sensorPort = sensorPort
    sensorNumDict = sensorNumDict
    if len(valueList)== 4:
        mcoDict['35:rrad630'] = valueList[0]['value']
        mcoDict['36:rrad800'] = valueList[1]['value']
        mcoDict['37:rradorient'] = valueList[2]['value']
        mcoDict['38:rradalpha'] = valueList[3]['value']
    return mcoDict

def parse_for_sensor115(valueList,sensorPort,sensorNumDict,mcoDict,sensorMeas):
    sensorMeas = sensorMeas
    sensorPort = sensorPort
    sensorNumDict = sensorNumDict
    if len(valueList)== 4:
        mcoDict['39:irad630'] = valueList[0]['value']
        mcoDict['40:irad800'] = valueList[1]['value']
        mcoDict['41:iradorient'] = valueList[2]['value']
        mcoDict['42:iradalpha'] = valueList[3]['value']
    return mcoDict

def parse_for_sensor119(valueList,sensorPort,sensorNumDict,mcoDict,sensorMeas):
    sensorMeas = sensorMeas
    sensorPort = sensorPort
    sensorNumDict = sensorNumDict
    portList = sensorNumDict['119']
    
    if portList.index(sensorPort)== 0:
        if len(valueList)== 3:
            mcoDict['20:soilvwc4'] = valueList[0]['value']
            mcoDict['25:soilt4'] = valueList[1]['value']
            mcoDict['30:soilec4'] = valueList[2]['value']   

    if portList.index(sensorPort)== 1:
        if len(valueList)== 3:   
            mcoDict['21:soilvwc8'] = valueList[0]['value']
            mcoDict['26:soilt8'] = valueList[1]['value']    
            mcoDict['31:soilec8'] = valueList[2]['value']

    if portList.index(sensorPort)== 2:        
        if len(valueList)== 3:   
            mcoDict['22:soilvwc20'] = valueList[0]['value']
            mcoDict['27:soilt20'] = valueList[1]['value']    
            mcoDict['32:soilec20'] = valueList[2]['value']

    if portList.index(sensorPort)== 3:
        if len(valueList)== 3:
            mcoDict['23:soilvwc36'] = valueList[0]['value']
            mcoDict['28:soilt36'] = valueList[1]['value']
            mcoDict['33:soilec36'] = valueList[2]['value']

    if portList.index(sensorPort)== 4:
        if len(valueList)== 3:
            mcoDict['24:soilvwc0'] = valueList[0]['value']
            mcoDict['29:soilt0'] = valueList[1]['value']
            mcoDict['34:soilec0'] = valueList[2]['value']
    return mcoDict

def parse_for_sensor133(valueList,sensorPort,sensorNumDict,mcoDict,sensorMeas):
    sensorMeas = sensorMeas
    sensorPort = sensorPort
    sensorNumDict = sensorNumDict
    if len(valueList)== 2:
        mcoDict['43:batteryper'] = valueList[0]['value']
        mcoDict['44:batterymv'] = valueList[1]['value']
    return mcoDict

def parse_for_sensor134(valueList,sensorPort,sensorNumDict,mcoDict,sensorMeas):
    sensorPort = sensorPort
    sensorNumDict = sensorNumDict
    if len(valueList)== 2:
        # NOTE: Pass measurement string, should sort this out
        # for case when sensor 133 data is written to sensor 134
        # either both voltage values are zero, or millivolts > 60 (60 celsius)
        if (valueList[0]==0 and valueList[1]==0) or (valueList[1] > 60):
            mcoDict['43:batteryper'] = valueList[0]['value']
            mcoDict['44:batterymv'] = valueList[1]['value']
        else:    
            mcoDict['45:loggerpress'] = valueList[0]['value']
            mcoDict['46:loggertemp'] = valueList[1]['value']
    return mcoDict

#======================================================================================
## START OF PROGRAM

# Print program path if argument set to 'True'
get_program_path(True)

sensorLabelDict = create_sensor_label_dict()

# Create a table view for the feature table containing active sites
# that can be accessed via the Decagon API
siteView = create_tableView_forActiveSites(mesonetSiteInfo)

# Create a search cursor in for table view of active sites
siteCursor = create_searchCursor_forSiteTable(siteView)

# Create a dictionary of all active sites, with a tuple as the value
# The tuple is a collection that contains name-value pairs for station attributes
# To access a specific items use: stationDict[key].attribute, 
# e.g. stationDict[station].displayName
stationDict = build_dictionary_forStations(siteCursor)

# Create sorted list of keys based on display name
stationKeys = create_listOfSortedKeys_fromDictionary(stationDict)
sensorDict = build_dictionary_forSensors(stationKeys,stationDict,mesonetSensorLineage)

#==========================================================
# Prepare JSON output file for writing
#==========================================================
# Clean mesowest files older than 10 days
meter.clean_mesowest_hourly_files(mesowestFilePath,10)

data = {}
# data = [] 
data['stations'] = []

for station in stationKeys:
    # print "Processing ",sensorDict[station].loggerUserName, sensorDict[station].displayName
    # Testing for date conversions
    # meter.testing_time(sensorDict[station].loggerLocalDate)
    # API call for this device returned as JSON string
    readings = meter.get_device_readings(sensorDict[station].loggerUserName, \
                                         sensorDict[station].loggerPassword, \
                                         sensorDict[station].loggerLocalDate)
                                         
    settings = meter.get_device_settings(sensorDict[station].loggerUserName, \
                                         sensorDict[station].loggerPassword)
    # Verify that response is not NULL
    if readings is not None and settings is not None:
        #==========================================================
        # Prepare CSV output file for writing
        #==========================================================
        # Create JSON file output path
        mcoJSONsettings = create_outputJSONsettings_forClimateOffice(station,mcoFilePath)
        mcoJSONreadings = create_outputJSONreadings_forClimateOffice(station,mcoFilePath)

        # Create METADATA file output path
        mesowestMeta = create_outputMeta_forMesoWest(station,mesowestFilePath)
        mcoMeta = create_outputMeta_forClimateOffice(station,mcoFilePath)
        
        # Create CSV file output path
        mcoCSV = create_outputCSV_forClimateOffice(station,mcoFilePath)
        mcoCSVlev01 = create_outputCSVlevel1_forClimateOffice(station,mcoFilePath)

        # Open file for writing CSV
        mcoCSVfile  = open(mcoCSV, "wb")
        mcoCSVlevel1 = open(mcoCSVlev01, "wb")
        # Set CSV write parameters; dialect='excel', 
        mcoCSVwriter = csv.writer(mcoCSVfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        mcoCSVlevel1Writer = csv.writer(mcoCSVlevel1, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')

        # Save all station settings as JSON dictionary file
        stationSettingsDict = meter.get_readings_as_dictionary(settings)
        write_as_MCO_JSON(mcoJSONsettings,stationSettingsDict)

        # Save all station readings as JSON file
        stationReadingsDict = meter.get_readings_as_dictionary(readings)
        write_as_MCO_JSON(mcoJSONreadings,stationReadingsDict)
        write_station_siteMetadata(mesowestMeta,stationSettingsDict)
        write_station_siteMetadata(mcoMeta,stationSettingsDict)  
     
        #==========================================================
        # Nested JSON level 0 information: root node
        #==========================================================
        # Extract metadata and write to metadata file
        stationCreated = meter.get_readings_created(stationReadingsDict)
        stationVersion = meter.get_readings_version(stationReadingsDict)
        stationDevice = meter.get_readings_device(stationReadingsDict)
        write_station_metadata(mesowestMeta,stationCreated,stationVersion)
        write_station_metadata(mcoMeta,stationCreated,stationVersion)
 
        #==========================================================
        # Nested JSON level 1 information: device node
        #==========================================================
        deviceInfo = meter.get_device_info(stationDevice)
        deviceType = meter.get_device_type(deviceInfo)
        deviceSerialNumber = meter.get_device_serialno(deviceInfo)
        deviceFirmware = meter.get_device_firmware(deviceInfo)
        deviceTrait = meter.get_device_trait(deviceInfo)
        write_device_metadata(mcoMeta,deviceTrait,deviceSerialNumber,\
                              deviceFirmware,deviceType)
        #==========================================================
        # Nested JSON level 1 information: timeseries node
        #==========================================================
        # Device time series returned as a list
        deviceTimeseries = meter.get_timeseries(stationDevice)
        rowid=[]
        # Write MCO CSV header element row
        masterSensorDict = meter.get_climateOffice_sensorDict()
        for k,v in sorted(masterSensorDict.iteritems()):
            rowid.append(k[3:])
        mcoCSVwriter.writerow(rowid)
        mcoCSVlevel1Writer.writerow(rowid)
        # Write MCO CSV header units row
        rowid=[]
        masterSensorUnits = meter.get_climateOffice_sensorUnits()
        for k,v in sorted(masterSensorUnits.iteritems()):
            rowid.append(v)
        mcoCSVwriter.writerow(rowid)
        mcoCSVlevel1Writer.writerow(rowid)
        # Initialize end-of-timeseries timestamps
        timemax = -1
        timemax24 = -1
        graphmin = -1
        rowcount = 1
        if deviceTimeseries:
            for timeSeries in deviceTimeseries:
                deviceTimeseriesConfig = meter.get_timeseries_config(timeSeries)
                tsConfigValidSince = meter.get_config_valid_since(deviceTimeseriesConfig)
                sensors = meter.get_config_sensors(deviceTimeseriesConfig)
                values = meter.get_config_values(deviceTimeseriesConfig)
                write_sensorConfig_metadata(mcoMeta,tsConfigValidSince)
                sensorNumberDict = {'93':[],'114':[],'115':[],'119':[],'133':[],'134':[]}
    
                # Get last record in timeseries
                if values[len(values)-1][0] > timemax:
                    timemax = values[len(values)-1][0]
    
                # Write metadata records and get list of ports used for this configuration
                portList = []
                for sensor in sensors:
                    sensorNumber = meter.get_sensor_number(sensor)
                    sensorPort = meter.get_sensor_port(sensor)
                    textfile = open(mcoMeta,"a")
                    textfile.write("\n" + str(sensor)+ "\n")
                    textfile.write(str(sensorNumber) + ":" + str(sensorPort)+ "\n")
                    textfile.close()
    
                    if str(sensorNumber) in sensorNumberDict:
                        if sensorPort not in portList:
                            portList.append(sensorPort)
                        sensorNumberDict[str(sensorNumber)].append(sensorPort)
                        sensorIndex = portList.index(sensorPort)
                        sensorMeasurements = meter.get_sensor_measurements(sensor)
                        write_sensor_metadata(mcoMeta,sensorNumber,sensorPort,sensorIndex)
                        write_measurement_metadata(mcoMeta,sensorNumber,sensorMeasurements,sensorLabelDict)
                # START EACH MEASUREMENT RECORD  -- WRITE RECORD
                # Start all records
                for value in values:
                    masterSensorDict = meter.get_climateOffice_sensorDict()
                    masterSensorDict['01:recordnum']= rowcount
                    masterSensorDict['04:timestamp']= value[0]
                    masterSensorDict['05:localdate']= meter.UTCms_to_localstring(value[0])
                    masterSensorDict['02:apirecord']= value[1]
                    masterSensorDict['03:apicode']= value[2]        
                    for sensorNum,portNums in sensorNumberDict.iteritems():
                        for portNum in portNums:
                            subListIndex = portList.index(portNum)+3
                            subList = value[subListIndex]
                            # print "Calling parse: ", int(sensorNum), portNum, subListIndex, subList
                            # print sensorNumberDict
                            parse_for_sensor(subList,int(sensorNum),portNum,sensorNumberDict,masterSensorDict,sensorMeasurements)
                    # Write raw masterSensorDict
                    rowid = [] 
                    for k,v in sorted(masterSensorDict.iteritems()):
                        rowid.append(v)
                    mcoCSVwriter.writerow(rowid)
                    # Write sample record to metadata file
                    if rowcount%1000 == 0:
                        textfile = open(mcoMeta,"a")
                        textfile.write("\nSample Record:\n" + str(sorted(masterSensorDict.iteritems()))+ "\n")
                        textfile.close()
                    # Write Level 1 masterSensorDict
                    masterSensorDict = meter.mco_value_extract(masterSensorDict)
                    masterSensorDict = meter.mco_level1_qa(masterSensorDict,mcoMeta)
                    rowid = []
                    for k,v in sorted(masterSensorDict.iteritems()):
                        rowid.append(v)
                    mcoCSVlevel1Writer.writerow(rowid)
                    rowcount = rowcount + 1
            # Close MCO CSV file
            mcoCSVfile.close()
            mcoCSVlevel1.close()
            # print "- Export to " + mcoCSVfile.name + " completed"
            #-----------------------------------------------------------------------#
            # EXPORT COMPLETE, START CONVERSIONS
            # RE-READ MCO RAW CSV FILE FOR PRODUCING MESOWEST OUTPUT AND GRAPHS
            #-----------------------------------------------------------------------#
            #-----------------------------------------------------------------------#
            # Derive time slice end points for output files and graphs
            #-----------------------------------------------------------------------#
            # print "Max time: ", timemax, meter.UTCms_to_localstring(timemax)
            # Last record 1-hour ago
            timemax01 = timemax -(3600)
            # print "01-hr time: ", timemax01, meter.UTCms_to_localstring(timemax01)
            # Last record 24-hours ago
            timemax24 = timemax -(3600*24)
            # print "24-hr time: ", timemax24, meter.UTCms_to_localstring(timemax24)
            # Last record 7-days ago
            graphmin7 = timemax -(3600*24*7)
            # print "7-day time: ", graphmin7, meter.UTCms_to_localstring(graphmin7)
            graphmin21 = timemax -(3600*24*21)
            # print "21-day time: ", graphmin21, meter.UTCms_to_localstring(graphmin21)
            #-----------------------------------------------------------------------#
            # Initialize default dictionaries for output and graphing
            #-----------------------------------------------------------------------#
            # MesoWest output template (current record)
            mcoMesoWestDict = meter.get_mesowest_dict()
            # Mobile Web (current record and 24-hours prior)
            mcoMobileDictWeb = meter.get_mobile_web_dict()
            # Mobile 7 days ago (7-day history)
            mcoMobileDict7d = meter.get_mobile_graph_dict()
            # Mobile 21 days ago (21-day history)
            mcoMobileDict21d = meter.get_mobile_graph_dict()
            # Open MCO input file for reading
            # mcoCSV = open(mcoCSVlev01,"rb")
            # Logical yes or no for reporting to MesoWest
            mesoWest = False
            if stationDict[station].mesoWest == "yes":
                mesoWest = True
            # Process all records in input MCO data file
            dictmax = None
            dictmax24 = None
            with open(mcoCSVlev01) as mcoCSVDataFile:
                # If active MesoWest station then initialize output files
                if mesoWest:
                    # Create MesoWest CSV file output path for full and one-hour
                    mesowestCSV01hr = create_outputCSV_forMesoWest01hr(station,mesowestFilePath,timemax)
                    mesowestCSV = create_outputCSV_forMesoWest(station,mesowestFilePath)
                    # Open full and one-hour CSV files for writing
                    mesowestCSVfile01hr  = open(mesowestCSV01hr, "wb")
                    mesowestCSVfile  = open(mesowestCSV, "wb")
                    # Set CSV write parameters for full and one-hour file
                    # dialect='excel', 
                    mesowestCSVwriter01hr = csv.writer(mesowestCSVfile01hr, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
                    mesowestCSVwriter = csv.writer(mesowestCSVfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
                    # Write CSV file header rows
                    mesowestSensorDict = meter.get_mesowest_sensorUnits()
                    # Build field header row for CSV from dictionary values; Truncate numeric sorting values
                    rowid=[]
                    for k,v in sorted( mesowestSensorDict.iteritems()):
                        rowid.append(k[3:])
                    # Write CSV field header row to CSV file
                    mesowestCSVwriter01hr.writerow(rowid)
                    mesowestCSVwriter.writerow(rowid)
                    # Build unit header row for CSV from dictionary values
                    rowid=[]
                    mesowestSensorUnits = meter.get_mesowest_sensorUnits()
                    for k,v in sorted(mesowestSensorUnits.iteritems()):
                        rowid.append(v)
                    # Write CSV field unit row to CSV file
                    mesowestCSVwriter01hr.writerow(rowid)
                    mesowestCSVwriter.writerow(rowid)
                #-----------------------------------------------------------------------#
                # START of reading MCO input file
                #-----------------------------------------------------------------------#
                mcoCSVReader = csv.reader(mcoCSVDataFile,dialect='excel')
                # Skip field name row
                mcoCSVReader.next()
                # Skip field unit labels row
                mcoCSVReader.next()
                # Read remainder of file
                for row in mcoCSVReader:
                    # Initialize default MCO dictionary
                    masterSensorDict = meter.get_climateOffice_sensorDict()
                    # Map values from row to dictionary
                    # print sorted(masterSensorDict.iteritems())
                    masterSensorDict = meter.map_climateOffice_sensorDict(masterSensorDict,row)
                    # print row
                    # print masterSensorDict['40:batteryper'], masterSensorDict['41:batterymv']
                    # If active MesoWest station then write to MesoWest output files
                    if mesoWest:
                        # Map values from MCO dictionary to MesoWest dictionary
                        mcoMesoWestDict = meter.map_mesowest_sensorDict(masterSensorDict, mcoMesoWestDict)
                        # Write record to MesoWest all records file          
                        rowid=[]
                        for k,v in sorted(mcoMesoWestDict.iteritems()):
                            rowid.append(v)
                        mesowestCSVwriter.writerow(rowid)
                        # Write last-hour records to MesoWest past hour record file
                        rowid=[]
                        if int(row[3]) >= timemax01:
                            for k,v in sorted(mcoMesoWestDict.iteritems()):
                                rowid.append(v)
                            mesowestCSVwriter01hr.writerow(rowid)
                    # Map current values from MCO dictionary to mobile web dictionary
                    if int(row[3]) == timemax:
                        dictmax = masterSensorDict
                    # Map 24-hour values from MCO dictionary to mobile web dictionary
                    if int(row[3]) == timemax24:
                        dictmax24 = masterSensorDict
                    if int(row[3]) >= graphmin7:
                        mcoMobileDict7d = meter.map_graph_sensorDict(masterSensorDict,mcoMobileDict7d,int(row[3]))
                    if int(row[3]) >= graphmin21:
                        mcoMobileDict21d = meter.map_graph_sensorDict(masterSensorDict,mcoMobileDict21d,int(row[3]))
                # Close MesoWest output files
                if mesoWest:
                    mesowestCSVfile01hr.close()
                    mesowestCSVfile.close()
            # Map current and prior 24-hour sensor data fields to mobile dictionary
            mcoMobileDictWeb = meter.map_mobile_sensorDict(dictmax,dictmax24,mcoMobileDictWeb)
            mcoMobileDictWeb['00:loggerusername'] = sensorDict[station].loggerUserName
            mcoMobileDictWeb['00:displayname'] = sensorDict[station].displayName
            mcoMobileDictWeb['01:recordnum'] = rowcount
            mcoMobileDictWeb['04:timestamp'] = timemax
            mcoMobileDictWeb['05:localdate'] = meter.UTCms_to_localstring(timemax)
            # Close MCO CSV input file
            mcoCSVlevel1.close()
            #==========================================================
            # WRITE JSON FILE AND BUILD GRAPHS
            # Note: test stations with default graph, then add graph in
            #==========================================================
            jsonDict = meter.get_mcoWeb_jsonDict()
            jsonDict = meter.map_mobiledict_to_jsondict(mcoMobileDictWeb,jsonDict,station)
            #-----------------------------------------
            # Build graphs and add graphing URL
            #-----------------------------------------
            graphpath = os.path.normpath(os.path.join(webGraphFilePath,station))
            if not os.path.exists(graphpath):
                os.makedirs(graphpath)
            webpath = mcoURL + "/" + station +"/"+station
            jsonDict = meter.build_mobile_graphs(jsonDict,graphpath,webpath,mcoMobileDict7d,mcoMobileDict21d)
            # Add dictionary to JSON list
            data['stations'].append(jsonDict)
            del dictmax
            del dictmax24
            del mcoMobileDictWeb
#Change dictionary to a list        
data = data['stations']
with open(jsonFilePath, 'w') as outfile:
    json.dump(data,outfile)
