import numpy as np
import pandas as pd
from lds_pipelines.core.sprt_detector import SPRTLeakDetector
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def calculate_zn_values(df):
    """Processes the input file and appends Z_n values for each row."""

    window_sizes = [300, 700, 1100] if len(df) > 300 else [10, 15]
    global_window_factor = 20
    
    detectors = {w: SPRTLeakDetector(window_size=w, global_window_factor=global_window_factor) for w in window_sizes}
    
    z_values_dict = {w: [] for w in window_sizes}
    min_Z_n = []

    for i in range(1, len(df), 1):
        intermediate_z_values = []
        for w in window_sizes:
            detectors[w].process_new_data(df.at[i, 'inlet_volume'], df.at[i, 'outlet_volume'], i, calibration_factor= 0, delta_mass_previous= (df.at[i-1, 'inlet_volume']-df.at[i-1, 'outlet_volume']))

        for w, detector in detectors.items():
            _, values = detector.time_stamps, detector.Z_values
            z_values_dict[w].append(values[-1])
            intermediate_z_values.append(values[-1]) 
        min_Z_n.append(min(intermediate_z_values))

    for w in window_sizes:
        df[f'zn_{w}'] = [0] + z_values_dict[w] 
    df['min_zn'] = [0] + min_Z_n 
    
    return df


if __name__ == "__main__":
    pass
