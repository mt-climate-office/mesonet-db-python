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
import util.config as config
import util.configdownload as configdownload
import util.misc as misc
import csv

#==========================================================================
# Class Definition
#==========================================================================
class metadataClimateOffice():
    
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
        # Load Zentra-Mesonet miscellaneous functions
        self.miscfunc = misc.Pathways()
        
    #==========================================================
    # Functions for Montana Climate Office metadata production
    #==========================================================

    def create_metadata_path(self,station) :
        # Declare output file name
        filename = "MCO-Metadata-" + station + ".txt"        
        # Declare output file path
        path = self.miscfunc.local_normpath(self.zentraconfig.mesonet_metadata_folder,filename) 
        return path

    def write_settings(self,station,src):
        metapath = self.create_metadata_path(station)
        # Open file for settings
        mcoCSVfile  = open(src, "rb")
        # Instantiate CSV reader object
        reader = csv.reader(mcoCSVfile)
        # Get contents as list of list
        rows = list(reader)
        # Get last list in list
        row = rows[-1]
        mcoCSVfile.close()
        # Get settings dictionary
        mcodict = self.get_mco_csv_settings_dictionary()
        # Populate dictionary with last row in settings CSV
        rowindex = 0
        for k,v in sorted(mcodict.iteritems()):
            v=v
            mcodict[k]= row[rowindex]
            rowindex = rowindex+1
        
        text_file = open(metapath, "w")
        text_file.write("Valid since: %s\n"                % mcodict['02:valid_since'])
        text_file.write("Device Serial Number: %s\n"       % mcodict['04:device_sn'])
        text_file.write("Device Type: %s\n"                % mcodict['03:device_type'])
        text_file.write("Device Firmware: %s\n"            % mcodict['05:device_fw'])
        text_file.write("Device Trait: %s\n"               % mcodict['06:device_trait'])
        text_file.write("Measurement Interval (min): %s\n"   % str(int(int(mcodict['01:measurement_interval'])/60)))
        text_file.write("Mean Station longitude: %s\n"     % str(round(float(mcodict['07:longitude']),5)))
        text_file.write("Mean Station latitude: %s\n"      % str(round(float(mcodict['08:latitude']),5)))
        text_file.write("Mean Station altitude (m): %s\n"  % str(round((float(mcodict['10:altitude'])/1000.0),1)))
        text_file.write("Mean Station accuracy (m): %s\n"  % str(round((float(mcodict['09:accuracy'])/1000.0),1)))
        text_file.write("Mean number of satellites: %s\n"  % mcodict['11:satellite'])
        text_file.close()
        
        return

    def get_mco_csv_settings_dictionary(self):
        header_dict = {
                    '01:measurement_interval': "Measurement Interval [s]",
                    '02:valid_since':          "Valid Since Date",
                    '03:device_type':          "Device Type",
                    '04:device_sn':            "Device SN",
                    '05:device_fw':            "Device Firmward",
                    '06:device_trait':         "Device Trait",
                    '07:longitude':            "Mean Longitude [deg]",    
                    '08:latitude':             "Mean Latitude [deg]",
                    '09:accuracy':             "Mean Accuracy [mm]",
                    '10:altitude':             "Mean Altitude [mm]",
                    '11:satellite':            "Mean Satellites [n]"
                }
        return header_dict


