"""domain."""

from datetime import date, datetime
from typing import Annotated

import pandas as pd
from pydantic import BaseModel, BeforeValidator, Field
from pytz import UTC

from kabu.shared.types import date_from_iso_string
from kabu.shared.utils import find_crossings, find_intervals


class UnderValuedTerm(BaseModel):
    """割安期間."""

    start: date
    end: date

    @property
    def interval(self) -> tuple[date, date]:  # noqa: D102
        return (self.start, self.end)

    def __str__(self):  # noqa: D105
        return f"{self.start} ~ {self.end}"


class CatchUpDate(BaseModel):
    """実株価が理論株価に追いついた日."""

    date: date


class EPS(BaseModel):
    """Earnings Per Share 1株当たり純利益."""

    report_date: Annotated[date, BeforeValidator(date_from_iso_string)] = Field(
        title="決算報告日",
    )
    value: float


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


def to_theorical_price_and_rate(
    real_stock_price: pd.Series,
    eps_ls: list[EPS],
) -> tuple[pd.Series, pd.Series]:
    """理論株価と割安比を返す."""
    end_date = real_stock_price.index[-1]
    theoretical_price_sr = resample_eps_to_daily(eps_ls, end_date.date()) * 10
    theoretical_price_sr.name = "theoretical_price"
    underval_rate_sr = (theoretical_price_sr - real_stock_price) / theoretical_price_sr
    underval_rate_sr.name = "underval_rate"

    return theoretical_price_sr, underval_rate_sr


def find_undervalued_terms(
    underval_rate_sr: pd.Series,
    underval_target_rate: float,
) -> list[UnderValuedTerm]:
    """underval_target_rateよりも高い日を割安期間として取得する."""
    intval_ls = find_intervals(underval_rate_sr, underval_target_rate)

    return [
        UnderValuedTerm(
            start=intval[0].date(),
            end=intval[1].date(),
        )
        for intval in intval_ls
    ]


def find_latest_catch_up_date(
    term: UnderValuedTerm,
    underval_rate_sr: pd.Series,
) -> CatchUpDate | None:
    """割安期間の直後に来る追いつき日を返す."""
    all_crossings = find_crossings(underval_rate_sr, level=0.0)

    catch_up_dates = []
    for t in all_crossings:
        # クロス直前の値を取得
        value_before = underval_rate_sr.asof(t - pd.Timedelta(nanoseconds=1))
        if value_before > 0:
            catch_up_dates.append(t)

    term_end_ts = pd.Timestamp(term.end)
    future_catch_ups = [d for d in sorted(catch_up_dates) if d > term_end_ts]

    if not future_catch_ups:
        return None

    latest_catch_up = future_catch_ups[0]

    return CatchUpDate(date=latest_catch_up.date())
