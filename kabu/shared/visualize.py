"""可視化."""

from collections.abc import Callable

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes


def save_image():
    """Save plot as image."""
    # This will now create an interactive plotly figure
    # fig = dailies.plot(title="Daily Resampled EPS (Interactive)")
    #
    # # Save the plot to an HTML file
    # plot_filename = "daily_eps_visualization.html"
    # fig.write_html(plot_filename)
    #
    # print(f"Interactive plot saved to {plot_filename}")
    # print(dailies)

    # plt.figure(figsize=(10, 6))
    # dailies.plot(title="Daily Resampled EPS")
    # plt.xlabel("Date")
    # plt.ylabel("EPS")
    # plt.grid(True)


def saveimg(
    df: pd.DataFrame,
    title: str,
    xlabel: str = "Date",
    ylabel: str = "Price",
    proc_ax: Callable[[Axes], None] = lambda _ax: None,
):
    """Save plot as image."""
    # plt.figure(figsize=(12, 6))
    # plt.plot(df.index, df)
    # plt.title(title)
    # plt.xlabel("Date")
    # plt.ylabel("EPS")
    # plt.grid(True)
    # plt.savefig(f"{title}.png")

    fig, ax = plt.subplots(figsize=(12, 6))
    df.plot(ax=ax, title=title, grid=True)

    proc_ax(ax)

    ax.grid(True)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.savefig(f"{title}.png")
    plt.close(fig)
