#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Nov 10, 2016

@author: mike.sweet

Decagon Em60 climate station API interface
http://data.decagon.com/api/v1

'''

import ast
import datetime
import json
import numbers
import os
import time
import urllib2
import math
import numpy as np

import pytz

import pandas as pd
import mobilegraph as mg

# from smo.util import mobilegraph as mg
# GLOBALS
# api_user = "michael.sweet@umontana.edu"
api_user = "kevin.hyde@umontana.edu"
api_user_password = "MapsRgr8#"
api_user_password = "mco2016//"
api_ip_address = "zentracloud.com"
NULL_VALUE = 65535
NA_VALUE = "NA"
LOCAL_TIME_ZONE = pytz.timezone("America/Denver")

# URL for settings
# http://data.decagon.com/api/v1/settings?user=michael.sweet@umontana.edu&user_password=password&sn=06-00151&device_password=moitu-blud

#==========================================================
# Utility functions for time conversions to Local and UTC
#==========================================================
def testing_time(input_dt):
    printTest=True
    result1 = datestr_to_naive_dt(input_dt,printTest)
    result2 = naive_dt_to_local_timestr(result1,printTest)
    local_timestr_to_UTCstr(result2,printTest)
    result3 = naive_dt_to_utcms(result1,printTest)
    utcms_to_datestr(result3,printTest)
    return

def datestr_to_naive_dt(input_dt,printTest=False):
    naive_time_dt = datetime.datetime.strptime(str(input_dt), "%Y-%m-%d %H:%M:%S")
    if printTest:
        print "Naive time (no alteration) is: ", naive_time_dt
    return naive_time_dt

def naive_dt_to_local_timestr(naive_time_dt,printTest=False):
    local_timestr = LOCAL_TIME_ZONE.localize(naive_time_dt, is_dst=None)
    if printTest:
        print "Local equivalent is: ", local_timestr
    return local_timestr

def local_timestr_to_UTCstr(local_timestr,printTest=False):
    utc_time_str = local_timestr.astimezone(pytz.utc)
    if printTest:
        print "UTC equivalent is: ", utc_time_str
    return utc_time_str

def naive_dt_to_utcms(naive_time_dt,printTest=False):
    utc_ms = int(time.mktime(naive_time_dt.utctimetuple()))
    if printTest:
        print "UTC in milliseconds: ", utc_ms
    return utc_ms

def utcms_to_datestr(utc_ms,printTest=False):
    datetuple = datetime.datetime.utcfromtimestamp(utc_ms)
    datestr = datetuple.strftime('%Y-%m-%dT%H:%M:%SZ')
    if printTest:
        print "UTC in milliseconds to date string: ", datestr
    return datestr

#==========================================================
# Utility functions
#==========================================================
def make_str_unicode(instr):
    return unicode(instr,'unicode-escape')

def UTCms_to_string(utcms):
    datetuple = datetime.datetime.utcfromtimestamp(utcms)
    datestr = datetuple.strftime('%Y-%m-%dT%H:%M:%SZ')
    return datestr

def UTCms_to_localstring(utcms):
    datetuple = datetime.datetime.utcfromtimestamp(utcms)
    local_dt = datetuple.replace(tzinfo=pytz.utc).astimezone(LOCAL_TIME_ZONE)
    local_dtn = LOCAL_TIME_ZONE.normalize(local_dt) # .normalize might be unnecessary
    datestr = local_dtn.strftime('%Y-%m-%d %H:%M')
    return datestr

def UTCms_to_localfilestring(utcms):
    datetuple = datetime.datetime.utcfromtimestamp(utcms)
    local_dt = datetuple.replace(tzinfo=pytz.utc).astimezone(LOCAL_TIME_ZONE)
    local_dtn = LOCAL_TIME_ZONE.normalize(local_dt) # .normalize might be unnecessary
    datestr = local_dtn.strftime('%Y%m%dT%H%M')
    return datestr

def check_for_NULL(inval):
    outval = "NULL"
    if inval != str(NULL_VALUE):
        if isinstance(inval,int):
            outval = inval
        elif isinstance(inval,float):
            outval = inval
        elif isinstance(inval,str) and len(inval) > 0:
            outval = inval
    return outval

def check_for_NA(inval):
    # print "In val: ", inval, type(inval)
    outval = NA_VALUE
    # if input is integer return integer
    if isinstance(inval,int):
        outval = inval
    # if input is float return float
    elif isinstance(inval,float):
        outval = inval
    # if input is string and not empty return string
    elif isinstance(inval,str) and len(inval) > 0 and inval != "NA":
        outval = inval
    # else return "NA"
    return outval

def str_or_na_from_int(inval):
    # print "INVAL: " ,inval
    inval = check_for_NA(inval)
    if inval == NA_VALUE:
        outval = inval
    elif isinstance(inval,int):
        outval = str(inval)
    elif isinstance(inval,float):
        outval = str(round(inval,0))
    # print "OUTVAL: ",outval
    return outval

def strdegF_or_na_from_float(inval):
    try:
        outval = str(int(round(((float(inval)*1.8)+32.0),0)))
    except ValueError:
        outval = NA_VALUE
    return outval

def strdewpt_or_na_from_float(tval,rhval):
    try:
        outval = str(int(round((float(tval)-(100.0-float(rhval)/5.0)),0)))
    except ValueError:
        outval = NA_VALUE
    return outval

def strrelhum_or_na_from_real(inval):
    try:
        outval = str(int(round((float(inval)*100.0),0)))
    except ValueError:
        outval = NA_VALUE
    return outval

def strpervwc_or_na_from_real(inval):
    try:
        outval = str(int(round((float(inval)*100.0),0)))
    except ValueError:
        outval = NA_VALUE
    return outval

def str_mph_from_meterpersec(inval):
    try:
        outval = str(round((float(inval)*2.23694),1))
    except ValueError:
        outval = NA_VALUE
    return outval

def strdecimal_inches_or_na_from_float(inval,places):
    # will print 0.0 for zero, and three decimals for values > 0
    try:
        outval = str('{0:.3}'.format(round(float(inval)*0.0393701,places)))
    except ValueError:
        outval = NA_VALUE
    return outval
    
def dewpt_from_float(tval,rhval):
    try:
        outval = str(int(round(float(tval)-((100.0-float(rhval))/5.0),0)))
    except ValueError:
        outval = NA_VALUE
    return outval

def strbar_or_na_from_float(inval):
    inval = check_for_NA(inval)
    if isinstance(inval,float):
        outval = str(round(inval*0.2953,2))
    else:
        outval = inval
    return outval

def bar_or_na_from_float(inval):
    inval = check_for_NA(inval)
    try:
        outval = round(float(inval)*0.2953,2)
    except:
        outval = inval
    return outval

def decimal_inches_or_na_from_float(inval,places):
    inval = check_for_NA(inval)
    if isinstance(inval,float):
        # convert mm to inches
        outval = round(inval*0.0393701,places)
    else:
        outval = inval
    return outval

def strint_or_na_from_float(inval):
    inval = check_for_NA(inval)
    if isinstance(inval,float):
        outval = str(int(round(inval,0)))
    else:
        outval = inval
    return outval

def int_or_na_from_float(inval):
    inval = check_for_NA(inval)
    if isinstance(inval,float):
        outval = int(round(inval,0))
    else:
        outval = inval
    return outval

def strpercent_or_na_from_real(inval):
    inval = check_for_NA(inval)
    if isinstance(inval,float):
        outval = str(int(round((inval*100.0),0)))
    else:
        outval = inval
    return outval

def percent_or_null_from_real(inval):
    inval = check_for_NULL(inval)
    if isinstance(inval,float):
        outval = round((inval*100.0),2)
    else:
        outval = inval
    return outval

def mph_from_meterpersec(inval):
    inval = check_for_NULL(inval)
    if isinstance(inval,float):
        outval = round((inval*2.23694),1)
    else:
        outval = inval
    return outval

def get_start_epoch(device_serial_number):
    mytime = datetime.datetime(year=2016, month=9, day=23, hour=0, minute=0, second=0, microsecond=0)
    ts = int(time.mktime(mytime.utctimetuple()))
    return ts

#==========================================================
# Functions for FILE OR PATHWAY response
#==========================================================
def ensure_dir(dir_path):
    try:
        os.stat(dir_path)
    except:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    return

def clean_mesowest_hourly_files(mesowestFilePath,days=10):
    fileList = []
    dayList = []
    # Build list of valid dates
    for d in range(0,days):
        now = datetime.datetime.now()-datetime.timedelta(days=d)
        dayList.append(now.strftime("%Y%m%d"))
    # Get list of files
    hourlyFilePath = os.path.normpath(os.path.join(mesowestFilePath,'Hourly'))
    for files in next(os.walk(hourlyFilePath))[2]:
        fileList.append(os.path.normpath(os.path.join(hourlyFilePath,files)))
    for files in fileList:
        saveFlag = False
        for daystr in dayList:
            if daystr in files:
                saveFlag = True
        if not saveFlag and os.path.isfile(files):
            os.remove(files)
    return

#==========================================================
# Functions for URL response
#==========================================================
def get_device_readings(device_serial_number,device_password,starttime):
    # Check for empty starttime
    starttime = datetime.datetime(year=2017,month=9,day=1)
    if starttime:
        naive_dt = datestr_to_naive_dt(starttime)
        utcmsstr = str(naive_dt_to_utcms(naive_dt))
    else:
        utcmsstr = "0"
    # Build request URL        
    requesturl = ('http://' + api_ip_address + '/api/v1/readings'
                  + '?' + "user=" + api_user
                  + '&' + "user_password=" + api_user_password
                  + '&' + "sn=" + device_serial_number
                  + '&' + "device_password=" + device_password
                  + '&' + "start_time=" + utcmsstr
                  )
    # Make request
    print requesturl
    req = urllib2.Request(requesturl)

    try:
        # Test for response
        response = urllib2.urlopen(req)
    except urllib2.URLError as e:
        # Rules for failed response
        if hasattr(e, 'reason'):
            print 'Failed to reach a server: ' + requesturl
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
    else:
        # If valid, return response string
        return response

def get_device_settings(device_serial_number,device_password):
    # Build request URL
    requesturl = ('http://' + api_ip_address + '/api/v1/settings'
                  + '?' + "user=" + api_user
                  + '&' + "user_password=" + api_user_password
                  + '&' + "sn=" + device_serial_number
                  + '&' + "device_password=" + device_password
                  )
    # Make request
    print requesturl
    req = urllib2.Request(requesturl)
    try:
        # Test for response
        response = urllib2.urlopen(req)
    except urllib2.URLError as e:
        # Rules for failed response
        if hasattr(e, 'reason'):
            print 'Failed to reach a server: ' + requesturl
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
    else:
        # If valid, return response string
        return response

#==========================================================
# Functions for information about URL response
#==========================================================
def get_response_url(response):
    return response.geturl()

def get_response_info(response):
    return response.info()

def print_readings(readings):
    print json.dumps(readings, sort_keys=True, indent=4, ensure_ascii=False)
    return

#==========================================================
# Functions for Level One information
#==========================================================
def get_readings_as_dictionary(response):
    readings_str = response.read()
    readings_dict = json.loads(readings_str)
    return readings_dict # returns dictionary

def get_readings_version(readings):
    # val = json.dumps(readings['get_readings_ver'])
    val = readings['get_readings_ver']
    return val # returns integer

def get_readings_created(readings):
    # val = json.dumps(readings['created'])
    val = readings['created']
    return val # returns UTC date as string

def get_readings_device(readings):
    # val = json.dumps(readings['device'])
    val = readings['device']
    return val # returns dictionary

#==========================================================
# Functions for Level Two information (Device)
#==========================================================
def get_device_info(device):
    val = device['device_info'] 
    return val # returns dictionary

def get_device_type(device):
    val = device['device_type']
    return val # returns integer

def get_device_serialno(device):
    val = device['device_sn'] 
    return val # returns string

def get_device_firmware(device):
    val = device['device_fw']
    return val # returns integer

def get_device_trait(device):
    val = device['device_trait']
    return val # returns integer

#==========================================================
# Functions for Level Two information (Timeseries)
#==========================================================
def get_timeseries(device):
    val = device['timeseries']
    return val # returns list

def get_timeseries_config(timeseries):
    val = timeseries['configuration']
    return val # returns configuration as dictionary

#==========================================================
# Functions for Level Three information (Configuration)
#==========================================================
def get_config_valid_since(config):
    val = config['valid_since']
    return val # returns UTC data string

def get_config_sensors(config):
    val = config['sensors']
    return val # returns list

def get_config_values(config):
    val = config['values']
    return val # returns list

def get_sensors(sensors):
    for sensor in sensors:
        # Number of keys for this sensor
        skeylen = len(sensor.keys())
        # Get list of keys for this sensor
        skeys = sensor.keys()
        # Sorted list of keys for this sensor
        skeyset = sorted(set(skeys))   
        print "SINDEX: ", skeylen, skeyset, sensor
    return

#==========================================================
# Functions for Level Four information (Sensors)
#==========================================================
def get_sensor_number(sensor):
    val = sensor['sensor_number']
    return val # returns integer

def get_sensor_port(sensor):
    val = sensor['port']
    return val # returns integer

def get_sensor_measurements(sensor):
    val = sensor['measurements']
    return val # returns list

#==========================================================
# Functions for Level Five information (Sensor Measurements)
#==========================================================
def get_port_values(port,values):
    print "Port: ", port
    # Next line returns all of the values 
    valu = values[4]
    print valu[port+2]
    return

#==========================================================
# Functions for Level Five information (Sensor Values)
#==========================================================
def get_value_timestamp(value):
    val = value[0]
    return val # returns integer

def get_value_recordno(value):
    val = value[1]
    return val # returns integer

def get_value_recordcode(value):
    val = value[2]
    return val # returns integer

#==========================================================
# Pandas Functions (Prototype) for dictionary to pandas array
#==========================================================
def dict_to_pandas_dataframe(stationdict):
    df = pd.DataFrame.from_dict(stationdict)
    print df.columns
    print df.index
    print df.shape
    print df.iloc[0]
    print df.iloc[1]

#==========================================================
# Function to return dictionary of sensor mappings
#==========================================================
def get_sensorconfig(sensors):
    # smax = len(sensors)
    print; print "Sensor Configuration:"       
    for sensor in sensors:
        # Number of keys for this sensor
        skeylen = len(sensor.keys())
        # Get list of keys for this sensor
        skeys = sensor.keys()
        # Sorted list of keys for this sensor
        skeyset = sorted(set(skeys))   
        print "SINDEX: ", sensor.index(), sensor['sensor_number'], skeylen, skeyset
        for jindex in range(0,skeylen):
            print skeyset[jindex],": ",sensor[skeyset[jindex]]
    return

def print_sensorconfig(sensorconfig):
    print; print "Sensor Configuration:"      
    for sensors in sensorconfig.keys():
        sensorlist = sensorconfig[sensors]
        for k in range(0,len(sensorlist)):
            print "\tSensor Port: ", sensors, " Measure: ", k, ":", sensorlist[k]
    return

def get_sensor_measure(sensorconfig,port,index):
    meas = ""
    if port in sensorconfig:
        measures = sensorconfig.get(port,None)
        if index >= 0 and index <= len(measures):
            meas = measures[index]
    return meas

#==========================================================
# Function to return dictionary of value mappings
#==========================================================
def get_nmp_datarow(deviceid,valuerow,rowid):
    sensorconfigs = {"06-00148":"sensorconfig1",
                     "06-00149":"sensorconfig1",
                     "06-00150":"sensorconfig1",
                     "06-00151":"sensorconfig1",
                     "06-00152":"sensorconfig1",
                     "06-00153":"sensorconfig1",
                     "06-00155":"sensorconfig1",
                     "06-00156":"sensorconfig1",
                     "06-00157":"sensorconfig1",
                     "06-00158":"sensorconfig1",
                     "06-00184":"sensorconfig1",
                     "06-00185":"sensorconfig1",
                     "06-00186":"sensorconfig1",
                     "06-00187":"sensorconfig1",
                     "06-00188":"sensorconfig1",
                     "06-00189":"sensorconfig1",
                     "06-00331":"sensorconfig1",
                     "06-00332":"sensorconfig1",
                     "06-00334":"sensorconfig1",
                     "06-00674":"sensorconfig1",
                     "06-00679":"sensorconfig1",
                     "06-00757":"sensorconfig1",
                     "06-00759":"sensorconfig1",
                     "06-00761":"sensorconfig1",
                     "06-00762":"sensorconfig1",
                     "06-00763":"sensorconfig1"
                     }
    sensorconfig = sensorconfigs.get(deviceid,None)
    if sensorconfig == "sensorconfig1":
        datarow = []
        # Append row id
        datarow.append(rowid[0])
        # Append latitude
        datarow.append(rowid[1])
        # Append longitude
        datarow.append(rowid[2])
        # append datetime
        datarow.append(UTCms_to_string(valuerow[0]))
        # append elevation
        datarow.append(rowid[3])
        # append solar radiation
        datarow.append(check_for_NULL(valuerow[3][0]))
        # append total precipitation
        datarow.append(check_for_NULL(valuerow[3][1]))
        # append wind direction
        datarow.append(check_for_NULL(valuerow[3][4]))
        # append wind speed
        datarow.append(check_for_NULL(valuerow[3][5]))
        # append wind gusts
        datarow.append(check_for_NULL(valuerow[3][6]))
        # append air temperature
        datarow.append(check_for_NULL(valuerow[3][7]))
        # append relative humidity
        datarow.append(percent_or_null_from_real(valuerow[3][8]))
        # append standard pressure
        datarow.append(check_for_NULL(valuerow[3][9]))
        # append soil depths
        soilstr = '4;8;20;36#'
        soilstr = soilstr + str(check_for_NULL(valuerow[4][1])) + ";" 
        soilstr = soilstr + str(check_for_NULL(valuerow[5][1])) + ";"
        soilstr = soilstr + str(check_for_NULL(valuerow[6][1])) + ";" 
        soilstr = soilstr + str(check_for_NULL(valuerow[7][1])) + "#"
        soilstr = soilstr + str(percent_or_null_from_real(valuerow[4][2])) + ";"
        soilstr = soilstr + str(percent_or_null_from_real(valuerow[5][2])) + ";"
        soilstr = soilstr + str(percent_or_null_from_real(valuerow[6][2])) + ";"
        soilstr = soilstr + str(percent_or_null_from_real(valuerow[7][2]))   
        datarow.append(soilstr)
        #
    else:
        datarow = []
    return datarow

def get_smo_datarow(deviceid,valuerow,rowid):
    sensorconfigs = {"06-00148":"sensorconfig1",
                     "06-00149":"sensorconfig1",
                     "06-00150":"sensorconfig1",
                     "06-00151":"sensorconfig1",
                     "06-00152":"sensorconfig1",
                     "06-00153":"sensorconfig1",
                     "06-00155":"sensorconfig1",
                     "06-00156":"sensorconfig1",
                     "06-00157":"sensorconfig1",
                     "06-00158":"sensorconfig1",
                     "06-00184":"sensorconfig1",
                     "06-00185":"sensorconfig1",
                     "06-00186":"sensorconfig1",
                     "06-00187":"sensorconfig1",
                     "06-00188":"sensorconfig1",
                     "06-00189":"sensorconfig1",
                     "06-00331":"sensorconfig1",
                     "06-00332":"sensorconfig1",
                     "06-00334":"sensorconfig1",
                     "06-00674":"sensorconfig1",
                     "06-00679":"sensorconfig1",
                     "06-00757":"sensorconfig1",
                     "06-00759":"sensorconfig1",
                     "06-00761":"sensorconfig1",
                     "06-00762":"sensorconfig1",
                     "06-00763":"sensorconfig1"
                     }
    sensorconfig = sensorconfigs.get(deviceid,None)
    
    devids = {"06-00148":"lololowr",
              "06-00149":"lolouppr",
              "06-00150":"kalispel",
              "06-00151":"corvalli",
              "06-00152":"conradmt",
              "06-00153":"havrenmt",
              "06-00155":"sidneymt",
              "06-00156":"huntleys",
              "06-00157":"sevnoner",
              "06-00158":"moccasin",
              "06-00184":"ebarllob",
              "06-00185":"turekran",
              "06-00186":"moccasin",
              "06-00187":"sidneymt",
              "06-00188":"huntleys",
              "06-00189":"lubrecht",
              "06-00331":"crowagen",
              "06-00332":"argentan",
              "06-00334":"turekran",
              "06-00674":"virginia",
              "06-00679":"mccartny",
              "06-00757":"rapeljen",
              "06-00759":"bentonlk",
              "06-00760":"blmkiddn",
              "06-00761":"ftkeoghn",
              "06-00762":"vandermo",
              "06-00763":"baileysw"
             }
    devid = devids.get(deviceid,None)

    if sensorconfig == "sensorconfig1":
        datarow = []
        # Append device serial number
        datarow.append(str(rowid[4])+"-"+devid)
        # Append datetime
        datarow.append(UTCms_to_localstring(valuerow[0]))
        # Append device firmware code returned as integer
        datarow.append(rowid[5])
        # Append device type code returned as integer
        datarow.append(rowid[6])
        # Append device trait code returned as integer
        datarow.append(rowid[7])
        # Append latitude
        datarow.append(rowid[1])
        # Append longitude
        datarow.append(rowid[2])
        # Append elevation
        datarow.append(rowid[3])        
        # Append battery percentage
        datarow.append(valuerow[8][0])        
        # Append battery millivolts
        datarow.append(valuerow[8][1])
        # Append solar radiation
        datarow.append(valuerow[3][0])
        # Append total precipitation
        datarow.append(valuerow[3][1])
        # Append event counts
        datarow.append(valuerow[3][2])
        # Append average distance
        datarow.append(valuerow[3][3])
        # append wind direction
        datarow.append(valuerow[3][4])
        # append wind speed
        datarow.append(valuerow[3][5])
        # append wind gusts
        datarow.append(valuerow[3][6])
        # append air temperature
        datarow.append(valuerow[3][7])
        # append relative humidity
        datarow.append(valuerow[3][8])
        # append standard pressure
        datarow.append(valuerow[9][0]) 
        # append standard pressure temperature
        datarow.append(valuerow[9][1])
        # append soil temperatures
        datarow.append(valuerow[4][1])
        datarow.append(valuerow[5][1])
        datarow.append(valuerow[6][1])
        datarow.append(valuerow[7][1])
        # append soil moisture
        datarow.append(valuerow[4][0])
        datarow.append(valuerow[5][0])
        datarow.append(valuerow[6][0])
        datarow.append(valuerow[7][0])
        # append soil conductivity
        datarow.append(valuerow[4][2])
        datarow.append(valuerow[5][2])
        datarow.append(valuerow[6][2])
        datarow.append(valuerow[7][2])
    else:
        datarow = []
    return datarow

def dictupdate(graphdict,element,timestamp,value):
    elemdict = graphdict.get(element,None)
    ts = elemdict.get('timestamp',None)
    val = elemdict.get('values',None)
    ts.append(timestamp)
    val.append(value)
    elemdict.update({'timestamp':ts})
    elemdict.update({'values':val})
    graphdict.update({element:elemdict})
    return graphdict

def get_mobile_graphrow(deviceid,valuerow,graphdict):

    current_dict = {
            'batteryper':   {'timestamp':[],'values':[]},
            'batterymv':    {'timestamp':[],'values':[]},
            'temperature':  {'timestamp':[],'values':[]},
            'relhumidity':  {'timestamp':[],'values':[]},
            'windspeed':    {'timestamp':[],'values':[]},
            'windgust':     {'timestamp':[],'values':[]},
            'winddir':      {'timestamp':[],'values':[]},
            'dewpoint':     {'timestamp':[],'values':[]},
            'precipitation':{'timestamp':[],'values':[]},
            'barometer':    {'timestamp':[],'values':[]},
            'soilt4':       {'timestamp':[],'values':[]},
            'soilt8':       {'timestamp':[],'values':[]},
            'soilt20':      {'timestamp':[],'values':[]},
            'soilt36':      {'timestamp':[],'values':[]},
            'soilvwc4':     {'timestamp':[],'values':[]},
            'soilvwc8':     {'timestamp':[],'values':[]},
            'soilvwc20':    {'timestamp':[],'values':[]},
            'soilvwc36':    {'timestamp':[],'values':[]},
        }
    
    if isinstance(valuerow[8][0], numbers.Number):
        dictupdate(graphdict,'batteryper',(int(valuerow[0])),(valuerow[8][0]))
    
    if isinstance(valuerow[8][1], numbers.Number):
        dictupdate(graphdict,'batterymv',(int(valuerow[0])),(valuerow[8][1]))

    if isinstance(valuerow[3][0], numbers.Number):
        dictupdate(graphdict,'solrad',(int(valuerow[0])),
                   (strint_or_na_from_float(valuerow[3][0])))

    if isinstance(valuerow[3][7], numbers.Number):
        dictupdate(graphdict,'temperature',(int(valuerow[0])),
                   (strdegF_or_na_from_float(valuerow[3][7])))

    if isinstance(valuerow[3][8], numbers.Number):
        dictupdate(graphdict,'relhumidity',(int(valuerow[0])),
                   (strpercent_or_na_from_real(valuerow[3][8])))

    if isinstance(valuerow[3][5], numbers.Number):
        dictupdate(graphdict,'windspeed',(int(valuerow[0])),
                   (mph_from_meterpersec(valuerow[3][5])))

    if isinstance(valuerow[3][6], numbers.Number):
        dictupdate(graphdict,'windgust',(int(valuerow[0])),
                   (mph_from_meterpersec(valuerow[3][6])))

    if isinstance(valuerow[3][4], numbers.Number):
        dictupdate(graphdict,'winddir',(int(valuerow[0])),
                   (int_or_na_from_float(valuerow[3][4])))

    if isinstance(valuerow[3][7], numbers.Number) & isinstance(valuerow[3][8], numbers.Number):
        dictupdate(graphdict,'dewpoint',(int(valuerow[0])),
                   (dewpt_from_float(valuerow[3][7],valuerow[3][8])))

    if isinstance(valuerow[3][1], numbers.Number):
        dictupdate(graphdict,'precipitation',(int(valuerow[0])),
                   (decimal_inches_or_na_from_float(valuerow[3][1],3)))

    if isinstance(valuerow[3][9], numbers.Number):
        dictupdate(graphdict,'barometer',(int(valuerow[0])),
                   (bar_or_na_from_float(valuerow[3][9])))

    if isinstance(valuerow[3][2], numbers.Number):
        dictupdate(graphdict,'hitnum',(int(valuerow[0])),
                   ((valuerow[3][2])))

    if isinstance(valuerow[3][3], numbers.Number):
        dictupdate(graphdict,'hitdist',(int(valuerow[0])),
                   ((valuerow[3][3])))

    if isinstance(valuerow[4][1], numbers.Number):
        dictupdate(graphdict,'soilt4',(int(valuerow[0])),
                   (strdegF_or_na_from_float(valuerow[4][1])))

    if isinstance(valuerow[5][1], numbers.Number):
        dictupdate(graphdict,'soilt8',(int(valuerow[0])),
                   (strdegF_or_na_from_float(valuerow[5][1])))

    if isinstance(valuerow[6][1], numbers.Number):
        dictupdate(graphdict,'soilt20',(int(valuerow[0])),
                   (strdegF_or_na_from_float(valuerow[6][1])))

    if isinstance(valuerow[7][1], numbers.Number):
        dictupdate(graphdict,'soilt36',(int(valuerow[0])),
                   (strdegF_or_na_from_float(valuerow[7][1])))

    if isinstance(valuerow[4][0], numbers.Number):
        dictupdate(graphdict,'soilvwc4',(int(valuerow[0])),
                   (strpercent_or_na_from_real(valuerow[4][0])))

    if isinstance(valuerow[5][0], numbers.Number):
        dictupdate(graphdict,'soilvwc8',(int(valuerow[0])),
                   (strpercent_or_na_from_real(valuerow[5][0])))

    if isinstance(valuerow[6][0], numbers.Number):
        dictupdate(graphdict,'soilvwc20',(int(valuerow[0])),
                   (strpercent_or_na_from_real(valuerow[6][0])))

    if isinstance(valuerow[7][0], numbers.Number):
        dictupdate(graphdict,'soilvwc36',(int(valuerow[0])),
                   (strpercent_or_na_from_real(valuerow[7][0])))

    """
    graphdict['precipTOT'] =     'NA'
    """
    return graphdict

def build_mobile_graphs(jsonDict,graphpath,webpath,mcoMobileDict7d,mcoMobileDict21d):
    name = jsonDict['displayname']
    station = jsonDict['station']
    print name
    outpath = os.path.join(graphpath,station+'-'+'batteryper')
    # if graph is successfully produced then update URL
    if mg.graph_batteryper(name,outpath,mcoMobileDict7d['43:batteryper']):
        jsonDict['batteryperURL']=webpath+'-'+'batteryper.png'

    outpath = os.path.join(graphpath,station+'-'+'batterymv')
    # if graph is successfully produced then update URL
    if mg.graph_batterymv(name,outpath,mcoMobileDict7d['44:batterymv']):
        jsonDict['batterymvURL']=webpath+'-'+'batterymv.png' 

    outpath = os.path.join(graphpath,station+'-'+'solrad')
    # if graph is successfully produced then update URL
    if mg.graph_solrad(name,outpath,mcoMobileDict7d['06:solrad']):
        jsonDict['solradURL']=webpath+'-'+'solrad.png' 

    outpath = os.path.join(graphpath,station+'-'+'temperature')
    # if graph is successfully produced then update URL
    if mg.graph_temperature(name,outpath,mcoMobileDict7d['13:temperature']):
        jsonDict['temperatureURL']=webpath+'-'+'temperature.png' 

    outpath = os.path.join(graphpath,station+'-'+'relhumidity')
    # if graph is successfully produced then update URL
    if mg.graph_relhumidity(name,outpath,mcoMobileDict7d['14:relhumidity']):
        jsonDict['relhumidityURL']=webpath+'-'+'relhumidity.png' 

    outpath = os.path.join(graphpath,station+'-'+'windspeed')
    # if graph is successfully produced then update URL
    if mg.graph_windspeed(name,outpath,mcoMobileDict7d['11:windspeed']):
        jsonDict['windspeedURL']=webpath+'-'+'windspeed.png' 

    outpath = os.path.join(graphpath,station+'-'+'windgust')
    # if graph is successfully produced then update URL
    if mg.graph_windgust(name,outpath,mcoMobileDict7d['12:windgust']):
        jsonDict['windgustURL']=webpath+'-'+'windgust.png' 

    outpath = os.path.join(graphpath,station+'-'+'winddir')
    # if graph is successfully produced then update URL
    if mg.graph_winddir(name,outpath,mcoMobileDict7d['10:winddir']):
        jsonDict['winddirURL']=webpath+'-'+'winddir.png' 

    outpath = os.path.join(graphpath,station+'-'+'dewpoint')
    if mg.graph_dewpoint(name,outpath,mcoMobileDict7d['13:temperature'],mcoMobileDict7d['14:relhumidity']):
        jsonDict['dewpointURL']=webpath+'-'+'dewpoint.png' 

    outpath = os.path.join(graphpath,station+'-'+'precipitation')
    if mg.graph_precipitation(name,outpath,mcoMobileDict21d['07:precipitation']):
        jsonDict['precipitationURL']=webpath+'-'+'precipitation.png'   

    outpath = os.path.join(graphpath,station+'-'+'preciptotal')
    # Call to function returns a named tuple of the form: 'TotalPrecip', ['isGraph', 'value','value24'
    graphout = mg.graph_preciptotal(name,outpath,mcoMobileDict21d['07:precipitation'])
    jsonDict['preciptotal'] = graphout.value
    jsonDict['preciptotal24'] = graphout.value24
    if graphout.isGraph:
        jsonDict['preciptotalURL']=webpath+'-'+'preciptotal.png'

    outpath = os.path.join(graphpath,station+'-'+'pressure')    
    if mg.graph_pressure(name,outpath,mcoMobileDict7d['15:pressure']):
        jsonDict['pressureURL']=webpath+'-'+'pressure.png' 

    outpath = os.path.join(graphpath,station+'-'+'hitnum')    
    if mg.graph_hitnum(name,outpath,mcoMobileDict7d['08:hitnum']):
        jsonDict['hitnumURL']=webpath+'-'+'hitnum.png' 

    outpath = os.path.join(graphpath,station+'-'+'hitdist')    
    if mg.graph_hitdist(name,outpath,mcoMobileDict7d['09:hitdist']):
        jsonDict['hitdistURL']=webpath+'-'+'hitdist.png' 

    outpath = os.path.join(graphpath,station+'-'+'soilt4')    
    if mg.graph_soilt4(name,outpath,mcoMobileDict7d['25:soilt4']):
        jsonDict['soilt4URL']=webpath+'-'+'soilt4.png' 

    outpath = os.path.join(graphpath,station+'-'+'soilt8')    
    if mg.graph_soilt8(name,outpath,mcoMobileDict7d['26:soilt8']):
        jsonDict['soilt8URL']=webpath+'-'+'soilt8.png' 

    outpath = os.path.join(graphpath,station+'-'+'soilt20')    
    if mg.graph_soilt20(name,outpath,mcoMobileDict21d['27:soilt20']):
        jsonDict['soilt20URL']=webpath+'-'+'soilt20.png' 

    outpath = os.path.join(graphpath,station+'-'+'soilt36')    
    if mg.graph_soilt36(name,outpath,mcoMobileDict21d['28:soilt36']):
        jsonDict['soilt36URL']=webpath+'-'+'soilt36.png' 

    outpath = os.path.join(graphpath,station+'-'+'soilvwc4')    
    if mg.graph_soilvwc4(name,outpath,mcoMobileDict7d['20:soilvwc4']):
        jsonDict['soilvwc4URL']=webpath+'-'+'soilvwc4.png' 

    outpath = os.path.join(graphpath,station+'-'+'soilvwc8')    
    if mg.graph_soilvwc8(name,outpath,mcoMobileDict7d['21:soilvwc8']):
        jsonDict['soilvwc8URL']=webpath+'-'+'soilvwc8.png' 

    outpath = os.path.join(graphpath,station+'-'+'soilvwc20')    
    if mg.graph_soilvwc20(name,outpath,mcoMobileDict21d['22:soilvwc20']):
        jsonDict['soilvwc20URL']=webpath+'-'+'soilvwc20.png'

    outpath = os.path.join(graphpath,station+'-'+'soilvwc36')    
    if mg.graph_soilvwc36(name,outpath,mcoMobileDict21d['23:soilvwc36']):
        jsonDict['soilvwc36URL']=webpath+'-'+'soilvwc36.png' 

    return jsonDict

def get_mobile_datarow(deviceid,valuerow,jsondict,valuerow24):
    
    mcourl = 'http://mco.cfc.umt.edu/mesonet'

    sensorconfigs = {"06-00148":"sensorconfig1",
                     "06-00149":"sensorconfig1",
                     "06-00150":"sensorconfig1",
                     "06-00151":"sensorconfig1",
                     "06-00152":"sensorconfig1",
                     "06-00153":"sensorconfig1",
                     "06-00155":"sensorconfig1",
                     "06-00156":"sensorconfig1",
                     "06-00157":"sensorconfig1",
                     "06-00158":"sensorconfig1",
                     "06-00184":"sensorconfig1",
                     "06-00185":"sensorconfig1",
                     "06-00186":"sensorconfig1",
                     "06-00187":"sensorconfig1",
                     "06-00188":"sensorconfig1",
                     "06-00189":"sensorconfig1",
                     "06-00331":"sensorconfig1",
                     "06-00332":"sensorconfig1",
                     "06-00334":"sensorconfig1",
                     "06-00674":"sensorconfig1",
                     "06-00679":"sensorconfig1",
                     "06-00757":"sensorconfig1",
                     "06-00759":"sensorconfig1",
                     "06-00761":"sensorconfig1",
                     "06-00762":"sensorconfig1",
                     "06-00763":"sensorconfig1"
                     }
    sensorconfig = sensorconfigs.get(deviceid,None)
    
    devids = {"06-00148":"lololowr",
              "06-00149":"lolouppr",
              "06-00150":"kalispel",
              "06-00151":"corvalli",
              "06-00152":"conradmt",
              "06-00153":"havrenmt",
              "06-00155":"sidneymt",
              "06-00156":"huntleys",
              "06-00157":"sevnoner",
              "06-00158":"moccasin",
              "06-00184":"ebarllob",
              "06-00185":"turekran",
              "06-00186":"moccasin",
              "06-00187":"sidneymt",
              "06-00188":"huntleys",
              "06-00189":"lubrecht",
              "06-00331":"crowagen",
              "06-00332":"argentan",
              "06-00334":"turekran",
              "06-00674":"virginia",
              "06-00679":"mccartny",
              "06-00757":"rapeljen",
              "06-00759":"bentonlk",
              "06-00760":"blmkiddn",
              "06-00761":"ftkeoghn",
              "06-00762":"vandermo",
              "06-00763":"baileysw"
              }
    devid = devids.get(deviceid,None)
    
    names = {"06-00148":"Lower Lolo",
             "06-00149":"Upper Lolo",
             "06-00150":"ARC-NW Kalispell",
             "06-00151":"ARC-W Corvallis",
             "06-00152":"ARC-WTri Conrad",
             "06-00153":"ARC-N Havre",
             "06-00155":"ARC-E Sidney",
             "06-00156":"ARC-S Huntley",
             "06-00157":"Ingomar NE",
             "06-00158":"ARC-C Mocassin",
             "06-00184":"Clearwater SE",
             "06-00185":"Coffee Creek N",
             "06-00186":"ARC-C Mocassin",
             "06-00187":"ARC-E Sidney",
             "06-00188":"ARC-S Huntley",
             "06-00189":"Lubrecht Forest",
             "06-00331":"Crow Agency",
             "06-00332":"BLM Argenta",
             "06-00334":"Coffee Creek N",
             "06-00674":"BLM Virginia City",
             "06-00674":"BLM McCartney Mtn",             
             "06-00757":"Rapelje N",
             "06-00759":"Benton Lake W",
             "06-00761":"ARS Fort Keogh",
             "06-00762":"Vandermolen",
             "06-00763":"Bailey"
             }

    name = names.get(deviceid,None)

    outpath = mcourl + "/" + devid + "/" + devid
    if sensorconfig == "sensorconfig1":
        # Check to see if prior 24-hour match was found
        # If timestamps match then prior 24-hour was not found
        na24flag = False
        if valuerow[0] == valuerow24[0]:
            na24flag = True

        jsondict['id'] = devid
        jsondict['name'] = name
        jsondict['device'] = 'Decagon ' +  deviceid
        jsondict['datetime'] = UTCms_to_localstring(valuerow[0])
        jsondict['batteryper'] =    str_or_na_from_int(valuerow[8][0])
        jsondict['batteryperURL'] =  outpath +'-'+'batteryper'+'.png'
        jsondict['batterymv'] =     str_or_na_from_int(valuerow[8][1])
        jsondict['batterymvURL'] =       outpath +'-'+'batterymv'+'.png'
        jsondict['solrad'] =        strint_or_na_from_float(valuerow[3][0])
        jsondict['solradURL'] =       outpath +'-'+'solrad'+'.png'
        if not na24flag: jsondict['solrad24'] =      str_or_na_from_int(valuerow24[3][0])
        jsondict['temperature'] =   strdegF_or_na_from_float(valuerow[3][7])
        jsondict['TAirURL'] =       outpath +'-'+'temperature'+'.png'
        if not na24flag: jsondict['TAir24'] =        strdegF_or_na_from_float(valuerow24[3][7])
        jsondict['relhumidity'] =   strpercent_or_na_from_real(valuerow[3][8])
        if not na24flag: jsondict['RelHum24'] =      strpercent_or_na_from_real(valuerow24[3][8])
        jsondict['RelHumURL'] =     outpath +'-'+'relhumidity'+'.png'
        jsondict['windspeed'] =     str_mph_from_meterpersec(valuerow[3][5])
        jsondict['WindSpeedURL'] =  outpath +'-'+'windspeed'+'.png'
        if not na24flag: jsondict['WindSpeed24'] =   str_mph_from_meterpersec(valuerow24[3][5])
        jsondict['windgust'] =      str_mph_from_meterpersec(valuerow[3][6])
        jsondict['WindGustURL'] =   outpath +'-'+'windgust'+'.png'
        if not na24flag: jsondict['WindGust24'] =    str_mph_from_meterpersec(valuerow24[3][6])
        jsondict['winddir'] =       str_or_na_from_int(valuerow[3][4])
        jsondict['WindDirURL'] =    outpath +'-'+'winddir'+'.png'
        if not na24flag: jsondict['WindDir24'] =     str_or_na_from_int(valuerow24[3][4])
        jsondict['dewpoint'] =      strdewpt_or_na_from_float(valuerow[3][7],valuerow[3][8])
        jsondict['DewPtURL'] =      outpath +'-'+'dewpoint'+'.png'
        if not na24flag: jsondict['DewPt24'] =       strdewpt_or_na_from_float(valuerow24[3][7],valuerow24[3][8])
        jsondict['precipitation'] = strdecimal_inches_or_na_from_float(valuerow[3][1],3)
        jsondict['PrecipURL'] =     outpath +'-'+'precipitation'+'.png'
        if not na24flag: jsondict['Precip24'] =      strdecimal_inches_or_na_from_float(valuerow24[3][1],3)
        jsondict['precipTOT'] =     'http://mco.cfc.umt.edu/mesonet/NoGraph.png'
        jsondict['Precip7URL'] =    outpath +'-'+'precipitation'+'.png'
        jsondict['barometer'] =     strbar_or_na_from_float(valuerow[3][9])
        jsondict['BaromURL'] =      outpath +'-'+'barometer'+'.png'
        if not na24flag: jsondict['Barom24'] =       strbar_or_na_from_float(valuerow24[3][9])
        jsondict['hitnum'] =        str_or_na_from_int(valuerow[3][2])
        jsondict['hitnumURL'] =      outpath +'-'+'hitnum'+'.png'
        if not na24flag: jsondict['hitnum24'] =       str_or_na_from_int(valuerow24[3][2])
        jsondict['hitdist'] =     str_or_na_from_int(valuerow[3][3])
        jsondict['hitdistURL'] =      outpath +'-'+'hitdist'+'.png'
        if not na24flag: jsondict['hitdist24'] =       str_or_na_from_int(valuerow24[3][3])
        jsondict['soilt4'] =        strdegF_or_na_from_float(valuerow[4][1])
        jsondict['Soilt4URL'] =     outpath +'-'+'soilt4'+'.png'
        if not na24flag: jsondict['Soilt424'] =      strdegF_or_na_from_float(valuerow24[4][1])
        jsondict['soilt8'] =        strdegF_or_na_from_float(valuerow[5][1])
        jsondict['Soilt8URL'] =     outpath +'-'+'soilt8'+'.png'
        if not na24flag: jsondict['Soilt824'] =      strdegF_or_na_from_float(valuerow24[5][1])
        jsondict['soilt20'] =       strdegF_or_na_from_float(valuerow[6][1])
        jsondict['Soilt20URL'] =    outpath +'-'+'soilt20'+'.png'
        if not na24flag: jsondict['Soilt2024'] =     strdegF_or_na_from_float(valuerow24[6][1])
        jsondict['soilt36'] =       strdegF_or_na_from_float(valuerow[7][1])
        jsondict['Soilt36URL'] =    outpath +'-'+'soilt36'+'.png'
        if not na24flag: jsondict['Soilt3624'] =     strdegF_or_na_from_float(valuerow24[7][1])
        jsondict['soilvwc4'] =      strpercent_or_na_from_real(valuerow[4][0])
        jsondict['Soilvwc4URL'] =   outpath +'-'+'soilvwc4'+'.png'
        if not na24flag: jsondict['Soilvwc424'] =    strpercent_or_na_from_real(valuerow24[4][0])
        jsondict['soilvwc8'] =      strpercent_or_na_from_real(valuerow[5][0])
        jsondict['Soilvwc8URL'] =   outpath +'-'+'soilvwc8'+'.png'
        if not na24flag: jsondict['Soilvwc824'] =    strpercent_or_na_from_real(valuerow24[5][0])
        jsondict['soilvwc20'] =     strpercent_or_na_from_real(valuerow[6][0])
        jsondict['Soilvwc20URL'] =  outpath +'-'+'soilvwc20'+'.png'
        if not na24flag: jsondict['Soilvwc2024'] =   strpercent_or_na_from_real(valuerow24[6][0])
        jsondict['soilvwc36'] =     strpercent_or_na_from_real(valuerow[7][0])
        jsondict['Soilvwc36URL'] =  outpath +'-'+'soilvwc36'+'.png'
        if not na24flag: jsondict['Soilvwc3624'] =   strpercent_or_na_from_real(valuerow24[7][0])

    return jsondict

def get_mcoWeb_jsonDict():
    ## MAKE OUTPUT JSON FILE FOR WEB INTERFACE
    jsondict = {}
    jsondict['station'] =          None
    jsondict['displayname'] =      None
    jsondict['loggerusername'] =   None
    jsondict['localdate'] =        None
    jsondict['recordno'] =         None
    jsondict['batteryper'] =       None
    jsondict['batteryper24'] =     None
    jsondict['batteryperURL'] =    None
    jsondict['batterymv'] =        None
    jsondict['batterymv24'] =      None
    jsondict['batterymvURL'] =     None
    jsondict['solrad'] =           None
    jsondict['solrad24'] =         None
    jsondict['solradURL'] =        None
    jsondict['temperature'] =      None
    jsondict['temperature24'] =    None
    jsondict['temperatureURL'] =   None
    jsondict['relhumidity'] =      None
    jsondict['relhumidity24'] =    None
    jsondict['relhumidityURL'] =   None
    jsondict['windspeed'] =        None
    jsondict['windspeed24'] =      None
    jsondict['windspeedURL'] =     None
    jsondict['windgust'] =         None
    jsondict['windgust24'] =       None
    jsondict['windgustURL'] =      None
    jsondict['winddir'] =          None
    jsondict['winddir24'] =        None
    jsondict['winddirURL'] =       None
    jsondict['dewpoint'] =         None
    jsondict['dewpoint24'] =       None
    jsondict['dewpointURL'] =      None
    jsondict['precipitation'] =    None
    jsondict['precipitation24'] =  None
    jsondict['precipitationURL'] = None
    jsondict['preciptotal'] =      None
    jsondict['preciptotal24'] =    None
    jsondict['preciptotalURL'] =   None
    jsondict['pressure'] =         None
    jsondict['pressure24'] =       None
    jsondict['pressureURL'] =      None
    jsondict['hitnum'] =           None
    jsondict['hitnum24'] =         None
    jsondict['hitnumURL'] =        None
    jsondict['hitdist'] =          None
    jsondict['hitdist24'] =        None
    jsondict['hitdistURL'] =       None
    jsondict['soilt4'] =           None
    jsondict['soilt424'] =         None
    jsondict['soilt4URL'] =        None
    jsondict['soilt8'] =           None
    jsondict['soilt824'] =         None
    jsondict['soilt8URL'] =        None
    jsondict['soilt20'] =          None
    jsondict['soilt2024'] =        None
    jsondict['soilt20URL'] =       None
    jsondict['soilt36'] =          None
    jsondict['soilt3624'] =        None
    jsondict['soilt36URL'] =       None
    jsondict['soilvwc4'] =         None
    jsondict['soilvwc424'] =       None
    jsondict['soilvwc4URL'] =      None
    jsondict['soilvwc8'] =         None
    jsondict['soilvwc824'] =       None
    jsondict['soilvwc8URL'] =      None
    jsondict['soilvwc20'] =        None
    jsondict['soilvwc2024'] =      None
    jsondict['soilvwc20URL'] =     None
    jsondict['soilvwc36'] =        None
    jsondict['soilvwc36'] =        None
    jsondict['soilvwc3624'] =      None
    jsondict['soilvwc36URL'] =     None

    return jsondict

def map_mobiledict_to_jsondict(mcodict,jsondict,station):

    jsondict['station'] =          station
    jsondict['displayname'] =      mcodict['00:displayname']
    jsondict['loggerusername'] =   mcodict['00:loggerusername']
    jsondict['localdate'] =        mcodict['05:localdate']
    jsondict['recordno'] =         mcodict['01:recordnum']
    jsondict['batteryper'] =       mcodict['43:batteryper']['Value']
    jsondict['batteryper24'] =     mcodict['43:batteryper']['Value24']
    jsondict['batteryperURL'] =    mcodict['43:batteryper']['GraphURL']
    jsondict['batterymv'] =        mcodict['44:batterymv']['Value']
    jsondict['batterymv24'] =      mcodict['44:batterymv']['Value24']
    jsondict['batterymvURL'] =     mcodict['44:batterymv']['GraphURL']
    jsondict['solrad'] =           mcodict['06:solrad']['Value']
    jsondict['solrad24'] =         mcodict['06:solrad']['Value24']
    jsondict['solradURL'] =        mcodict['06:solrad']['GraphURL']
    jsondict['temperature'] =      strdegF_or_na_from_float(mcodict['13:temperature']['Value'])
    jsondict['temperature24'] =    strdegF_or_na_from_float(mcodict['13:temperature']['Value24'])
    jsondict['temperatureURL'] =   mcodict['13:temperature']['GraphURL']
    jsondict['relhumidity'] =      strrelhum_or_na_from_real(mcodict['14:relhumidity']['Value'])
    jsondict['relhumidity24'] =    strrelhum_or_na_from_real(mcodict['14:relhumidity']['Value24'])
    jsondict['relhumidityURL'] =   mcodict['14:relhumidity']['GraphURL']
    jsondict['windspeed'] =        str_mph_from_meterpersec(mcodict['11:windspeed']['Value'])
    jsondict['windspeed24'] =      str_mph_from_meterpersec(mcodict['11:windspeed']['Value24'])
    jsondict['windspeedURL'] =     mcodict['11:windspeed']['GraphURL']
    jsondict['windgust'] =         str_mph_from_meterpersec(mcodict['12:windgust']['Value'])
    jsondict['windgust24'] =       str_mph_from_meterpersec(mcodict['12:windgust']['Value24'])
    jsondict['windgustURL'] =      mcodict['12:windgust']['GraphURL']
    jsondict['winddir'] =          mcodict['10:winddir']['Value']
    jsondict['winddir24'] =        mcodict['10:winddir']['Value24']
    jsondict['winddirURL'] =       mcodict['10:winddir']['GraphURL']
    jsondict['dewpoint'] =         strdegF_or_na_from_float(dewpt_from_float(mcodict['13:temperature']['Value'],strrelhum_or_na_from_real(mcodict['14:relhumidity']['Value'])))
    jsondict['dewpoint24'] =       strdegF_or_na_from_float(dewpt_from_float(mcodict['13:temperature']['Value24'],strrelhum_or_na_from_real(mcodict['14:relhumidity']['Value24'])))
    jsondict['dewpointURL'] =     'NA'
    jsondict['precipitation'] =    strdecimal_inches_or_na_from_float(mcodict['07:precipitation']['Value'],3)
    jsondict['precipitation24'] =  strdecimal_inches_or_na_from_float(mcodict['07:precipitation']['Value24'],3)
    jsondict['precipitationURL'] = mcodict['07:precipitation']['GraphURL']
    jsondict['preciptotal'] =     'NA'
    jsondict['preciptotal24'] =   'NA'
    jsondict['preciptotalURL'] =  'NA'
    jsondict['pressure'] =         bar_or_na_from_float(mcodict['15:pressure']['Value'])
    jsondict['pressure24'] =       bar_or_na_from_float(mcodict['15:pressure']['Value24'])
    jsondict['pressureURL'] =      mcodict['15:pressure']['GraphURL']
    jsondict['hitnum'] =           mcodict['08:hitnum']['Value']
    jsondict['hitnum24'] =         mcodict['08:hitnum']['Value24']
    jsondict['hitnumURL'] =        mcodict['08:hitnum']['GraphURL']
    jsondict['hitdist'] =          mcodict['09:hitdist']['Value']
    jsondict['hitdist24'] =        mcodict['09:hitdist']['Value24']
    jsondict['hitdistURL'] =       mcodict['09:hitdist']['GraphURL']
    jsondict['soilt4'] =           strdegF_or_na_from_float(mcodict['25:soilt4']['Value'])
    jsondict['soilt424'] =         strdegF_or_na_from_float(mcodict['25:soilt4']['Value24'])
    jsondict['soilt4URL'] =        mcodict['25:soilt4']['GraphURL']
    jsondict['soilt8'] =           strdegF_or_na_from_float(mcodict['26:soilt8']['Value'])
    jsondict['soilt824'] =         strdegF_or_na_from_float(mcodict['26:soilt8']['Value24'])
    jsondict['soilt8URL'] =        mcodict['26:soilt8']['GraphURL']
    jsondict['soilt20'] =          strdegF_or_na_from_float(mcodict['27:soilt20']['Value'])
    jsondict['soilt2024'] =        strdegF_or_na_from_float(mcodict['27:soilt20']['Value24'])
    jsondict['soilt20URL'] =       mcodict['27:soilt20']['GraphURL']
    jsondict['soilt36'] =          strdegF_or_na_from_float(mcodict['28:soilt36']['Value'])
    jsondict['soilt3624'] =        strdegF_or_na_from_float(mcodict['28:soilt36']['Value24'])
    jsondict['soilt36URL'] =       mcodict['28:soilt36']['GraphURL']
    jsondict['soilvwc4'] =         strpervwc_or_na_from_real(mcodict['20:soilvwc4']['Value'])
    jsondict['soilvwc424'] =       strpervwc_or_na_from_real(mcodict['20:soilvwc4']['Value24'])
    jsondict['soilvwc4URL'] =      mcodict['20:soilvwc4']['GraphURL']
    jsondict['soilvwc8'] =         strpervwc_or_na_from_real(mcodict['21:soilvwc8']['Value'])
    jsondict['soilvwc824'] =       strpervwc_or_na_from_real(mcodict['21:soilvwc8']['Value24'])
    jsondict['soilvwc8URL'] =      mcodict['21:soilvwc8']['GraphURL']
    jsondict['soilvwc20'] =        strpervwc_or_na_from_real(mcodict['22:soilvwc20']['Value'])
    jsondict['soilvwc2024'] =      strpervwc_or_na_from_real(mcodict['22:soilvwc20']['Value24'])
    jsondict['soilvwc20URL'] =     mcodict['22:soilvwc20']['GraphURL']
    jsondict['soilvwc36'] =        strpervwc_or_na_from_real(mcodict['23:soilvwc36']['Value'])
    jsondict['soilvwc3624'] =      strpervwc_or_na_from_real(mcodict['23:soilvwc36']['Value24'])
    jsondict['soilvwc36URL'] =     mcodict['23:soilvwc36']['GraphURL']

    return jsondict

#====================================================================
# Function to return National Mesonet Program (NMP) headers and codes
#====================================================================
def get_code_dictionary(sensorconfig):
    codedict = {"Solar Radiation": {"DecUnits":"W/m\xb2","MADISName":"SOLRAD","MADISDesc":"solar radiation - unknown type","MADISUnits":"watt/(m**2)"},
                "Precipitation": {"DecUnits":"mm","MADISName":"PCPTOTL","MADISDesc":"total precipitation","MADISUnits":"m"},
                "Wind Direction": {"DecUnits":"\xba","MADISName":"DD","MADISDesc":"wind direction","MADISUnits":"deg"},
                "Wind Speed": {"DecUnits":"m/s","MADISName":"FF","MADISDesc":"wind speed","MADISUnits":"m/s"},
                "Wind Gusts": {"DecUnits":"m/s","MADISName":"FFGUST","MADISDesc":"wind gust","MADISUnits":"m/s"},
                "Air  Temperature ": {"DecUnits":"\xbaC","MADISName":"T","MADISDesc":"air temperature","MADISUnits":"K"},                     
                "Relative Humidity": {"DecUnits":"kPa","MADISName":"RH","MADISDesc":"relative humidity","MADISUnits":"%"},
                "Standard Pressure": {"DecUnits":"kPa","MADISName":"P","MADISDesc":"station pressure","MADISUnits":"Pa"},
                "Soil Temperature": {"DecUnits":"\xbaC","MADISName":"SOILT","MADISDesc":"Soil temperature","MADISUnits":"K"},
                "Soil Moisture": {"DecUnits":"m\xb3/m\xb3","MADISName":"SOIMP","MADISDesc":"Soil moisture percent","MADISUnits":"%"}
                }
    codes = codedict.get(sensorconfig,None)
    return codes

def get_smo_header_fields(deviceid):
    headerfields =  {"06-00148":["station_id","Date and Time","Firmware","Type","Trait",
                                 "LAT [deg N]","LON [deg E]","ELEV [m]","BATPER [%]","BATMV [mV]",
                                 "SOLRAD [W/(m\xb2)]","PCPTOTL [mm]","Events [n]","Distance [km]",
                                 "DD [deg]","FF [m/s]","FFGUSTS [m/s]","T [\xb0C]","RH [%]","P [kPa]","PT [\xb0C]",
                                 "SOILT04 [\xb0C]", "SOILT08 [\xb0C]", "SOILT20 [\xb0C]", "SOILT36 [\xb0C]",
                                 "SOILVWC04 [m\xb3/m\xb3]", "SOILVWC08 [m\xb3/m\xb3]", "SOILVWC20 [m\xb3/m\xb3]", "SOILVWC36 [m\xb3/m\xb3]",
                                 "SOILMP04 [mS/cm]", "SOILMP08 [mS/cm]", "SOILMP20 [mS/cm]", "SOILMP36 [mS/cm]"],
                    }

    return headerfields.get(deviceid,None)

def get_mobile_web_dict():
    current_dict = {
            '00:loggerusername': "NA",
            '00:displayname':  "NA",
            '01:recordnum':    "NA",
            '04:timestamp':    "NA",
            '05:localdate':    "NA",
            '06:solrad':       {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '07:precipitation':{"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '08:hitnum':       {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '09:hitdist':      {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},    
            '10:winddir':      {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '11:windspeed':    {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '12:windgust':     {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '13:temperature':  {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '14:relhumidity':  {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '15:pressure':     {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '20:soilvwc4':     {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '21:soilvwc8':     {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '22:soilvwc20':    {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '23:soilvwc36':    {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '24:soilvwc0':     {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '25:soilt4':       {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '26:soilt8':       {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '27:soilt20':      {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '28:soilt36':      {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '29:soilt0':       {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '30:soilec4':      {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '31:soilec8':      {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '32:soilec20':     {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '33:soilec36':     {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '34:soilec0':      {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '43:batteryper':   {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"},
            '44:batterymv':    {"Value":"NA","Value24":"NA","GraphURL":"http://mco.cfc.umt.edu/mesonet/NoGraph.png"}
            }
    return current_dict

def get_mobile_graph_dict():
    current_dict = {
            '06:solrad':       {'timestamp':[],'values':[]},
            '07:precipitation':{'timestamp':[],'values':[]},
            '08:hitnum':       {'timestamp':[],'values':[]},
            '09:hitdist':      {'timestamp':[],'values':[]},    
            '10:winddir':      {'timestamp':[],'values':[]},
            '11:windspeed':    {'timestamp':[],'values':[]},
            '12:windgust':     {'timestamp':[],'values':[]},
            '13:temperature':  {'timestamp':[],'values':[]},
            '14:relhumidity':  {'timestamp':[],'values':[]},
            '15:pressure':     {'timestamp':[],'values':[]},
            '20:soilvwc4':     {'timestamp':[],'values':[]},
            '21:soilvwc8':     {'timestamp':[],'values':[]},
            '22:soilvwc20':    {'timestamp':[],'values':[]},
            '23:soilvwc36':    {'timestamp':[],'values':[]},
            '25:soilt4':       {'timestamp':[],'values':[]},
            '26:soilt8':       {'timestamp':[],'values':[]},
            '27:soilt20':      {'timestamp':[],'values':[]},
            '28:soilt36':      {'timestamp':[],'values':[]},
            '30:soilec4':      {'timestamp':[],'values':[]},
            '31:soilec8':      {'timestamp':[],'values':[]},
            '32:soilec20':     {'timestamp':[],'values':[]},
            '33:soilec36':     {'timestamp':[],'values':[]},
            '43:batteryper':   {'timestamp':[],'values':[]},
            '44:batterymv':    {'timestamp':[],'values':[]}    
           }
    return current_dict

def write_level1_metadata(metadataFile,recordNumber,sensorLabel,oldval,newval):
    text_file = open(metadataFile, "a")
    text_file.write("Updating record {0} for {1}: replace {2} with {3}\n".format(str(recordNumber),sensorLabel,str(oldval),str(newval)))
    text_file.close()
    return

def mco_value_extract(sensordict):
    for k,v in sorted(sensordict.iteritems()):
        # Change all NaN values to NULL_VALUE for non-literals
        if type(v) is dict:
            sensordict[k] = v['value']
            # print "\t",sensordict[k]
    return sensordict

def mco_level1_qa(sensordict,mcometafile):
    exceptionList = ['01:recordnum','02:apirecord','03:apicode','04:timestamp','05:localdate']
    nullList = [65533,65534]
    # Set all nulls to max value
    recno = sensordict['01:recordnum']
    for k,v in sorted(sensordict.iteritems()):
        # Change all NaN values to NULL_VALUE for non-literals
        if type(v) is dict:
            v = v['value']
        if k not in exceptionList and (v is None or math.isnan(float(v))):
            # print "\tConverting NaN ...", k,v,type(v),NULL_VALUE
            # np.nan_to_num(x)
            sensordict[k] = NULL_VALUE
            # print "\t",sensordict[k]
    # Change all nulls to NULL_VALUE
    for k,v in sorted(sensordict.iteritems()):
        for n in nullList:
            if k not in exceptionList and int(v) == n:
                # print "Updating ...", k,v,type(v),type(int(v)),NULL_VALUE
                sensordict[k] = NULL_VALUE
    # Change all units to default resolution and range
    for k,v in sorted(sensordict.iteritems()):
        if k not in exceptionList and int(v) != NULL_VALUE:
            if k[3:] == 'solrad':
                if int(v) < 0 or int(v) > 1750:
                    sensorLabel = "solar radiation"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = int(round(v,0))
            if k[3:] == 'precipitation':
                if float(v) <  0.0 or float(v) > 125.0:
                    sensorLabel = "precipitation"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = round(v,3)
            if k[3:] == 'hitdist':
                if int(v) < 0 or int(v) > 40:
                    sensorLabel = "lightening hit distance"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
            if k[3:] == 'winddir':
                if int(v) < 0 or int(v) > 359:
                    sensorLabel = "wind direction"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = int(round(v,0))
            if k[3:] == 'windspeed':
                # Note: sensor specifications are 60, but 50 more reasonable for Montana
                if float(v) < 0.0 or float(v) > 50.0:
                    sensorLabel = "wind speed"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = round(v,2)
            if k[3:] == 'windgusts':
                # Note: sensor specifications are 60, but 50 more reasonable for Montana
                if float(v) < 0.0 or float(v) > 50.0:
                    sensorLabel = "wind gusts"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = round(v,2)
            if k[3:] == 'temperature':
                if float(v) < -40.0 or float(v) > 50.0:
                    sensorLabel = "air temperature"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = round(v,1)
            if k[3:] == 'relhumidity':
                # Note: cutoff set to less than 0.001 since the RH sensor reports a missing value as zero
                if float(v) < 0.001 or float(v) > 1.1:
                    sensorLabel = "relative humidity"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    if float(v) > 1.0:
                        sensordict[k] = 1.000
                    else:
                        sensordict[k] = round(v,3)
            if k[3:] == 'pressure':
                if float(v) < 40.0 or float(v) > 110.0:
                    sensorLabel = "air pressure"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = round(v,4)
            if k[3:] == 'sensortiltx':
                if float(v) < -10.0 or float(v) > 10.0:
                    sensorLabel = "sensor tilt x"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = round(v,1)
            if k[3:] == 'sensortilty':
                if float(v) < -10.0 or float(v) > 10.0:
                    sensorLabel = "sensor tilt y"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = round(v,1)
            if k[3:] == 'maxprecip':
                if float(v) <  0.0 or float(v) > 125.0:
                    sensorLabel = "Maximum precipitation"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = round(v,3)
            if k[3:] == 'soilvwc4' or k[3:] == 'soilvwc8' or k[3:] == 'soilvwc20' or k[3:] == 'soilvwc36' or k[3:] == 'soilvwc0':
                if float(v) < 0.0 or float(v) > 0.80:
                    sensorLabel = "soil volumetric water content"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = round(v,3)
            if k[3:] == 'soilt4' or k[3:] == 'soilt8' or k[3:] == 'soilt20' or k[3:] == 'soilt36' or k[3:] == 'soilt0':
                if float(v) < -40.0 or float(v) > 60.0:
                    sensorLabel = "soil temperature"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = round(v,1)
            if k[3:] == 'soilec4' or k[3:] == 'soilec8' or k[3:] == 'soilec20' or k[3:] == 'soilec36' or k[3:] == 'soilec0':
                if float(v) <  0.0 or float(v) > 25.0:
                    sensorLabel = "soil electrical conductivity"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = round(v,3)
            if k[3:] == 'humiditytemp':
                if float(v) < -40.0 or float(v) > 60.0:
                    sensorLabel = "relative humidity temperature"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = round(v,1)
            if k[3:] == 'rrad630' or k[3:] == 'rrad800' or k[3:] == 'irad630' or k[3:] == 'irad800':
                if float(v) < 0.0 or float(v) > 1.0:
                    sensorLabel = "reflectance"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = round(v,4)
            if k[3:] == 'rradorient' or k[3:] == 'iradorient':
                    inval = int(round(v,0))
                    outval = "0:undetermined"
                    if inval == 1:
                        outval = "1:face-down"
                    if inval == 2:
                        outval = "2:face-up"                  
                    sensordict[k] = outval
            if k[3:] == 'rradalpha' or k[3:] == 'iradalpha':
                # http://manuals.decagon.com/Manuals/14597_SRS_Web.pdf
                if float(v) < 0.0 or float(v) > 3.0:
                    sensorLabel = "relectance alpha"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = int(round(v,4))
            if k[3:] == 'batteryper':
                if int(v) < 0 or int(v) > 100:
                    sensorLabel = "battery percentage"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = int(round(v,0))
            if k[3:] == 'batterymv':
                if int(v) < 0 or int(v) > 8000:
                    sensorLabel = "battery millivolts"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = int(round(v,0))
            if k[3:] == 'loggerpress':
                if float(v) < 40.0 or float(v) > 110.0:
                    sensorLabel = "logger pressure"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = round(v,4)
            if k[3:] == 'loggertemp':
                if float(v) < -40.0 or float(v) > 50.0:
                    sensorLabel = "logger temperature"
                    write_level1_metadata(mcometafile,recno,sensorLabel,v,NULL_VALUE)
                    sensordict[k] = NULL_VALUE
                else:
                    sensordict[k] = round(v,1)

    return sensordict

def get_mesowest_sensorUnits():
    mesowestDict = get_mesowest_dict()
    mcoSensorUnits = get_climateOffice_sensorUnits()
    for k,v in sorted(mesowestDict.iteritems()):
        v=v
        if k in mcoSensorUnits:
            mesowestDict[k]= mcoSensorUnits[k]    
    return mesowestDict

def get_climateOffice_sensorUnits():
    current_dict = {
            '01:recordnum':    "n",
            '02:apirecord':    " ",
            '03:apicode':      " ",            
            '04:timestamp':    "UTC zone",
            '05:localdate':    "Mtn zone",
            '06:solrad':       "W/m^2",
            '07:precipitation':"mm",
            '08:hitnum':       "n",
            '09:hitdist':      "km",            
            '10:winddir':      "deg",
            '11:windspeed':    "m/s",
            '12:windgust':     "m/s",
            '13:temperature':  "deg C",
            '14:relhumidity':  "ratio",
            '15:pressure':     "atm kPa",
            '16:sensortiltx':  "deg",
            '17:sensortilty':  "deg",
            '18:maxprecip':    "mm/hr",
            '19:humiditytemp': "deg C",
            '20:soilvwc4':     "m^3/m^3",
            '21:soilvwc8':     "m^3/m^3",
            '22:soilvwc20':    "m^3/m^3",
            '23:soilvwc36':    "m^3/m^3",
            '24:soilvwc0':     "m^3/m^3",
            '25:soilt4':       "deg C",
            '26:soilt8':       "deg C",
            '27:soilt20':      "deg C",
            '28:soilt36':      "deg C",
            '29:soilt0':       "deg C",
            '30:soilec4':      "mS/cm",
            '31:soilec8':      "mS/cm",
            '32:soilec20':     "mS/cm",
            '33:soilec36':     "mS/cm",
            '34:soilec0':      "mS/cm",
            '35:rrad630':      "watts/m^2/nm/sr",
            '36:rrad800':      "watts/m^2/nm/sr",
            '37:rradorient':   "n",
            '38:rradalpha':    "alpha",
            '39:irad630':      "watts/m^2/nm",
            '40:irad800':      "watts/m^2/nm",
            '41:iradorient':   "n",
            '42:iradalpha':    "alpha",
            '43:batteryper':   "%",
            '44:batterymv':    "mv",
            '45:loggerpress':  "atm kPa",
            '46:loggertemp':   "deg C"
            }
    return current_dict

def map_climateOfficeWeb_sensorDict(sensorDict,mobileDict):
    for k,v in mobileDict.iteritems():
        v=v
        if k in sensorDict:
            mobileDict[k]= sensorDict[k]
    return mobileDict

def map_climateOffice_sensorDict(sensorDict,datarow):
    rowindex = 0
    for k,v in sorted(sensorDict.iteritems()):
        v=v
        sensorDict[k]= datarow[rowindex]
        rowindex = rowindex+1
    return sensorDict

def map_mobile_sensorDict(tmaxDict,tmax24Dict,mobileDict):
    exceptionList = ['00:loggerusername','00:displayname','01:recordnum','02:apirecord','03:apicode','04:timestamp','05:localdate']
    # Map current and 24-hour values to mobile dictionary
    for k,v in sorted(mobileDict.iteritems()):
        v=v
        if k not in exceptionList and k in tmaxDict:
            try:
                mobileDict[k]['Value'] = tmaxDict[k]
            except AttributeError:
                mobileDict[k]['Value'] = str(NULL_VALUE)
            # try:
                # mobileDict[k]['Value24'] = tmax24Dict[k]
            # except AttributeError:
                # mobileDict[k]['Value24'] = str(NULL_VALUE)

    # Convert all NULL values to 'NA'
    for k,v in sorted(mobileDict.iteritems()):
        if k not in exceptionList:
            if mobileDict[k]['Value'] == str(NULL_VALUE):
                mobileDict[k]['Value'] = "NA"
            if mobileDict[k]['Value24'] == str(NULL_VALUE):
                mobileDict[k]['Value24'] = "NA"
               
    return mobileDict

def map_graph_sensorDict(sensorDict,graphDict,timestamp):
    for k,v in sorted(graphDict.iteritems()):
        v=v
        # Keyword match and graph value is not null
        # if sensorDict[k] == str(NULL_VALUE):
        #     print sensorDict[k]
        if k in sensorDict and k in graphDict and sensorDict[k] != str(NULL_VALUE) :
            graphDict[k]['timestamp'].append(timestamp)
            graphDict[k]['values'].append(sensorDict[k])
    return graphDict

def map_mesowest_sensorDict(sensorDict,mesowestDict):
    for k,v in sorted(mesowestDict.iteritems()):
        v=v
        if k in sensorDict:
            mesowestDict[k]= sensorDict[k]
    return mesowestDict

def get_mesowest_dict():
    current_dict = {
            '01:recordnum':    65535,
            '04:timestamp':    65535,
            '05:localdate':    65535,
            '06:solrad':       65535,
            '07:precipitation':65535,
            '08:hitnum':       65535,
            '09:hitdist':      65535,            
            '10:winddir':      65535,
            '11:windspeed':    65535,
            '12:windgust':     65535,
            '13:temperature':  65535,
            '14:relhumidity':  65535,
            '15:pressure':     65535,
            '18:maxprecip':    65535,
            '20:soilvwc4':     65535,
            '21:soilvwc8':     65535,
            '22:soilvwc20':    65535,
            '23:soilvwc36':    65535,
            '25:soilt4':       65535,
            '26:soilt8':       65535,
            '27:soilt20':      65535,
            '28:soilt36':      65535,
            '30:soilec4':      65535,
            '31:soilec8':      65535,
            '32:soilec20':     65535,
            '33:soilec36':     65535, 
           }
    return current_dict

def get_climateOffice_sensorDict():
    # 65535 is NULL or None
    current_dict = {
            '01:recordnum':    65535,
            '02:apirecord':    65535,
            '03:apicode':      65535,            
            '04:timestamp':    65535,
            '05:localdate':    65535,
            '06:solrad':       65535,
            '07:precipitation':65535,
            '08:hitnum':       65535,
            '09:hitdist':      65535,            
            '10:winddir':      65535,
            '11:windspeed':    65535,
            '12:windgust':     65535,
            '13:temperature':  65535,
            '14:relhumidity':  65535,
            '15:pressure':     65535,
            '16:sensortiltx':  65535,
            '17:sensortilty':  65535,
            '18:maxprecip':    65535,
            '19:humiditytemp': 65535,
            '20:soilvwc4':     65535,
            '21:soilvwc8':     65535,
            '22:soilvwc20':    65535,
            '23:soilvwc36':    65535,
            '24:soilvwc0':     65535,
            '25:soilt4':       65535,
            '26:soilt8':       65535,
            '27:soilt20':      65535,
            '28:soilt36':      65535,
            '29:soilt0':       65535,
            '30:soilec4':      65535,
            '31:soilec8':      65535,
            '32:soilec20':     65535,
            '33:soilec36':     65535,
            '34:soilec0':      65535,
            '35:rrad630':      65535,
            '36:rrad800':      65535,
            '37:rradorient':   65535,
            '38:rradalpha':    65535,
            '39:irad630':      65535,
            '40:irad800':      65535,
            '41:iradorient':   65535,
            '42:iradalpha':    65535,
            '43:batteryper':   65535,
            '44:batterymv':    65535,
            '45:loggerpress':  65535,
            '46:loggertemp':   65535
            }
    return current_dict
