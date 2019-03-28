"""Connect to the Montana Mesonet database

This module uses sqlalchemy to connect to the MT Mesonet database via
a username and password, and to create an optimized engine for the connection.

This script requires that `sqlalchemy` be installed within the Python
environment you are running this script in.

"""

import sqlalchemy
import urllib


def connect(username=None, password=None):
    """
    Gets a user token using a POST request to the Zentra API.
    Wraps build and parse functions.

    Parameters
    ----------
    username : str
        The username
    password : str
        The password

    """

    server = "cfcsql17.gs.umt.edu"
    database = 'MCOMesonet'

    params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +
                                     ';DATABASE=' + database +
                                     ';UID=' + username +
                                     ';PWD=' + password)

    return sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params,
                                    fast_executemany=True)
