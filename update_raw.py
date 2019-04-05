from os import getenv
from zentra.api import *
from mesonet.connect import connect
from mesonet.zentra import ZentraReadings
from mesonet.write_to_db import write_to_db
import pandas as pd
import warnings

con = connect(username=getenv("cfcsql_un"),
              password=getenv("cfcsql_pw"))

token = ZentraToken(username=getenv("zentra_un"),
                    password=getenv("zentra_pw"))

stations = pd.read_sql(
    sql=" \
        SELECT x.logger_sn, y.mrid \
        FROM \
        ( \
            SELECT logger_sn \
            FROM private_data.stations AS stations \
            JOIN public_data.logger_deployment AS loggers \
                ON (stations.station_key = loggers.station_key) \
                AND loggers.date_end IS NULL AND stations.data_transfer='automated' \
        ) AS x \
        LEFT JOIN \
        ( \
            SELECT logger_sn, max(mrid) AS mrid \
            FROM observations.raw \
            GROUP BY logger_sn \
        ) y \
            ON (x.logger_sn = y.logger_sn) \
    ",
    con=con).fillna(0).to_dict('records')

# test = ZentraStatus(token=token,
#              sn='06-01827')
#
# test = ZentraReadings(token=token,
#                       sn=stations[0]['logger_sn'],
#                       start_mrid=stations[0]['mrid'] + 1)
#
# write_to_db(test.prepare_raw(),
#             con=con,
#             schema="observations",
#             table="raw",
#             append=True
#             )

def write(logger, mrid):
    print(logger)

    data = ZentraReadings(token=token,
                          sn=logger,
                          start_mrid=np.int(mrid))

    if len(data.timeseries) == 0:
        return None

    write_to_db(data.prepare_raw(),
                con=con,
                schema="observations",
                table="raw",
                append=True
                )

# station = stations[1]

for station in stations:
    try:
        write(logger=station['logger_sn'],
              mrid=station['mrid'] + 1)
    except:
        warnings.warn("Something went wrong! Skipping this file.", RuntimeWarning)
        pass
