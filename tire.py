import os

import pandas as pd
from matplotlib.pyplot import title
from scipy.stats import alpha

from data_handling import *
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Constants for plot formatting.
MARKERSIZE = 5
LINEWIDTH = 0
ALPHA = 0.5
FIGSIZE = (16, 9)


class Tire:
    """
    Tire model
    """
    def __init__(self, long_path=None, lat_path=None):

        # Dataframe init and clean
        self.name = input('Enter Tire Name: ')
        self.data = {
            'lateral': read_ttc_data_from_path(lat_path) if lat_path else None,
            'longitudinal': read_ttc_data_from_path(long_path) if long_path else None,
        }
        # Lateral data
        self._plot_vs_time(['P', 'IA', 'FZ'], 'lateral')
        self._clean_data('lateral')
        controlled_vars_lat = self._cluster_controlled_variables('lateral')

        # Longitudinal data
        self._plot_vs_time(['P', 'IA', 'FZ'], 'longitudinal')
        self._clean_data('longitudinal')
        controlled_vars_long = self._cluster_controlled_variables('longitudinal')
        # Initializes dataframes to organize controlled variable values for cornering and drive/brake run
        self.controlled_vars = {
            'lateral': {
                'P': controlled_vars_lat[0],
                'IA': controlled_vars_lat[1],
                'FZ': controlled_vars_lat[2],
            },
            'longitudinal': {
                'P': controlled_vars_long[0],
                'IA': controlled_vars_long[1],
                'FZ': controlled_vars_long[2],
            },
        }
        # Plot formatting
        sns.set_theme(style='darkgrid')


    def _plot_vs_time(self, cols: list[str], run_type, every_nth_point=10, xtick_spacing=10000):
        """
        Plots specified columns against time in a single figure.
        :param cols:
        :param run_type:
        :param every_nth_point:
        :param xtick_spacing:
        :return:
        """
        fig, axes = plt.subplots(len(cols), 1, figsize=FIGSIZE)
        for i, col in enumerate(cols):
            data_downscaled = self.data[run_type][col].iloc[::every_nth_point] # Downscales data to every nth data point to increase performance.
            sns.scatterplot(
                data_downscaled,
                ax=axes[i],
                s=MARKERSIZE,
                linewidth=LINEWIDTH,
                alpha=ALPHA,
                c=data_downscaled,
                cmap='plasma'
            )
            axes[i].set_xticks(np.arange(0, len(self.data[run_type][col]), xtick_spacing))
        plt.show()


    def _clean_data(self, run_type):
        """
        Allows user to slice out warmup/cooldown data manually. Also cleans data specific to run type.
        Removes slip angles close to 0 in cornering runs. Only includes SA = 0 for drive/brake runs (pure slip).
        :param run_type:
        :return:
        """
        # Asks the user to manually slice out warm up and cool down
        start_idx = int(input("Select run start index: "))
        end_idx = int(input("Select run end index: "))
        self.data[run_type] = self.data[run_type][start_idx:end_idx]

        # Removes SA = 0 for cornering and SA != 0 for drive/brake
        # Also calculates friction coefficients
        if run_type == 'lateral':
            self.data[run_type]['muy'] = self.data[run_type]['FY'] / self.data[run_type]['FZ']
        elif run_type == 'longitudinal':
            # keeps points where slip angle is close to zero
            self.data[run_type] = self.data[run_type][np.isclose(self.data[run_type]['SA'], 0, atol=0.1)]
            self.data[run_type]['mux'] = self.data[run_type]['FX'] / self.data[run_type]['FZ']


    def _cluster_controlled_variables(self, run_type):
        """
        Creates clusters for controlled variables. Takes number of values per variable, sotres cluster centers in
        dictionary, and replaces value in variable column with corresponding center value.
        :param run_type:
        :return:
        """
        n_p = int(input("# of pressures observed in time plot: "))
        n_ia = int(input("# of inclination angles observed in time plot: "))
        n_fz = int(input("# of vertical forces observed in time plot: "))

        controlled_vars = [0, 0, 0]
        controlled_vars[0], self.data[run_type]['P'] = cluster_and_label_col(
            self.data[run_type], column='P', n_clusters=n_p
        )
        controlled_vars[1], self.data[run_type]['IA'] = cluster_and_label_col(
            self.data[run_type], column='IA', n_clusters=n_ia
        )
        controlled_vars[2], self.data[run_type]['FZ'] = cluster_and_label_col(
            self.data[run_type], column='FZ', n_clusters=n_fz
        )

        return controlled_vars


    def plot_raw_data(self, run_type: str, plots: list[tuple[str, str]]):
        """
        Plots the raw tire data as specified by plots argument ([(x1, y1), (x2, y2), ..., (xn, yn)]) given test
        conditions (pressure and inclination angle).
        :param run_type:
        :param plots:
        :return:
        """
        for plot in plots:
            print(f'Plotting {plot[0]} VS {plot[1]}...')
            for (p, ia), group in self.data[run_type].groupby(['P', 'IA']):
                plt.clf()
                g = sns.scatterplot(
                    group, x=plot[0], y=plot[1],
                    linewidth=LINEWIDTH,
                    s=MARKERSIZE,
                    alpha=ALPHA,
                    hue='FZ', palette='turbo_r'
                )

                g.set_title(f'{self.name} {plot[0]} VS {plot[1]} @ {p}kPa, {ia} Deg')

                legend = plt.legend(markerscale=5, title='Vertical Load')

                for handle in legend.legend_handles:
                    handle.set_alpha(1)

                plt.savefig(create_plot_path(self.name, plot, [f'{p}kPa', f'{ia}deg']))
