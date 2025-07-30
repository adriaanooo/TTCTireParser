from tire import Tire
import tkinter as tk
from tkinter.filedialog import askopenfilename
tk.Tk().withdraw()

if __name__ == '__main__':

    # Path selection
    lat_path = askopenfilename(
        title='Lateral Tire Data',
        filetypes=[('Text Files', ['*.txt', '*.dat'])]
    )
    long_path = askopenfilename(
        title='Longitudinal Tire Data',
        filetypes=[('Text Files', ['*.txt', '*.dat'])]
    )
    my_tire = Tire(lat_path=lat_path, long_path=long_path)

    print('\n')
    print('---PLOTTING DATA---')
    print('\n')

    my_tire.plot_raw_data('lateral', [('SA', 'FY'), ('SA', 'MZ'), ('SA', 'muy')])
    my_tire.plot_raw_data('longitudinal', [('SL', 'FX'), ('SL', 'mux')])

    print('\n')
