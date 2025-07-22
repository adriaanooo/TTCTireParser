import os
from tire import Tire


if __name__ == '__main__':

    # Path selection
    run_selected = False
    compound_selected = False
    while not run_selected:
        while not compound_selected:
            print(f"Tire compounds: {os.listdir('Tires')}")
            compound = input('Enter compounds: ')
            if compound in os.listdir('Tires'):
                compound_selected = True
        print(f"Runs: {os.listdir(f'Tires/{compound}')}")
        lat_run = input('Enter cornering run (n for None): ')
        if lat_run == 'n':
            lat_run = None
        long_run = input('Enter drive/brake run (n for None): ')
        if long_run == 'n':
            long_run = None
        if lat_run and long_run in os.listdir(f'Tires/{compound}'):
            long_path = f'Tires/{compound}/{long_run}'
            lat_path = f'Tires/{compound}/{lat_run}'
            run_selected = True
        elif lat_run in os.listdir(f'Tires/{compound}') and not long_run:
            lat_path = f'Tires/{compound}/{lat_run}'
            run_selected = True
        elif long_run in os.listdir(f'Tires/{compound}') and not lat_run:
            long_path = f'Tires/{compound}/{long_run}'
            run_selected = True

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

    # Plotting loop to allow user to visualize plots under different test conditions
    # For each run type, test conditions are listed first, then user inputs conditions for plotting
    user_plotting = True
    while user_plotting:

        if cornering_data:
            print('\n')
            my_tire.print_controlled_variable_values('cornering')
            print('\n')
            my_tire.plot_raw_data(
                [('SA', 'FY'), ('SA', 'MZ'), ('SA', 'muy')], int(input('Pressure: ')), int(input('Inclination angle: ')), 'cornering'
            )

        if drive_brake_data:
            print('\n')
            my_tire.print_controlled_variable_values('drive_brake')
            print('\n')
            my_tire.plot_raw_data(
                [('SL', 'FX'), ('SL', 'mux')], int(input('Pressure: ')), int(input('Inclination angle: ')), 'drive_brake'
            )

        # Loop exit
        print('\n')
        user_continue = input("Continue plotting? (Y/n) ")
        if user_continue == 'n':
            user_plotting = False
