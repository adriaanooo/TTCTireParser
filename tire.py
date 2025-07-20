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
        self.data = {
            'cornering': read_ttc_data_from_path(lat_path) if lat_path else None,
            'drive_brake': read_ttc_data_from_path(long_path) if long_path else None,
        }
        self.p_vals = {}
        self.ia_vals = {}
        self.fz_vals = {}

        sns.set_theme(style='darkgrid')

    def __check_for_run_type_data(self, run_type):
        if self.data[run_type] is None:
            raise ValueError(f"No data for {run_type} run")

    def plot_vs_time(self, cols: list[str], run_type, every_nth_point=10, xtick_spacing=10000):
        self.__check_for_run_type_data(run_type)

        for col in cols:
            if col not in self.data[run_type].columns:
                raise ValueError(f"Column {col} not found in {run_type} DataFrame")

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
        plt.tight_layout()
        plt.show()

    def clean_data(self, run_type, pure_slip=True):
        self.__check_for_run_type_data(run_type)

        # Asks the user to manually slice out warm up and cool down
        self.data[run_type] = self.data[run_type][int(input("Select run start index: ")):int(input("Select run end index: "))]

        # Removes SA = 0 for cornering and SA != 0 for drive/brake
        # Also calculates friction coefficients
        if run_type == 'cornering':
            self.data[run_type] = self.data[run_type][~np.isclose(self.data[run_type]['SA'], 0, atol=0.1)]
            self.data[run_type]['muy'] = self.data[run_type]['FY'] / self.data[run_type]['FZ']
        elif (run_type == 'drive_brake') and pure_slip:
            self.data[run_type] = self.data[run_type][np.isclose(self.data[run_type]['SA'], 0, atol=0.1)]
            self.data[run_type]['mux'] = self.data[run_type]['FX'] / self.data[run_type]['FZ']

    def cluster_controlled_variables(self, run_type):
        self.__check_for_run_type_data(run_type)

        n_p = int(input("# of pressures observed in time plot: "))
        n_ia = int(input("# of inclination angles observed in time plot: "))
        n_fz = int(input("# of vertical forces observed in time plot: "))

        print('\n')
        self.p_vals[run_type], self.data[run_type]['P'] = cluster_and_label_col(
            self.data[run_type], column='P', n_clusters=n_p
        )
        self.ia_vals[run_type], self.data[run_type]['IA'] = cluster_and_label_col(
            self.data[run_type], column='IA', n_clusters=n_ia
        )
        self.fz_vals[run_type], self.data[run_type]['FZ'] = cluster_and_label_col(
            self.data[run_type], column='FZ', n_clusters=n_fz
        )

        self.data[run_type].set_index(['P', 'IA', 'FZ', 'ET'], inplace=True)
        self.data[run_type].sort_index(inplace=True)

    def print_controlled_variable_values(self, run_type):
        print(f"{run_type} values:"
              f"\n\tPressures: {[int(p) for p in self.p_vals[run_type]]}"
              f"\n\tInclination angles: {[int(ia) for ia in self.ia_vals[run_type]]}"
              f"\n\tVertical forces: {[int(fz) for fz in self.fz_vals[run_type]]}")

    def plot_raw_data(self, plots: list[tuple[str, str]], p, ia, run_type):
        self.__check_for_run_type_data(run_type)

        fig, axes = plt.subplots(1, len(plots), figsize=FIGSIZE)
        for fz in self.fz_vals[run_type]:
            for i, plot in enumerate(plots):
                try:
                    x = self.data[run_type].loc[(p, ia, fz)][plot[0]]
                    y = self.data[run_type].loc[(p, ia, fz)][plot[1]]
                except:
                    raise KeyError(f"{plot[0]} and {plot[1]} data not found in {run_type} run")
                sns.scatterplot(
                    x=x, y=y, ax=axes[i], s=MARKERSIZE, linewidth=LINEWIDTH, alpha=ALPHA, label=f'{fz}N'
                )
        for i, ax in enumerate(axes):
            ax.set_title(
                f'{plots[i][0]} VS {plots[i][1]} @ {p}kPa, {ia}DEG Inclination'
            )
        plt.show()


