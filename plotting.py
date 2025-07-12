import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


MARKERSIZE = 5
LINEWIDTH = 0
ALPHA = 0.2


def configure_plot_style(style='darkgrid'):
    sns.set_theme(style=style)


def plot_multiple_columns(data: pd.DataFrame(), cols: list[str]):
    fig, axes = plt.subplots(len(cols), 1)
    for i, col in enumerate(cols):
        sns.scatterplot(
            data[col],
            ax=axes[i],
            s=MARKERSIZE,
            linewidth=LINEWIDTH,
            alpha=ALPHA,
            c=data[col],
            cmap='plasma'
        )
        axes[i].set_xticks(np.arange(0, len(data[col]), 20000))
    plt.show()


def recursive_plot_cornering_data(
        df: pd.DataFrame,
        pressure, ia_centers, fz_centers,
        plots: list[tuple[str, str]]
):
    fig, axes = plt.subplots(1, len(plots), figsize=(16, 8))
    for ia_center in ia_centers:
        for fz_center in fz_centers:
            for i, plot in enumerate(plots):
                sns.scatterplot(
                    df.loc[(pressure, ia_center, fz_center)],
                    x=plot[0], y=plot[1], ax=axes[i],
                    s=MARKERSIZE, linewidth=LINEWIDTH, alpha=ALPHA,
                    label=f'{ia_center}DEG, {fz_center}N'
                )
    for i, ax in enumerate(axes):
        ax.set_title(f'{plots[i][0]} VS {plots[i][1]}')
        ax.margins(x=0, y=0.1)
        ax.legend(markerscale=5, loc='best')
    plt.show()
