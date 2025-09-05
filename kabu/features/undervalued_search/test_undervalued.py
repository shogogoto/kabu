"""割安検索テスト."""

# @pytest.mark.skip

from kabu.features.undervalued_search.usecase import search_undervalued


def test_get_eps():
    """EPS取得テスト."""
    code = "8473"
    result = search_undervalued(code, 0.1)

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
