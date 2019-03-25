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
import provider.parseReadings as parsereadings
import provider.parseSettings as parsesettings
import datetime
import csv
import os

#==========================================================================
# Class Definition
#==========================================================================
class csvReadingsWriter():
    
    """
        Configuration file for downloading Zentra station data from
        https://zentra.com and writing to local path 
        \\mcofiles\Resources$\Data\Mesonet
        
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
    # Functions for Montana Climate Office CSV data (RAW)
    #==========================================================

    def create_csv_readings_path(self,station,theday) :
        # Get path to write CSV output for this day
        zentrapath = self.miscfunc.local_normpath(self.zentraconfig.mesonet_csv_folder,'Readings')
        zentrapath = self.miscfunc.local_normpath(zentrapath,station)
        zentrapath = self.miscfunc.local_normpath(zentrapath,str(theday.year))                                
        self.miscfunc.check_if_path_exists(zentrapath)
        zentrafilename = "Readings" + self.miscfunc.folder_string_from_date(theday) + ".csv"        
        zentrapath = self.miscfunc.local_normpath(zentrapath,zentrafilename)
        return zentrapath

    def write_readings_csv(self,station,theday,mcodict):
        # Declare CSV file path
        mcoCSV = self.create_csv_readings_path(station,theday)
        # Open file for writing CSV
        mcoCSVfile  = open(mcoCSV, "wb")
        # Set CSV write parameters; dialect='excel', 
        mcoCSVwriter = csv.writer(mcoCSVfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        # Write MCO CSV Header
        mcoCSVwriter.writerow(self.get_mco_csv_header())
        for k,v in sorted(mcodict.iteritems()):
            # Create empty list for CSV row
            rowid=[]
            k=k
            # Get sorted list of dictionary keys
            rowdict = sorted(v.keys())
            # For each key in dictionary get value
            for row in rowdict:
                # if value is of type dictionary and not empty append value on key 'value'
                if type(v[row]) is dict and v[row]:
                    rowid.append(v[row]['value'])
                # if value is of type dictionary and empty append NULL
                elif not v[row]:
                    rowid.append(self.zentraconfig.zentra_NULL_VALUE)
                # otherwise, append value
                else:
                    rowid.append(v[row])
            # Write row to CSV file
            mcoCSVwriter.writerow(rowid)
        # Close CSV file
        mcoCSVfile.close()
        return
    
    #====================================================================
    # Function for header
    #====================================================================
    def get_mco_csv_header(self):
        header_dict = {
                '01:recordnum':     "Record Number [n]",
                '02:apirecord':     "API Record Number [n]",
                '03:apicode':       "API Code",       
                '04:timestamp':     "UTC Time [ms]",
                '05:localdate':     "Local Date",
                '06:solrad':        "Solar Radiation [W/m^2]",
                '07:precipitation': "Precipitation [mm]",
                '08:hitnum':        "Lightning Activity [n]",
                '09:hitdist':       "Lightning Distance [km]",            
                '10:winddir':       "Wind Direction [deg]",
                '11:windspeed':     "Wind Speed [m/s] ",
                '12:windgust':      "Gust Speed [m/s]",
                '13:temperature':   "Air Temperature [deg C]",
                '14:relhumidity':   "Relative Humidity [RH ratio]",
                '15:pressure':      "Atmospheric Pressure [atm kPa]",
                '16:sensortiltx':   "X-axis Level [deg]",
                '17:sensortilty':   "Y-axis Level [deg]",
                '18:maxprecip':     "Max Precip Rate [mm/h]",
                '19:humiditytemp':  "RH Sensor Temp [deg C]",
                '20:soilvwc4':      "4-in Water Content [m^3/m^3]",
                '21:soilvwc8':      "8-in Water Content [m^3/m^3]",
                '22:soilvwc20':     "20-in Water Content [m^3/m^3]",
                '23:soilvwc36':     "36-in Water Content [m^3/m^3]",
                '24:soilvwc0':      "0-in Water Content [m^3/m^3]",
                '25:soilt4':        "4-in Soil Temperature [deg C]",
                '26:soilt8':        "8-in Soil Temperature [deg C]",
                '27:soilt20':       "20-in Soil Temperature [deg C]",
                '28:soilt36':       "36-in Soil Temperature [deg C]",
                '29:soilt0':        "0-in Soil Temperature [deg C]",
                '30:soilec4':       "4-in Saturation Extract EC [mS/cm]",
                '31:soilec8':       "8-in Saturation Extract EC [mS/cm]",
                '32:soilec20':      "20-in Saturation Extract EC [mS/cm]",
                '33:soilec36':      "36-in Saturation Extract EC [mS/cm]",
                '34:soilec0':       "0-in Saturation Extract EC [mS/cm]",
                '35:rrad630':       "650 nm Radiance [watts/m^2/nm/sr]",
                '36:rrad800':       "810 nm Radiance [watts/m^2/nm/sr]",
                '37:rradorient':    "Radiance Orientation",
                '38:rradalpha':     "Radiance Alpha",
                '39:irad630':       "650 nm Irradiance [watts/m^2/nm/sr]",
                '40:irad800':       "810 nm Irradiance [watts/m^2/nm/sr]",
                '41:iradorient':    "Irradiance Orientation",
                '42:iradalpha':     "Irradiance Alpha",
                '43:batteryper':    "Battery Percent [%]",
                '44:batterymv':     "Battery Voltage [mV]",
                '45:loggerpress':   "Reference Pressure [atm kPa]",
                '46:loggertemp':    "Logger Temperature [deg C]"
                }
        header_list = []
        for k,v in sorted(header_dict.iteritems()):
            k=k
            header_list.append(v)
        return header_list

#==========================================================================
# Class Definition
#==========================================================================
class csvSettingsWriter():
    
    """
        Configuration file for downloading Zentra station data from
        https://zentra.com and writing to local path 
        \\mcofiles\Resources$\Data\Mesonet
        
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
    # Functions for Montana Climate Office CSV data (RAW)
    #==========================================================

    def create_csv_settings_path(self,station,theday) :
        # Get path to write CSV output for this day
        zentrapath = self.miscfunc.local_normpath(self.zentraconfig.mesonet_csv_folder,'Settings')
        zentrapath = self.miscfunc.local_normpath(zentrapath,station)
        zentrapath = self.miscfunc.local_normpath(zentrapath,str(theday.year))                                
        self.miscfunc.check_if_path_exists(zentrapath)
        zentrafilename = "Settings" + self.miscfunc.folder_string_from_date(theday) + ".csv"        
        zentrapath = self.miscfunc.local_normpath(zentrapath,zentrafilename)
        return zentrapath

    def write_settings_csv(self,station,theday,mcodict):
        # Declare CSV file path
        mcoCSV = self.create_csv_settings_path(station,theday)
        # Open file for writing CSV
        mcoCSVfile  = open(mcoCSV, "wb")
        # Set CSV write parameters; dialect='excel', 
        mcoCSVwriter = csv.writer(mcoCSVfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        # Write MCO CSV Header
        mcoCSVwriter.writerow(self.get_mco_csv_header())
        # Create empty list for CSV row
        rowid=[]
        for k,v in sorted(mcodict.iteritems()):
            k=k
            rowid.append(v)
        # Write row to CSV file
        mcoCSVwriter.writerow(rowid)
        # Close CSV file
        mcoCSVfile.close()
        return

    #====================================================================
    # Function for header
    #====================================================================
    def get_mco_csv_header(self):
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
        header_list = []
        for k,v in sorted(header_dict.iteritems()):
            k=k
            header_list.append(v)
        return header_list

#==========================================================================
# Class Definition
#==========================================================================
class csvMerge():
    
    """
        Configuration file for downloading Zentra station data from
        https://zentra.com and writing to local path 
        \\mcofiles\Resources$\Data\Mesonet
        
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
    # Functions for Montana Climate Office CSV data (RAW)
    #==========================================================
    def create_levelzero_path(self,csvpath):
        # Extract file name from path
        head, tail = os.path.split(csvpath)
        head=head
        # Create destination path
        dst = self.miscfunc.local_normpath(self.zentraconfig.mesonet_levelzero_folder,tail)
        return dst

    def create_csv_readings_path(self,station) :
        # Get path to write CSV output for this day
        zentrapath = self.miscfunc.local_normpath(self.zentraconfig.mesonet_csv_folder,'Readings')
        zentrapath = self.miscfunc.local_normpath(zentrapath,station)
        return zentrapath

    def create_csv_readings_output_path(self,station) :
        # Get path to write CSV output for this day
        zentrapath = self.miscfunc.local_normpath(self.zentraconfig.mesonet_csv_folder,'Readings')
        zentrapath = self.miscfunc.local_normpath(zentrapath,station)
        outfile = "MCO-Readings-" + station + ".csv"
        zentrapath = self.miscfunc.local_normpath(zentrapath,outfile)
        return zentrapath

    def create_csv_settings_path(self,station) :
        # Get path to write CSV output for this day
        zentrapath = self.miscfunc.local_normpath(self.zentraconfig.mesonet_csv_folder,'Settings')
        zentrapath = self.miscfunc.local_normpath(zentrapath,station)
        return zentrapath

    def create_csv_settings_output_path(self,station) :
        # Get path to write CSV output for this day
        zentrapath = self.miscfunc.local_normpath(self.zentraconfig.mesonet_csv_folder,'Settings')
        zentrapath = self.miscfunc.local_normpath(zentrapath,station)
        outfile = "MCO-Settings-" + station + ".csv"
        zentrapath = self.miscfunc.local_normpath(zentrapath,outfile)
        return zentrapath

    #==========================================================
    # Functions for Montana Climate Office CSV data (RAW)
    #==========================================================
    def get_csv_readings_list(self,station):
        rootpath =  self.create_csv_readings_path(station)
        folder_list = os.listdir(rootpath)
        csv_list = []
        for folder in folder_list:
            folderpath = self.miscfunc.local_normpath(rootpath,folder)
            if os.path.isdir(folderpath):
                folderlist = os.listdir(folderpath)
                for csv_file in folderlist:
                    folderlist[folderlist.index(csv_file)] = self.miscfunc.local_normpath(folderpath,folderlist[folderlist.index(csv_file)])           
                csv_list.extend(folderlist)
        return csv_list

    def get_csv_settings_list(self,station):
        rootpath =  self.create_csv_settings_path(station)
        folder_list = os.listdir(rootpath)
        csv_list = []
        for folder in folder_list:
            folderpath = self.miscfunc.local_normpath(rootpath,folder)
            if os.path.isdir(folderpath):  
                folderlist = os.listdir(folderpath)
                for csv_file in folderlist:
                    folderlist[folderlist.index(csv_file)] = self.miscfunc.local_normpath(folderpath,folderlist[folderlist.index(csv_file)])           
                csv_list.extend(folderlist)
        return csv_list
        
    #==========================================================
    # Functions for Montana Climate Office CSV data (RAW)
    #==========================================================
    def merge_csv_files(self,filelist,outcsv):
        print outcsv
        outfile  = open(outcsv,"wb")
        # Set CSV write parameters; dialect='excel', 
        mcoCSVwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        # Process all files in the list
        for csvfile in filelist:
            # Open file for readings
            mcoCSVfile  = open(csvfile, "rb")
            reader = csv.reader(mcoCSVfile)
            # skip header if not first file
            if filelist.index(csvfile) > 0:
                next(reader, None)    
            for row in reader:
                mcoCSVwriter.writerow(row)
            mcoCSVfile.close()
        outfile.close()
        return

#==========================================================================
# Main and tests
#==========================================================================
if __name__ == "__main__":
    # Load user configuration settings as configuration object
    zconfig = config.ZentraConfig()
    # Load Zentra configuration settings as configuration object
    zconfigdownload = configdownload.ZentraDownloadConfig()
    # Load CSV Writer object
    csvreadingswriter = csvReadingsWriter(zconfig,zconfigdownload)
    csvsettingswriter = csvSettingsWriter(zconfig,zconfigdownload)
    csvmerge = csvMerge(zconfig,zconfigdownload)
    # Load miscellaneous functions
    miscfn = misc.Pathways()
    # Populate MCO sensor dictionary
    # Instantiate parsing object
    zentrareadings = parsereadings.ParseDictionary(zconfig,zconfigdownload)
    # Instantiate parsing object
    zentrasettings = parsesettings.ParseDictionary(zconfig,zconfigdownload)
    # Populate MCO sensor dictionary
    # testday = datetime.datetime(year=2018,month=5,day=3)
    testday = datetime.datetime(year=2017,month=7,day=1)
    station = "lubrecht"
    # mcoreadings = zentrareadings.fill_climateOffice_mcoDict(station,testday)
    # mcosettings = zentrasettings.fill_climateOffice_mcoDict(station,testday)
    # csvreadingswriter.write_readings_csv(station,testday,mcoreadings)
    # csvsettingswriter.write_settings_csv(station,testday,mcosettings)
    # csvlist = csvmerge.get_csv_settings_list(station)
    # outcsv = csvmerge.create_csv_settings_output_path(station)
    # csvmerge.merge_csv_files(csvlist,outcsv)
    csvlist = csvmerge.get_csv_readings_list(station)
    outcsv = csvmerge.create_csv_readings_output_path(station)
    csvmerge.merge_csv_files(csvlist,outcsv)