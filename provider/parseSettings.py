#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@created="May 2018"
@description=('This Zentra class provides the properties and',
              'functions that define the parameters necessary',
              'to process Zentra content for use by the'
              'Montana Climate Office),
@attention='http://climate.umt.edu
@author: 'Michael D. Sweet',
@email='michael.sweet@umontana.edu',
@organization: 'Montana Climate Office'
#==========================================================================
# USE
#==========================================================================
This class is instantiated to provide resource variables and methods
for downloading raw Zentra content using REST JSON protocols
'''

import util.config as zentraconfig
import util.configdownload as zentraconfigdownload
import util.httpsget as zentrahttp
import util.misc as misc
import provider.Mesonet as mesonet
import util.timeconvert as timeconvert
import datetime
import numpy as np

#==========================================================================
# Class Definition
#==========================================================================
class ParseDictionary():
    
    """
        Configuration file for downloading Zentra station data from
        https://zentra.com and writing to local path 
        \\mcofiles\Resources$\Data\Mesonet
        
        Load using:
            import util.httpsget
    """

    #==========================================================================
    # Methods for object instantiation
    #==========================================================================
    def __init__(self,zentraconfig,zentraconfigdownload):
        """
            Initializes properties for Zentra HTTPS request object
            INPUTS: ZentraConfig() object from config.py
                    ZentraDownloadConfig() object from configdownload.py
         """
        # Load user configuration settings as configuration object
        self.zentraconfig = zentraconfig
        # Load Zentra configuration settings as configuration object
        self.zentraconfigdownload = zentraconfigdownload
        # Load Zentra-Mesonet time conversion functions
        self.timeconv = timeconvert.MesonetTimeConvert()
        # Load Zentra-Mesonet miscellaneous functions
        self.miscfunc = misc.Pathways()
        # Load http request object
        self.zhttp = zentrahttp.HttpsRequest(self.zentraconfig,self.zentraconfigdownload)
        # Mesonet station object instantiation
        self.monet = mesonet.MesonetStations()

    #==========================================================
    # Functions for Level One information for Readings
    #==========================================================
    """
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
    """

    #==========================================================
    # Functions for Level One information (Device)
    #==========================================================
    def get_settings_device(self,settings):
        # val = json.dumps(readings['get_readings_ver'])
        val = settings['device']
        return val # returns dictionary
    
    #==========================================================
    # Functions for Level Two information (Device)
    #==========================================================

    def get_device_measurement_settings(self,device):
        # val = json.dumps(readings['get_readings_ver'])
        val = device['measurement_settings']
        return val # returns list of dictionaries

    def get_device_time_settings(self,device):
        # val = json.dumps(readings['get_readings_ver'])
        val = device['time_settings']
        return val # returns dictionary

    def get_device_info(self,device):
        # val = json.dumps(readings['get_readings_ver'])
        val = device['device_info']
        return val # returns dictionary

    def get_device_locations(self,device):
        # val = json.dumps(readings['get_readings_ver'])
        val = device['locations']
        return val # returns dictionary

    def get_device_installation_metadata(self,device):
        # val = json.dumps(readings['get_readings_ver'])
        val = device['installation_metadata']
        return val # returns dictionary

    #==========================================================
    # Functions for Level Three information
    #==========================================================
    def extract_current_measurement_settings(self,measurement_settings,mcodict):
        # Measurement Settings is a list
        mcodict['01:measurement_interval'] = measurement_settings[0]['measurement_interval_seconds']
        mcodict['02:valid_since'] = measurement_settings[0]['valid_since']
        return mcodict # returns dictionary

    def extract_current_device_info(self,device_info,mcodict):
        # Device Info is a dictionary
        mcodict['03:device_type'] =  device_info['device_type']
        mcodict['04:device_sn'] =    device_info['device_sn']
        mcodict['05:device_fw'] =    device_info['device_fw']
        mcodict['06:device_trait'] = device_info['device_trait']
        return mcodict # returns dictionary

    def extract_current_location(self,locations,mcodict):
        # Locations is a list
        longitude_list = []
        latitude_list = []
        accuracy_list = []
        altitude_list = []
        satellite_list = []
        for item in locations:
            longitude_list.append(item['longitude'])
            latitude_list.append(item['latitude']) 
            if item['accuracyEstimate_mm'] < 100000:
                if not np.isnan(item['accuracyEstimate_mm']):
                    accuracy_list.append(item['accuracyEstimate_mm'])
            if item['accuracyEstimate_mm'] < 10000000.0:
                if not np.isnan(item['altitude_mm']):
                    altitude_list.append(item['altitude_mm'])
            if item['satelliteVehicles'] > 0 and item['satelliteVehicles'] < 20:
                satellite_list.append(item['satelliteVehicles'])
        if longitude_list:
            mcodict['07:longitude'] = np.round(np.mean(longitude_list),7)
        if latitude_list:
            mcodict['08:latitude'] =  np.round(np.mean(latitude_list),7)
        if accuracy_list:
            mcodict['09:accuracy'] =  int(np.round(np.mean(accuracy_list),0))
        if altitude_list:
            mcodict['10:altitude'] =  int(np.round(np.mean(altitude_list),0))
        if satellite_list:
            mcodict['11:satellite'] = int(np.round(np.mean(satellite_list),0))
        return mcodict # returns dictionary

    #==========================================================
    # Functions for Level Four information (Sensors)
    #==========================================================

    #==========================================================
    # Functions for Level Five information (Sensor Values)
    #==========================================================

    #==========================================================
    # Functions for Climate Office standardized dictionary
    #==========================================================
    def get_climateOffice_settingsDict(self):
        # zconfig.zentra_NULL_VALUE is NULL or None
        current_dict = {
                '01:measurement_interval': self.zentraconfig.zentra_NULL_VALUE,
                '02:valid_since':          self.zentraconfig.zentra_NULL_VALUE,
                '03:device_type':          self.zentraconfig.zentra_NULL_VALUE,
                '04:device_sn':            self.zentraconfig.zentra_NULL_VALUE,
                '05:device_fw':            self.zentraconfig.zentra_NULL_VALUE,
                '06:device_trait':         self.zentraconfig.zentra_NULL_VALUE,
                '07:longitude':            self.zentraconfig.zentra_NULL_VALUE,    
                '08:latitude':             self.zentraconfig.zentra_NULL_VALUE,
                '09:accuracy':             self.zentraconfig.zentra_NULL_VALUE,
                '10:altitude':             self.zentraconfig.zentra_NULL_VALUE,
                '11:satellite':            self.zentraconfig.zentra_NULL_VALUE
                }
        return current_dict

    def print_climateOffice_mcoDict(self,mcoDict):
        for k,v in sorted(mcoDict.iteritems()):
            print k, v
        return

    def fill_climateOffice_mcoDict(self,station,theday):
        # Initialize NULL dictionary
        mcoDict = self.get_climateOffice_settingsDict()
        # Initialize NULL dictionary
        settingsdict = {}
        # Get path to station's JSON output for this day
        zsettingspath = self.zhttp.create_settings_path(station,theday)
        print "Processing: ", zsettingspath
        # Check if path exists
        if self.miscfunc.check_if_file_path_exists(zsettingspath):
            # If path exists, read JSON into dictionary
            settingsdict = self.zhttp.read_as_MCO_JSON(zsettingspath)
            if 'device' in settingsdict.keys():
                device = self.get_settings_device(settingsdict)
                measurement_settings = self.get_device_measurement_settings(device)
                # time_settings = self.get_device_time_settings(device)
                device_info = self.get_device_info(device)
                locations = self.get_device_locations(device)
                # installation_metadata = self.get_device_installation_metadata(device)
                #
                mcoDict = self.extract_current_measurement_settings(measurement_settings,mcoDict)
                mcoDict = self.extract_current_device_info(device_info,mcoDict)
                mcoDict = self.extract_current_location(locations,mcoDict)
                # self.print_climateOffice_mcoDict(mcoDict)
        return mcoDict
    
#==========================================================================
# Main and tests
#==========================================================================
if __name__ == "__main__":
    # Load user configuration settings as configuration object
    zconfig = zentraconfig.ZentraConfig()
    # Load Zentra configuration settings as configuration object
    zconfigdownload = zentraconfigdownload.ZentraDownloadConfig()
    # Instantiate time conversion class
    timeconv = timeconvert.MesonetTimeConvert()
    # Load http request object
    zhttp = zentrahttp.HttpsRequest(zconfig,zconfigdownload)
    # Mesonet station object instantiation
    monet = mesonet.MesonetStations()
    # Load miscellaneous pathway functions
    miscfn = misc.Pathways()
    # Instantiate parsing object
    zparse = ParseDictionary(zconfig,zconfigdownload)
    # Populate MCO sensor dictionary
    # testday = datetime.datetime(year=2018,month=5,day=3)
    testday = datetime.datetime(year=2017,month=7,day=1)
    station = "lubrecht"
    settingsdict = zparse.fill_climateOffice_mcoDict(station,testday)
    # zparse.print_climateOffice_mcoDict(settingsdict)
    
#==========================================================================
# END
#==========================================================================
        