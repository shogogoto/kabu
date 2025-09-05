"""理論株価よりも実株価が安いタイミングと買い時を検索する.

input:
    銘柄コード
    割安比率
        underval_target_rate < 理論株価 - 実株価 / 理論株価 を検索
    期間
        from_yyyymmdd
        past_months
output:
    割安期間
        start
        end
    買い時 = 追いつき日 + 1
    株価
        割安期間
        買いタイミング
    利益 = 買い時 - 割安開始日
"""
