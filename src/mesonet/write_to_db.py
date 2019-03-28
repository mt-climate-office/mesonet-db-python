"""Write a Pandas dataframe to the Mesonet database

"""

import numpy as np
import warnings


def write_to_db(x, table, schema, con, append=True):
    """
    Gets a user token using a POST request to the Zentra API.
    Wraps build and parse functions.

    Parameters
    ----------
    x :
        A pandas data frame
    table : str
        The table name
    schema : str
        The schema name
    con : sqlalchemy.Engine
        A sqlalchemy Engine object
    append : bool, optional
        Append records to table?
    verbose : bool, optional
        Report what's going on?

    """

    if not append:
        # Delete all rows
        warnings.warn("append=False! Deleting all records from " + schema + "." + table, RuntimeWarning)
        con.execute("DELETE FROM " + schema + "." + table)


    start_count = con.execute("SELECT COUNT(*) FROM " + schema + "." + table).fetchall()[0][0]

    x \
        .replace('NA', np.nan) \
        .to_sql(con=con,
                name=table,
                schema=schema,
                if_exists='append',
                chunksize=np.int(np.floor((2000 / len(x.columns)))),
                index=False,
                method='multi')

    end_count = con.execute("SELECT COUNT(*) FROM " + schema + "." + table).fetchall()[0][0]

    rows_added = end_count - start_count

    if rows_added < len(x.index):
        warnings.warn("Fewer rows added than in input data frame!\n" +
                      'Input rows: ' + str(len(x.index)) + "\n" +
                      'Rows added: ' + str(rows_added),
                      RuntimeWarning)

