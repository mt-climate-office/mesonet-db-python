'''
Created on Dec 4, 2017

@author: michael.sweet
'''
import arcpy

#==========================================================================
# Class Definition
#==========================================================================
class ConnectGDB():

    #==========================================================================
    # Methods for object instantiation
    #==========================================================================
    def __init__(self):
        """
        """
        # Set variables
        self.folderName = r"D:\Runtime\ConnectionFiles"
        self.fileName = "Connection_to_CFCSQL17.sde"
        # self.fileName = "Connection_to_gismco.sde"  # for Mike Sweet
        self.databaseName = "GISMCO"
        self.authType = "OPERATING_SYSTEM_AUTH"

    def create_connection(self):
        #Process: Use the CreateArcSDEConnectionFile function
        arcpy.env.overwriteOutput = True

        conn = arcpy.CreateDatabaseConnection_management(out_folder_path=self.folderName, 
                                                         out_name=self.fileName, 
                                                         database_platform="SQL_SERVER", 
                                                         instance="CFCSQL17", 
                                                         account_authentication=self.authType, 
                                                         username="", 
                                                         password="#", 
                                                         save_user_pass="SAVE_USERNAME", 
                                                         database=self.databaseName, 
                                                         schema="", 
                                                         version_type="TRANSACTIONAL", 
                                                         version="dbo.DEFAULT", 
                                                         date="")
        arcpy.env.overwriteOutput = False
        return conn

#==========================================================================
# Main and tests
#==========================================================================

if __name__ == "__main__":
    gdbconn = ConnectGDB()
    mcoconn = gdbconn.create_connection()
    print mcoconn
#==========================================================================
# END
#==========================================================================
