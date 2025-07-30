import os
from sklearn.cluster import KMeans
import pandas as pd


def cluster_and_label_col(df: pd.DataFrame, column: str, n_clusters: int):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(df[[column]])
    labels = kmeans.labels_
    centers = dict(enumerate(kmeans.cluster_centers_.flatten().round().astype(int)))
    return sorted(list(centers.values())), [centers[label] for label in labels]


def read_ttc_data_from_path(path):
    return pd.read_table(path, sep='\t', skiprows=[0, 2], header=0).astype(float)


def create_plot_path(tire: str, vars: tuple[str, str], conditions: list[str, str]):
    plot = f'{vars[0]}_{vars[1]}'
    dir = f'Plots/{tire}/{plot}'
    if not os.path.isdir(dir):
        os.makedirs(dir)

    return f'{dir}/{tire}_{plot}_{conditions[0]}_{conditions[1]}.png'
