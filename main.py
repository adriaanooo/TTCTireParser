from magicFormula import fit_magic_formula
from data_handling import *
from plotting import *
import pandas as pd


if __name__ == '__main__':
    print('\n---DATA PARSING---\n')
    path = 'B1965raw21.dat'
    df = pd.read_table(path, sep='\t', skiprows=[0, 2], header=0).astype(float)
    configure_plot_style()
    plot_multiple_columns(df, ['P', 'IA', 'FZ', 'V', 'TSTC'])

    # Asks user for start and end indices of the run to neglect warm up and cool down
    run_start = int(input("Enter run start index: "))
    run_end = int(input("Enter run end index: "))
    df = df[run_start:run_end]

    # Asks users for the number of different pressures, IAs, and FZs, and clusters data accordingly
    # Creates a hierarchal index in the data frame to allow for indexing of tire run parameters
    print('\n---Data Clustering---\n')
    p_clusters = int(input('# of Tire pressures: '))
    ia_clusters = int(input('# of Inclination angles: '))
    fz_clusters = int(input('# of Vertical forces: '))
    p_centers, df['P_cluster'] = cluster_and_label_col(df, column='P', n_clusters=p_clusters)
    ia_centers, df['IA_cluster'] = cluster_and_label_col(df, column='IA', n_clusters=ia_clusters)
    fz_centers, df['FZ_cluster'] = cluster_and_label_col(df, column='FZ', n_clusters=fz_clusters)
    df.set_index(['P_cluster', 'IA_cluster', 'FZ_cluster'], inplace=True)

    print('---FITTING MAGIC FORMULA---')
    for p_center

    print('\n---PLOTTING DATA---\n')
    recursive_plot_cornering_data(
        df, 83, ia_centers, fz_centers,
        [('SA', 'FY'), ('SA', 'MZ'), ]
    )
