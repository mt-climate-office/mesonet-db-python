from os import getenv
from mesonet.connect import connect
from mesonet.zentra import ZentraReadings
from mesonet.write_to_db import write_to_db
from pathlib import Path

con = connect(username=getenv("cfcsql_un"),
              password=getenv("cfcsql_pw"))

schema = 'observations'
table = 'raw'

# Start fresh
con.execute("DELETE FROM " + schema + "." + table).close()

[
    write_to_db(ZentraReadings(json_file=x).prepare_raw(),
                con=con,
                schema="observations",
                table="raw",
                append=True
                )
    for x
    in list(
        Path('//mcofiles.cfc.umt.edu/Resources$/Data/Mesonet/ZentraTest/API-Output/ClimateOffice/Readings').glob(
            '**/*.json'))
]

# write_to_db(ZentraReadings(json_file=Path("./tests/data/Readings2019.03.25.json")).prepare_raw(),
#             con=con,
#             schema="observations",
#             table="raw",
#             append=True
#             )