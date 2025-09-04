"""domain."""

from datetime import date, datetime
from typing import Annotated

import pandas as pd
from pydantic import BaseModel, BeforeValidator, Field
from pytz import UTC

from kabu.shared.types import date_from_iso_string


class UnderValuedTerm(BaseModel):
    """割安期間."""

    start: date
    end: date


class CatchUpDate(BaseModel):
    """実株価が理論株価に追いついた日."""


class EPS(BaseModel):
    """Earnings Per Share 1株当たり純利益."""

    report_date: Annotated[date, BeforeValidator(date_from_iso_string)] = Field(
        title="決算報告日",
    )
    value: float

    # def to_theorical_stock_price(self, rate: float):
    #     """理論株価に変換する."""
    #     return


def resample_eps_to_daily(
    eps_list: list[EPS],
    end_date: date | str | None = None,
) -> pd.Series:
    """四半期ごとのEPSリストを日次のSeriesにリサンプリングし、前方補完する."""
    if not eps_list:
        return pd.Series(dtype=float)

    eps_list.sort(key=lambda e: e.report_date)

    start_date = eps_list[0].report_date

    def to_final_date(end_date: date | str | None) -> date:
        match end_date:
            case None:
                return datetime.now(tz=UTC).date()
            case str():
                return date_from_iso_string(end_date)
            case date():
                return end_date

    final_date: date = to_final_date(end_date)
    if start_date > final_date:
        return pd.Series(dtype=float)

    dates = [e.report_date for e in eps_list]
    values = [e.value for e in eps_list]
    eps_series = pd.Series(values, index=pd.to_datetime(dates))

    # 重複があった場合は、最後に見つかったデータを正とする
    if not eps_series.index.is_unique:
        eps_series = eps_series.loc[~eps_series.index.duplicated(keep="last")]

    daily_index = pd.date_range(start=start_date, end=final_date, freq="D")
    return eps_series.reindex(daily_index, method="ffill")
