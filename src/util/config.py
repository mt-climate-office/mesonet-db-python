'''
@created="May 2018"
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
This class is instantiated to provide static resource variables for
local paths, web URLs, user names, user passwords, and SMAP parameters
'''
import util.ConnectSQL as connSQL
import datetime
import pytz

#==========================================================================
# Class Definition
#==========================================================================
class ZentraConfig():
        
    '''
    Description: 
        Configuration file for downloading Zentra data from
        https://zentracloud.com and writing to local path
        \\mcofiles\Resources$\Data\Mesonet
        
        Load using:
            import util.ZentraConfig
    '''
    
    #==========================================================================
    # Methods for object instantiation
    #==========================================================================
    def __init__(self):
        """
            Initializes properties for Zentra configuration object
        """
        # Minimum start year as integer for Zentra, Do Not Change
        self.STARTZENTRAYEAR = 2016
        # Minimum start month as integer for Zentra, Do Not Change
        self.STARTZENTRAMONTH = 7
        # Minimum start day as integer for Zentra, Do Not Change
        self.STARTZENTRADAY = 1
        # Zentra user login
        self.zentra_api_user = "state.climatologist@umontana.edu"
        # Zentra user password
        self.zentra_api_user_password = "climate2018!"
        # Zentra API root web address
        self.zentra_api_ip_address = "zentracloud.com"
        # Mesonet maximum value. Values greater than this are NoData values
        self.mt_mesonet_maxval_limit = 65000
        # Zentra-Mesonet NULL value for CSV file output
        self.zentra_NULL_VALUE = 65535
        # Zentra-Mesonet NULL value for web display
        self.zentra_NA_VALUE = "NA"
        # Local time zone for API calls
        self.local_time_zone = pytz.timezone("America/Denver")
        # Latest day
        self.latest_day = datetime.datetime.now()
        # Earliest day
        self.earliest_day = datetime.datetime.now()
        # Root target output path for Zentra downloads on local file system
        self.zentra_local_folder = r"\\mmcofiles.cfc.umt.edu\Resources$\Data\Mesonet\ZentraTest\API-Output"
        # Root target output path for Zentra JSON download of readings on local file system
        self.zentra_readings_folder = r"\\mcofiles.cfc.umt.edu\Resources$\Data\Mesonet\ZentraTest\API-Output\ClimateOffice\Readings"
        # Root target output path for Zentra JSON downloads of settings on local file system
        self.zentra_settings_folder = r"\\mcofiles.cfc.umt.edu\Resources$\Data\Mesonet\ZentraTest\API-Output\ClimateOffice\Settings"
        # Root target output path for Mesonet metadata on local file system
        self.mesonet_metadata_folder = r"\\mcofiles.cfc.umt.edu\Resources$\Data\Mesonet\ZentraTest\API-Output\ClimateOffice\Metadata"
        # Root target output path for Mesonet metadata on local file system
        self.mesowest_metadata_folder = r"\\cfcweb\ftp$\mesowest\Zentra\Metadata"
        # Root target output path for Mesonet MesoWest data on local file system
        self.mesowest_fullcsv_folder = r"\\cfcweb\ftp$\mesowest\Zentra\Full"
        # Root target output path for Mesonet MesoWest data on local file system
        self.mesowest_dailycsv_folder = r"\\cfcweb\ftp$\mesowest\Zentra\Daily"
        # Root target output path for Mesonet data on local file system
        self.mesonet_csv_folder = r"\\mcofiles.cfc.umt.edu\Resources$\Data\Mesonet\ZentraTest\API-Output\ClimateOffice\MesonetCSV"
        # Root target output path for Level-0 Mesonet data on local file system
        self.mesonet_levelzero_folder = r"\\mcofiles.cfc.umt.edu\Resources$\Data\Mesonet\ZentraTest\API-Output\ClimateOffice\Level0"
        # Root target output path for Level-1 Mesonet data on local file system
        self.mesonet_levelone_folder = r"\\mcofiles.cfc.umt.edu\Resources$\Data\Mesonet\ZentraTest\API-Output\ClimateOffice\Level1"
        # Root target output path for Level-2 Mesonet data on local file system
        self.mesonet_leveltwo_folder = r"\\mcofiles.cfc.umt.edu\Resources$\Data\Mesonet\ZentraTest\API-Output\ClimateOffice\Level2"
        # Root target output path for Level-1 Mesonet data on local file system
        self.mt_mesonet_levelone_production = r"\\mcofiles.cfc.umt.edu\Resources$\Data\Mesonet\API-Output\ClimateOffice\Level1Production"
        # Mesonet web folder for posting graphics
        self.mt_mesonet_web_path = r"\\CFCWEB\mco.cfc.umt.edu$"
        # self.mt_mesonet_web_path = r"\\mcofiles.cfc.umt.edu\Resources$\Data\Mesonet\ZentraTest\API-Output\ClimateOffice\Web"
        # Mesonet HTTP path
        self.mt_mesonet_http_path = "http://mco.cfc.umt.edu/mesonet"
        # Number of days to look back for download relative to current day
        self.lookbackdays = 3
        # Length of timeout in seconds for processing multiple HTTP requests to Zentra (see httpget.py)
        self.timedelay = 1
        # PyPlot sign-in user name
        self.pyplotuser = 'mdsweet'
        # PyPlot hash code
        self.pyplotapikey = 'ddejj1kzPeisigzHeaw8'
        # Path to Montana Mesonet master site file (SQL production copy)
        self.mt_meosnet_feature_class = str(self.connSQLGDB())+ "\\" + "GISMCO.DBO.MesonetSiteInfo"
        # Set variable for child Mesonet table for sensors associated with each site
        self.mt_mesonet_sensor_lineage_table = str(self.connSQLGDB())+ "\\" + "GISMCO.DBO.MesonetSensorLineage"
        # Set variable for child Mesonet table for sensor configurations associated with each site
        self.mt_mesonet_sensor_config_table = str(self.connSQLGDB())+ "\\" + "GISMCO.DBO.MesonetSensorConfiguration"

        # Mesonet Level1 fields
        self.mt_mesonet_fields = ['recordnum','apirecord','apicode','timestamp','localdate','solrad','precipitation','hitnum','hitdist',
                               'winddir','windspeed','windgust','temperature','relhumidity','pressure','sensortiltx','sensortilty',
                               'maxprecip','humiditytemp','soilvwc4','soilvwc8','soilvwc20','soilvwc36','soilvwc0','soilt4','soilt8',
                               'soilt20','soilt36','soilt0','soilec4','soilec8','soilec20','soilec36','soilec0','rrad630','rrad800',
                               'rradorient','rradalpha','irad630','irad800','iradorient','iradalpha','batteryper','batterymv', 
                               'loggerpress','loggertemp']
        # Mesonet Level1 units
        self.mt_mesonet_units = ['n','','','UTC zone','Mtn zone','W/m^2','mm,n','km,deg','m/s','m/s','deg C','ratio','atm kPa','deg',
                              'deg','mm/hr','deg C','m^3/m^3','m^3/m^3','m^3/m^3','m^3/m^3','m^3/m^3','deg C','deg C','deg C','deg C','deg C',
                              'mS/cm','mS/cm','mS/cm','mS/cm','mS/cm','watts/m^2/nm/sr','watts/m^2/nm/sr','n','alpha','watts/m^2/nm',
                              'watts/m^2/nm','n','alpha','%','mv','atm kPa','deg C']
        # Mesonet extract heading list
        self.mt_mesonet_field_list = ['localdate', 'soilvwc4','soilvwc8','soilt4', 'soilt8', 'temperature', 'precipitation']

        # Sites not reporting
        self.mt_mesonet_reject_list = []
        
        # Color Brewer at http://colorbrewer2.org/#type=diverging&scheme=RdBu&n=5
        self.hex_colors = {'redish':'#ca0020', 'pinkish':'#f4a582','whitish':'#f7f7f7','ltbluish':'#92c5de','dkbluish':'#0571b0','blackish':'#A0A0A0'}
        self.rgb_colors = {'redish':'rgb(202,0,32)', 'pinkish':'rgb(244,165,130)','whitish':'rgb(247,247,247)','ltbluish':'rgb(146,197,222)','dkbluish':'rgb(5,113,176)','blackish':'rgb(160,160,160)'}

    def connSQLGDB(self):
        """
            Initializes SQL connection to Mesonet geodatabase object of station installations and configurations
        """
        gdbconn = connSQL.ConnectGDB()
        mcoconn = gdbconn.create_connection()
        return mcoconn

#==========================================================================
# Main and tests
#==========================================================================
if __name__ == "__main__":
    # Test object instantiation
    zentraconfig = ZentraConfig()
    # Print Zentra start date
    print 'Zentra date is: {}-{}-{}'.format(zentraconfig.latest_day.year,zentraconfig.latest_day.month,zentraconfig.latest_day.day)
    # Print Zentra source URL
    print "Zentra source URL is: ", zentraconfig.zentra_api_ip_address
    # Print Zentra local folder
    print "Zentra local folder is: ", zentraconfig.zentra_local_folder
    # Print default number of look-back days (download days to check prior to current date)
    print "Default number of look-back days: ", zentraconfig.lookbackdays
    # Print path to Montana Mesonet site feature class
    print zentraconfig.mt_meosnet_feature_class
#==========================================================================
# END
#==========================================================================
