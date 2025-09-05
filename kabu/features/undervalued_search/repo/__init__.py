"""repo."""

from datetime import date

from dateutil.relativedelta import relativedelta

from kabu.features.undervalued_search.domain.model import EPS as EPS
from kabu.shared.types import date_from_iso_string


def start_date_from_end(end_yyyymmdd: str, past_months: int) -> date:
    """検索期間の終わりと遡り月数から開始日を計算する."""
    end_date = date_from_iso_string(end_yyyymmdd)
    delta = relativedelta(months=past_months)
    return end_date - delta


def end_date_from_start(start_yyyymmdd: str, months: int) -> date:
    """検索期間の開始日と月数から終了日を計算する."""
    start_date = date_from_iso_string(start_yyyymmdd)
    delta = relativedelta(months=months)
    return start_date + delta
