'''
@created="Mar 2018"
@description=('The Zentra configuration class is a Python configuration '
              'resource file for defining parameters necessary to process '
              'Zentra content for use by the Montana Climate Office),
@attention='http://climate.umt.edu'
@author: 'Michael D. Sweet',
@email='michael.sweet@umontana.edu',
@organization: 'Montana Climate Office'
#==========================================================================
# USE
#==========================================================================
This class is instantiated to provide resource variables and methods
for managing valid date ranges for the Zentra-Mesonet collection
'''
import datetime
import config

#==========================================================================
# Class Definition
#==========================================================================
class ZentraDownloadConfig():
    
    '''
    Description: 
        Configuration file for downloading Zentra data from
        https://zentracloud.com and writing to local path
        \\mcofiles\Resources$\Data\Mesonet
        
        Load using:
            import util.ZentraDownloadConfig
    '''

    #==========================================================================
    # Methods for object instantiation
    #==========================================================================
    def __init__(self):
        """
            Initializes properties for Zentra download configuration object
            INPUT: Instantiates config.py class containing configuration parameters
                    Class ZentraDownloadConfig() instantiates util\config.ZentraConfig()
            OUTPUT: Latest date for download as date-time object and string object (YYYY.MM.DD)
            OUTPUT: First date for download as date-time object and string object (YYYY.MM.DD)
        """
        # Load configuration settings as Zentra object
        self.zentraconfig = config.ZentraConfig()
        # Initialize minimum day for collection as date-time object
        self.minimum_day = self.set_minimum_day()
        # Initialize latest day string to None
        self.latestdaystring = None
        # Set latest day of Zentra collection as date-time object.
        self.latestday, self.latestdaystring = self.set_default_latest_day()
        # Initialize first day string to None
        self.firstdaystring = None
        # Set first day of Zentra collection as date-time object.
        self.firstday, self.firstdaystring = self.set_default_first_day()

    # Function to set minimum day based on configuration setting. 
    def set_minimum_day(self):
        # Derive date-time object based on first day values in configuration file
        # Set first day property as date-time object
        self.minimum_day = datetime.datetime(year=self.zentraconfig.STARTZENTRAYEAR, 
                                     month=self.zentraconfig.STARTZENTRAMONTH, 
                                     day=self.zentraconfig.STARTZENTRADAY)
        return self.minimum_day
    
    # Function to set latest day based on configuration setting or user input. 
    def set_default_latest_day(self):
        """
            Sets default latest day for Zentra download as current date.
            OUTPUT: (1) latest date for download as date-time object, and 
                    (2) latest day as string object (YYYY.MM.DD)
            CALLS CLASS METHOD: set_latestday_string
        """
        # Set latest day property as date-time object
        self.latestday = self.zentraconfig.latest_day
        # Call function to set date-time object as string in form YYYY.MM.DD
        self.latestdaystring = self.set_latestday_string(self.latestday)
        # Return tuple for date-time object and string
        return (self.latestday, self.latestdaystring)

    def set_default_first_day(self,N=None):
        """
            Sets default first day for Zentra download as N days prior to current date (default N =3).
            INPUT: Number of days prior to current date
            OUTPUT: (1) first date for download as date-time object, and 
                    (2) first day as string object (YYYY.MM.DD)
            CALLS CLASS METHOD: set_firstday_string
        """
        # If number of days is not passed as argument then default to default number of look-back days. Bounds checked.
        if N is None or N < self.zentraconfig.lookbackdays:
            N = self.zentraconfig.lookbackdays
        # Derive date-time object based on current date and offset
        # Set latest day property as date-time object
        self.firstday = self.zentraconfig.latest_day - datetime.timedelta(days=N)
        # Call function to set date-time object as string in form YYYY.MM.DD
        self.firstdaystring = self.set_firstday_string(self.firstday)
        return (self.firstday, self.firstdaystring)

    def set_latestday_string(self,theday):
        """
            Sets standardized string format for latest day for Zentra download
            INPUT: Date-time object
            OUTPUT: Latest day as string object (YYYY.MM.DD)
            CALLS CLASS METHOD: string_from_day
       """
        self.latestdaystring = self.string_from_day(theday)
        # Return Latest Day as string
        return self.latestdaystring

    def set_firstday_string(self,theday):
        """
            Sets standardized string format for first day for Zentra download
            INPUT: Date-time object
            OUTPUT: First day as string object (YYYY.MM.DD)
            CALLS CLASS METHOD: string_from_day
       """
        self.firstdaystring = self.string_from_day(theday)
        # Return First Day as string
        return self.firstdaystring

    # Function to set latest day based user date input as date-time object.
    def set_latest_day(self,theday):
        """
            Sets latest day for Zentra download based on user date input as date-time object.
            INPUT: Date-time object
            OUTPUT: (1) latest date for download as date-time object, and 
                    (2) latest day as string object (YYYY.MM.DD)
            CALLS CLASS METHOD: set_latestday_string
        """
        # Set (reset) latest day of Zentra collection as date-time object. Default is set in configuration file
        self.latestday, self.latestdaystring = self.set_default_latest_day()
        # If input date range valid then set latest day property as date-time object
        if self.test_datetime_range(theday):
            self.latestday = theday
            # Call function to set date-time object as string in form YYYY.MM.DD
            self.latestdaystring = self.set_latestday_string(self.latestday)
        # Return tuple for date-time object and string
        return self.latestday

    # Function to set first day based user date input as date-time object.
    def set_first_day(self,theday):
        """
            Sets first day for Zentra download based on user date input as date-time object.
            INPUT: Date-time object
            OUTPUT: Tuple with (1) first day as date-time object, and 
                    (2) first day as string object (YYYY.MM.DD)
            CALLS CLASS METHOD: set_firstday_string
        """
        # Set (reset) first day of Zentra collection as date-time object. Default is set in configuration file
        self.firstday,self.firstdaystring = self.set_default_first_day()
        # If input date range valid then set latest day property as date-time object
        if self.test_datetime_range(theday):
            self.firstday = theday
            # Call function to set date-time object as string in form YYYY.MM.DD
            self.firstdaystring = self.set_firstday_string(self.firstday)
        # Return tuple for date-time object and string
        return self.firstday

    def test_datetime_range(self,dt):
        """
            Tests if input date-time object is within date range of Zentra collection
            INPUT: Date-time object
            OUTPUT: logical true or false
        """
        # Instantiate local object for testing default date range
        local = ZentraDownloadConfig()
        # Test if date is within Zentra collection date bounds
        if dt >= local.minimum_day and dt <= local.latestday:
            return True
        else:
            return False

    def string_from_day(self,theday):
        """
            Standardizes the string format of the date-time object to YYYY.MM.DD
            INPUT: Date-time object
            OUTPUT: formatted string
        """
        datestring = '{:0>4d}.{:0>2d}.{:0>2d}'.format(theday.year,theday.month,theday.day)
        # Return formated string
        return datestring

    def day_from_string(self,daystring):
        """
            Standardizes the string format of the date-time object to YYYY.MM.DD
            INPUT: formatted string
            OUTPUT: Date-time object
        """
        theday = datetime.datetime(year=int(daystring[0:4]),month=int(daystring[5:7]),day=int(daystring[8:10]))
        # Return formated string
        return theday

