import json

import requests
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

    def get_jquants_token(self):
        """JQuantsのトークンを取得する."""
        data = {"mailaddress": self.JQUANTS_EMAIL, "password": self.JQUANTS_PASSWORD}
        r_post = requests.post(
            "https://api.jquants.com/v1/token/auth_user",
            data=json.dumps(data),
            timeout=10,
        )
        print(r_post.text)
        return r_post.json()
