from os import getenv
from mesonet.connect import connect
from mesonet.zentra import ZentraReadings
from mesonet.write_to_db import write_to_db
from pathlib import Path
import warnings

con = connect(username=getenv("cfcsql_un"),
              password=getenv("cfcsql_pw"))

schema = 'observations'
table = 'raw'

# Start fresh
con.execute("DELETE FROM " + schema + "." + table).close()


def write(x):
    print(x)
    write_to_db(ZentraReadings(json_file=x).prepare_raw(),
                con=con,
                schema="observations",
                table="raw",
                append=True
                )


# files = Path('/Volumes/Resources$/Data/Mesonet/ZentraTest/API-Output/ClimateOffice/Readings/blm2virg/2019/').glob(
#     '**/*.json')

files = Path('//mcofiles.cfc.umt.edu/Resources$/Data/Mesonet/ZentraTest/API-Output/ClimateOffice/Readings').glob(
    '**/*.json')

for file in files:
    try:
        write(file)
    except:
        warnings.warn("Something went wrong! Skipping this file.", RuntimeWarning)
        pass
