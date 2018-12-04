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
import datetime
import config
import configdownload
import pandas as pd
import json
import timeconvert
import urllib2
import misc
import time
#==========================================================================
# Class Definition
#==========================================================================
class HttpsRequest():
    
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
        
    #==========================================================
    # Functions for URL response
    #==========================================================
    def get_device_readings(self,device_serial_number,device_password,starttime,endtime):
        # Check for empty start time.  If start time is empty set to latest day
        if not starttime:
            starttime = self.zentraconfig.latest_day
        # naive_dt = self.timeconv.datestr_to_naive_dt(starttime)
        utcms_start = str(self.timeconv.naive_dt_to_utcms(starttime))
        if not endtime:
            endtime = starttime
        # naive_dt = self.timeconv.datestr_to_naive_dt(endtime)
        utcms_end = str(self.timeconv.naive_dt_to_utcms(endtime))
        print "START:", starttime, utcms_start, " END: ", endtime, utcms_end
        # Build request URL        
        requesturl = ('http://' + self.zentraconfig.zentra_api_ip_address + '/api/v1/readings'
                      + '?' + "user=" + self.zentraconfig.zentra_api_user
                      + '&' + "user_password=" + self.zentraconfig.zentra_api_user_password
                      + '&' + "sn=" + device_serial_number
                      + '&' + "device_password=" + device_password
                      + '&' + "start_time=" + utcms_start
                      + '&' + "end_time=" + utcms_end                    
                      )
        # Make request
        # print requesturl
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

    def get_device_settings(self,device_serial_number,device_password):
        # Build request URL
        requesturl = ('http://' + self.zentraconfig.zentra_api_ip_address + '/api/v1/settings'
                      + '?' + "user=" + self.zentraconfig.zentra_api_user
                      + '&' + "user_password=" + self.zentraconfig.zentra_api_user_password
                      + '&' + "sn=" + device_serial_number
                      + '&' + "device_password=" + device_password
                      )
        # Make request
        # print requesturl
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
    def get_response_url(self,response):
        return response.geturl()
    
    def get_response_info(self,response):
        return response.info()

    #==========================================================
    # Functions for managing content from URL response
    #==========================================================
    def print_readings(self,readings):
        print json.dumps(readings, sort_keys=True, indent=4, ensure_ascii=False)
        return

    def print_settings(self,settings):
        print json.dumps(settings, sort_keys=True, indent=4, ensure_ascii=False)
        return

    def create_settings_path(self,station,theday):
        # Declare output file name
        zentrapath = self.miscfunc.local_normpath(self.zentraconfig.zentra_settings_folder,station)
        zentrapath = self.miscfunc.local_normpath(zentrapath,str(theday.year))
        self.miscfunc.check_if_path_exists(zentrapath)                                      
        zentrafilename = "Settings" + self.miscfunc.folder_string_from_date(theday) + ".json"        
        zentrapath = self.miscfunc.local_normpath(zentrapath,zentrafilename)
        return zentrapath
    
    def create_outputJSONsettings_forClimateOffice(self,zentrapath,response):
        # Declare output file name
        settingsdict = self.get_settings_as_dictionary(response)
        self.write_as_MCO_JSON(zentrapath,settingsdict)
        return settingsdict

    def create_readings_path(self,station,theday):
        # Declare output file name
        zentrapath = self.miscfunc.local_normpath(self.zentraconfig.zentra_readings_folder,station)
        zentrapath = self.miscfunc.local_normpath(zentrapath,str(theday.year))                                    
        self.miscfunc.check_if_path_exists(zentrapath) 
        zentrafilename = "Readings" + self.miscfunc.folder_string_from_date(theday) + ".json"        
        zentrapath = self.miscfunc.local_normpath(zentrapath,zentrafilename)
        return zentrapath
    
    def create_outputJSONreadings_forClimateOffice(self,zentrapath,response):
        # Declare output file name
        readingsdict = self.get_readings_as_dictionary(response)
        self.write_as_MCO_JSON(zentrapath,readingsdict)
        return readingsdict

    def write_as_MCO_JSON(self,outFile,outDict):
        # print "Size of dictionary in bytes is: ", sys.getsizeof(settingsDict)
        f = open(outFile,'w')
        f.write(json.dumps(outDict))
        # for chunk in json.JSONEncoder().iterencode(settingsDict):
        #    f.write(chunk)
        f.close
        return
    
    def read_as_MCO_JSON(self,inFile):
        f = open(inFile, 'r')
        inDict = json.loads(f.read())
        f.close
        return inDict
    
    #==========================================================
    # Functions for Level One information for Readings
    #==========================================================
    def get_readings_as_dictionary(self,response):
        readings_str = response.read()
        readings_dict = json.loads(readings_str)
        return readings_dict # returns dictionary
    
    #==========================================================
    # Functions for Level One information for Settings
    #==========================================================
    def get_settings_as_dictionary(self,response):
        settings_str = response.read()
        settings_dict = json.loads(settings_str)
        return settings_dict # returns dictionary
    
    #=========================================================================
    # Functions for automating download for a single device over a time period
    #=========================================================================

    def download_files(self,station,device_serial_number,device_password,starttime,endtime):
        """
            Downloads the raw Zentra files using the Zentra URL command string for a Zentra folder for a given day
            INPUT: Start date and end date as date-time object
            OUTPUT: Array of dates downloaded
        """
        # Derive latest day
        self.zentraconfigdownload.set_latest_day(endtime)
        lastday = self.zentraconfigdownload.latestday
        # print self.zentraconfigdownload.latestday, self.zentraconfigdownload.latestdaystring
        # Derive first day
        self.zentraconfigdownload.set_first_day(starttime)
        firstday = self.zentraconfigdownload.firstday
        # print self.zentraconfigdownload.firstday, self.zentraconfigdownload.firstdaystring
        
        # Validate start of date range
        # If requested start day is greater than latest day, set start day to latest day
        if firstday > lastday:
            firstday = lastday
        # Strip time from date
        firstday = datetime.datetime(year=firstday.year,month=firstday.month,day=firstday.day)
        lastday = datetime.datetime(year=lastday.year,month=lastday.month,day=lastday.day)
        # Build day array given date range
        datearray = pd.date_range(firstday,lastday,freq="D")
        # For each day in range download files
        for d in range(0,len(datearray)):
            before_midnight = datearray[d]+datetime.timedelta(days=1)-datetime.timedelta(milliseconds=1)
            zreadings = self.get_device_readings(device_serial_number,device_password,datearray[d],before_midnight)
            zreadingspath = self.create_readings_path(station,datearray[d])
            self.create_outputJSONreadings_forClimateOffice(zreadingspath,zreadings)
            time.sleep(self.zentraconfig.timedelay)
            zsettings = self.get_device_settings(device_serial_number,device_password)
            zsettingspath = self.create_settings_path(station,datearray[d])
            self.create_outputJSONsettings_forClimateOffice(zsettingspath,zsettings)
            time.sleep(self.zentraconfig.timedelay)
        # Return array of dates downloaded
        return datearray


