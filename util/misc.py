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
import os
import errno
import util.config as config
import numpy as np

#==========================================================================
# Class Definition
#==========================================================================
class Pathways():
    
    """
        Configuration file for downloading Zentra station data from
        https://zentra.com and writing to local path 
        \\mcofiles\Resources$\Data\Mesonet
        
        Load using:
            import util.misc
    """

    #==========================================================================
    # Methods for object instantiation
    #==========================================================================
    def __init__(self):
        """
            Object initialization
        """
    #==========================================================
    # Functions
    #==========================================================
    def folder_string_from_date(self,theday):
        """
            Standardizes the folder data string format of the date-time object to YYYY.MM.DD
            INPUT: Date-time object
            OUTPUT: formatted string
        """
        datestring = '{:0>4d}.{:0>2d}.{:0>2d}'.format(theday.year,theday.month,theday.day)
        # Return formatted string
        return datestring

    def local_normpath(self,predecessor,successor):
        normpath = os.path.normpath(os.path.join(predecessor,successor))
        return normpath

    def check_if_path_exists(self,workspace):
        try:
            os.makedirs(workspace)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
            else:
                pass

    def check_if_file_path_exists(self,workspace):
        if os.path.exists(workspace):
            return True
        else:
            return False

class Conversion():

    #==========================================================================
    # Methods for object instantiation
    #==========================================================================
    def __init__(self):
        
        """
            Object initialization
        """
        # Load user configuration settings as configuration object
        self.zconfig = config.ZentraConfig()

        
    #==========================================================
    # Functions
    #==========================================================

    def check_for_NA(self,inval):
        # print "In val: ", inval, type(inval)
        outval = self.zconfig.zentra_NA_VALUE
        # if input is integer return integer
        if isinstance(inval,int):
            # If interger is not NULL value then return val otherwise 'NA'
            if inval < int(self.zconfig.zentra_NULL_VALUE):
                outval = inval
        # if input is float return float
        elif isinstance(inval,float):
            # If float is not NULL value then return val otherwise "NA"
            if inval < float(self.zconfig.zentra_NULL_VALUE):
                outval = inval
        # if input is string and not empty return string
        elif isinstance(inval,str) and len(inval) > 0 and inval != "NA":
            outval = inval
        # else return "NA"
        return outval

    def str_or_na_from_int(self,inval):
        # print "INVAL: " ,inval
        inval = self.check_for_NA(inval)
        if inval == self.zconfig.zentra_NA_VALUE:
            outval = inval
        elif isinstance(inval,int):
            outval = str(inval)
        elif isinstance(inval,float):
            outval = str(round(inval,0))
        # print "INT OUTVAL: ",outval, " INVAL: ", inval
        return outval
    
    def strdegF_or_na_from_float(self,inval):
        inval = self.check_for_NA(inval)
        if inval == self.zconfig.zentra_NA_VALUE:
            outval = inval
        else:
            try:
                outval = str(int(round(((float(inval)*1.8)+32.0),0)))
            except ValueError:
                outval = self.zconfig.zentra_NA_VALUE
        return outval

    def degF_from_float(self,inval):
        if inval == np.nan:
            outval = inval
        else:
            try:
                outval = str(int(round(((float(inval)*1.8)+32.0),0)))
            except ValueError:
                outval = np.nan
        return outval

    def strrelhum_or_na_from_float(self,inval):
        inval = self.check_for_NA(inval)
        if inval == self.zconfig.zentra_NA_VALUE:
            outval = inval
        else:
            try:
                outval = str(int(round((float(inval)*100.0),0)))
            except ValueError:
                outval = self.zconfig.zentra_NA_VALUE
        return outval

    def relhum_from_float(self,inval):
        if inval == np.nan:
            outval = inval
        else:
            try:
                outval = str(int(round((float(inval)*100.0),0)))
            except ValueError:
                outval = np.nan
        return outval

    def strpervwc_or_na_from_float(self,inval):
        inval = self.check_for_NA(inval)
        if inval == self.zconfig.zentra_NA_VALUE:
            outval = inval
        else:
            try:
                outval = str(int(round((float(inval)*100.0),0)))
            except ValueError:
                outval = self.zconfig.zentra_NA_VALUE
        return outval

    def pervwc_from_float(self,inval):
        if inval == np.nan:
            outval = inval
        else:
            try:
                outval = str(int(round((float(inval)*100.0),0)))
            except ValueError:
                outval = np.nan
        return outval
    
    def strmph_or_na_from_meterpersec(self,inval):
        inval = self.check_for_NA(inval)
        if inval == self.zconfig.zentra_NA_VALUE:
            outval = inval
        else:
            try:
                outval = str(round((float(inval)*2.23694),1))
            except ValueError:
                outval = self.zconfig.zentra_NA_VALUE
        return outval

    def mph_from_meterpersec(self,inval):
        if inval == np.nan:
            outval = inval
        else:
            try:
                outval = str(round((float(inval)*2.23694),1))
            except ValueError:
                outval = np.nan
        return outval
    
    def strdecimal_inches_or_na_from_float(self,inval,places):
        # will print 0.0 for zero, and three decimals for values > 0
        inval = self.check_for_NA(inval)
        if inval == self.zconfig.zentra_NA_VALUE:
            outval = inval
        else:
            try:
                outval = str('{0:.3}'.format(round(float(inval)*0.0393701,places)))
            except ValueError:
                outval = self.zconfig.zentra_NA_VALUE
        return outval

    def decimal_inches_from_float(self,inval,places=3):
        if inval == np.nan:
            outval = inval
        else:
            try:
                outval = str('{0:.3}'.format(round(float(inval)*0.0393701,places)))
            except ValueError:
                outval = np.nan
        return outval
        
    def strdewpt_or_na_from_float(self,tval,rhval):
        tval = self.check_for_NA(tval)
        rhval = self.check_for_NA(rhval)
        if tval == self.zconfig.zentra_NA_VALUE or rhval == self.zconfig.zentra_NA_VALUE:
            outval = self.zconfig.zentra_NA_VALUE
        else:
            try:
                outval = str(int(round(float(tval)-((100.0-float(rhval))/5.0),0)))
            except ValueError:
                outval = self.zconfig.zentra_NA_VALUE
        return outval
    
    def strbar_or_na_from_float(self,inval):
        inval = self.check_for_NA(inval)
        if inval == self.zconfig.zentra_NA_VALUE:
            outval = inval
        else:
            if isinstance(inval,float):
                try:
                    outval = str(round(inval*0.2953,2))
                except ValueError:
                    outval = self.zconfig.zentra_NA_VALUE
            else:
                outval = inval
        return outval

    def bar_from_float(self,inval):
        if inval == np.nan:
            outval = inval
        else:
            if isinstance(inval,float):
                try:
                    outval = str(round(inval*0.2953,2))
                except ValueError:
                    outval = np.nan
            else:
                outval = inval
        return outval
        
    def strint_or_na_from_float(self,inval):
        inval = self.check_for_NA(inval)
        if isinstance(inval,float):
            outval = str(int(round(inval,0)))
        else:
            outval = inval
        return outval
    
    def int_or_na_from_float(self,inval):
        inval = self.check_for_NA(inval)
        if isinstance(inval,float):
            outval = int(round(inval,0))
        else:
            outval = inval
        return outval
    
    def strpercent_or_na_from_real(self,inval):
        inval = self.check_for_NA(inval)
        if isinstance(inval,float):
            outval = str(int(round((inval*100.0),0)))
        else:
            outval = inval
        return outval
    
    def percent_or_null_from_real(self,inval):
        inval = self.check_for_NULL(inval)
        if isinstance(inval,float):
            outval = round((inval*100.0),2)
        else:
            outval = inval
        return outval
    
        inval = self.check_for_NULL(inval)
        if isinstance(inval,float):
            outval = round((inval*2.23694),1)
        else:
            outval = inval
        return outval
