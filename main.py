from tire import Tire


if __name__ == '__main__':

    my_tire = Tire(lat_path='Tires/ZTD1_18_6-10/B2356run40.dat', long_path='Tires/ZTD1_18_6-10/B2356run63.dat')
    if my_tire.data['cornering'] is not None:
        cornering_data = True
    else:
        cornering_data = False
    if my_tire.data['drive_brake'] is not None:
        drive_brake_data = True
    else:
        drive_brake_data = False

    print('---PREPROCESSING---')

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

        print('\n')
        user_continue = input("Continue plotting? (Y/n) ")
        if user_continue == 'n':
            user_plotting = False
