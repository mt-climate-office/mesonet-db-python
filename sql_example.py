import pymssql
import pandas as pd
from os import getenv

conn = pymssql.connect(server='cfcsql17.gs.umt.edu',
                       user=getenv("cfcsql_un"),
                       password=getenv("cfcsql_pw"),
                       database="MCOMesonet")

query = "SELECT [station], [Local Date] FROM mesonet_records WHERE station IN ('arskeogh', 'bentlake')"

# query = "SELECT TOP 10 * FROM mesonet_records"

# query = "Select name AS TableName, object_id AS ObjectID From sys.tables where name = 'mesonet_records'"


pd.read_sql(sql=query,
            con=conn).columns
