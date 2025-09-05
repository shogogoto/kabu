"""repo."""

from datetime import date

from dateutil.relativedelta import relativedelta

from kabu.features.undervalued_search.domain.model import EPS
from kabu.shared.types import date_from_iso_string


def start_date_from_end(end_yyyymmdd: str, past_months: int) -> date:
    """検索期間の終わりと遡り月数から開始日を計算する."""
    end_date = date_from_iso_string(end_yyyymmdd)
    delta = relativedelta(months=past_months)
    return end_date - delta


def eps_adapter(code: str, start_date: date, end_date: date) -> list[EPS]:
    """任意のeps datasourceとのインターフェイス."""
    return []


def search_undervalued_stock(
    code: str,
    underval_target_rate: float,
    end_yyyymmdd: str,
    past_months: int,
    # eps_source:
):
    """理論株価よりも実株価が安い期間と買い時を検索する.

    Args:
        code: 銘柄コード
        underval_target_rate: r < 理論株価 - 実株価 / 理論株価 な期間を絞る割安比率
        end_yyyymmdd: 検索期間の終わり
        past_months: 遡り月数
    Returns:
        割安期間と追いつき日とそれぞれの日の実株価と利益のリスト
        割安期間: 割安ターゲット比よりも割安な期間
        買い時 = 追いつき日 + 1
        株価
            割安期間
            買いタイミング
        利益 = 買い時 - 割安開始日

    """
    start_date = start_date_from_end(end_yyyymmdd, past_months)
    end_date = date_from_iso_string(end_yyyymmdd)
    eps_ls = eps_adapter(code, start_date, end_date)

    # aaa
    print("Ahan")
    print("Ahan")
