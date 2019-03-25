"""Functions to interact with the Zenta API.

"""
import zentra.api as zentra


def get_readings_since_last_mrid(station_key, token, mesonet_db_con, start_mrid=None):
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
        return self.timeseries[0].values

    def prepare_level_0(self):
        return self.prepare_raw()

    def prepare_level_1(self):
        return self.prepare_raw()

    def prepare_level_2(self):
        return self.prepare_raw()

    def prepare(self):
        return self.prepare_raw()



ZentraReadings(json_file = "/Volumes/Resources$/Data/Mesonet/ZentraTest/API-Output/ClimateOffice/Readings/arskeogh/2019/Readings2019.03.25.json").prepare()


get_readings_since_last_mrid(station_key="arskeogh",
                             token=token,
                             mesonet_db_con=con,
                             start_mrid=30607).prepare()
