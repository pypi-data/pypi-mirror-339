import pandas as pd
from datetime import datetime, timedelta
import requests
from requests.auth import HTTPBasicAuth
import urllib3
import json
import matplotlib.pyplot as plt
from lds_pipelines.core.sprt_detector import SPRTLeakDetector
from lds_pipelines.core.csv_processor import calculate_zn_values
import pkg_resources

urllib3.disable_warnings()

class MockAPIGenerator:
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)
        self.df['timestamps'] = pd.to_datetime(self.df['timestamps'])
        self.df = self.df.sort_values('timestamps').reset_index(drop=True)
        self.pointer = 0

    def get_starting_df(self, rows=10):
        self.pointer = rows
        return self.df.iloc[:self.pointer].copy()

    def get_next_df(self, step=1):
        if self.pointer >= len(self.df):
            return pd.DataFrame()

        next_pointer = min(self.pointer + step, len(self.df))
        result = self.df.iloc[self.pointer:next_pointer].copy()
        self.pointer = next_pointer
        return result

mockapi = MockAPIGenerator(pkg_resources.resource_filename('lds_pipelines.core', 'mock_api_data.csv'))#'./src/lds_pipeline/core/mock_api_data.csv')


def login(api_url, api_username, api_password):
    # Define PI Web API server details
    pi_web_api_url = api_url
    username = api_username
    password = api_password
    auth = HTTPBasicAuth(username, password)

    data_archive_name = "delews141odapri"
    pi_point_names = {
        "nqop": "PI-PS-MHANQONQP-DCS-PI2207",
        "nqof": "PI-PS-MHANQONQP-DCS-MUTOIL1FC2_NN3",
        "uranp": "PI-PS-URTTBYT-URN-MUT-21PT6101",
        "uranf": "PI-PS-URTTBYTURN-URN-FI6101"
    }

    web_ids = []
    web_id_data = [
        'F1DP8p7t-9NniEOgPfJJ19IjowaDgEAAREVMRVdTMTQxT0RBUFJJXFBJLVBTLU1IQU5RT05RUC1EQ1MtUEkyMjA3',
        'F1DP8p7t-9NniEOgPfJJ19IjowygEIAAREVMRVdTMTQxT0RBUFJJXFBJLVBTLU1IQU5RT05RUC1EQ1MtTVVUT0lMMUZDMl9OTjM',
        'F1DP8p7t-9NniEOgPfJJ19IjowKAIIAAREVMRVdTMTQxT0RBUFJJXFBJLVBTLVVSVFRCWVQtVVJOLU1VVC0yMVBUNjEwMQ',
        'F1DP8p7t-9NniEOgPfJJ19IjowfAIIAAREVMRVdTMTQxT0RBUFJJXFBJLVBTLVVSVFRCWVRVUk4tVVJOLUZJNjEwMQ',
    ]

now = datetime.now()

timestamps = []
inlet_pressure = []
inlet_volume = []
outlet_pressure = []
outlet_volume = []

def get_starting_df(start_time):
    # for i in range(len(web_ids)):
    #     interpolated_url = f"{pi_web_api_url}/streams/{web_ids[i]}/interpolated"

    #     params = {
    #     "startTime": f"{now}",
    #     "endTime": f"{start_time}",
    #     "interval": "1s",
    #     }

    #     response = requests.get(interpolated_url, auth=HTTPBasicAuth(username, password), params=params, verify=False)
    #     if response.status_code == 200:
    #         data = response.json()
    #         for item in data["Items"]:
    #             if i==0:
    #                 inlet_pressure.append(item["Value"])
    #                 timestamps.append(item["Timestamp"])
    #             if i==1:
    #                 inlet_volume.append(item["Value"])
    #             if i==2:
    #                 outlet_pressure.append(item["Value"])
    #             if i==3:
    #                 outlet_volume.append(item["Value"])
    #     else:
    #         print(f"Error: {response.status_code} - {response.reason}")

    # df = pd.DataFrame(list(zip(timestamps, inlet_pressure, inlet_volume, outlet_pressure, outlet_volume)),
    #                   columns=["timestamps", "inlet_pressure", "inlet_volume", "outlet_pressure", "outlet_volume"])

    df = mockapi.get_starting_df(rows=17000)
    df['timestamps'] = pd.to_datetime(df['timestamps'])
    df = df.sort_values('timestamps').reset_index(drop=True)
    df = calculate_zn_values(df)
    return df

