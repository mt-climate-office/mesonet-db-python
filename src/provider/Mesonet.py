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
import util.config as config
import arcpy
import collections
#==========================================================================
# Class Definition
#==========================================================================
class MesonetStations():
    
    '''
    Description: 
        Configuration file for downloading Zentra data from
        https://zentracloud.com and writing to local path
        \\mcofiles\Resources$\Data\Mesonet
        
        Load using:
            import provider.MesonetStations
    '''

    #==========================================================================
    # Methods for object instantiation
    #==========================================================================
    def __init__(self):
        """
            Initializes properties for Zentra download configuration object
            INPUT: Instantiates config.py class containing configuration parameters
                    Class ZentraDownloadConfig() instantiates util\config.ZentraConfig()
        """
        # Load configuration settings as Zentra object
        self.zentraconfig = config.ZentraConfig()
        # Create a table view for the feature table containing active sites
        self.siteview = self.create_tableview_for_active_sites(self.zentraconfig.mt_meosnet_feature_class)
        # Create a search cursor in for table view of active sites
        self.sitecursor = self.create_searchcursor_for_site_table(self.siteview)
        # Create a dictionary of all active sites, with a tuple as the value
        # The tuple is a collection that contains name-value pairs for station attributes
        self.stationdict = self.build_dictionary_for_stations(self.sitecursor)
        # Create sorted list of keys based on display name
        self.stationkeys = self.create_list_of_sorted_keys_from_dictionary(self.stationdict)
        # Create a dictionary for sensors from feature class sensor table
        self.sensordict = self.build_dictionary_for_sensors(self.stationkeys,self.stationdict,self.zentraconfig.mt_mesonet_sensor_lineage_table)
        # Create a dictionary for abandoned sensors from feature class sensor table
        self.abandoned_sensordict = self.build_dictionary_for_abandoned(self.stationkeys,self.stationdict,self.zentraconfig.mt_mesonet_sensor_lineage_table)
        # Create a dictionary for abandoned sensors from feature class sensor table
        self.sensor_config_dict, self.port_list = self.build_dictionary_for_sensorconfig(self.stationkeys,self.zentraconfig.mt_mesonet_sensor_config_table)

    def create_tableview_for_active_sites(self,sitetable):
        self.siteview = arcpy.MakeTableView_management(sitetable,"#", \
                                                  """"Reporting_status" = 'yes'""")
        return self.siteview
    
    def create_searchcursor_for_site_table(self,siteview):
        self.sitecursor = arcpy.SearchCursor(siteview,
                                        fields="Primary_key; Active_status; Reporting_status; \
                                        MesoWest; Display_name", 
                                        sort_fields="Display_name A")
        return self.sitecursor

    def build_dictionary_for_stations(self,sitecursor):
        # To access the value of an entry in this dictionary use the following form:
        # stationDict[mesonetPrimaryKey].displayName
        stationtuple = collections.namedtuple('Station','activeStatus reportingStatus mesoWest displayName')
        self.stationdict = {}
        for site in sitecursor:
            mesonetprimarykey =  site.getValue("Primary_key")
            self.stationdict[mesonetprimarykey] = stationtuple(activeStatus = site.getValue("Active_status"),\
                                                   reportingStatus = site.getValue("Reporting_status"), \
                                                   mesoWest = site.getValue("MesoWest"), \
                                                   displayName = site.getValue("Display_name"))
        return self.stationdict

    def create_list_of_sorted_keys_from_dictionary(self,stationDict):
        # create sorted list of keys in dictionary
        # k represents the keys, and v represents the tuple
        # [3] is the forth element in the tuple which is the display name
        sorted_dict = sorted(stationDict.iteritems(), key=lambda (k,v): v[3])
        self.stationkeys = [i[0] for i in sorted_dict]
        return self.stationkeys

    def build_dictionary_for_sensors(self,stationkeys,stationdict,sensorlineage):
        # To access the value of an entry in this dictionary use the following form:
        # stationdict[mesonetPrimaryKey].displayName
        sensortuple = collections.namedtuple('Sensor', 'loggerUserName loggerPassword loggerLocalDate displayName')
        self.sensordict = {}
        for station in stationkeys:
            # Search cursor for table view finding latest active record
            # Note: return email error message if more than one record
            sensorview = self.create_tableview_for_sensors(station,sensorlineage)
            # Create a search cursor in for table view of active sites
            self.sensorcursor = self.create_searchcursor_for_sensor_table(sensorview)
            for sensor in self.sensorcursor:
                self.sensordict[station] = sensortuple(loggerUserName = sensor.getValue("Logger_username"), \
                                                  loggerPassword = sensor.getValue("Logger_password"), \
                                                  loggerLocalDate = sensor.getValue("Record_start_local_date"), \
                                                  displayName = stationdict[station].displayName)
            # Delete this table view
            arcpy.Delete_management("sensorview")
        return self.sensordict

    def create_tableview_for_sensors(self,station,sensortable):
        # Where clause for child table query
        whereClause = 'Primary_key = ' + "'" + station + "'" + " AND Station_state = 'active'"
        # Create table view from query of child table
        self.sensorview = arcpy.MakeTableView_management(sensortable,"#",whereClause)
        return self.sensorview

    def build_dictionary_for_abandoned(self,stationkeys,stationdict,sensorlineage):
        # To access the value of an entry in this dictionary use the following form:
        # stationdict[mesonetPrimaryKey].displayName
        sensortuple = collections.namedtuple('Sensor', \
                                        'loggerUserName loggerPassword \
                                         loggerLocalDate, displayName')
        self.abandoned_sensordict = {}
        for station in stationkeys:
            # Search cursor for table view finding latest active record
            # Note: return email error message if more than one record
            sensorview = self.create_tableview_for_abandoned(station,sensorlineage)
            # Create a search cursor in for table view of active sites
            self.abandoned_sensorcursor = self.create_searchcursor_for_sensor_table(sensorview)
            for sensor in self.abandoned_sensorcursor:
                self.abandoned_sensordict[station] = sensortuple(loggerUserName = sensor.getValue("Logger_username"), \
                                                  loggerPassword = sensor.getValue("Logger_password"), \
                                                  loggerLocalDate = sensor.getValue("Record_start_local_date"), \
                                                  displayName = stationdict[station].displayName)
            # Delete this table view
            arcpy.Delete_management("sensorview")
        return self.abandoned_sensordict

    def create_tableview_for_abandoned(self,station,sensortable):
        # Where clause for child table query
        whereClause = 'Primary_key = ' + "'" + station + "'" + " AND Station_state = 'abandoned'"
        # Create table view from query of child table
        self.sensorview = arcpy.MakeTableView_management(sensortable,"#",whereClause)
        return self.sensorview

    def create_searchcursor_for_sensor_table(self,sensorview):
        self.sensorcursor = None
        self.sensorcursor = arcpy.SearchCursor(sensorview, 
                                          fields="Logger_username; Logger_password; Record_start_local_date", 
                                        sort_fields="Logger_username D")
        return self.sensorcursor

    def create_searchcursor_for_sensor_config(self,sensorview):
        self.configsearchcursor = None
        self.configsearchcursor = arcpy.SearchCursor(sensorview, 
                                          fields="Primary_key; Sensor_key; Sensor_port; Sensor_depth, Surface_type, Start_date, End_date", 
                                        sort_fields="Primary_key A; Sensor_port A")
        return self.configsearchcursor

    def create_tableview_for_sensorconfig(self,station,sensorconfigtable):
        # Where clause for child table query
        whereClause = 'Primary_key = ' + "'" + station + "'"
        # Create table view from query of child table
        self.sensorview = arcpy.MakeTableView_management(sensorconfigtable,"#",whereClause)
        return self.sensorview

    def build_dictionary_for_sensorconfig(self,stationkeys,sensorconfigtable):
        # To access the value of an entry in this dictionary use the following form:
        # self.sensor_config_dict[mesonetPrimaryKey].displayName
        sensortuple = collections.namedtuple('Sensor', \
                                        'sensorKey portNumber sensorDepth surfaceType \
                                         localStartDate, localEndDate')
        self.sensor_config_dict = {}
        self.port_list = []
        for station in stationkeys:
            sensorview = self.create_tableview_for_sensorconfig(station,sensorconfigtable)
            # Create a search cursor in for table view of active sites
            self.configsearchcursor = self.create_searchcursor_for_sensor_config(sensorview)
            configcount = 0
            for sensor in self.configsearchcursor:
                dict_key = station+'{:0>2d}'.format(sensor.getValue("Sensor_port"))+'{:0>1d}'.format(configcount)
                # If configuration exists then increment configuration count by 1
                if self.sensor_config_dict.has_key(dict_key):
                    configcount = configcount + 1
                    dict_key = station+'{:0>2d}'.format(sensor.getValue("Sensor_port"))+'{:0>1d}'.format(configcount)
                self.sensor_config_dict[dict_key] = \
                                                   sensortuple(sensorKey = sensor.getValue("Sensor_key"), \
                                                   portNumber = sensor.getValue("Sensor_port"), \
                                                   sensorDepth = sensor.getValue("Sensor_depth"), \
                                                   surfaceType = sensor.getValue("Surface_type"), \
                                                   localStartDate = sensor.getValue("Start_date"), \
                                                   localEndDate = sensor.getValue("End_date"))
                if sensor.getValue("Sensor_port") not in self.port_list:
                    self.port_list.append(sensor.getValue("Sensor_port"))
            # Delete this table view
            arcpy.Delete_management("sensorview")
        return (self.sensor_config_dict, self.port_list)

#==========================================================================
# Main and tests
#==========================================================================
if __name__ == "__main__":
    # Test object instantiation
    mesonet = MesonetStations()
    print type(mesonet.siteview)
    print type(mesonet.sitecursor)
    print type(mesonet.stationdict)
    for keys,values in mesonet.stationdict.items():
        print(keys)
        print(values)
    print type(mesonet.stationkeys)
    print mesonet.stationkeys
    print type(mesonet.sensordict)
    print len(mesonet.sensordict)
    """
    for keys,values in mesonet.sensordict.items():
        print(keys)
        print(values)
    """
    print type(mesonet.abandoned_sensordict)
    print len(mesonet.abandoned_sensordict)
    """
    for keys,values in mesonet.all_sensordict.items():
        print(keys)
        print(values)
    """
    print type(mesonet.sensor_config_dict)
    print len(mesonet.sensor_config_dict)
    print mesonet.sensor_config_dict['lubrecht050']
    print mesonet.sensor_config_dict['lubrecht051']
    print mesonet.port_list
#==========================================================================
# END
#==========================================================================
