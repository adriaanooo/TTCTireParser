from magicFormula import fit_using_magic_formula
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans


def get_clusters(df: pd.DataFrame, column: str, n_clusters: int):
    print(f'\nClustering {column} with {n_clusters} clusters...')
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(df[[column]])
    labels = kmeans.labels_
    centers = dict(enumerate(kmeans.cluster_centers_.flatten().astype(int)))
    print(f"{column} cluster centers: {[int(centers[key]) for key in centers.keys()]}")
    return sorted(list(centers.values()), reverse=False), [centers[label] for label in labels]


if __name__ == '__main__':
    print('\n---DATA PARSING---\n')
    path = 'B1654raw33.dat'
    df = pd.read_table(path, sep='\t', skiprows=[0, 2], header=0)
    df = df[2000:-2000].astype(float)

    # Cluster independent variables
    print('---Independent variable variations---')
    p_clusters = int(input('# Tire pressures: '))
    ia_clusters = int(input('# Inclination angles: '))
    fz_clusters = int(input('# Vertical forces: '))
    p_centers, df['P_cluster'] = get_clusters(df, column='P', n_clusters=p_clusters)
    ia_centers, df['IA_cluster'] = get_clusters(df, column='IA', n_clusters=ia_clusters)
    fz_centers, df['FZ_cluster'] = get_clusters(df, column='FZ', n_clusters=fz_clusters)
    df.set_index(['P_cluster', 'IA_cluster', 'FZ_cluster'], inplace=True)

    print('\n---PLOTTING DATA---\n')
    sns.set(style='darkgrid')
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    for fz_center in fz_centers:
        sns.scatterplot(df.loc[(83, 0, fz_center)],
                        x='SA', y='FY', s=5, linewidth=0, alpha=0.4,
                        ax=axes[0], label=f'{fz_center}N')
        sns.scatterplot(df.loc[(83, 0, fz_center)],
                        x='SA', y='MZ', s=5, linewidth=0, alpha=0.4,
                        ax=axes[1], label=f'{fz_center}N')
    for ax in axes:
        ax.margins(x=0, y=0.1)
        ax.legend(markerscale=5, loc='best')
    print("DONE")
    plt.show()