def get_latest_df(df):
    last_timestamp = df['timestamps'].iloc[-1]


    current_timestamp = last_timestamp + timedelta(seconds=30)

    timestamps = df['timestamps'].tolist()
    inlet_volume = df['inlet_volume'].tolist()
    outlet_volume = df['outlet_volume'].tolist()
    new_inlet_pressure = df['inlet_pressure'].tolist()
    outlet_pressure = df['outlet_pressure'].tolist()

    window_sizes = [300, 700, 1100] if len(df) > 300 else [10, 15]
    global_window_factor = 20

    delta_mass = [inlet_volume[i] - outlet_volume[i] for i in range(len(inlet_volume))]

    detectors = {
        w: SPRTLeakDetector(
            window_size=w,
            global_window_factor=global_window_factor,
            data_buffer=delta_mass[-w:],
            filtered_buffer=delta_mass[-w * global_window_factor:],
            mass1_buffer=inlet_volume[-w:],
            mass2_buffer=outlet_volume[-w:]
        ) for w in window_sizes
    }


    # new_timestamps=[]
    # new_inlet_volume=[]
    # new_outlet_volume=[]
    # new_inlet_pressure=[]
    # new_outlet_pressure=[]


    # for i in range(len(web_ids)):
    #     interpolated_url = f"{pi_web_api_url}/streams/{web_ids[i]}/interpolated"

    #     params = {
    #     "startTime": f"{current_timestamp}",
    #     "endTime": f"{last_timestamp}",
    #     "interval": "5s",
    #     }

    #     response = requests.get(interpolated_url, auth=HTTPBasicAuth(username, password), params=params, verify=False)
    #     if response.status_code == 200:
    #         data = response.json()
    #         for item in data["Items"]:
    #             if i==0:
    #                 new_inlet_pressure.append(item["Value"])
    #                 new_timestamps.append(item["Timestamp"])
    #             if i==1:
    #                 new_inlet_volume.append(item["Value"])
    #             if i==2:
    #                 new_outlet_pressure.append(item["Value"])
    #             if i==3:
    #                 new_outlet_volume.append(item["Value"])
    #     else:
    #         print(f"Error: {response.status_code} - {response.reason}")

    # new_df= pd.DataFrame(list(zip(new_timestamps, new_inlet_volume, new_outlet_volume, new_inlet_pressure, new_outlet_pressure)) , columns=['timestamps', 'inlet_volume', 'outlet_volume', 'inlet_pressure', 'outlet_pressure'])
    # new_df = new_df.sort_values(by='timestamps', ascending=True).reset_index(drop=True)


    # for i in range(len(new_df)):
    #     timestamp = new_df['timestamps'].iloc[i]
    #     exists = timestamp in df['timestamps'].values
    #     if exists:
    #         pass
    #     else:
    #         latest_zn_values = {w: 0 for w in window_sizes}
    #         for w in detectors.keys():
    #             latest_zn_values[w] = detectors[w].process_new_data(new_row['inlet_volume'], new_row['outlet_volume'], new_row['timestamps'])
    #         new_row={   
    #                 "timestamps": new_df['timestamps'].iloc[i],
    #                 "inlet_volume": new_df['inlet_volume'].iloc[i],
    #                 "outlet_volume": new_df['outlet_volume'].iloc[i],
    #                 "inlet_pressure": new_df['inlet_pressure'].iloc[i],
    #                 "outlet_pressure": new_df['outlet_pressure'].iloc[i],
    #         }
    #         for w in window_sizes:
    #             new_row[f'zn_{w}']= latest_zn_values[w]
    #         df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            



    result = mockapi.get_next_df()

    if result.empty:
        return df

    
    new_row = {}
    for col in result.columns:
        if col in ['timestamps', 'inlet_volume', 'outlet_volume', 'inlet_pressure', 'outlet_pressure']:
            new_row[col] = result[col].values[0]

    for w in window_sizes:
        new_row[f'zn_{w}'] = None
    new_row['min_zn'] = None

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    latest_zn_values = {w: 0 for w in window_sizes}
    for w in detectors.keys():
        latest_zn_values[w] = detectors[w].process_new_data(new_row['inlet_volume'], new_row['outlet_volume'], new_row['timestamps'], delta_mass_previous=df['inlet_volume'].iloc[-2]-df['outlet_volume'].iloc[-2])

    for w in window_sizes:
        prev = df[f'zn_{w}'].iloc[-2] if len(df) > 1 else 0
        df.at[len(df) - 1, f'zn_{w}'] = prev + latest_zn_values[w]
    
    zn_vals=[]
    for w in window_sizes:
        zn_vals.append(df.loc[len(df) - 1, f'zn_{w}'])
    prev_min_zn = df['min_zn'].iloc[-2] if len(df) > 1 else 0
    df.at[len(df) - 1, 'min_zn'] = min(zn_vals)

    return df

def check_alarm(dataframe, column='min_zn', threshold=7.6):
    count = 0
    max_count = 0

    timestamps= pd.to_datetime(dataframe['timestamps'], utc=True)

    timestamp= None

    if len(dataframe)<300:
        max_counter=10
    else:
        max_counter=720


    for val in range(len(dataframe)):
        if dataframe[column].iloc[val] > threshold:
            count += 1
            max_count = max(max_count, count)
            timestamp= timestamps.iloc[val]
        else:
            count = 0  # reset streak
        if max_count>max_counter:
            return timestamp
        
    return False


if __name__=="__main__":
    pass