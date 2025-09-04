"""可視化."""

import pandas as pd
from matplotlib import pyplot as plt


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


def saveimg(df: pd.DataFrame, title: str):
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("EPS")
    plt.grid(True)
    plt.savefig(f"{title}.png")
