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
