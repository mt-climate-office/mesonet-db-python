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
import os
import datetime
 
#==========================================================================
# Class Definition
#==========================================================================
class csvLevelOneWriter():
    
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

    def create_csv_levelone_path(self,csvpath) :
        # Extract file name from path
        head, tail = os.path.split(csvpath)
        head=head
        # Create destination path
        dst = self.miscfunc.local_normpath(self.zentraconfig.mesonet_levelone_folder,tail)
        return dst

    def create_csv_levelone_daily_path(self,csvpath,theday) :
        # Extract file name from path
        head, tail = os.path.split(csvpath)
        head=head
        # Create destination path
        dst = self.miscfunc.local_normpath(self.zentraconfig.mesowest_dailycsv_folder,tail)
        datestr = '{:0>4d}.{:0>2d}.{:0>2d}'.format(theday.year,theday.month,theday.day)
        dst = dst.replace(".csv","-"+datestr+".csv")
        return dst

    def create_csv_mesowest_path(self,csvpath) :
        # Extract file name from path
        head, tail = os.path.split(csvpath)
        head=head
        # Create destination path
        tail = tail.replace("MCO-Readings","MesoWest")
        dst = self.miscfunc.local_normpath(self.zentraconfig.mesowest_fullcsv_folder,tail)
        return dst

    def write_levelone_csv(self,incsv,outcsv,metapath,MesoWest):
        # Determine if MesoWest is to be written
        if MesoWest == "yes":
            MesoWest = True
        else:
            MesoWest = False
        # Construct the path to the Level One MesoWest CSV from the MCO Level One CSV
        if MesoWest: mesowestCSVpath = self.create_csv_mesowest_path(outcsv)

        # Print the path to the MCO Level One CSV
        print "MCO Level One path: ", outcsv
        if MesoWest: print "MesoWest Level One path: ", mesowestCSVpath
                
        # Open the metadata file for writing
        text_file = open(metapath,"a")
        text_file.write("\n\nLEVEL ONE DATA RANGE CHECK MODIFICATIONS:\n")
        
        # Open the MCO Level One CSV file for writing
        mcoCSVfile  = open(outcsv,"wb")
        # Set MCO CSV write parameters; dialect='excel', 
        mcoCSVwriter = csv.writer(mcoCSVfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        
        # Open the MesoWest Level One CSV file for writing
        if MesoWest: mesowestCSVfile  = open(mesowestCSVpath,"wb")
        # Set MesoWest CSV write parameters; dialect='excel', 
        if MesoWest: mesowestCSVwriter = csv.writer(mesowestCSVfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        
        # Open file for readings
        readingsCSVfile  = open(incsv, "rb")
        reader = csv.reader(readingsCSVfile)
        
        # Get MCO and MesoWest dictionaries
        mcodict = self.get_climateOffice_sensorDict()
        if MesoWest: mesodict = self.get_mesoWest_sensorDict()
        
        # Build a list of all keys in the MCO dictionary
        mcokeys = []
        for k,v in sorted(mcodict.iteritems()):
            v=v
            mcokeys.append(k)
       
        # Set header row flag to True for first row, othewise false
        headerrow = True
        # Initialize file record count to 1
        recno = 1
        # For each row in MCO Level 0 input CSV file
        lastday = None
        for row in reader:
            # If first row then it is a header row, then write to output CSV file
            if headerrow:
                # Write MCO header row
                mcoCSVwriter.writerow(row)
                # Get and write MesoWest header row
                if MesoWest: mesoheader = self.get_mesowest_csv_header()
                if MesoWest: mesowestCSVwriter.writerow(mesoheader)
                headerrow = False
            # Not first row, so data row and not header row.  Write data row.
            else:
                lastday = row[4]
                # Initialize an empty dictionaries 
                mcorowdict = {}
                for x in range(len(mcokeys)):
                    mcorowdict[mcokeys[x]] = row[x]
                # Update record number 
                mcorowdict['01:recordnum']= recno
                mcorowdict = self.mco_level1_qa(mcorowdict,text_file)
                # Map MCO data row to MesoWest data row
                if MesoWest:mesodict = self.map_level1_qa_to_mesowest(mcorowdict,mesodict)
                # Write out new MCO row
                newrow = []
                for k,v in sorted(mcorowdict.iteritems()):
                    newrow.append(v)
                mcoCSVwriter.writerow(newrow)
                # Write out new MesoWest row
                if MesoWest:
                    newrow = []
                    for k,v in sorted(mesodict.iteritems()):
                        newrow.append(v)
                    mesowestCSVwriter.writerow(newrow)
                # Increment row counter
                recno = recno + 1
        mcoCSVfile.close()
        if MesoWest: mesowestCSVfile.close()
        text_file.close()
        readingsCSVfile.close()
        # Write daily files based on MesoWest CSV and last day value
        if MesoWest: self.write_levelone_mesowest_daily(mesowestCSVpath,lastday)
        return
    
    def write_levelone_mesowest_daily(self,mesowestCSVpath,lastday):
        print "Extract daily from: ", mesowestCSVpath, "for", lastday
        # Use last recorded date in full record to export last day and previous last day MesoWest CSV
        lastday = datetime.datetime.strptime(lastday, "%Y-%m-%d %H:%M")
        prevday = lastday-datetime.timedelta(days=1)
        # Clean out old files
        print "Cleaning files.  Removing files older than previous 10 days"
        self.clean_mesowest_daily_files(lastday,10)
        # Get output CSV file path
        prevdaypath = self.create_csv_levelone_daily_path(mesowestCSVpath,prevday)
        lastdaypath = self.create_csv_levelone_daily_path(mesowestCSVpath,lastday)
        # Form search string for date in CSV input record
        searchlastdatestr = '{:0>4d}-{:0>2d}-{:0>2d}'.format(lastday.year,lastday.month,lastday.day)
        searchprevdatestr = '{:0>4d}-{:0>2d}-{:0>2d}'.format(prevday.year,prevday.month,prevday.day)
        # Open output CSV files for writing
        prevdayCSVfile  = open(prevdaypath,"wb")
        lastdayCSVfile  = open(lastdaypath,"wb")
        # Instantiate CSV writer objects
        prevdayCSVwriter = csv.writer(prevdayCSVfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        lastdayCSVwriter = csv.writer(lastdayCSVfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        # Open file input Level 1 MesoWest CSV file for this station
        readingsCSVfile  = open(mesowestCSVpath, "rb")
        reader = csv.reader(readingsCSVfile)
        # Set header row flag to True for first row, othewise false
        headerrow = True
        # For each row in MCO Level 0 input CSV file
        for row in reader:
            # If first row then it is a header row, then write to output CSV file
            if headerrow:
                # Write MCO header row
                prevdayCSVwriter.writerow(row)
                lastdayCSVwriter.writerow(row)
                headerrow = False
            # Not first row, so data row and not header row.  Write data row.
            else:
                # print row
                if searchprevdatestr in row[2]:
                    prevdayCSVwriter.writerow(row)
                if searchlastdatestr in row[2]:
                    lastdayCSVwriter.writerow(row)
        prevdayCSVfile.close()
        lastdayCSVfile.close()
        readingsCSVfile.close()
        return
    
    def clean_mesowest_daily_files(self,lastday,days=10):
        fileList = []
        dayList = []
        # Build list of valid dates
        for d in range(0,days):
            now = lastday-datetime.timedelta(days=d)
            dayList.append(now.strftime("%Y.%m.%d"))
        # Get list of files
        hourlyFilePath = self.zentraconfig.mesowest_dailycsv_folder
        for files in next(os.walk(hourlyFilePath))[2]:
            fileList.append(os.path.normpath(os.path.join(hourlyFilePath,files)))
        for files in fileList:
            saveFlag = False
            for daystr in dayList:
                if daystr in files:
                    daystr,files
                    saveFlag = True
            if not saveFlag and os.path.isfile(files):
                os.remove(files)
        return

    #==========================================================
    # Functions for Montana Climate Office Level One Cleanup
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

    def write_level1_metadata(self,mcometafile,recno,apirec,sensorLabel,oldval,nullval):
        # Ignore NULL values
        if float(oldval) < 65535.0 or int(oldval) < 65535:
            mcometafile.write("Updating MCO record {0}:API record {1} for {2}: replace {3} with {4}\n".format(str(recno),str(apirec),sensorLabel,str(oldval),str(nullval)))
        return

    def mco_level1_qa(self,sensordict,mcometafile):
        exceptionList = ['01:recordnum','02:apirecord','03:apicode','04:timestamp','05:localdate']
        # Change all units to default resolution and range
        recno = sensordict['01:recordnum']
        apirec = sensordict['02:apirecord']
        for k,v in sorted(sensordict.iteritems()):
            if k not in exceptionList:
                if v:
                    v = float(v)
                else:
                    v = self.zentraconfig.zentra_NULL_VALUE
                if k[3:] == 'solrad':
                    if int(v) < 0 or int(v) > 1750:
                        sensorLabel = "solar radiation"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        sensordict[k] = int(round(v,0))
                if k[3:] == 'precipitation':
                    if v <  0.0 or v > 125.0:
                        sensorLabel = "precipitation"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        sensordict[k] = round(v,3)
                if k[3:] == 'hitdist':
                    if int(v) < 0 or int(v) > 40:
                        sensorLabel = "lightening hit distance"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                if k[3:] == 'winddir':
                    if int(v) < 0 or int(v) > 359:
                        sensorLabel = "wind direction"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        sensordict[k] = int(round(v,0))
                if k[3:] == 'windspeed':
                    # Note: sensor specifications are 60, but 50 more reasonable for Montana
                    if v < 0.0 or v > 50.0:
                        sensorLabel = "wind speed"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        sensordict[k] = round(v,2)
                if k[3:] == 'windgusts':
                    # Note: sensor specifications are 60, but 50 more reasonable for Montana
                    if v < 0.0 or v > 50.0:
                        sensorLabel = "wind gusts"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        sensordict[k] = round(v,2)
                if k[3:] == 'temperature':
                    if v < -40.0 or v > 50.0:
                        sensorLabel = "air temperature"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        sensordict[k] = round(v,1)
                if k[3:] == 'relhumidity':
                    # Note: cutoff set to less than 0.001 since the RH sensor reports a missing value as zero
                    if v < 0.001 or v > 1.1:
                        sensorLabel = "relative humidity"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        if v > 1.0:
                            sensordict[k] = 1.000
                        else:
                            sensordict[k] = round(v,3)
                if k[3:] == 'pressure':
                    if v < 40.0 or v > 110.0:
                        sensorLabel = "air pressure"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        sensordict[k] = round(v,4)
                if k[3:] == 'sensortiltx':
                    if v < -10.0 or v > 10.0:
                        sensorLabel = "sensor tilt x"
                        # write_level1_metadata(mcometafile,recno,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        sensordict[k] = round(v,1)
                if k[3:] == 'sensortilty':
                    if v < -10.0 or v > 10.0:
                        sensorLabel = "sensor tilt y"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        sensordict[k] = round(v,1)
                if k[3:] == 'maxprecip':
                    if v <  0.0 or v > 125.0:
                        sensorLabel = "Maximum precipitation"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        sensordict[k] = round(v,3)
                if k[3:] == 'humiditytemp':
                    if v < -40.0 or v > 60.0:
                        sensorLabel = "relative humidity temperature"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        sensordict[k] = round(v,1)
                if k[3:] == 'soilvwc4' or k[3:] == 'soilvwc8' or k[3:] == 'soilvwc20' or k[3:] == 'soilvwc36' or k[3:] == 'soilvwc0':
                    if v < 0.0 or v > 0.80:
                        sensorLabel = "soil volumetric water content"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        sensordict[k] = round(v,3)
                if k[3:] == 'soilt4' or k[3:] == 'soilt8' or k[3:] == 'soilt20' or k[3:] == 'soilt36' or k[3:] == 'soilt0':
                    if v < -40.0 or v > 60.0:
                        sensorLabel = "soil temperature"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        sensordict[k] = round(v,1)
                if k[3:] == 'soilec4' or k[3:] == 'soilec8' or k[3:] == 'soilec20' or k[3:] == 'soilec36' or k[3:] == 'soilec0':
                    if v <  0.0 or v > 25.0:
                        sensorLabel = "soil electrical conductivity"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        sensordict[k] = round(v,3)
                if k[3:] == 'rrad630' or k[3:] == 'rrad800' or k[3:] == 'irad630' or k[3:] == 'irad800':
                    if v < 0.0 or v > 1.0:
                        sensorLabel = "reflectance"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
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
                    if v < 0.0 or v > 3.0:
                        sensorLabel = "reflectance alpha"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        sensordict[k] = int(round(v,4))
                if k[3:] == 'batteryper':
                    if int(v) < 0 or int(v) > 100:
                        sensorLabel = "battery percentage"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        sensordict[k] = int(round(v,0))
                if k[3:] == 'batterymv':
                    if int(v) < 0 or int(v) > 8000:
                        sensorLabel = "battery millivolts"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        sensordict[k] = int(round(v,0))
                if k[3:] == 'loggerpress':
                    if v < 40.0 or v > 110.0:
                        sensorLabel = "logger pressure"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                        sensordict[k] = self.zentraconfig.zentra_NULL_VALUE
                    else:
                        sensordict[k] = round(v,4)
                if k[3:] == 'loggertemp':
                    if v < -40.0 or v > 50.0:
                        sensorLabel = "logger temperature"
                        self.write_level1_metadata(mcometafile,recno,apirec,sensorLabel,v,self.zentraconfig.zentra_NULL_VALUE)
                    else:
                        sensordict[k] = round(v,1)
        return sensordict

    def get_mesoWest_sensorDict(self):
        mesowestdict = {
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
        return mesowestdict

    def get_mesowest_csv_header(self):
        header_dict = {
                '01:recordnum':     "Record Number [n]",
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
                '18:maxprecip':     "Max Precip Rate [mm/h]",
                '20:soilvwc4':      "4-in Water Content [m^3/m^3]",
                '21:soilvwc8':      "8-in Water Content [m^3/m^3]",
                '22:soilvwc20':     "20-in Water Content [m^3/m^3]",
                '23:soilvwc36':     "36-in Water Content [m^3/m^3]",
                '25:soilt4':        "4-in Soil Temperature [deg C]",
                '26:soilt8':        "8-in Soil Temperature [deg C]",
                '27:soilt20':       "20-in Soil Temperature [deg C]",
                '28:soilt36':       "36-in Soil Temperature [deg C]",
                '30:soilec4':       "4-in Saturation Extract EC [mS/cm]",
                '31:soilec8':       "8-in Saturation Extract EC [mS/cm]",
                '32:soilec20':      "20-in Saturation Extract EC [mS/cm]",
                '33:soilec36':      "36-in Saturation Extract EC [mS/cm]",
                }
        header_list = []
        for k,v in sorted(header_dict.iteritems()):
            k=k
            header_list.append(v)
        return header_list

    def map_level1_qa_to_mesowest(self,mcorowdict,mesodict):
        for k,v in sorted(mesodict.iteritems()):
            v=v
            mesodict[k] = mcorowdict[k]
        return mesodict

#==========================================================================
# Main and tests
#==========================================================================
if __name__ == "__main__":
    # Load user configuration settings as configuration object
    zconfig = config.ZentraConfig()
    # Load Zentra configuration settings as configuration object
    zconfigdownload = configdownload.ZentraDownloadConfig()
    # Load CSV Writer object
    csvleveloneswriter = csvLevelOneWriter(zconfig,zconfigdownload)
    src = r"\\mcofiles.cfc.umt.edu\Resources$\Data\Mesonet\ZentraTest\API-Output\ClimateOffice\Level0\MCO-Readings-corvalli.csv"
    dst = csvleveloneswriter.create_csv_levelone_path(src)
    metapath = r"\\mcofiles.cfc.umt.edu\Resources$\Data\Mesonet\ZentraTest\API-Output\ClimateOffice\Metadata\MCO-Metadata-corvalli.txt"
    csvleveloneswriter.write_levelone_csv(src,dst,metapath,"yes")