#==========================================================================
# Class Definition
#==========================================================================
class metadataMesoWest():
    
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
        # Load Zentra-Mesonet miscellaneous functions
        self.miscfunc = misc.Pathways()
        
    #==========================================================
    # Functions for MesoWest metadata production
    #==========================================================

    def create_metadata_path(self,station) :
        # Declare output file name
        filename = "MesoWest-Metadata-" + station + ".txt"        
        # Declare output file path
        path = self.miscfunc.local_normpath(self.zentraconfig.mesowest_metadata_folder,filename) 
        return path

    def write_settings(self,station,src):
        metapath = self.create_metadata_path(station)
        # Open file for settings
        mcoCSVfile  = open(src, "rb")
        # Instantiate CSV reader object
        reader = csv.reader(mcoCSVfile)
        # Get contents as list of list
        rows = list(reader)
        # Get last list in list
        row = rows[-1]
        mcoCSVfile.close()
        # Get settings dictionary
        mcodict = self.get_mco_csv_settings_dictionary()
        # Populate dictionary with last row in settings CSV
        rowindex = 0
        for k,v in sorted(mcodict.iteritems()):
            v=v
            mcodict[k]= row[rowindex]
            rowindex = rowindex+1
        
        text_file = open(metapath, "w")
        text_file.write("Valid since: %s\n"                % mcodict['02:valid_since'])
        text_file.write("Device Serial Number: %s\n"       % mcodict['04:device_sn'])
        text_file.write("Device Type: %s\n"                % mcodict['03:device_type'])
        text_file.write("Device Firmware: %s\n"            % mcodict['05:device_fw'])
        text_file.write("Device Trait: %s\n"               % mcodict['06:device_trait'])
        text_file.write("Measurement Interval (min): %s\n"   % str(int(int(mcodict['01:measurement_interval'])/60)))
        text_file.write("Mean Station longitude: %s\n"     % str(round(float(mcodict['07:longitude']),5)))
        text_file.write("Mean Station latitude: %s\n"      % str(round(float(mcodict['08:latitude']),5)))
        text_file.write("Mean Station altitude (m): %s\n"  % str(round((float(mcodict['10:altitude'])/1000.0),1)))
        text_file.write("Mean Station accuracy (m): %s\n"  % str(round((float(mcodict['09:accuracy'])/1000.0),1)))
        text_file.write("Mean number of satellites: %s\n"  % mcodict['11:satellite'])
        text_file.close()
        
        return

    def get_mco_csv_settings_dictionary(self):
        header_dict = {
                    '01:measurement_interval': "Measurement Interval [s]",
                    '02:valid_since':          "Valid Since Date",
                    '03:device_type':          "Device Type",
                    '04:device_sn':            "Device SN",
                    '05:device_fw':            "Device Firmward",
                    '06:device_trait':         "Device Trait",
                    '07:longitude':            "Mean Longitude [deg]",    
                    '08:latitude':             "Mean Latitude [deg]",
                    '09:accuracy':             "Mean Accuracy [mm]",
                    '10:altitude':             "Mean Altitude [mm]",
                    '11:satellite':            "Mean Satellites [n]"
                }
        return header_dict

#==========================================================================
# Class Definition
#==========================================================================
class metadataWriter():
    
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
        # Load Zentra-Mesonet miscellaneous functions
        self.miscfunc = misc.Pathways()
    
    def write_sensorConfig_metadata(self,metadataFile,validSince=""):
        text_file = open(metadataFile, "a")
        text_file.write("Sensor configuration valid since: %s\n" % validSince)
        text_file.close()
        return
    
    def write_sensor_metadata(self,metadataFile,number="",port="",index=""):
        text_file = open(metadataFile, "a")
        text_file.write("Sensor number: %s" % number)
        text_file.write(" on port: %s" % port)
        text_file.write(" with port index: %s\n" % index)
        text_file.close()
        return
    
    def write_measurement_metadata(self,metadataFile,sensorNumber,measurementList,sensorLabel):
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
    
    def write_level1_metadata(self,metadataFile,recordNumber,sensorLabel,oldval,newval):
        text_file = open(metadataFile, "a")
        text_file.write("Updating record {0} for {1}: replace {2} with {3}\n".format(str(recordNumber),sensorLabel,str(oldval),str(newval)))
        text_file.close()
        return

#==========================================================================
# Main and tests
#==========================================================================
if __name__ == "__main__":
    # Load user configuration settings as configuration object
    zconfig = config.ZentraConfig()
    # Load Zentra configuration settings as configuration object
    zconfigdownload = configdownload.ZentraDownloadConfig()
    # Load MCO metadata object
    mcometa = metadataClimateOffice(zconfig,zconfigdownload)
    # Load MesoWest metadata object
    mesowestmeta = metadataMesoWest(zconfig,zconfigdownload)
    # Load miscellaneous functions
    miscfn = misc.Pathways()
    #
    station = 'ebarllob'
    src = r"Y:\Data\Mesonet\ZentraTest\API-Output\ClimateOffice\Level0\MCO-Settings-ebarllob.csv"
    print mcometa.create_metadata_path(station)
    mcometa.write_settings(station,src)
    print mesowestmeta.create_metadata_path(station)
    mesowestmeta.write_settings(station,src)
