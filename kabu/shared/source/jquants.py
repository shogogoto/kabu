"""jquants source."""

from functools import cache
from pathlib import Path

import pandas as pd

from kabu.shared.settings import Settings


@cache
def _get_statements_all(start_dt: str, end_dt: str) -> pd.DataFrame:
    """3層キャッシュで財務情報を取得する.

    読み取りが重いので3段階のキャッシュを利用したい
    1. jquants組み込み
    2. それらを1ファイルに結合した jsonファイル
    3. pythonのメモリキャッシュ
    """
    s = Settings()
    fname = f"{start_dt}-{end_dt}.json"
    cache_path = Path.cwd() / f"{s.JQ_CACHE_DIR}/{fname}"
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    if cache_path.exists():
        return pd.read_json(cache_path, orient="records")

    client = s.jquants_client
    df = client.get_statements_range(
        start_dt=start_dt,
        end_dt=end_dt,
        cache_dir=s.JQ_CACHE_DIR,
    )
    df.to_json(cache_path, indent=2, orient="records")
    return df


def get_statements_cached(
    code: str,
    # 2025/9/5で使用できたfreeプランの期間
    start_dt="20230613",
    end_dt="20250613",
) -> pd.DataFrame:
    """cacheを利用して財務情報を取得する.

    銘柄指定や期間指定はこのキャッシュを利用する
    """
    return _get_statements_all(start_dt, end_dt)

    # print(df["LocaoCode"])
