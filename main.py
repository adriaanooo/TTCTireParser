import os
from tire import Tire
from data_handling import select_tire_data_path


if __name__ == '__main__':

    # Path selection
    lat_path, long_path = select_tire_data_path()

    my_tire = Tire(lat_path=lat_path, long_path=long_path)
    # This checks which types of data is submitted
    # Prob a better way to do this but DataFrame truth is ambiguous
    if my_tire.data['cornering'] is not None:
        cornering_data = True
    else:
        cornering_data = False
    if my_tire.data['drive_brake'] is not None:
        drive_brake_data = True
    else:
        drive_brake_data = False

    print('\n')
    print('---PREPROCESSING---')

    # Raw data is visualized -> cleaned -> visualized -> clustered
    # Data cleanup for cornering runs
    if cornering_data:
        my_tire.plot_vs_time(['P', 'IA', 'FZ', 'V', 'SA'], 'cornering')
        print('\n')
        my_tire.clean_data('cornering')
        my_tire.plot_vs_time(['P', 'IA', 'FZ', 'V', 'SA'], 'cornering')
        print('\n')
        my_tire.cluster_controlled_variables('cornering')

    # Data cleanup for drive/brake runs
    if drive_brake_data:
        my_tire.plot_vs_time(['P', 'IA', 'FZ', 'SA', 'SR'], 'drive_brake')
        print('\n')
        my_tire.clean_data('drive_brake')
        my_tire.plot_vs_time(['P', 'IA', 'FZ', 'SA', 'SR'], 'drive_brake')
        print('\n')
        my_tire.cluster_controlled_variables('drive_brake')

    print('\n')
    print('---PLOTTING DATA---')
    print('\n')

    # Plotting loop to allow user to visualize plots under different test conditions
    # For each run type, test conditions are listed first, then user inputs conditions for plotting
    my_tire.plot_raw_data('cornering', [('SA', 'FY'), ('SA', 'MZ'), ('SA', 'muy')])
    my_tire.plot_raw_data('drive_brake', [('SL', 'FX'), ('SL', 'mux')])

    print('\n')
    print('---Magic Formula 5.2 Fitting---')
