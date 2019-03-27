"""Connect to the Montana Mesonet database

This module uses sqlalchemy to connect to the MT Mesonet database via
a username and password, and to create an optimized engine for the connection.

This script requires that `sqlalchemy` be installed within the Python
environment you are running this script in.

"""

from mesonet.connect import connect
from zentra.api import *
# import mesonet.zentra
import src.mesonet.zentra
import pandas as pd
from dfply import *
from os import getenv
from pandas import Timestamp

from datetime import datetime, timedelta

con = connect(username=getenv("cfcsql_un"),
              password=getenv("cfcsql_pw"))

test = con.execute("SELECT logger_sn \
FROM public_data.logger_deployment \
WHERE station_key='arskeogh'").fetchall()

query = "SELECT logger_sn \
FROM public_data.logger_deployment \
WHERE station_key='arskeogh'"

pd.read_sql(sql=query,
            con=con)['logger_sn'].tolist()

pd.read_sql_table(table_name="logger_deployment",
                  schema="public_data",
                  con=con).columns

pd.read_sql(sql="SELECT logger_sn, station_key FROM public_data.logger_deployment",
            con=con)

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

stations = pd.read_sql(sql="SELECT logger_sn FROM private_data.stations \
JOIN public_data.logger_deployment \
ON (private_data.stations.station_key = public_data.logger_deployment.station_key) \
WHERE date_end IS NULL AND data_transfer='automated'",
                       con=con)["logger_sn"].tolist()

for x in stations:
    print(x)
    ZentraReadings(sn=x,
                   token=token,
                   start_time=int((datetime.today() - timedelta(hours=3)).timestamp())
                   ).timeseries[0].values

test = list(
    map(lambda x:
        ZentraReadings(sn=x,
                       token=token,
                       start_time=int((datetime.today() - timedelta(1)).timestamp())
                       ).timeseries[0].values,
        stations)
)

# all_readings = ZentraReadings(station="06-00761",
#                           token=token,
#                               start_mrid=1)

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 500)

test = src.mesonet.zentra.ZentraReadings(json_file="./tests/data/Readings2019.03.25.json")

test_out = test.prepare_raw()

# Delete all rows
con.execute("DELETE FROM observations.raw")



test_out.replace('NA', np.nan).to_sql(con=con,
                                      name="raw",
                                      schema="observations",
                                      if_exists='append',
                                      chunksize=np.int(np.floor((2000 / len(test_out.columns)))),
                                      index=False,
                                      method='multi')

pd.read_sql_table(con=con,
                                      table_name="raw",
                                      schema="observations")


test_out.

test_out.value

src.mesonet.zentra.get_readings_since_last_mrid(station_key="arskeogh",
                                                token=token,
                                                mesonet_db_con=con,
                                                start_mrid=30607).prepare_raw()
