import pymssql
import datetime
import pandas as pd
from dfply import *
from os import getenv
import zentra.api
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

conn = pymssql.connect(server='cfcsql17.gs.umt.edu',
                       user=getenv("cfcsql_un"),
                       password=getenv("cfcsql_pw"),
                       database="MCOMesonet")

query = "SELECT [station], [Local Date] FROM mesonet_records WHERE station IN ('arskeogh', 'bentlake')"

# query = "SELECT TOP 10 * FROM mesonet_records"

# query = "Select name AS TableName, object_id AS ObjectID From sys.tables where name = 'mesonet_records'"

query = 'SELECT MAX (Local Date) AS Date FROM mesonet_records'

pd.read_sql(sql=query,
            con=conn).columns

pd.read_sql(sql="SELECT * FROM MESONETSENSORLINEAGE ORDER BY Primary_key ASC, Record_start_local_date DESC",
            con=conn)


# token = zentra.api. \
#     get_token(user=getenv("zentra_un"),
#               password=getenv("zentra_pw"))

token = getenv("zentra_token")

settings = zentra.api. \
    get_station_settings(station="06-00187",
                         token=token)
# Parsing Device Settings
settings['get_settings_ver']
settings['created']
settings['device']['device_info']
pd.DataFrame(settings['device']['measurement_settings'])
pd.DataFrame(settings['device']['time_settings'])
pd.DataFrame(settings['device']['locations'])
settings['device']['installation_metadata'] = settings['device']['installation_metadata'][0]
pd.DataFrame(settings['device']['installation_metadata']['sensor_elevations'])
settings['device']['installation_metadata']['node_elevation_mm']
settings['device']['installation_metadata']['site_name']
settings['device']['installation_metadata']['valid_since']
settings['device']['installation_metadata']['device_name']


status = zentra.api. \
    get_station_status(station="06-00187",
                       token=token)

# parsing Device Status
status['get_status_ver']
status['created']
status['device']['cellular_error_counters']
status['device']['device_info']
status['device']['device_error_counters']['sensor_errors'] = pd.DataFrame(status['device']['device_error_counters']['sensor_errors'])
status['device']['device_error_counters']
pd.DataFrame(status['device']['cellular_statuses'])

readings = zentra.api. \
    get_station_readings(station="06-00187",
                         token=token,
                         start_time=int(datetime.datetime(year=2018, month=12, day=1).timestamp()))

# Parsing Device Readings
readings['get_readings_ver']
readings['created']
readings['device']['device_info']
readings['device']['timeseries'] = dict(readings['device']['timeseries'][0])
pd.DataFrame(readings['device']['timeseries']['configuration']['sensors'])
pd.DataFrame(readings['device']['timeseries']['configuration']['values'])[3].map(pd.DataFrame)

pd.DataFrame(readings['device']['timeseries']['configuration']['values'])[3]


vals = pd.DataFrame(readings['device']['timeseries']['configuration']['values'])

(vals >> mutate([3] = X[3].map(pd.DataFrame)))


vals[0] = datetime.datetime(int(list(vals[0])))
vals[3] = vals[3].map(pd.DataFrame)
vals.assign(`3` = )



pd.DataFrame(readings['device']['timeseries']['configuration']['values'])[3].map(pd.DataFrame)
readings['device']['timeseries']['configuration']['valid_since']
readings.keys()

