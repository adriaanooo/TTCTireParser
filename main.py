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

    # This checks which types of data is submitted
    # Prob a better way to do this but DataFrame truth is ambiguous
    if my_tire.data['lateral'] is not None:
        lateral_data = True
    else:
        lateral_data = False
    if my_tire.data['longitudinal'] is not None:
        longitudinal_data = True
    else:
        longitudinal_data = False

    print('\n')
    print('---PREPROCESSING---')

    # Raw data is visualized -> cleaned -> visualized -> clustered
    # Data cleanup for cornering runs
    if lateral_data:
        my_tire.plot_vs_time(['P', 'IA', 'FZ', 'V', 'SA'], 'lateral')
        print('\n')
        my_tire.clean_data('lateral')
        my_tire.plot_vs_time(['P', 'IA', 'FZ', 'V', 'SA'], 'lateral')
        print('\n')
        my_tire.cluster_controlled_variables('lateral')

    # Data cleanup for drive/brake runs
    if longitudinal_data:
        my_tire.plot_vs_time(['P', 'IA', 'FZ', 'SA', 'SR'], 'longitudinal')
        print('\n')
        my_tire.clean_data('longitudinal')
        my_tire.plot_vs_time(['P', 'IA', 'FZ', 'SA', 'SR'], 'longitudinal')
        print('\n')
        my_tire.cluster_controlled_variables('longitudinal')

    print('\n')
    print('---PLOTTING DATA---')
    print('\n')

    if lateral_data:
        my_tire.plot_raw_data('lateral', [('SA', 'FY'), ('SA', 'MZ'), ('SA', 'muy')])
    if longitudinal_data:
        my_tire.plot_raw_data('longitudinal', [('SL', 'FX'), ('SL', 'mux')])

    print('\n')
    print('---Magic Formula 5.2 Fitting---')