#==========================================================================
# Main and tests
#==========================================================================
def test_null_latest_date():
    print "Test for condition where requested offset is not specified (default offset is N=3 days)"
    print 'Current Zentra latest day is', zentra.latestday
    zentra.set_default_latest_day()
    print 'Resulting Zentra latest day is', zentra.latestday
    print 'Resulting Zentra latest day as string is', zentra.latestdaystring
    print 'Resulting Zentra first day is', zentra.firstday
    print 'Resulting Zentra first day as string is', zentra.firstdaystring
    print
    return

def test_date_offset(N):
    print "Test for condition where requested offset differs from default offset (N=3 days)"
    print '{}-day offset from current date'.format(N)
    zentra.set_default_latest_day()
    print 'Current Zentra latest day is', zentra.latestday
    zentra.set_default_first_day(N)
    print 'Resulting Zentra latest day is', zentra.latestday
    print 'Resulting Zentra latest day as string is', zentra.latestdaystring
    print 'Resulting Zentra first day is', zentra.firstday
    print 'Resulting Zentra first day as string is', zentra.firstdaystring
    print
    return

def test_default_first_date():
    print "Test for default condition for first available date for Zentra download"
    print 'Zentra first day is', zentra.firstday
    print 'Zentra first day as file string is', zentra.firstdaystring
    print
    return

def test_date_range_checking(dt):
    print 'Testing date-time range checking for {:0>4d}.{:0>2d}.{:0>2d}'.format(dt.year,dt.month,dt.day)
    print zentra.test_datetime_range(dt)
    print
    return

def test_user_defined_latest_date(dt):
    print 'Testing user-defined latest date for {:0>4d}.{:0>2d}.{:0>2d}'.format(dt.year,dt.month,dt.day)
    zentra.set_latest_day(dt)
    print 'Resulting Zentra latest day is', zentra.latestday
    print 'Resulting Zentra latest day as string is', zentra.latestdaystring
    print    
    return

def test_user_defined_first_date(dt):
    print 'Testing user-defined first date for {:0>4d}.{:0>2d}.{:0>2d}'.format(dt.year,dt.month,dt.day)
    zentra.set_first_day(dt)
    print 'Resulting Zentra first day is', zentra.firstday
    print 'Resulting Zentra first day as string is', zentra.firstdaystring
    print
    return

if __name__ == "__main__":
    # Test object instantiation
    zentra = ZentraDownloadConfig()
    # Test for null latest date
    test_null_latest_date()
    # Test for date offset greater than default
    test_date_offset(5)
    # Test for date offset less than default
    test_date_offset(1)
    # Test default first date
    test_default_first_date()

    # Test range checking on user-defined date
    print "...False test, date out of range"
    test_date_range_checking(datetime.datetime(year=2012, month=2, day=9))
    print "...True test, date in range"
    test_date_range_checking(datetime.datetime(year=2017, month=2, day=9))
    
    # Test range checking on user-defined latest date
    print "...Testing out-of-range condition for user-defined latest date"
    test_user_defined_latest_date(datetime.datetime(year=2012, month=2, day=9))
    print "...Testing in range condition for user-defined latest date"
    test_user_defined_latest_date(datetime.datetime(year=2017, month=2, day=9))

    # Test range checking on user-defined first date
    print "...Testing out-of-range condition for user-defined first date"
    test_user_defined_first_date(datetime.datetime(year=2012, month=2, day=9))
    print "...Testing in range condition for user-defined first date"
    test_user_defined_first_date(datetime.datetime(year=2017, month=2, day=9))

    # Test conversion of day from string
    print zentra.day_from_string("2018.03.12")

#==========================================================================
# END
#==========================================================================
