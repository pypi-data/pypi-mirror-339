import numpy as np
import pandas as pd
import collections
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class SPRTLeakDetector:
    def __init__(self, window_size, global_window_factor=20, alpha=0.0005, beta=0.0005, decay_factor=0.999, data_buffer=None, filtered_buffer=None, mass1_buffer= None, mass2_buffer= None, calibration= False):
        self.window_size = window_size
        self.global_window_factor = global_window_factor
        self.alpha = alpha
        self.beta = beta
        self.decay_factor = decay_factor
        self.calibration= calibration

        self.A = np.log((1 - beta) / alpha) 
        self.B = np.log(beta / (1 - alpha))  

        if not data_buffer:
            self.mass1= collections.deque(maxlen=window_size)
        else:
            self.mass1= collections.deque(mass1_buffer, maxlen=window_size)
        if not data_buffer:
            self.mass2= collections.deque(maxlen=window_size)
        else:
            self.mass2= collections.deque(mass2_buffer, maxlen=window_size)

        if not data_buffer:
            self.data_buffer = collections.deque(maxlen=window_size)
        else:
            self.data_buffer = collections.deque(data_buffer, maxlen=window_size)
        
        if not filtered_buffer:
            self.filtered_buffer = collections.deque(maxlen=window_size*global_window_factor)  #list(np.zeros(1000))
        else:
            self.filtered_buffer = collections.deque(filtered_buffer, maxlen=window_size*global_window_factor)

        self.mass1_last = None
        self.mass2_last = None
        self.Z_n = 0
        self.previous_leak = False
        
        self.Z_values = []
        self.time_stamps = []
    
    def calculate_autocorrelation(self, data):
        try:
            if len(data) < 2:
                return 0
            
            data= data
            x_t = data[:-1]
            x_t1 = data[1:]

            if np.std(x_t)!=0 and np.std(x_t1)!=0:
                R_xx = np.corrcoef(x_t, x_t1)[0, 1]
                return (R_xx+1)/2
            else:
                return -1
        except:
            return -1
    
    def update_rolling_stats(self):
        global_window = self.window_size * self.global_window_factor

        filtered_array = np.array(self.filtered_buffer) if len(self.filtered_buffer) > 0 else np.array([0])
        mean_global = np.mean(filtered_array)
        std_global = np.std(filtered_array) 

        data_array = np.array(self.data_buffer) if len(self.data_buffer) > 0 else np.array([0])
        mean_window = np.mean(data_array)

        return mean_global, std_global, mean_window

    def process_new_data(self, mass1, mass2, timestamp, calibration_factor=0, delta_mass_previous=0):
        mass1 = mass1 if not pd.isna(mass1) else self.mass1_last
        mass2 = mass2 if not pd.isna(mass2) else self.mass2_last

        self.mass1.append(mass1)
        self.mass2.append(mass2)

        self.mass1_last, self.mass2_last = mass1, mass2
        
        delta_mass = mass1 - mass2
        
        self.data_buffer.append(delta_mass)
        
        if self.previous_leak==0:
            self.filtered_buffer.append(delta_mass)
        
        mu_0, sigma_0, mu_1 = self.update_rolling_stats()
        sigma_0 = sigma_0 if sigma_0 != 0 else 1e-5
        

        if len(self.filtered_buffer) >= self.window_size:
            R1 = self.calculate_autocorrelation(list(self.mass1)[-int(len(self.mass1)):])#-int(len(self.data_buffer)/10):])
            R2 = self.calculate_autocorrelation(list(self.mass2)[-int(len(self.mass2)):])
            if R1!=-1 and R2!=-1:
                R = (R1 + R2)/2
            elif R1!=-1:
                R=R1/2
            elif R2!=-1:
                R=R2/2
            else:
                R=0

            delta_mu = mu_1 - mu_0

            new_Z_n = (delta_mu / sigma_0**2/ (1+R)) * (delta_mass - R*delta_mass_previous -(1-R)*(mu_0 + 0.5 * delta_mu))
        else:
            new_Z_n = 0
        
        if self.previous_leak:
            self.Z_n = self.Z_n + new_Z_n
        else:
            if self.Z_n>0 and new_Z_n>0:
                self.Z_n = self.decay_factor * self.Z_n + new_Z_n
            else:
                self.Z_n = self.Z_n + new_Z_n
        if self.calibration==False:
            leak_detected = self.Z_n > self.A
        else:
            leak_detected= 0
        self.previous_leak = leak_detected

        self.Z_values.append(self.Z_n)
        self.time_stamps.append(timestamp)

        return self.Z_n