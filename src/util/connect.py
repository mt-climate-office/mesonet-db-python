"""Connect to the Montana Mesonet database

This module uses sqlalchemy to connect to the MT Mesonet database via
a username and password, and to create an optimized engine for the connection.

This script requires that `sqlalchemy` be installed within the Python
environment you are running this script in.

"""

import sqlalchemy
from sqlalchemy.engine import url


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
    return sqlalchemy.create_engine(url.URL(drivername="mssql+pyodbc",
                                            username=username,
                                            password=password,
                                            host='MCOMesonet'),
                                    fast_executemany=True)
