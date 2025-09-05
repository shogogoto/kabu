"""可視化."""

from collections.abc import Callable, Iterable
from datetime import date

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes

type AxesProc = Callable[[Axes], None]


def saveimg(
    df: pd.DataFrame,
    title: str,
    xlabel: str = "Date",
    ylabel: str = "Price",
    ax_proces: Iterable[AxesProc] = (),
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

    for p in ax_proces:
        p(ax)

    ax.grid(True)  # noqa: FBT003
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.savefig(f"{title}.png")
    plt.close(fig)


def add_axes_vertical_line(dates: Iterable[date]) -> Callable[[Axes], None]:
    """指定日付に縦線を引く."""

    def _f(ax: Axes):
        for d in dates:
            ax.axvline(x=d, color="r", linestyle="--", linewidth=1)

    return _f


def add_axes_span(
    intervals: Iterable[tuple[date, date]],
    color: str = "lightgray",
    alpha: float = 0.5,
) -> Callable[[Axes], None]:
    """指定された区間の背景を色付けする関数を返す.

    Args:
        intervals: 色付けする区間 (開始日, 終了日) のタプルのイテラブル.
        color: 色.
        alpha: 透明度.

    Returns:
        Axesを処理する関数.

    """

    def _f(ax: Axes):
        for start, end in intervals:
            ax.axvspan(start, end, color=color, alpha=alpha)

    return _f
