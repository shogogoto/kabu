"""util."""

import numpy as np
import pandas as pd


def find_crossings(
    series: pd.Series,
    level: float = 0.0,
) -> list[pd.Timestamp]:
    """pandas.Seriesが指定したレベルをクロスする点を線形補間で探す.

    Args:
        series: 日付/時刻をインデックスに持つpandas.Series
        level: クロスを検出する値のレベル (デフォルト: 0.0)
        ceil_to_date: タイムスタンプを日付に切り上げて返すか (デフォルト: False)

    Returns:
        クロスした点のタイムスタンプまたは日付のリスト

    """
    # levelを引いて、ゼロクロスの問題に変換
    shifted_series = series - level
    valid_series = shifted_series.dropna()

    if len(valid_series) < 2:  # noqa: PLR2004
        return []

    # 符号が変わる場所を探す
    sign_changes = np.where(np.diff(np.sign(valid_series.to_numpy())))[0]

    crossings = []
    for idx in sign_changes:
        # 符号が変わる前後の2点を取得
        p1_idx, p2_idx = valid_series.index[idx], valid_series.index[idx + 1]
        p1_val, p2_val = valid_series.iloc[idx], valid_series.iloc[idx + 1]

        if p1_val == p2_val:
            continue

        # 2点間の線形補間でゼロになる点を計算
        time_diff = p2_idx - p1_idx
        val_diff = p2_val - p1_val

        cross_time_offset = -p1_val * (time_diff / val_diff)
        cross_time = p1_idx + cross_time_offset
        crossings.append(cross_time)
    return crossings


def find_zero_crossings(series: pd.Series) -> list[pd.Timestamp]:
    """pandas.Seriesのゼロクロス点を線形補間で探す."""
    return find_crossings(series, level=0.0)
