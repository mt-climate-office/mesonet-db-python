#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests

def get_token(user, password):
    return requests.post("https://zentracloud.com/api/v1/tokens",
                         data={'username': user,
                               'password': password}). \
        json(). \
        get("token")


def get_station_settings(station, token, start_time=None, end_time=None):
    return requests.get("https://zentracloud.com/api/v1/settings",
                        headers={'Authorization': "Token " + token},
                        params={'sn': station,
                                'start_time': start_time,
                                'end_time': end_time}).\
        json()

# # Parsing Device Settings
# settings['get_settings_ver']
# settings['created']
# settings['device']['device_info']
# pd.DataFrame(settings['device']['measurement_settings'])
# pd.DataFrame(settings['device']['time_settings'])
# pd.DataFrame(settings['device']['locations'])
# settings['device']['installation_metadata'] = settings['device']['installation_metadata'][0]
# pd.DataFrame(settings['device']['installation_metadata']['sensor_elevations'])
# settings['device']['installation_metadata']['node_elevation_mm']
# settings['device']['installation_metadata']['site_name']
# settings['device']['installation_metadata']['valid_since']
# settings['device']['installation_metadata']['device_name']

def get_station_status(station, token, start_time=None, end_time=None):
    return requests.get("https://zentracloud.com/api/v1/statuses",
                        headers={'Authorization': "Token " + token},
                        params={'sn': station,
                                'start_time': start_time,
                                'end_time': end_time}).\
        json()

# # parsing Device Status
# status['get_settings_ver']
# status['created']
# status['device']['cellular_error_counters']
# status['device']['device_info']
# status['device']['device_error_counters']['sensor_errors'] = pd.DataFrame(status['device']['device_error_counters']['sensor_errors'])
# status['device']['device_error_counters']
# pd.DataFrame(status['device']['cellular_statuses'])

def get_station_readings(station, token, start_time=None, start_mrid=None):

    return requests.get("https://zentracloud.com/api/v1/readings",
                        headers={'Authorization': "Token " + token},
                        params={'sn': station,
                                'start_time': start_time,
                                'start_mrid': start_mrid}).\
        json()
