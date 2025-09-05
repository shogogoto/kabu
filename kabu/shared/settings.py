"""環境変数由来の設定."""

import jquantsapi
from alpha_vantage.fundamentaldata import FundamentalData
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """環境変数."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,  # 追加
    )

    ALPHA_VANTAGE_API_KEY: str
    JQUANTS_EMAIL: str
    JQUANTS_PASSWORD: str

    JQ_CACHE_DIR: str = "kabu_cache/"
    STOCK_PRICE_CACHE_DIR: str = "kabu_cache/stock_price/"

    # def get_jquants_token(self):
    #     """JQuantsのトークンを取得する."""
    #     data = {"mailaddress": self.JQUANTS_EMAIL, "password": self.JQUANTS_PASSWORD}
    #     r_post = requests.post(
    #         "https://api.jquants.com/v1/token/auth_user",
    #         data=json.dumps(data),
    #         timeout=10,
    #     )
    #     print(r_post.text)
    #     return r_post.json()

    @property
    def jquants_client(self):
        """J-Quants APIクライアントを取得する."""
        return jquantsapi.Client(
            mail_address=self.JQUANTS_EMAIL,
            password=self.JQUANTS_PASSWORD,
        )

    def aplha_vantage_client(self) -> FundamentalData:
        """Alpha Vantage APIクライアントを取得する."""
        # e.g. res = fd.get_earnings_annual(symbol="IBM")
        return FundamentalData(key=self.ALPHA_VANTAGE_API_KEY, output_format="pandas")
