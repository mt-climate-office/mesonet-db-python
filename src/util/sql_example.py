import pymssql
import datetime
import pandas as pd
from dfply import *
from os import getenv
from zentra.api import *
from datetime import datetime, timedelta

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

conn = pymssql.connect(server='cfcsql17.gs.umt.edu',
                       user=getenv("cfcsql_un"),
                       password=getenv("cfcsql_pw"),
                       database="MCOMesonet")

query = "SELECT [station], [Local Date] FROM mesonet_records WHERE station IN ('arskeogh', 'bentlake')"

# query = "SELECT TOP 10 * FROM mesonet_records"

# query = "Select name AS TableName, object_id AS ObjectID From sys.tables where name = 'mesonet_records'"

query = 'SELECT MAX ([Local Date]) AS Date FROM mesonet_records'

pd.read_sql(sql=query,
            con=conn).columns

pd.read_sql(sql="SELECT * FROM MESONETSENSORLINEAGE ORDER BY Primary_key ASC, Record_start_local_date DESC",
            con=conn)

# token = zentra.api. \
#     get_token(user=getenv("zentra_un"),
#               password=getenv("zentra_pw"))

# token = getenv("zentra_token")

token = ZentraToken(username=getenv("zentra_un"),
                    password=getenv("zentra_pw"))

# token = ZentraToken(token=getenv("zentra_token"))

settings = ZentraSettings(sn="06-00331",
                          token=token)

status = ZentraStatus(sn="06-00331",
                      token=token)

readings = ZentraReadings(sn="06-00761",
                          token=token,
# start_mrid=25876,
                          start_time=int((datetime.today() - timedelta(1)).timestamp())
                          ).timeseries[0].values

stations = ["06-00187", "06-00761", "06-02072"]

test = list(map(lambda x: ZentraReadings(station=x,
                                         token=token,
                                         start_mrid=25876,
                                         #start_time=int(datetime.datetime(year=2018,
                                                                          #month=12,
                                                                          #day=31).timestamp())),
                                         ),
                stations))

# all_readings = ZentraReadings(station="06-00761",
#                           token=token,
#                               start_mrid=1)
