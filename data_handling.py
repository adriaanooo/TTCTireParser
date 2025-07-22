import os
from sklearn.cluster import KMeans
import pandas as pd


def cluster_and_label_col(df: pd.DataFrame, column: str, n_clusters: int):
    print(f'Clustering {column} with {n_clusters} clusters...')
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(df[[column]])
    labels = kmeans.labels_
    centers = dict(enumerate(kmeans.cluster_centers_.flatten().round().astype(int)))
    return sorted(list(centers.values())), [centers[label] for label in labels]


def read_ttc_data_from_path(path):
    return pd.read_table(path, sep='\t', skiprows=[0, 2], header=0).astype(float)


def select_tire_data_path():
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

    return lat_path, long_path
