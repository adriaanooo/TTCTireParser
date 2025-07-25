import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


class MF52:

    def __init__(self, data: pd.DataFrame):
        self.lat_data = data['cornering']
        self.long_data = data['drive_brake']
        self.mf_params = pd.DataFrame(columns = ['FZ', 'B', 'C', 'D', 'E', 'SVx'])

    def Fx0(kappax, Bx, Cx, Dx, Ex, SVx):
        return Dx * np.sin(Cx * np.arctan(Bx * kappax - Ex * (Bx * kappax - np.arctan(Bx * kappax)))) + SVx

    def fit_Fx0(self, fz):
        data = self.long_data[self.long_data['FZ'] == fz and self.long_data['IA'] == 0]
        p0 = [10, 1.6, 500, 0.5, 0]
        popt = curve_fit(self.Fx0, self.data['SL'], self.data['FX'], p0)
        self.long_data['B'] = popt[0]
        self.long_data['C'] = popt[1]
        self.long_data['D'] = popt[2]
        self.long_data['E'] = popt[3]
        self.long_data['SVx'] = popt[4]
