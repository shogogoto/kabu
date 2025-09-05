"""test."""


def test_get_info():
    """動作確認用."""
    # 最初のコードをサンプルとして使用します

    # print(f"コード: {code}")
    # print(f"yfinanceティッカー: {ticker_code}")
    # print(f"EPS: {eps}")

    # sp = get_stock_price("8473", "2022-01-01", "2022-12-31")
    # print(type(sp))
    # reset_index()を使って、インデックスになっている日付を通常の列に変換することで、JSONに日付を含める
    # print(sp.reset_index().to_json(indent=2, orient="records", date_format="iso"))

    # print(get_eps("8473", "2025-01-01", "2025-12-31"))

    # print(get_eps_by_alpha_vantage("8473", "2025-01-01", "2025-12-31"))

    # {"Your subscription covers the following dates: 2023-06-11 ~ 2025-06-11.
    # If you want more data, please check other plans:https://jpx-jquants.com/"}

    # start_date = date(2023, 8, 3)
    # end_date = date(2025, 6, 11)

    # 日付を1日ずつ増やしながらループ
    # current_date = start_date
    # while current_date <= end_date:
    #     sp2 = get_eps_by_jquants("8473", str(current_date))
    #     print(sp2.reset_index().to_json(indent=2, orient="records", date_format="iso"))
    #     print(str(current_date))
    #     current_date += timedelta(days=1)

    # sleep(1)
    # print(Settings().get_jquants_token())

    # 2023-08-03 に現れた 他は空
