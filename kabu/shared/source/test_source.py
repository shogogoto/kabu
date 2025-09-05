"""source test."""

from kabu.shared.settings import Settings


def test_study():
    """動作調査用."""
    client = Settings().jquants_client

    # x = client.get_market_segments()
    # x = client.get_markets_short_selling_positions_range()  # ng at free plan
    # x = client.get_markets_short_selling_positions(code="8473")  # ng at free plan
    # x = client.get_markets_short_selling(sector_33_code="0050") # ng at free plan
    # print(x)
    # a = client.get_fins_announcement() # ok
    # x = client.get_fs_details_range(cache_dir="kabu_cache/") # ng

    # Your subscription covers the following dates: 2023-06-13 ~ 2025-06-13.
    # f1 = client.get_fins_statements(date_yyyymmdd="2023-06-13")
    # f2 = client.get_fins_statements(date_yyyymmdd="2023-06-15")
    # print(f1.to_json(indent=2, orient="records", date_format="iso"))
    # print(f1)

    # f1とf2の差分を計算
    # diff = pd.concat([f1, f2]).drop_duplicates(keep=False)
    # print("Diff:")
    # print(diff)

    # df = get_stock_price("8473", "2022-01-01", "2022-12-31")
    # print(df)