#==========================================================================
# Main and tests
#==========================================================================
if __name__ == "__main__":
    # Load user configuration settings as configuration object
    zconfig = config.ZentraConfig()
    # Load Zentra configuration settings as configuration object
    zconfigdownload = configdownload.ZentraDownloadConfig()
    # Load http request object
    zhttp = HttpsRequest(zconfig,zconfigdownload)
    # Load miscellaneous functions
    miscfn = misc.Pathways()
    """
    # Create start and end test dates
    testday1 = datetime.datetime(year=2018,month=5,day=6)
    testday2 = datetime.datetime(year=2018,month=5,day=7)
    
    # Write readings dictionary
    zreadings = zhttp.get_device_readings("06-00184", "imdue-dabr",testday1,testday2)
    # print zhttp.get_response_url(zreadings)
    # print zhttp.get_response_info(zreadings)
    # print zhttp.print_readings(zreadings)
    zreadingspath = zhttp.create_readings_path("ebarlowr",testday1)
    readingsdict = zhttp.create_outputJSONreadings_forClimateOffice(zreadingspath,zreadings)
    
    # Write settings dictionary
    zsettings = zhttp.get_device_settings("06-00184", "imdue-dabr")
    # print zhttp.get_response_url(zsettings)
    # print zhttp.get_response_info(zsettings)
    # print zhttp.print_settings(zsettings)
    zsettingspath = zhttp.create_settings_path("ebarlowr",testday1)
    settingsdict = zhttp.create_outputJSONsettings_forClimateOffice(zsettingspath,zsettings)
    
    # Read back in and write out (compare files)
    readingsdict = zhttp.read_as_MCO_JSON(zreadingspath)
    f = open(zreadingspath+"2",'w')
    f.write(json.dumps(readingsdict))
    f.close
    
    # Read back in and write out (compare files)
    settingsdict = zhttp.read_as_MCO_JSON(zsettingspath)
    f = open(zsettingspath+"2",'w')
    f.write(json.dumps(settingsdict))
    f.close
    """
    # Create start and end test dates
    testday1 = datetime.datetime(year=2018,month=5,day=17)
    testday2 = datetime.datetime(year=2018,month=5,day=17)   
    testday1 = datetime.datetime.now()
    testday2 = testday1
    # Test bulk download
    datearray = zhttp.download_files("ebarlowr","06-00184", "imdue-dabr",testday1,testday2)
    print datearray
#==========================================================================
# END
#==========================================================================
