from os import getenv
from mesonet.connect import connect
from mesonet.zentra import ZentraReadings
from mesonet.write_to_db import write_to_db
from pathlib import Path
import multiprocessing

try:
    cpus = multiprocessing.cpu_count()
except NotImplementedError:
    cpus = 2   # arbitrary default

con = connect(username=getenv("cfcsql_un"),
              password=getenv("cfcsql_pw"))

schema = 'observations'
table = 'raw'

# Start fresh
con.execute("DELETE FROM " + schema + "." + table).close()

def write(x):
    write_to_db(ZentraReadings(json_file=x).prepare_raw(),
                con=con,
                schema="observations",
                table="raw",
                append=True
                )

pool = multiprocessing.Pool(processes=cpus)
pool.map(write,
               list(
        Path("./tests/data/").glob(
            '**/*.json')))
pool.close()

[
    write(x)
    for x
    in list(
        Path('//mcofiles.cfc.umt.edu/Resources$/Data/Mesonet/ZentraTest/API-Output/ClimateOffice/Readings').glob(
            '**/*.json'))
    # in list(
    #     Path('./tests/data/').glob(
    #         '**/*.json'))
]

import datetime
datetime.dt.tz_localize()

test = ZentraReadings(json_file=Path("./tests/data/Readings2017.11.05.json")) \
    .timeseries[0] \
    .values \
    .sort_values(by=['port', 'description', 'mrid']) \
    .groupby(by=['port', 'description'])

test = [test.get_group(x) for x in test.groups]

[x.assign(datetime=x.datetime.dt.tz_localize("America/Denver", ambiguous='infer')) for x in test]


test.groupby(by=['port','description'])['datetime'].apply(lambda x: x.dt.tz_localize("America/Denver", ambiguous='infer'))

[gb.get_group(x) for x in gb.groups]

test\
    .sort_values(by=['port','description','mrid'])\
    .groupby(by=['port','description'])\
    .assign(datetime=test.dt.tz_localize("America/Denver", ambiguous='infer'))

write_to_db(ZentraReadings(json_file=Path("./tests/data/Readings2017.11.05.json")).prepare_raw(),
            con=con,
            schema="observations",
            table="raw",
            append=True
            )
