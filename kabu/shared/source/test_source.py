"""source test."""

from kabu.shared.settings import Settings
from kabu.shared.source.jquants import get_statements_cached


def test_get_eps():
    client = Settings().jquants_client

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

    df = get_statements_cached("84730")

    print(df)
    # x.to_json("x.json", indent=2, orient="records", date_format="iso", force_ascii=False)
    # x.to_csv("x.csv")
