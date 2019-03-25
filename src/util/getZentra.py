#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@created="May 2018"
@description=('This module calls functions necessary',
              'to process Zentra content for use by the'
              'Montana Climate Office),
@attention='http://climate.umt.edu
@author: 'Michael D. Sweet',
@email='michael.sweet@umontana.edu',
@organization: 'Montana Climate Office'
#==========================================================================
# USE
#==========================================================================
This is program module is for downloading the Zentra data for the Mesonet project
'''
import util.config as zentraconfig
import util.configdownload as zentraconfigdownload
import util.httpsget as zentraget
import util.inputparser as inputparser
import util.misc as misc
import util.timeconvert as timeconvert
import provider.parseReadings as parsereadings
import provider.csvWriter as csvwriter
import provider.parseSettings as parsesettings
import provider.Mesonet as mesonet
import provider.levelOne as csvlevelone
import provider.metadataWriter as metadatawriter
import provider.mobileWriter as mobilewriter
import collections
import shutil
import json

#=========================================================================
# Functions for automating download for a single device over a time period
#=========================================================================

def build_station_list(stationkeys,station):
    # If station key passed as an argument then use station, otherwise use all active stations
    station_list = stationkeys
    if station in stationkeys:
        station_list = []
        station_list.append(station)
    return station_list

def test_date(lowerlimit,thedate,upperlimit):
    if lowerlimit <= thedate <= upperlimit:
        return True
    else:
        return False

def check_date_range(sensorstart,sensorend,userstart,userend):
    newstartday = userstart
    newendday = userend
    if not test_date(sensorstart,userstart,sensorend):
        if userstart < sensorstart:
            newstartday = sensorstart
            # print "SensorStart: ", sensorstart, "UserStart: ", userstart, "NewStart", newstartday
        if userstart > sensorend:
            newendday = sensorend
            # print "SensorEnd: ", sensorend, "UserStart: ", userstart, "NewEnd", newendday
    if not test_date(sensorstart,userend,sensorend):
        if userend > sensorend:
            newendday = sensorend
            # print "SensorEnd: ", sensorend, "UserEnd: ", userend, "NewEnd", newendday
        if userend < sensorstart:
            newstartday = sensorstart
            # print "SensorStart: ", sensorstart, "UserEnd: ", userend, "NewStart", newstartday
    if newstartday > newendday:
        newstartday = newendday
    return (newstartday,newendday)

def build_abandoned_dict(stations,active,abandoned,startday,endday):
    # Build download dictionary of primary keys device_serial_number, device_password, start time, end time
    download_dict = {}
    sensortuple = collections.namedtuple('Sensor','loggerUserName loggerPassword loggerStartDay loggerEndDay displayName')
    for station in stations:
        if station in abandoned.keys():
            # print "ABANDONED ", station,"SS:",abandoned[station].loggerLocalDate,"SE:",active[station].loggerLocalDate,"US:",startday,"UE",endday 
            newstartday,newendday = check_date_range(abandoned[station].loggerLocalDate,active[station].loggerLocalDate,startday,endday)
            # print "NEW ", newstartday, newendday
            # print
            # Is start day is later than end day, use end day as start
            download_dict[station] = sensortuple(loggerUserName = abandoned[station].loggerUserName, \
                                              loggerPassword = abandoned[station].loggerPassword, \
                                              loggerStartDay = newstartday, \
                                              loggerEndDay = newendday, \
                                              displayName = abandoned[station].displayName)
    return download_dict

def build_active_dict(stations,active,startday,endday):
    # Build download dictionary of primary keys device_serial_number, device_password, start time, end time
    download_dict = {}
    sensortuple = collections.namedtuple('Sensor','loggerUserName loggerPassword loggerStartDay loggerEndDay displayName')
    for station in stations:
        if station in active.keys():
            # print "ACTIVE ",station,"SS:",active[station].loggerLocalDate,"SE:",endday,"US:",startday,"UE",endday 
            newstartday,newendday = check_date_range(active[station].loggerLocalDate,endday,startday,endday)
            # print "NEW ", newstartday, newendday
            # print
            download_dict[station] = sensortuple(loggerUserName = active[station].loggerUserName, \
                                             loggerPassword = active[station].loggerPassword, \
                                             loggerStartDay = newstartday, \
                                             loggerEndDay = newendday, \
                                             displayName = active[station].displayName)
    return download_dict

def download_active(stations,sensordict,startday,endday):
    download_dict = build_active_dict(stations,sensordict,startday,endday)
    download_dict = validate_dict(download_dict)
    print
    print "ACTIVE"
    for station in download_dict.keys():
        device_serial_number = download_dict[station].loggerUserName
        device_password = download_dict[station].loggerPassword
        starttime = download_dict[station].loggerStartDay
        endtime = download_dict[station].loggerEndDay
        print station,device_serial_number,device_password,starttime,endtime
        dates_downloaded = zentrahttp.download_files(station,device_serial_number,device_password,starttime,endtime)
        print "Date array for downloaded files: ", dates_downloaded
    return dates_downloaded

def download_abandoned(stations,sensordict,abandoned_sensordict,startday,endday):
    download_dict = build_abandoned_dict(stations,sensordict,abandoned_sensordict,startday,endday)
    download_dict = validate_dict(download_dict)
    print "ABANDONED"
    for station in download_dict.keys():
        device_serial_number = download_dict[station].loggerUserName
        device_password = download_dict[station].loggerPassword
        starttime = download_dict[station].loggerStartDay
        endtime = download_dict[station].loggerEndDay
        print station,device_serial_number,device_password,starttime,endtime
        dates_downloaded = zentrahttp.download_files(station,device_serial_number,device_password,starttime,endtime)
        print "Date array for downloaded files: ", dates_downloaded
    return dates_downloaded

def validate_dict(sensordict):
    valid = True
    for station in sensordict.keys():
        if not sensordict[station].loggerUserName: valid = False
        if not sensordict[station].loggerPassword: valid = False
        if not sensordict[station].loggerStartDay: valid = False
        if not sensordict[station].loggerEndDay: valid = False
    if not valid:
        del sensordict[station]
    return sensordict 

#==========================================================================
# Main
#==========================================================================
if __name__ == "__main__":
    # Load user configuration settings as configuration object
    zconfig = zentraconfig.ZentraConfig()
    # Load Zentra configuration settings as configuration object
    zconfigdownload = zentraconfigdownload.ZentraDownloadConfig()
    # Zentra http download object instantiation
    zentrahttp = zentraget.HttpsRequest(zconfig,zconfigdownload)
    # Zentra download command line argument input parser
    zentraparser = inputparser.CommandArguments(zconfig,zconfigdownload)
    # Print argument values
    zentraparser.print_arguments()
    # Mesonet station object instantiation
    monet = mesonet.MesonetStations()
    # Load miscellaneous pathway functions
    miscfn = misc.Pathways()
    # Instantiate time conversion class
    timeconv = timeconvert.MesonetTimeConvert()
    # Instantiate Web Writer
    webwriter = mobilewriter.webWriter(zconfig,zconfigdownload)
    # Instantiate object for parsing values
    zentrareadings = parsereadings.ParseDictionary(zconfig,zconfigdownload)
    zentrasettings = parsesettings.ParseDictionary(zconfig,zconfigdownload)
    stations = build_station_list(monet.stationkeys,zentraparser.args.pkey)
    print "Parser date range: ", zentraparser.args.startday,zentraparser.args.endday
    print stations
    if zentraparser.args.abandoned:
        if zentraparser.args.update:
            dates_downloaded = download_abandoned(stations,monet.sensordict,monet.abandoned_sensordict,zentraparser.args.startday,zentraparser.args.endday)
        download_dict = build_abandoned_dict(stations,monet.sensordict,monet.abandoned_sensordict,zentraparser.args.startday,zentraparser.args.endday)
    else:
        if zentraparser.args.update:
            dates_downloaded = download_active(stations,monet.sensordict,zentraparser.args.startday,zentraparser.args.endday)
        download_dict = build_active_dict(stations,monet.sensordict,zentraparser.args.startday,zentraparser.args.endday)
    download_dict = validate_dict(download_dict)
    print "Download_dict", download_dict
    # Load CSV Writer object
    csvreadingswriter = csvwriter.csvReadingsWriter(zconfig,zconfigdownload)
    csvsettingswriter = csvwriter.csvSettingsWriter(zconfig,zconfigdownload)
    csvmerge = csvwriter.csvMerge(zconfig,zconfigdownload)
    # Load MCO metadata object
    mcometa = metadatawriter.metadataClimateOffice(zconfig,zconfigdownload)
    # Load MesoWest metadata object
    mesowestmeta = metadatawriter.metadataMesoWest(zconfig,zconfigdownload)
    # Iterate through stations and dates to parse JSON content for Readings into standardized format
    for station,values in sorted(download_dict.iteritems()):
        for d in timeconv.daterange(download_dict[station].loggerStartDay,download_dict[station].loggerEndDay):
            mcoreadings = zentrareadings.fill_climateOffice_mcoDict(station,d)
            mcosettings = zentrasettings.fill_climateOffice_mcoDict(station,d)
            csvreadingswriter.write_readings_csv(station,d,mcoreadings)
            csvsettingswriter.write_settings_csv(station,d,mcosettings)
        csvmerge.merge_csv_files(csvmerge.get_csv_readings_list(station),csvmerge.create_csv_readings_output_path(station))
        csvmerge.merge_csv_files(csvmerge.get_csv_settings_list(station),csvmerge.create_csv_settings_output_path(station))
    # Copy all merged files to Level0 folder
    for station,values in sorted(download_dict.iteritems()):
        # Merge all daily readings CSVs into composite CSV
        src = csvmerge.create_csv_readings_output_path(station)
        # Set destination path for Level0 copy of readings
        dst = csvmerge.create_levelzero_path(src)
        # Copy merged readings file from daily to Level0
        shutil.copyfile(src, dst)
        # Merge all daily settings CSVs into composite CSV
        src = csvmerge.create_csv_settings_output_path(station)
        # Set destination path for Level0 copy of setings
        dst = csvmerge.create_levelzero_path(src)
        # Copy merged settings file for daily to Level0
        shutil.copyfile(src, dst)
        # Initialize and update metadata files
        mcometa.write_settings(station,src)
        # If MesoWest station then write metadata
        if monet.stationdict[station].mesoWest == "yes":
            mesowestmeta.write_settings(station,src)
 
    data = {} 
    data['stations'] = []
    # Create Level One version of data files
    csvleveloneswriter = csvlevelone.csvLevelOneWriter(zconfig,zconfigdownload)
    for station,values in sorted(download_dict.iteritems()):
        src = csvmerge.create_csv_readings_output_path(station)
        dst = csvleveloneswriter.create_csv_levelone_path(src)
        csvleveloneswriter.write_levelone_csv(src,dst,mcometa.create_metadata_path(station),monet.stationdict[station].mesoWest)
        jsondict = webwriter.write_levelone_mcoweb(dst,monet.stationdict[station].displayName,monet.sensordict[station].loggerUserName,station)
        data['stations'].append(jsondict)
    #Change dictionary to a list        
    data = data['stations']
    jsonFilePath = miscfn.local_normpath(zconfig.mt_mesonet_web_path,"Stations.json")
    with open(jsonFilePath, 'w') as outfile:
        json.dump(data,outfile)
    outfile.close()

#==========================================================================
# END
#==========================================================================
