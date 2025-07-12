from sklearn.cluster import KMeans
import pandas as pd


def cluster_and_label_col(df: pd.DataFrame, column: str, n_clusters: int):
    print(f'\nClustering {column} with {n_clusters} clusters...')
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(df[[column]])
    labels = kmeans.labels_
    centers = dict(enumerate(kmeans.cluster_centers_.flatten().astype(int)))
    print(f"{column} cluster centers: {sorted([int(centers[key]) for key in centers.keys()])}")
    return sorted(list(centers.values())), [centers[label] for label in labels]
