#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@created="May 2018"
@description=('This Zentra class provides the properties and',
              'functions that define the parameters necessary',
              'to parse Zentra download command line options for use by the'
              'Montana Climate Office),
@attention='http://climate.umt.edu
@author: 'Michael D. Sweet',
@email='michael.sweet@umontana.edu',
@organization: 'Montana Climate Office'
#==========================================================================
# USE
#==========================================================================
This class is instantiated to provide resource variables and methods
for parsing Zentra download command line options
'''
import datetime
import argparse
import config as zentraconfig
import configdownload as zentraconfigdownload

#==========================================================================
# Class Definition
#==========================================================================
class CommandArguments():
    
    """
        Parse Zentra download command line arguments
       
        Load using:
            import util.importparser
    """

    #==========================================================================
    # Methods for object instantiation
    #==========================================================================
    def __init__(self,zentraconfig,zentraconfigdownload):
        """
            Initializes properties for Zentra command line arguments
            INPUTS: ZentraConfig() object from config.py
                    ZentraDownloadConfig() object from configdownload.py
         """
        # Load user configuration settings as configuration object
        self.zentraconfig = zentraconfig
        # Load Zentra configuration settings as configuration object
        self.zentraconfigdownload = zentraconfigdownload
        # Initiate the parser
        self.parser = self.configure_parser()
        self.args = self.parse_arguments()
        
    def configure_parser(self):
        # Add parser object
        parser = argparse.ArgumentParser(description='Downloader for Zentra collection.')
        # Add parser options
        parser.add_argument('-s', '--startday', dest='startday', 
                            default = self.zentraconfigdownload.latestday, 
                            help="Start day of download as YYYY.MM.DD")
        parser.add_argument('-e', '--endday', dest='endday', 
                            default = self.zentraconfigdownload.latestday, 
                            help="End day of download as YYYY.MM.DD")
        parser.add_argument('-u', '--update', dest = 'update', 
                            default=True, 
                            help="True (default) will overwrite existing content")
        parser.add_argument('-n', '--offset', dest='offset', 
                            default=self.zentraconfig.lookbackdays, 
                            help="Number of days prior to latest date to download")
        parser.add_argument('-k', '--pkey', dest='pkey', 
                            default=None, 
                            help="Primary key for single Mesonet station")
        parser.add_argument('-a', '--abandoned', dest='abandoned', 
                            default=False, 
                            help="True-False flag to download data for abandoned loggers")
        return parser

    def print_arguments(self):
        print
        print "Argument values:"
        print "Start download day is: ", self.args.startday
        print "End download day is: ", self.args.endday
        print "Download update flag is set to: ", self.args.update
        print "Download offset value is set to: ", self.args.offset
        print "Primary key of station is set to: ", self.args.pkey
        print "Download flag for abandoned loggers is set to: ", self.args.abandoned
        
    def parse_arguments(self):
        self.args = self.parser.parse_args()
        # Parse and error-check user-defined options and arguments
        if not isinstance(self.args.startday, datetime.datetime):
            try:
                self.args.startday = datetime.datetime.strptime(self.args.startday,'%Y.%m.%d')
            except:
                # print "Improperly formatted date string.", args.startday
                self.args.startday = self.zentraconfigdownload.latestday
                # print "Start day reset to latest day: ", args.startday
    
        if not isinstance(self.args.endday, datetime.datetime):
            try:
                self.args.endday = datetime.datetime.strptime(self.args.endday,'%Y.%m.%d')
            except:
                # print "Improperly formatted date string.", args.endday
                self.args.endday = self.zentraconfigdownload.latestday
                # print "End day reset to latest day: ", args.endday
    
        if not isinstance(self.args.offset, int):
            try:
                self.args.offset = int(self.args.offset)
                self.args.startday = self.args.endday - datetime.timedelta(days=self.args.offset)
            except:
                # print "Offset not an integer.", args.offset
                self.args.offset = self.zentraconfig.lookbackdays
                self.args.startday = self.args.endday - datetime.timedelta(days=self.args.offset)
                # print "Reset offset to default: ", args.offset
        
        if not isinstance(self.args.update, bool):
            print "Update flag is not a boolean.", self.args.update
            self.args.update = False
            print "Reset update flag to default: ", self.args.update
            
        return self.args

#==========================================================================
# Main and tests
#==========================================================================
if __name__ == "__main__":
    # Load user configuration settings as configuration object
    zconfig = zentraconfig.ZentraConfig()
    # Load Zentra configuration settings as configuration object
    zconfigdownload = zentraconfigdownload.ZentraDownloadConfig()
    # Zentra download command line argument input parser
    zentraparser = CommandArguments(zconfig,zconfigdownload)
    #------------------------------
    # MODIFY INPUT PARAMETERS in arguments for run configuration
    # Need to build test class to test command line in code
    #------------------------------
    # Print argument values
    zentraparser.print_arguments()
    

#==========================================================================
# END
#==========================================================================
