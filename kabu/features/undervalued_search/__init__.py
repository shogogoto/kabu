"""割安検索.

理論株価よりも実株価が安いタイミングを検索する

input:
    銘柄コード
    割安比率
        threshold_rate
    期間
        from_yyyymmdd
        past_months


output:
    kk

日付を横軸とした sinカーブを用意したらテストできるんじゃね?
"""
