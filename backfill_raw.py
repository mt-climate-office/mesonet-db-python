from os import getenv
from mesonet.connect import connect
from mesonet.zentra import ZentraReadings
from mesonet.write_to_db import write_to_db
from pathlib import Path
import warnings

# import multiprocessing
#
# try:
#     cpus = multiprocessing.cpu_count()
# except NotImplementedError:
#     cpus = 2   # arbitrary default

con = connect(username=getenv("cfcsql_un"),
              password=getenv("cfcsql_pw"))

schema = 'observations'
table = 'raw'

# Start fresh
con.execute("DELETE FROM " + schema + "." + table).close()


def catch(func, handle=lambda e: e, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return handle(e)


def write(x):
    print(x)
    write_to_db(ZentraReadings(json_file=x).prepare_raw(),
                con=con,
                schema="observations",
                table="raw",
                append=True
                )


# pool = multiprocessing.Pool(processes=cpus)
# pool.map(write,
#                list(
#         Path("./tests/data/").glob(
#             '**/*.json')))
# pool.close()

files = Path('//mcofiles.cfc.umt.edu/Resources$/Data/Mesonet/ZentraTest/API-Output/ClimateOffice/Readings').glob(
    '**/*.json')

for file in files:
    try:
        write(x)
    except:
        warnings.warn("Something went wrong! Skipping this file.", RuntimeWarning)
        pass

#
# write_to_db(ZentraReadings(json_file=Path("./tests/data/Readings2018.06.17.json")).prepare_raw(),
#             con=con,
#             schema="observations",
#             table="raw",
#             append=True
#             )
