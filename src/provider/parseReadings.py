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
import datetime
import util.timeconvert as timeconvert

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
    def get_readings_version(self,readings):
        # val = json.dumps(readings['get_readings_ver'])
        val = readings['get_readings_ver']
        return val # returns integer
    
    def get_readings_created(self,readings):
        # val = json.dumps(readings['created'])
        val = readings['created']
        return val # returns UTC date as string
    
    def get_readings_device(self,readings):
        # val = json.dumps(readings['device'])
        val = readings['device']
        return val # returns dictionary

    #==========================================================
    # Functions for Level Two information (Device)
    #==========================================================
    def get_device_info(self,device):
        val = device['device_info'] 
        return val # returns dictionary
    
    def get_device_type(self,device):
        val = device['device_type']
        return val # returns integer
    
    def get_device_serialno(self,device):
        val = device['device_sn'] 
        return val # returns string
    
    def get_device_firmware(self,device):
        val = device['device_fw']
        return val # returns integer
    
    def get_device_trait(self,device):
        val = device['device_trait']
        return val # returns integer

    def get_timeseries(self,device):
        val = device['timeseries']
        return val # returns list

    #==========================================================
    # Functions for Level Three information (Configurations)
    #==========================================================
    # Configuration is the only item in dictionary.
    # Sensor dictionaries are within the Configuration (level four)

    def get_config_sensors(self,config):
        val = config['sensors']
        return val # returns list
    
    def get_config_values(self,config):
        val = config['values']
        return val # returns list

    #==========================================================
    # Functions for Level Four information (Sensors)
    #==========================================================
    def get_sensor_serialno(self,sensor):
        val = sensor['sensor_sn']
        return val # returns text

    def get_sensor_bonusval(self,sensor):
        val = sensor['sensor_bonus_value']
        return val # returns text

    def get_sensor_measurements(self,sensor):
        val = sensor['measurements']
        return val # returns list

    def get_sensor_firmware_ver(self,sensor):
        val = sensor['sensor_firmware_ver']
        return val # returns text

    def get_sensor_number(self,sensor):
        val = sensor['sensor_number']
        return val # returns integer
    
    def get_sensor_port(self,sensor):
        val = sensor['port']
        return val # returns integer
    
    def get_sensors(self,sensors):
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
    # Functions for Level Five information (Sensor Values)
    #==========================================================
    def get_value_list(self,value):
        val = value[0]
        return val # returns list

    def get_value_timestamp(self,value):
        val = value[0]
        return val # returns integer
    
    def get_value_recordno(self,value):
        val = value[1]
        return val # returns integer
    
    def get_value_recordcode(self,value):
        val = value[2]
        return val # returns integer

    def get_value_sensors(self,value):
        val = value[3]
        return val # returns integer

    #==========================================================
    # Functions for Climate Office parsing of sensor
    #==========================================================

    def parse_for_sensor(self,mcoDict,sensor,valuelist,sensor_config_dict):
        # print "SENSOR"
        # print self.get_sensor_serialno(sensor)
        # print self.get_sensor_bonusval(sensor)
        # print self.get_sensor_measurements(sensor)
        # print self.get_sensor_firmware_ver(sensor)
        # print self.get_sensor_number(sensor)
        # print self.get_sensor_port(sensor)
        sensorNum = self.get_sensor_number(sensor)
        # print "Parsing for: ", int(sensorNum), valuelist
        if sensorNum == 93:
            measkeylist = self.get_sensor_measurements(sensor)
            mcoDict = self.parse_for_sensor093(mcoDict,measkeylist,valuelist)
        if sensorNum == 114:
            measkeylist = self.get_sensor_measurements(sensor)
            # ERROR TRAP: Have had cases where values for these sensors are switched
            if 'SI_630_R' in measkeylist:
                mcoDict = self.parse_for_sensor114(mcoDict,measkeylist,valuelist)
            if 'SI_630_I' in measkeylist:
                mcoDict = self.parse_for_sensor115(mcoDict,measkeylist,valuelist)
        if sensorNum == 115:
            measkeylist = self.get_sensor_measurements(sensor)
            # ERROR TRAP: Have had cases where values for these sensors are switched
            if 'SI_630_I' in measkeylist:
                mcoDict = self.parse_for_sensor115(mcoDict,measkeylist,valuelist)
            if 'SI_630_R' in measkeylist:
                mcoDict = self.parse_for_sensor114(mcoDict,measkeylist,valuelist)
        if sensorNum == 103:
            measkeylist = self.get_sensor_measurements(sensor)
            mcoDict = self.parse_for_sensor119(mcoDict,measkeylist,valuelist,sensor_config_dict)
        if sensorNum == 119:
            measkeylist = self.get_sensor_measurements(sensor)
            mcoDict = self.parse_for_sensor119(mcoDict,measkeylist,valuelist,sensor_config_dict)
        if sensorNum == 133:
            measkeylist = self.get_sensor_measurements(sensor)
            mcoDict = self.parse_for_sensor133(mcoDict,measkeylist,valuelist)
        if sensorNum == 134:
            measkeylist = self.get_sensor_measurements(sensor)
            mcoDict = self.parse_for_sensor134(mcoDict,measkeylist,valuelist)
        return mcoDict
    
    def parse_for_sensor093(self,mcoDict,measkeylist,valuelist):
        mcoDict['06:solrad'] =          valuelist[measkeylist.index('SOLARRAD')]
        mcoDict['07:precipitation'] =   valuelist[measkeylist.index('MILLRAIN')]
        mcoDict['08:hitnum'] =          valuelist[measkeylist.index('LIGHTNING_COUNT')]
        mcoDict['09:hitdist'] =         valuelist[measkeylist.index('LIGHTNING_KM')]
        mcoDict['10:winddir'] =         valuelist[measkeylist.index('DIRECTION')]
        mcoDict['11:windspeed'] =       valuelist[measkeylist.index('WINDSPEEDMPS')]
        mcoDict['12:windgust'] =        valuelist[measkeylist.index('WINDGUSTS')]
        mcoDict['13:temperature'] =     valuelist[measkeylist.index('TEMPC_AIR')]
        mcoDict['14:relhumidity'] =     valuelist[measkeylist.index('RELHUMID')]
        mcoDict['15:pressure'] =        valuelist[measkeylist.index('ATMOS_KPA')]
        mcoDict['16:sensortiltx'] =     valuelist[measkeylist.index('ACCELEROMETER_X')]
        mcoDict['17:sensortilty'] =     valuelist[measkeylist.index('ACCELEROMETER_Y')]
        mcoDict['18:maxprecip'] =       valuelist[measkeylist.index('MAXRAINRATE')]
        mcoDict['19:humiditytemp'] =    valuelist[measkeylist.index('TEMPC_RH_SENSOR')]
        return mcoDict
    
    def parse_for_sensor114(self,mcoDict,measkeylist,valuelist):
        mcoDict['35:rrad630'] =     valuelist[measkeylist.index('SI_630_R')]
        mcoDict['36:rrad800'] =     valuelist[measkeylist.index('SI_800_R')]
        mcoDict['37:rradorient'] =  valuelist[measkeylist.index('SRS_ROTATION')]
        mcoDict['38:rradalpha'] =   valuelist[measkeylist.index('ALPHA_FOR_NDVI')]
        return mcoDict
    
    def parse_for_sensor115(self,mcoDict,measkeylist,valuelist):
        mcoDict['39:irad630'] =     valuelist[measkeylist.index('SI_630_I')]
        mcoDict['40:irad800'] =     valuelist[measkeylist.index('SI_800_I')]
        mcoDict['41:iradorient'] =  valuelist[measkeylist.index('SRS_ROTATION')]
        mcoDict['42:iradalpha'] =   valuelist[measkeylist.index('ALPHA_FOR_NDVI')]
        return mcoDict
    
    def parse_for_sensor119(self,mcoDict,measkeylist,valuelist, configdict):
        # "PARSE 119"
        # print portnum
        # print measkeylist
        # print valuelist
        # print configdict.sensorDepth
        # print configdict
        if configdict.sensorDepth > -4 and configdict.sensorDepth < 0:
                if configdict.surfaceType <> "vegetated":
                    mcoDict['20:soilvwc4'] =   valuelist[measkeylist.index('VOLWATER')]
                    mcoDict['25:soilt4'] =     valuelist[measkeylist.index('TEMPC_SOIL')]
                    mcoDict['30:soilec4'] =    valuelist[measkeylist.index('SOIL_EC_SAT_EXT')] 
                else:
                    mcoDict['24:soilvwc0'] =   valuelist[measkeylist.index('VOLWATER')]
                    mcoDict['29:soilt0'] =     valuelist[measkeylist.index('TEMPC_SOIL')]
                    mcoDict['34:soilec0'] =    valuelist[measkeylist.index('SOIL_EC_SAT_EXT')] 

        if configdict.sensorDepth > -16 and configdict.sensorDepth <= -4:  
                mcoDict['21:soilvwc8'] =   valuelist[measkeylist.index('VOLWATER')]
                mcoDict['26:soilt8'] =     valuelist[measkeylist.index('TEMPC_SOIL')]
                mcoDict['31:soilec8'] =    valuelist[measkeylist.index('SOIL_EC_SAT_EXT')] 
    
        if configdict.sensorDepth > -28 and configdict.sensorDepth <= -16:
                mcoDict['22:soilvwc20'] =   valuelist[measkeylist.index('VOLWATER')]
                mcoDict['27:soilt20'] =     valuelist[measkeylist.index('TEMPC_SOIL')]
                mcoDict['32:soilec20'] =    valuelist[measkeylist.index('SOIL_EC_SAT_EXT')] 
    
        if configdict.sensorDepth <= -28:
                mcoDict['23:soilvwc36'] =   valuelist[measkeylist.index('VOLWATER')]
                mcoDict['28:soilt36'] =     valuelist[measkeylist.index('TEMPC_SOIL')]
                mcoDict['33:soilec36'] =    valuelist[measkeylist.index('SOIL_EC_SAT_EXT')] 
            
        return mcoDict

    def parse_for_sensor133(self,mcoDict,measkeylist,valuelist):
        mcoDict['43:batteryper'] = valuelist[measkeylist.index('BATTERY')]
        mcoDict['44:batterymv'] = valuelist[measkeylist.index('BATTERY_MV')]
        return mcoDict
    
    def parse_for_sensor134(self,mcoDict,measkeylist,valuelist):
        mcoDict['45:loggerpress'] = valuelist[measkeylist.index('REFERENCE_KPA')]
        mcoDict['46:loggertemp'] = valuelist[measkeylist.index('TEMPC_LOGGER')]
        return mcoDict

    #==========================================================
    # Functions for Climate Office standardized dictionary
    #==========================================================
    def get_climateOffice_sensorDict(self):
        # zconfig.zentra_NULL_VALUE is NULL or None
        current_dict = {
                '01:recordnum':    self.zentraconfig.zentra_NULL_VALUE,
                '02:apirecord':    self.zentraconfig.zentra_NULL_VALUE,
                '03:apicode':      self.zentraconfig.zentra_NULL_VALUE,            
                '04:timestamp':    self.zentraconfig.zentra_NULL_VALUE,
                '05:localdate':    self.zentraconfig.zentra_NULL_VALUE,
                '06:solrad':       {},
                '07:precipitation':{},
                '08:hitnum':       {},
                '09:hitdist':      {},            
                '10:winddir':      {},
                '11:windspeed':    {},
                '12:windgust':     {},
                '13:temperature':  {},
                '14:relhumidity':  {},
                '15:pressure':     {},
                '16:sensortiltx':  {},
                '17:sensortilty':  {},
                '18:maxprecip':    {},
                '19:humiditytemp': {},
                '20:soilvwc4':     {},
                '21:soilvwc8':     {},
                '22:soilvwc20':    {},
                '23:soilvwc36':    {},
                '24:soilvwc0':     {},
                '25:soilt4':       {},
                '26:soilt8':       {},
                '27:soilt20':      {},
                '28:soilt36':      {},
                '29:soilt0':       {},
                '30:soilec4':      {},
                '31:soilec8':      {},
                '32:soilec20':     {},
                '33:soilec36':     {},
                '34:soilec0':      {},
                '35:rrad630':      {},
                '36:rrad800':      {},
                '37:rradorient':   {},
                '38:rradalpha':    {},
                '39:irad630':      {},
                '40:irad800':      {},
                '41:iradorient':   {},
                '42:iradalpha':    {},
                '43:batteryper':   {},
                '44:batterymv':    {},
                '45:loggerpress':  {},
                '46:loggertemp':   {}
                }
        return current_dict

    def print_climateOffice_mcoDict(self,mcoDict):
        for k,v in sorted(mcoDict.iteritems()):
            print k, v
        return

    def fill_climateOffice_mcoDict(self,station,theday):
        # Initialize NULL dictionary
        mcoDict = self.get_climateOffice_sensorDict()
        mcoReadingsDict = {}
        # Get path to station's JSON output for this day
        zreadingspath = self.zhttp.create_readings_path(station,theday)
        print "Processing: ", zreadingspath
        # Check if path exists
        if self.miscfunc.check_if_file_path_exists(zreadingspath):
            # If path exists, read JSON into dictionary
            readingsdict = self.zhttp.read_as_MCO_JSON(zreadingspath)
            # print self.get_readings_version(readingsdict)
            # print self.get_readings_created(readingsdict)
            # Check if legit device dictionary
            if 'device' in readingsdict.keys():
                # Get device dictionary
                zdevicedict = self.get_readings_device(readingsdict)
                
                # Get device info dictionary
                zdeviceinfodict = self.get_device_info(zdevicedict)
                # print self.get_device_type(zdeviceinfodict)
                # print self.get_device_serialno(zdeviceinfodict)
                # print self.get_device_firmware(zdeviceinfodict)
                # print self.get_device_trait(zdeviceinfodict)
    
                # Get time series list for this device
                ztimeserieslist = self.get_timeseries(zdevicedict)
    
                # Process each time series configuration in list
                rowcount=1
                for ztimeseriesconfigdict in ztimeserieslist:
                    for zconfigkey,zconfigvalue in ztimeseriesconfigdict.items():
                        zconfigkey = zconfigkey
                        # print zparse.get_config_valid_since(zconfigvalue)
                        zsensorlist = self.get_config_sensors(zconfigvalue)
                        
                        # get a list of values for this sensor
                        zvaluelist = self.get_config_values(zconfigvalue)
                        for zvalue in zvaluelist:
                            # print a list of sensors for this device
                            # zparse.get_sensors(zsensorlist)
                            # Initialize MCO dictionary for this record
                            mcoDict = self.get_climateOffice_sensorDict()
                            mcoDict["01:recordnum"] = rowcount
                            mcoDict["02:apirecord"] = self.get_value_recordno(zvalue)
                            mcoDict["03:apicode"] = self.get_value_recordcode(zvalue)
                            mcoDict["04:timestamp"] = self.get_value_timestamp(zvalue)
                            mcoDict["05:localdate"] = self.timeconv.UTCms_to_localstring(self.get_value_timestamp(zvalue))
                            rowcount = rowcount+1
                            for zsensor in zsensorlist:
                                # Get value list index from position in sensor list
                                subListIndex = zsensorlist.index(zsensor)+3  # add index offset
                                # Get value list for this sensor
                                subList = zvalue[subListIndex]
                                # print zsensor['port'],subList
                                # Parse the values for this sensor to build common dictionary
                                if zsensor['port'] in self.monet.port_list:
                                    configkey = station+'{:0>2d}'.format(zsensor['port'])+'{:0>1d}'.format(0)
                                    if self.monet.sensor_config_dict.has_key(configkey):
                                        startdate = self.monet.sensor_config_dict[configkey].localStartDate
                                        enddate = self.monet.sensor_config_dict[configkey].localEndDate
                                        if startdate <= theday <= enddate:
                                            # print "CONFIG: 0"
                                            # print zsensor['port'],monet.sensor_config_dict[configkey].sensorKey
                                            # print startdate,testday,enddate
                                            # print
                                            sensorconfig = self.monet.sensor_config_dict[configkey]
                                            mcoDict = self.parse_for_sensor(mcoDict,zsensor,subList,sensorconfig)
                                    else:
                                        for configcount in range(1,10):           
                                            configkey = station+'{:0>2d}'.format(zsensor['port'])+'{:0>1d}'.format(configcount)
                                            if self.monet.sensor_config_dict.has_key(configkey):
                                                startdate = self.monet.sensor_config_dict[configkey].localStartDate
                                                enddate = self.monet.sensor_config_dict[configkey].localEndDate
                                                if startdate <= theday <= enddate:
                                                    # Process other possible configurations (up to 9)
                                                    # print "CONFIG: ", configcount
                                                    # print zsensor['port'],monet.sensor_config_dict[configkey].sensorKey
                                                    # print startdate,testday,enddate
                                                    # print
                                                    sensorconfig = self.monet.sensor_config_dict[configkey]                        
                                                    mcoDict = self.parse_for_sensor(mcoDict,zsensor,subList,sensorconfig)
                                else:
                                    # Address sensor not covered in sensor configuration table (e.g. Sensors 133 and 134)
                                    nullsensorconfig = {}
                                    mcoDict = self.parse_for_sensor(mcoDict,zsensor,subList,nullsensorconfig)
                            # Zentra retrieves excess records.  Test if record in this day
                            if self.timeconv.if_record_dt_sameday(mcoDict["05:localdate"],theday):
                                mcoReadingsDict[mcoDict["04:timestamp"]] = mcoDict
        return mcoReadingsDict
    
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
    testday = datetime.datetime(year=2018,month=8,day=31)
    # testday = datetime.datetime(year=2017,month=7,day=1)
    station = "lomawood"
    mcoreadings = zparse.fill_climateOffice_mcoDict(station,testday)
    for k,v in sorted(mcoreadings.iteritems()):
        print timeconv.UTCms_to_localstring(k)
    
#==========================================================================
# END
#==========================================================================
        