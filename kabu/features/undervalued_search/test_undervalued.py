"""割安検索テスト."""

# @pytest.mark.skip

import pandas as pd

from kabu.features.undervalued_search.usecase import search_undervalued
from kabu.shared.source.jquants import get_codes_has_statements


def test_execute_search():
    """テストでプログラムの実行を代用."""
    # code = "8473"
    codes = get_codes_has_statements()
    total = len(codes)
    all_results = []

    cnt = 0
    for i, c in enumerate(codes):
        result = search_undervalued(c, 0.1, save_img=False)
        if result.empty:
            print(f"{c} was failed")
        else:
            all_results.append(result)
            cnt += 1
            print(f"{i}/{total}")

    if all_results:
        final_df = pd.concat(all_results, ignore_index=True)
        print(final_df)
        final_df.to_csv("undervalued.csv")
    print(f"{cnt}/{total}のデータをまとめたお")

    # print(result.to_csv())
    # print("#" * 80)
    # print(
    #     result_df.to_csv(
    #         # indent=2,
    #         # orient="records",
    #         # date_format="iso",
    #         # force_ascii=False,
    #     ),
    # )
