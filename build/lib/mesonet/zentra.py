"""Functions to interact with the Zenta API.

"""
import zentra.api as zentra
import pandas as pd


def get_readings_since_last_mrid(station_key, token, mesonet_db_con, start_mrid=None):
    """
    Gets a the Zentra readings for a Mesonet station since a given
    mrid, or else since the last downloaded mrid for that station in
    the Mesonet database.

    Parameters
    ----------
    station_key : str
        The unique identifier for a station
    token : ZentraToken
        A valid ZentraToken object
    mesonet_db_con : Engine
        A sqlalchemy Engine object, as created by mesonet.connect.connect()
    start_mrid : int, optional
        Return readings with mrid ≥ start_mrid.
    """

    logger_sn = pd.read_sql(sql=("SELECT logger_sn " +
                                 "FROM public_data.logger_deployment " +
                                 "WHERE station_key='" + station_key + "'"),
                            con=mesonet_db_con)['logger_sn'].tolist()[0]

    if start_mrid is None:
        start_mrid = pd.read_sql(sql=("SELECT MAX(mrid) " +
                                      "FROM observations.raw " +
                                      "WHERE logger_sn='" + logger_sn + "'"),
                                 con=mesonet_db_con)['mrid'].tolist()[0] + 1

    return ZentraReadings(sn=logger_sn,
                          token=token,
                          start_mrid=start_mrid,
                          )


class ZentraReadings(zentra.ZentraReadings):
    def prepare_raw(self):
        out = [x
                   .values
                   .rename({'description': 'measurement'},
                           axis='columns')
                   .assign(timeseries=i,
                           logger_sn=self.device_info['device_sn'])[['logger_sn',
                                                                     'timeseries',
                                                                     'mrid',
                                                                     'datetime',
                                                                     'port',
                                                                     'measurement',
                                                                     'units',
                                                                     'value']]
               for i, x
               in enumerate(self.timeseries)]
        out = pd.concat(out)

        return (out
                .assign(timeseries=out.timeseries.astype('uint8'),
                        datetime=out.datetime.dt.tz_localize("America/Denver",
                                                             ambiguous='infer'),
                        port=out.port.astype('uint8'),
                        mrid=out.mrid.astype('uint32'),
                        units=out.units.str.strip(),
                        measurement=out.measurement.str.strip(),
                        value=out.value.astype('float').round(5))
                .drop_duplicates()
                .dropna()
                .sort_values(['logger_sn',
                              'timeseries',
                              'mrid',
                              'datetime',
                              'port',
                              'measurement']))

    def prepare_level_0(self):
        return self.prepare_raw()

    def prepare_level_1(self):
        return self.prepare_raw()

    def prepare_level_2(self):
        return self.prepare_raw()

    def prepare(self):
        return self.prepare_raw()
