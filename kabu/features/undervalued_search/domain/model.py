"""クラス."""

from datetime import date
from typing import Annotated

import pandas as pd
from pydantic import BaseModel, BeforeValidator, Field

from kabu.shared.types import date_from_iso_string


class UnderValuedTerm(BaseModel, frozen=True):
    """割安期間."""

    start: date
    end: date

    @property
    def interval(self) -> tuple[date, date]:  # noqa: D102
        return (self.start, self.end)

    def __str__(self):  # noqa: D105
        return f"{self.start} ~ {self.end}"

    @property
    def start_stamp(self) -> pd.Timestamp:  # noqa: D102
        return pd.Timestamp(self.start)

    @property
    def end_stamp(self) -> pd.Timestamp:  # noqa: D102
        return pd.Timestamp(self.end)


class CatchUpDate(BaseModel, frozen=True):
    """実株価が理論株価に追いついた日."""

    date: date

    @property
    def tomorrow(self) -> pd.Timestamp:
        """買いタイミング."""
        return pd.Timestamp(self.date) + pd.Timedelta(days=1)


class EPS(BaseModel, frozen=True):
    """Earnings Per Share 1株当たり純利益."""

    report_date: Annotated[date, BeforeValidator(date_from_iso_string)] = Field(
        title="決算報告日",
    )
    value: float
