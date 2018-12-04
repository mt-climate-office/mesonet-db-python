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
import datetime
import pandas as pd
import numpy as np
import util.mobilegraph2 as mg
import json

#==========================================================================
# Class Definition
#==========================================================================
class webWriter():
    
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
        self.convert = misc.Conversion()
        
    #==========================================================
    # Functions for Montana Climate Office CSV data (RAW)
    #==========================================================
    def write_levelone_mcoweb(self,mcoCSVpath,displayname,logger_username,station):
        # Open MCO Level1 CSV file for reading
        readingsCSVfile  = open(mcoCSVpath, "rb")
        # Read MCO Level 1 CSV file into pandas dataframe
        df = pd.read_csv(readingsCSVfile)
        # Close readings file
        readingsCSVfile.close()
        # Get last row in data frame
        row = df.tail(1).values.tolist()[0] # last row
        # Extract date string as datetime for last row
        lastday = datetime.datetime.strptime(row[4], "%Y-%m-%d %H:%M")
        # Get previous date-time from date of last row
        prevday = lastday-datetime.timedelta(days=1)
        prev07 = lastday-datetime.timedelta(days=7)
        prev21 = lastday-datetime.timedelta(days=21)
        # Cast Local Date column to date-time type
        df[df.columns[4]] = pd.to_datetime(df[df.columns[4]],format="%Y-%m-%d %H:%M")
        # Filter dataframe on start dates and times
        lastdaydf = df[df[df.columns[4]] >= lastday]
        prevdaydf = df[df[df.columns[4]] >= prevday]
        prev07df = df[df[df.columns[4]] >= prev07]
        prev21df = df[df[df.columns[4]] >= prev21]
        # Make copy of dataframe; converting NULL values to NaN for calculations and graphing
        prevdaydfNaN = prevdaydf.replace(self.zentraconfig.zentra_NULL_VALUE,np.nan)
        prev07dfNaN = prev07df.replace(self.zentraconfig.zentra_NULL_VALUE,np.nan)
        prev21dfNaN = prev21df.replace(self.zentraconfig.zentra_NULL_VALUE,np.nan)
        # Populate standard mco mobile dictionary
        mobiledict = self.map_to_web_dict(station,lastdaydf,prevdaydf,displayname,logger_username)
        # Populate web json dictionary
        jsondict = self.map_to_json_dict(mobiledict,station,prevdaydfNaN,prev07dfNaN)
        graphdict = self.fill_mobile_graph_dict(prev07dfNaN,prev21dfNaN)
        jsondict = self.build_mobile_graphs(jsondict,graphdict)
        return jsondict

    def map_to_json_dict(self,mcodict,station,prevdaydf,prev07df):
        httppath = self.zentraconfig.mt_mesonet_http_path + "/" + station + "/" + station
        jsondict = self.get_mcoWeb_jsonDict()
        jsondict['station'] =          station
        jsondict['displayname'] =      str(mcodict['00:displayname'])
        jsondict['loggerusername'] =   str(mcodict['00:loggerusername'])
        jsondict['localdate'] =        str(mcodict['05:localdate'])
        jsondict['recordno'] =         str(int(mcodict['01:recordnum']))
        jsondict['batteryper'] =       str(int(mcodict['43:batteryper']['Value']))
        jsondict['batteryper24'] =     str(int(mcodict['43:batteryper']['Value24']))
        jsondict['batteryperURL'] =    mcodict['43:batteryper']['GraphURL']
        jsondict['batterymv'] =        str(int(mcodict['44:batterymv']['Value']))
        jsondict['batterymv24'] =      str(int(mcodict['44:batterymv']['Value24']))
        jsondict['batterymvURL'] =     mcodict['44:batterymv']['GraphURL']
        jsondict['solrad'] =           str(int(mcodict['06:solrad']['Value']))
        jsondict['solrad24'] =         str(int(mcodict['06:solrad']['Value24']))
        jsondict['solradURL'] =        mcodict['06:solrad']['GraphURL']
        jsondict['temperature'] =      self.convert.strdegF_or_na_from_float(mcodict['13:temperature']['Value'])
        jsondict['temperature24'] =    self.convert.strdegF_or_na_from_float(mcodict['13:temperature']['Value24'])
        jsondict['temperatureURL'] =   mcodict['13:temperature']['GraphURL']
        jsondict['relhumidity'] =      self.convert.strrelhum_or_na_from_float(mcodict['14:relhumidity']['Value'])
        jsondict['relhumidity24'] =    self.convert.strrelhum_or_na_from_float(mcodict['14:relhumidity']['Value24'])
        jsondict['relhumidityURL'] =   mcodict['14:relhumidity']['GraphURL']
        jsondict['windspeed'] =        self.convert.strmph_or_na_from_meterpersec(mcodict['11:windspeed']['Value'])
        jsondict['windspeed24'] =      self.convert.strmph_or_na_from_meterpersec(mcodict['11:windspeed']['Value24'])
        jsondict['windspeedURL'] =     mcodict['11:windspeed']['GraphURL']
        jsondict['windgust'] =         self.convert.strmph_or_na_from_meterpersec(mcodict['12:windgust']['Value'])
        jsondict['windgust24'] =       self.convert.strmph_or_na_from_meterpersec(mcodict['12:windgust']['Value24'])
        jsondict['windgustURL'] =      mcodict['12:windgust']['GraphURL']
        jsondict['winddir'] =          str(int(mcodict['10:winddir']['Value']))
        jsondict['winddir24'] =        str(int(mcodict['10:winddir']['Value24']))
        jsondict['winddirURL'] =       mcodict['10:winddir']['GraphURL']
        jsondict['dewpoint'] =         self.convert.strdegF_or_na_from_float( self.convert.strdewpt_or_na_from_float(mcodict['13:temperature']['Value'], self.convert.strrelhum_or_na_from_float(mcodict['14:relhumidity']['Value'])))
        jsondict['dewpoint24'] =       self.convert.strdegF_or_na_from_float( self.convert.strdewpt_or_na_from_float(mcodict['13:temperature']['Value24'], self.convert.strrelhum_or_na_from_float(mcodict['14:relhumidity']['Value24'])))
        jsondict['dewpointURL'] =      httppath +'-'+'dewpoint'+'.png'
        jsondict['precipitation'] =    self.convert.strdecimal_inches_or_na_from_float(mcodict['07:precipitation']['Value'],3)
        jsondict['precipitation24'] =  self.convert.strdecimal_inches_or_na_from_float(mcodict['07:precipitation']['Value24'],3)
        jsondict['precipitationURL'] = mcodict['07:precipitation']['GraphURL']
        jsondict['preciptotal'] =      self.convert.strdecimal_inches_or_na_from_float(prevdaydf[prevdaydf.columns[6]].sum(),3)
        jsondict['preciptotal24'] =    self.convert.strdecimal_inches_or_na_from_float(prev07df[prev07df.columns[6]].sum(),3)
        jsondict['preciptotalURL'] =   httppath +'-'+'preciptotal'+'.png'
        jsondict['pressure'] =         self.convert.strbar_or_na_from_float(mcodict['15:pressure']['Value'])
        jsondict['pressure24'] =       self.convert.strbar_or_na_from_float(mcodict['15:pressure']['Value24'])
        jsondict['pressureURL'] =      mcodict['15:pressure']['GraphURL']
        jsondict['hitnum'] =           self.convert.str_or_na_from_int(mcodict['08:hitnum']['Value'])
        jsondict['hitnum24'] =         self.convert.str_or_na_from_int(mcodict['08:hitnum']['Value24'])
        jsondict['hitnumURL'] =        mcodict['08:hitnum']['GraphURL']
        jsondict['hitdist'] =          self.convert.str_or_na_from_int(mcodict['09:hitdist']['Value'])
        jsondict['hitdist24'] =        self.convert.str_or_na_from_int(mcodict['09:hitdist']['Value24'])
        jsondict['hitdistURL'] =       mcodict['09:hitdist']['GraphURL']
        jsondict['soilt4'] =           self.convert.strdegF_or_na_from_float(mcodict['25:soilt4']['Value'])
        jsondict['soilt424'] =         self.convert.strdegF_or_na_from_float(mcodict['25:soilt4']['Value24'])
        jsondict['soilt4URL'] =        mcodict['25:soilt4']['GraphURL']
        jsondict['soilt8'] =           self.convert.strdegF_or_na_from_float(mcodict['26:soilt8']['Value'])
        jsondict['soilt824'] =         self.convert.strdegF_or_na_from_float(mcodict['26:soilt8']['Value24'])
        jsondict['soilt8URL'] =        mcodict['26:soilt8']['GraphURL']
        jsondict['soilt20'] =          self.convert.strdegF_or_na_from_float(mcodict['27:soilt20']['Value'])
        jsondict['soilt2024'] =        self.convert.strdegF_or_na_from_float(mcodict['27:soilt20']['Value24'])
        jsondict['soilt20URL'] =       mcodict['27:soilt20']['GraphURL']
        jsondict['soilt36'] =          self.convert.strdegF_or_na_from_float(mcodict['28:soilt36']['Value'])
        jsondict['soilt3624'] =        self.convert.strdegF_or_na_from_float(mcodict['28:soilt36']['Value24'])
        jsondict['soilt36URL'] =       mcodict['28:soilt36']['GraphURL']
        jsondict['soilvwc4'] =         self.convert.strpervwc_or_na_from_float(mcodict['20:soilvwc4']['Value'])
        jsondict['soilvwc424'] =       self.convert.strpervwc_or_na_from_float(mcodict['20:soilvwc4']['Value24'])
        jsondict['soilvwc4URL'] =      mcodict['20:soilvwc4']['GraphURL']
        jsondict['soilvwc8'] =         self.convert.strpervwc_or_na_from_float(mcodict['21:soilvwc8']['Value'])
        jsondict['soilvwc824'] =       self.convert.strpervwc_or_na_from_float(mcodict['21:soilvwc8']['Value24'])
        jsondict['soilvwc8URL'] =      mcodict['21:soilvwc8']['GraphURL']
        jsondict['soilvwc20'] =        self.convert.strpervwc_or_na_from_float(mcodict['22:soilvwc20']['Value'])
        jsondict['soilvwc2024'] =      self.convert.strpervwc_or_na_from_float(mcodict['22:soilvwc20']['Value24'])
        jsondict['soilvwc20URL'] =     mcodict['22:soilvwc20']['GraphURL']
        jsondict['soilvwc36'] =        self.convert.strpervwc_or_na_from_float(mcodict['23:soilvwc36']['Value'])
        jsondict['soilvwc3624'] =      self.convert.strpervwc_or_na_from_float(mcodict['23:soilvwc36']['Value24'])
        jsondict['soilvwc36URL'] =     mcodict['23:soilvwc36']['GraphURL']
    
        return jsondict

    def get_mcoWeb_jsonDict(self):
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
        jsondict['precipitation'] =    None ## Now total precipitation in last 24 hours
        jsondict['precipitation24'] =  None ## Now total precipitation in last 7 days
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

    def map_to_web_dict(self,station,lastdaydf,prevdaydf,displayname,logger_username):
        httppath = self.zentraconfig.mt_mesonet_http_path + "/" + station + "/" + station
        
        # Get last row in CSV file
        current = lastdaydf.tail(1).values.tolist()[0] # last row
        prev24 = prevdaydf.head(1).values.tolist()[0] # last row
        webdict = self.get_mobile_web_dict()
        webdict['00:loggerusername'] = logger_username
        webdict['00:displayname'] = displayname
        webdict['01:recordnum'] = current[0]
        webdict['04:timestamp'] = current[3]
        webdict['05:localdate'] = current[4]
        # Solar Radiation [W/m^2], dtype: int64
        # print lastdaydf[lastdaydf.columns[5]]
        webdict['06:solrad']["Value"] = current[5]   
        webdict['06:solrad']["Value24"] = prev24[5]
        webdict['06:solrad']["GraphURL"] = httppath +'-'+'solrad'+'.png'
        # Precipitation [mm], dtype: float64
        webdict['07:precipitation']["Value"] = current[6]
        webdict['07:precipitation']["Value24"] = prev24[6]
        webdict['07:precipitation']["GraphURL"] = httppath +'-'+'precipitation'+'.png'
        # Lightning Activity [n], dtype: float64
        webdict['08:hitnum']["Value"] = current[7]
        webdict['08:hitnum']["Value24"] = prev24[7]
        webdict['08:hitnum']["GraphURL"] = httppath +'-'+'hitnum'+'.png'
        # Lightning Distance [km], dtype: float64
        webdict['09:hitdist']["Value"] = current[8]
        webdict['09:hitdist']["Value24"] = prev24[8]
        webdict['09:hitdist']["GraphURL"] = httppath +'-'+'hitdist'+'.png'
        # Wind Direction [deg], dtype: int64
        webdict['10:winddir']["Value"] = current[9]
        webdict['10:winddir']["Value24"] = prev24[9]
        webdict['10:winddir']["GraphURL"] = httppath +'-'+'winddir'+'.png'
        # Wind Speed [m/s] , dtype: float64
        webdict['11:windspeed']["Value"] = current[10]
        webdict['11:windspeed']["Value24"] = prev24[10]
        webdict['11:windspeed']["GraphURL"] = httppath +'-'+'windspeed'+'.png'
        # Gust Speed [m/s], dtype: float64
        webdict['12:windgust']["Value"] = current[11]
        webdict['12:windgust']["Value24"] = prev24[11]
        webdict['12:windgust']["GraphURL"] = httppath +'-'+'windgust'+'.png'
        # Air Temperature [deg C], dtype: float64
        webdict['13:temperature']["Value"] = current[12]
        webdict['13:temperature']["Value24"] = prev24[12]
        webdict['13:temperature']["GraphURL"] = httppath +'-'+'temperature'+'.png'
        # Relative Humidity [RH ratio], dtype: float64
        webdict['14:relhumidity']["Value"] = current[13]
        webdict['14:relhumidity']["Value24"] = prev24[13]
        webdict['14:relhumidity']["GraphURL"] = httppath +'-'+'relhumidity'+'.png'
        # Atmospheric Pressure [atm kPa], dtype: float64
        webdict['15:pressure']["Value"] = current[14]
        webdict['15:pressure']["Value24"] = prev24[14]
        webdict['15:pressure']["GraphURL"] = httppath +'-'+'barometer'+'.png'
        # 4-in Water Content [m^3/m^3], dtype: float64
        webdict['20:soilvwc4']["Value"] = current[19]
        webdict['20:soilvwc4']["Value24"] = prev24[19]
        webdict['20:soilvwc4']["GraphURL"] = httppath +'-'+'soilvwc4'+'.png'
        # 8-in Water Content [m^3/m^3], dtype: float64
        webdict['21:soilvwc8']["Value"] = current[20]
        webdict['21:soilvwc8']["Value24"] = prev24[20]
        webdict['21:soilvwc8']["GraphURL"] = httppath +'-'+'soilvwc8'+'.png'
        # 20-in Water Content [m^3/m^3], dtype: float64
        webdict['22:soilvwc20']["Value"] = current[21]
        webdict['22:soilvwc20']["Value24"] = prev24[21]
        webdict['22:soilvwc20']["GraphURL"] = httppath +'-'+'soilvwc20'+'.png'
        # 36-in Water Content [m^3/m^3], dtype: float64
        webdict['23:soilvwc36']["Value"] = current[22]
        webdict['23:soilvwc36']["Value24"] = prev24[22]
        webdict['23:soilvwc36']["GraphURL"] = httppath +'-'+'soilvwc36'+'.png'
        # 0-in Water Content [m^3/m^3], dtype: int64
        webdict['24:soilvwc0']["Value"] = current[23]
        webdict['24:soilvwc0']["Value24"] = prev24[23]
        webdict['24:soilvwc0']["GraphURL"] = httppath +'-'+'soilvwc0'+'.png'
        # 4-in Soil Temperature [deg C], dtype: float64
        webdict['25:soilt4']["Value"] = current[24]
        webdict['25:soilt4']["Value24"] = prev24[24]
        webdict['25:soilt4']["GraphURL"] = httppath +'-'+'soilt4'+'.png'
        # 8-in Soil Temperature [deg C], dtype: float64
        webdict['26:soilt8']["Value"] = current[25]
        webdict['26:soilt8']["Value24"] = prev24[25]
        webdict['26:soilt8']["GraphURL"] = httppath +'-'+'soilt8'+'.png'
        # 20-in Soil Temperature [deg C], dtype: float64
        webdict['27:soilt20']["Value"] = current[26]
        webdict['27:soilt20']["Value24"] = prev24[26]
        webdict['27:soilt20']["GraphURL"] = httppath +'-'+'soilt20'+'.png'
        # 36-in Soil Temperature [deg C], dtype: float64
        webdict['28:soilt36']["Value"] = current[27]
        webdict['28:soilt36']["Value24"] = prev24[27]
        webdict['28:soilt36']["GraphURL"] = httppath +'-'+'soilt36'+'.png'
        # 0-in Soil Temperature [deg C], dtype: int64
        webdict['29:soilt0']["Value"] = current[28]
        webdict['29:soilt0']["Value24"] = prev24[28]
        webdict['29:soilt0']["GraphURL"] = httppath +'-'+'soilt0'+'.png'
        # 4-in Saturation Extract EC [mS/cm], dtype: float64
        webdict['30:soilec4']["Value"] = current[29]
        webdict['30:soilec4']["Value24"] = prev24[29]
        webdict['30:soilec4']["GraphURL"] = httppath +'-'+'soilec4'+'.png'
        # 8-in Saturation Extract EC [mS/cm], dtype: float64
        webdict['31:soilec8']["Value"] = current[30]
        webdict['31:soilec8']["Value24"] = prev24[30]
        webdict['31:soilec8']["GraphURL"] = httppath +'-'+'soilec4'+'.png'
        # 20-in Saturation Extract EC [mS/cm], dtype: float64
        webdict['32:soilec20']["Value"] = current[31]
        webdict['32:soilec20']["Value24"] = prev24[31]
        webdict['32:soilec20']["GraphURL"] = httppath +'-'+'soilec4'+'.png'
        # 36-in Saturation Extract EC [mS/cm], dtype: float64
        webdict['33:soilec36']["Value"] = current[32]
        webdict['33:soilec36']["Value24"] = prev24[32]
        webdict['33:soilec36']["GraphURL"] = httppath +'-'+'soilec4'+'.png'
        # 0-in Saturation Extract EC [mS/cm], dtype: int64
        webdict['34:soilec0']["Value"] = current[33]
        webdict['34:soilec0']["Value24"] = prev24[33]
        webdict['34:soilec0']["GraphURL"] = httppath +'-'+'soilec4'+'.png'
        # Battery Percent [%], dtype: int64
        webdict['43:batteryper']["Value"] = current[42]
        webdict['43:batteryper']["Value24"] = prev24[42]
        webdict['43:batteryper']["GraphURL"] = httppath +'-'+'batteryper'+'.png'
        # Battery Voltage [mV], dtype: int64
        webdict['44:batterymv']["Value"] = current[43]
        webdict['44:batterymv']["Value24"] = prev24[43]
        webdict['44:batterymv']["GraphURL"] =  httppath +'-'+'batterymv'+'.png'
        
        return webdict
    
    def get_mobile_web_dict(self):
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

    def fill_mobile_graph_dict(self,mco7df,mco21df):
        # Initialize graphing dictionary
        graphdict = self.get_mobile_graph_dict()
        # Solar Radiation [W/m^2]
        graphdict['solrad']['timestamp'] = mco7df['UTC Time [ms]'].tolist()
        graphdict['solrad']['values'] = mco7df['Solar Radiation [W/m^2]'].tolist()
        # Precipitation [mm]
        graphdict['precipitation']['timestamp'] = mco21df['UTC Time [ms]'].tolist()
        mappedlist = map(self.convert.decimal_inches_from_float,mco7df['Precipitation [mm]'].tolist())
        graphdict['precipitation']['values'] = mappedlist
        # preciptotal
        graphdict['preciptotal']['timestamp'] = mco7df['UTC Time [ms]'].tolist()
        graphdict['preciptotal']['values'] = []
        # Lightning Activity [n]
        graphdict['hitnum']['timestamp'] = mco7df['UTC Time [ms]'].tolist()
        graphdict['hitnum']['values'] = mco7df['Lightning Activity [n]'].tolist()
        # Lightning Distance [km]
        graphdict['hitdist']['timestamp'] = mco7df['UTC Time [ms]'].tolist()
        graphdict['hitdist']['values'] = mco7df['Lightning Distance [km]'].tolist()
        # Wind Direction [deg]
        graphdict['winddir']['timestamp'] = mco7df['UTC Time [ms]'].tolist()
        graphdict['winddir']['values'] = mco7df['Wind Direction [deg]'].tolist()
        # Wind Speed [m/s]
        graphdict['windspeed']['timestamp'] = mco7df['UTC Time [ms]'].tolist()
        mappedlist = map(self.convert.mph_from_meterpersec,mco7df['Wind Speed [m/s] '].tolist())
        graphdict['windspeed']['values'] = mappedlist
        # Gust Speed [m/s]
        graphdict['windgust']['timestamp'] = mco7df['UTC Time [ms]'].tolist()
        mappedlist = map(self.convert.mph_from_meterpersec,mco7df['Gust Speed [m/s]'].tolist())
        graphdict['windgust']['values'] = mappedlist
        # Air Temperature [deg C]
        graphdict['temperature']['timestamp'] = mco7df['UTC Time [ms]'].tolist()
        mappedlist = map(self.convert.degF_from_float,mco7df['Air Temperature [deg C]'].tolist())
        graphdict['temperature']['values'] = mappedlist
        # Relative Humidity [RH ratio]
        graphdict['relhumidity']['timestamp'] = mco7df['UTC Time [ms]'].tolist()
        mappedlist = map(self.convert.relhum_from_float,mco7df['Relative Humidity [RH ratio]'].tolist())        
        graphdict['relhumidity']['values'] = mappedlist
        # Atmospheric Pressure [atm kPa]
        graphdict['pressure']['timestamp'] = mco7df['UTC Time [ms]'].tolist()
        mappedlist = map(self.convert.bar_from_float,mco7df['Atmospheric Pressure [atm kPa]'].tolist())
        graphdict['pressure']['values'] = mappedlist
        # 4-in Water Content [m^3/m^3]
        graphdict['soilvwc4']['timestamp'] = mco7df['UTC Time [ms]'].tolist()
        mappedlist = map(self.convert.pervwc_from_float,mco7df['4-in Water Content [m^3/m^3]'].tolist())
        graphdict['soilvwc4']['values'] = mappedlist
        # 8-in Water Content [m^3/m^3]
        graphdict['soilvwc8']['timestamp'] = mco7df['UTC Time [ms]'].tolist()
        mappedlist = map(self.convert.pervwc_from_float,mco7df['8-in Water Content [m^3/m^3]'].tolist())
        graphdict['soilvwc8']['values'] = mappedlist
        # 20-in Water Content [m^3/m^3]
        graphdict['soilvwc20']['timestamp'] = mco21df['UTC Time [ms]'].tolist()
        mappedlist = map(self.convert.pervwc_from_float,mco21df['20-in Water Content [m^3/m^3]'].tolist())
        graphdict['soilvwc20']['values'] = mappedlist
        # 36-in Water Content [m^3/m^3]
        graphdict['soilvwc36']['timestamp'] = mco21df['UTC Time [ms]'].tolist()
        mappedlist = map(self.convert.pervwc_from_float,mco21df['36-in Water Content [m^3/m^3]'].tolist())
        graphdict['soilvwc36']['values'] = mappedlist
        # 4-in Soil Temperature [deg C]
        graphdict['soilt4']['timestamp'] = mco7df['UTC Time [ms]'].tolist()
        mappedlist = map(self.convert.degF_from_float,mco7df['4-in Soil Temperature [deg C]'].tolist())
        graphdict['soilt4']['values'] = mappedlist
        # 8-in Soil Temperature [deg C]
        graphdict['soilt8']['timestamp'] = mco7df['UTC Time [ms]'].tolist()
        mappedlist = map(self.convert.degF_from_float,mco7df['8-in Soil Temperature [deg C]'].tolist())
        graphdict['soilt8']['values'] = mappedlist
        # 20-in Soil Temperature [deg C]
        graphdict['soilt20']['timestamp'] = mco21df['UTC Time [ms]'].tolist()
        mappedlist = map(self.convert.degF_from_float,mco21df['20-in Soil Temperature [deg C]'].tolist())
        graphdict['soilt20']['values'] = mappedlist
        # 36-in Soil Temperature [deg C]
        graphdict['soilt36']['timestamp'] = mco21df['UTC Time [ms]'].tolist()
        mappedlist = map(self.convert.degF_from_float,mco21df['36-in Soil Temperature [deg C]'].tolist())
        graphdict['soilt36']['values'] = mappedlist
        # 4-in Saturation Extract EC [mS/cm]
        graphdict['soilec4']['timestamp'] = mco7df['UTC Time [ms]'].tolist()
        graphdict['soilec4']['values'] = mco7df['4-in Saturation Extract EC [mS/cm]'].tolist()
        # 8-in Saturation Extract EC [mS/cm]
        graphdict['soilec8']['timestamp'] = mco7df['UTC Time [ms]'].tolist()
        graphdict['soilec8']['values'] = mco7df['8-in Saturation Extract EC [mS/cm]'].tolist()
        # 20-in Saturation Extract EC [mS/cm]
        graphdict['soilec20']['timestamp'] = mco21df['UTC Time [ms]'].tolist()
        graphdict['soilec20']['values'] = mco21df['20-in Saturation Extract EC [mS/cm]'].tolist()
        # 4-in Saturation Extract EC [mS/cm]
        graphdict['soilec36']['timestamp'] = mco21df['UTC Time [ms]'].tolist()
        graphdict['soilec36']['values'] = mco21df['36-in Saturation Extract EC [mS/cm]'].tolist()
        # Battery Percent [%]
        graphdict['batteryper']['timestamp'] = mco21df['UTC Time [ms]'].tolist()
        graphdict['batteryper']['values'] = mco21df['Battery Percent [%]'].tolist()
        # Battery Voltage [mV]
        graphdict['batterymv']['timestamp'] = mco21df['UTC Time [ms]'].tolist()
        graphdict['batterymv']['values'] = mco21df['Battery Voltage [mV]'].tolist()

        return graphdict
    
    def build_mobile_graphs(self,jsonDict,graphdict):
        name = jsonDict['displayname']
        station = jsonDict['station']
        graphpath = self.miscfunc.local_normpath(self.zentraconfig.mt_mesonet_web_path,'mesonet')
        outpath = self.miscfunc.local_normpath(graphpath,station)
        
        # Battery Percent
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'batteryper.png')
        if not mg.GraphBatteryPer(name,pngpath,graphdict['batteryper']['timestamp'],graphdict['batteryper']['values']):
            jsonDict['batteryperURL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        # Battery Millivolts
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'batterymv.png')
        if not mg.GraphBatteryMV(name,pngpath,graphdict['batterymv']['timestamp'],graphdict['batterymv']['values']):
            jsonDict['batterymvURL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"
        
        # Solar radiation
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'solrad.png')
        if not mg.GraphSolarRad(name,pngpath,graphdict['solrad']['timestamp'],graphdict['solrad']['values']):
            jsonDict['solradURL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"
            
        # Temperature
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'temperature.png')
        if not mg.GraphTemperature(name,pngpath,graphdict['temperature']['timestamp'],graphdict['temperature']['values']):
            jsonDict['temperatureURL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        # Relative Humidity
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'relhumidity.png')
        if not mg.GraphRelHumidity(name,pngpath,graphdict['relhumidity']['timestamp'],graphdict['relhumidity']['values']):
            jsonDict['relhumidityURL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"


        # Windspeed
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'windspeed.png')
        if not mg.GraphWindspeed(name,pngpath,graphdict['windspeed']['timestamp'],graphdict['windspeed']['values']):
            jsonDict['windspeedURL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        # Wind Gusts
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'windgust.png')
        if not mg.GraphWindGusts(name,pngpath,graphdict['windgust']['timestamp'],graphdict['windgust']['values']):
            jsonDict['windgustURL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        # Wind Direction
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'winddir.png')
        if not mg.GraphWindDirection(name,pngpath,graphdict['winddir']['timestamp'],graphdict['winddir']['values']):
            jsonDict['winddirURL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        # Dewpoint
        # pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'dewpoint.png')
        # if not mg.GraphDewpoint(name,pngpath,graphdict['dewpoint']['timestamp'],graphdict['dewpoint']['values']):
        #    jsonDict['dewpointURL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"
       
        # Precipitation
        # pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'precipitation.png')
        # if not mg.GraphPrecipitation(name,pngpath,graphdict['precipitation']['timestamp'],graphdict['precipitation']['values']):
        #   jsonDict['precipitationURL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"
       
        # Total Precipitation
        # pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'preciptotal.png')
        # if not mg.GraphPrecipTotal(name,pngpath,graphdict['preciptotal']['timestamp'],graphdict['preciptotal']['values']):
        #    jsonDict['preciptotalURL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        # Pressure
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'barometer.png')
        if not mg.GraphPressure(name,pngpath,graphdict['pressure']['timestamp'],graphdict['pressure']['values']):
            jsonDict['pressureURL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        # Hit numbers
        # pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'hitnum.png')
        # if not mg.GraphHitNumber(name,pngpath,graphdict['hitnum']['timestamp'],graphdict['hitnum']['values']):
        #    jsonDict['hitnumURL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"
 
        # Hit distance
        # pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'hitdist.png')
        # if not mg.GraphHitDistance(name,pngpath,graphdict['hitdist']['timestamp'],graphdict['hitdist']['values']):
        #    jsonDict['hitdistURL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"
 
        # Soil Temperature (4-inch)
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'soilt4.png')
        if not mg.GraphSoilTemp4(name,pngpath,graphdict['soilt4']['timestamp'],graphdict['soilt4']['values']):
            jsonDict['soilt4URL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        # Soil Temperature (8-inch)
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'soilt8.png')
        if not mg.GraphSoilTemp8(name,pngpath,graphdict['soilt8']['timestamp'],graphdict['soilt8']['values']):
            jsonDict['soilt8URL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        # Soil Temperature (20-inch)
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'soilt20.png')
        if not mg.GraphSoilTemp20(name,pngpath,graphdict['soilt20']['timestamp'],graphdict['soilt20']['values']):
            jsonDict['soilt20URL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        # Soil Temperature (36-inch)
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'soilt36.png')
        if not mg.GraphSoilTemp36(name,pngpath,graphdict['soilt36']['timestamp'],graphdict['soilt36']['values']):
            jsonDict['soilt36URL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        # Soil Water Content (4-inch)
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'soilvwc4.png')
        if not mg.GraphSoilVWC4(name,pngpath,graphdict['soilvwc4']['timestamp'],graphdict['soilvwc4']['values']):
            jsonDict['soilvwc4URL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        # Soil Water Content (8-inch)
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'soilvwc8.png')
        if not mg.GraphSoilVWC8(name,pngpath,graphdict['soilvwc8']['timestamp'],graphdict['soilvwc8']['values']):
            jsonDict['soilvwc8URL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        # Soil Water Content (20-inch)
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'soilvwc20.png')
        if not mg.GraphSoilVWC20(name,pngpath,graphdict['soilvwc20']['timestamp'],graphdict['soilvwc20']['values']):
            jsonDict['soilvwc20URL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        # Soil Water Content (36-inch)
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'soilvwc36.png')
        if not mg.GraphSoilVWC36(name,pngpath,graphdict['soilvwc36']['timestamp'],graphdict['soilvwc36']['values']):
            jsonDict['soilvwc36URL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        # Soil Electrical Conductivity (4-inch)
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'soilec4.png')
        if not mg.GraphSoilEC4(name,pngpath,graphdict['soilec4']['timestamp'],graphdict['soilec4']['values']):
            jsonDict['soilec4URL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        # Soil Electrical Conductivity (8-inch)
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'soilec8.png')
        if not mg.GraphSoilEC8(name,pngpath,graphdict['soilec8']['timestamp'],graphdict['soilec8']['values']):
            jsonDict['soilec8URL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        # Soil Electrical Conductivity (20-inch)
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'soilec20.png')
        if not mg.GraphSoilEC20(name,pngpath,graphdict['soilec20']['timestamp'],graphdict['soilec20']['values']):
            jsonDict['soilec20URL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        # Soil Electrical Conductivity (36-inch)
        pngpath = self.miscfunc.local_normpath(outpath,station+'-'+'soilec36.png')
        if not mg.GraphSoilEC36(name,pngpath,graphdict['soilec36']['timestamp'],graphdict['soilec36']['values']):
            jsonDict['soilec36URL']="http://mco.cfc.umt.edu/mesonet/NoGraph.png"

        return jsonDict

    def get_mobile_graph_dict(self):
        current_dict = {
                'solrad':       {'timestamp':[],'values':[]},
                'precipitation':{'timestamp':[],'values':[]},
                'preciptotal':  {'timestamp':[],'values':[]},
                'hitnum':       {'timestamp':[],'values':[]},
                'hitdist':      {'timestamp':[],'values':[]},    
                'winddir':      {'timestamp':[],'values':[]},
                'windspeed':    {'timestamp':[],'values':[]},
                'windgust':     {'timestamp':[],'values':[]},
                'temperature':  {'timestamp':[],'values':[]},
                'relhumidity':  {'timestamp':[],'values':[]},
                'pressure':     {'timestamp':[],'values':[]},
                'soilvwc4':     {'timestamp':[],'values':[]},
                'soilvwc8':     {'timestamp':[],'values':[]},
                'soilvwc20':    {'timestamp':[],'values':[]},
                'soilvwc36':    {'timestamp':[],'values':[]},
                'soilt4':       {'timestamp':[],'values':[]},
                'soilt8':       {'timestamp':[],'values':[]},
                'soilt20':      {'timestamp':[],'values':[]},
                'soilt36':      {'timestamp':[],'values':[]},
                'soilec4':      {'timestamp':[],'values':[]},
                'soilec8':      {'timestamp':[],'values':[]},
                'soilec20':     {'timestamp':[],'values':[]},
                'soilec36':     {'timestamp':[],'values':[]},
                'batteryper':   {'timestamp':[],'values':[]},
                'batterymv':    {'timestamp':[],'values':[]}    
               }
        return current_dict


#==========================================================================
# Main and tests
#==========================================================================
if __name__ == "__main__":
    # Load user configuration settings as configuration object
    zconfig = config.ZentraConfig()
    # Load Zentra configuration settings as configuration object
    zconfigdownload = configdownload.ZentraDownloadConfig()
    # Load CSV Writer object
    mcowebwriter = webWriter(zconfig,zconfigdownload)
    mcoCSV = r"\\mcofiles.cfc.umt.edu\Resources$\Data\Mesonet\ZentraTest\API-Output\ClimateOffice\Level1\MCO-Readings-ebarllob.csv"
    settings = r"\\mcofiles.cfc.umt.edu\Resources$\Data\Mesonet\ZentraTest\API-Output\ClimateOffice\Level0\MCO-Settings-ebarllob.csv"
    jsonpath = r"\\mcofiles.cfc.umt.edu\Resources$\Data\Mesonet\ZentraTest\API-Output\ClimateOffice\Web\Stations.json"
    displayname = "Clearwater SW"
    logger_username = "06-00184"
    station = "ebarllob"
    data = {} 
    data['stations'] = []
    jsondict = mcowebwriter.write_levelone_mcoweb(mcoCSV,displayname,logger_username,station)
    data['stations'].append(jsondict)
    #Change dictionary to a list        
    data = data['stations']
    print data
    with open(jsonpath, 'w') as outfile:
        json.dump(data,outfile)
    outfile.close()