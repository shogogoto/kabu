"""組み合わせた高度な処理."""

from datetime import date

import pandas as pd

from kabu.features.undervalued_search.domain import (
    find_latest_catch_up_date,
    find_undervalued_terms,
)
from kabu.features.undervalued_search.domain.model import CatchUpDate, UnderValuedTerm
from kabu.shared.visualize import add_axes_span, add_axes_vertical_line, saveimg


def find_undervalued(
    r_underval: pd.Series,
    r_target: float,
) -> tuple[list[UnderValuedTerm], list[CatchUpDate | None]]:
    """特定codeに対して."""
    terms = find_undervalued_terms(r_underval, underval_target_rate=r_target)
    catchups = [find_latest_catch_up_date(a, r_underval) for a in terms]
    return terms, catchups


def save_undervalued_img(
    df: pd.DataFrame,
    terms: list[UnderValuedTerm],
    catchups: list[CatchUpDate | None],
    save_name: str,
):
    """割安タイミングの画像保存."""
    saveimg(
        df,
        save_name,
        ax_proces=(
            add_axes_span([a.interval for a in terms]),
            add_axes_vertical_line([c.date for c in catchups if c is not None]),
        ),
    )


def to_result(
    code: str,
    search_start: pd.Timestamp | date,
    search_end: pd.Timestamp | date,
    r_underval: float,
    term: UnderValuedTerm,
    catchup: CatchUpDate | None,
    price: pd.DataFrame,
):
    """検索結果をまとめる."""
    profit = price.loc[catchup.tomorrow] - price.loc[pd.Timestamp(term.start)]
    return {
        "code": code,
        "割安ターゲット比": r_underval,
        "検索期間 開始日": search_start,
        "検索期間 終了日": search_end,
        "割安開始日": term.start,
        "割安終了日": term.end,
        "買いタイミング": catchup.tomorrow,
        "実株価(割安開始日)": price.loc[term.start_stamp],
        "実株価(割安終了日)": price.loc[term.end_stamp],
        "実株価(買いタイミング)": price.loc[catchup.tomorrow],
        "利益": profit,
        "利益率": profit / price.loc[catchup.tomorrow],
    }
