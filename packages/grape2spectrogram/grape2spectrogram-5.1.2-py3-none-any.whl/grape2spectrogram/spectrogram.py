"""
Grape 2 Spectrogram Generator

Generates spectrograms from Digital RF files created by Grape 2 receivers.

TODO: make eclipse and solar overlay optional

@author: Cuong Nguyen
"""

# Standard library imports
import os
import sys
import datetime
import argparse

# Third-party imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import signal

# Local imports
try:
    from .reader import Reader
    from . import solarContext
except ImportError:
    from reader import Reader
    import solarContext


class Plotter:
    """
    Creates spectrograms from Grape 2 Digital RF data.

    Handles the visualization of frequency data across time, with solar
    context information overlaid.
    """

    PLOT_CONFIG = {
        "font.size": 12,
        "font.weight": "bold",
        "axes.grid": True,
        "axes.titlesize": 30,
        "grid.linestyle": ":",
        "figure.figsize": np.array([15, 8]),
        "axes.xmargin": 0,
        "legend.fontsize": "xx-large",
    }

    SOLAR_OVERLAY_CONFIG = {"color": "white", "lw": 4, "alpha": 0.75}

    HARC_PLOT_CONFIG = {
        "figure.titlesize": "xx-large",
        "axes.titlesize": "xx-large",
        "axes.labelsize": "xx-large",
        "xtick.labelsize": "xx-large",
        "ytick.labelsize": "xx-large",
        "legend.fontsize": "large",
        "figure.titleweight": "bold",
        "axes.titleweight": "bold",
        "axes.labelweight": "bold",
    }

    vmin, vmax = -90, 100

    def __init__(self, data_reader, output_dir="output"):
        """
        Initialize the plotter with a data reader and output directory.

        Args:
            data_reader: Reader object for accessing Digital RF data
            output_dir: Directory where plots will be saved
        """
        for key, value in self.PLOT_CONFIG.items():
            mpl.rcParams[key] = value
        for key, value in self.HARC_PLOT_CONFIG.items():
            mpl.rcParams[key] = value

        self.data_reader = data_reader
        self.metadata = data_reader.get_metadata()
        self.fs = self.data_reader.resampled_fs
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        # Create filename for plots based on date and station
        self.event_fname = (
            f"{self.metadata['utc_date'].date()}_{self.metadata['station']}_grape2DRF"
        )

    def plot_spectrogram(self, channel_indices=None):
        """
        Plot spectrograms for selected channels or all if not specified.

        Args:
            channel_indices: List of channel indices to plot. If None, plot all channels.
        """
        print(f"Now plotting {self.event_fname}...")
        if channel_indices is None:
            channel_indices = range(len(self.metadata["center_frequencies"]))
        else:
            channel_indices = [int(ch) for ch in sorted(channel_indices)]

        # Create figure with appropriate size
        nrows = len(channel_indices)
        fig = plt.figure(figsize=(27, nrows * 5))

        # Add title
        station = self.metadata["station"]
        location = self.metadata["city_state"]
        date = self.metadata["utc_date"].date()
        fig.text(
            0.45,
            1.0,
            f"{station} ({location})\nGrape 2 Spectrogram for {date}",
            ha="center",
            fontsize=42,
        )

        # Plot each channel
        for i, idx in enumerate(range(len(channel_indices))):
            cfreq_idx = channel_indices[::-1][idx]
            plot_position = idx + 1

            print(f"Plotting {self.metadata['center_frequencies'][cfreq_idx]} MHz...")

            # Get data and create subplot
            data = self.data_reader.read_data(channel_index=cfreq_idx)
            ax = fig.add_subplot(nrows, 1, plot_position)

            # Plot the data
            self._plot_ax(
                data,
                ax,
                freq=self.metadata["center_frequencies"][cfreq_idx],
                lastrow=(plot_position == len(channel_indices)),
            )

        # Save the figure
        fig.tight_layout()
        png_fpath = os.path.join(self.output_dir, f"{self.event_fname}.png")
        fig.savefig(png_fpath, bbox_inches="tight")
        print(f"Plot saved to {png_fpath}")

    def _plot_ax(self, data, ax, freq, lastrow=False):
        """
        Plot spectrogram data on the given axes.

        Args:
            data: The signal data to plot
            ax: The matplotlib axis to plot on
            freq: Center frequency in MHz
            lastrow: Whether this is the bottom plot (for x-axis labels)
        """
        # Set y-axis label
        ax.set_ylabel(f"{freq:.2f}MHz\nDoppler Shift (Hz)")

        # Generate spectrogram
        nperseg = int(self.fs / 0.01)  # 10ms segments
        f, t_spec, Sxx = signal.spectrogram(
            data, fs=self.fs, window="hann", nperseg=nperseg
        )
        print(data.shape, t_spec.shape, f.shape, Sxx.shape)

        # Convert to dB scale
        Sxx_db = np.log10(Sxx) * 10
        print("Min/Max dB:", np.nanmin(Sxx_db), np.nanmax(Sxx_db))

        # Center frequencies around zero
        f -= self.data_reader.target_bandwidth / 2

        # Set y-axis limits to match bandwidth
        bandwidth = self.data_reader.target_bandwidth
        ax.set_ylim(-bandwidth / 2, bandwidth / 2)

        # Create time axis from UTC date
        time_range = pd.date_range(
            start=self.metadata["utc_date"],
            end=self.metadata["utc_date"] + datetime.timedelta(days=1),
            periods=len(t_spec),
        )

        # Plot spectrogram
        cmap = mpl.colors.LinearSegmentedColormap.from_list(
            " ", ["black", "darkgreen", "green", "yellow", "red"]
        )
        norm = mpl.colors.Normalize(vmin=self.vmin, vmax=self.vmax)
        cax = ax.pcolormesh(time_range, f, Sxx_db, cmap=cmap, norm=norm)

        # Add solar context
        sts = solarContext.solarTimeseries(
            self.metadata["utc_date"],
            self.metadata["utc_date"] + datetime.timedelta(days=1),
            self.metadata["lat"],
            self.metadata["lon"],
        )

        # Overlay solar elevation and eclipse information
        self.overlay_colorbar(ax, cax)
        sts.overlaySolarElevation(ax, **self.SOLAR_OVERLAY_CONFIG)
        sts.overlayEclipse(ax, **self.SOLAR_OVERLAY_CONFIG)

        # Get x-ticks for consistent grid across all subplots
        xticks = ax.get_xticks()
        ax.set_xticks(xticks)

        # Only show x-axis labels on the bottom plot
        if lastrow:
            labels = [mpl.dates.num2date(xtk).strftime("%H:%M") for xtk in xticks]
            ax.set_xticklabels(labels)
            ax.set_xlabel("UTC")
        else:
            ax.set_xticklabels([""] * len(xticks))
            ax.tick_params(
                axis="x", which="both", length=0
            )  # Hide tick marks but keep grid

        # Ensure grid is visible
        ax.grid(visible=True, which="both", axis="both")

    def overlay_colorbar(self, ax, cax):
        """
        Overlay a colorbar on the spectrogram plot.
        """
        cbar = plt.colorbar(cax, ax=ax, orientation="vertical", pad=0.1)
        cbar.set_label("PSD (dB)")
        cbar.minorticks_on()
        cbar.ax.spines["right"].set_position(("axes", 1.1))
        return cbar


def main():
    parser = argparse.ArgumentParser(description="Grape2 Spectrogram Generator")
    parser.add_argument(
        "-i",
        "--input_dir",
        help="Path to the directory containing a ch0 subdirectory",
        required=True,
    )
    parser.add_argument(
        "-o", "--output_dir", help="Output directory for plot", required=True
    )
    parser.add_argument(
        "-k",
        "--keep_cache",
        action="store_true",
        help="Keep cache files after processing (by default, cache is removed)",
    )
    parser.add_argument(
        "-c",
        "--channels",
        nargs="*",
        help="Specific channel indices to plot (e.g., 0 1 2)",
    )
    args = parser.parse_args()
    try:
        # Initialize reader and plotter
        data_reader = Reader(args.input_dir, cleanup_cache=not args.keep_cache)
        plotter = Plotter(data_reader, output_dir=args.output_dir)

        # Plot with specified channels or all channels
        plotter.plot_spectrogram(channel_indices=args.channels)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
