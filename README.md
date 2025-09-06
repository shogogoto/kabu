# 株分析ツール

## 必要なもの
- python: 3.10 ~ のバージョンのどれか
- Poetry: ライブラリ管理ツール
- Git: バージョン管理ツール、ソースコードを取って来たり、変更履歴を管理できる
- VSCode: ソースコードを編集、実行等できる環境
  - 人気あるからとりあえずこれ使っとこう
  - いろんな拡張機能(プラグイン)があるから、適宜使うべし。

このファイルをAIにコピペしたりしつつ、環境整備をしてくれ


## 準備
必要なものを全てインストールできていることが前提

```bash
git clone このURL # ソースコードを取得
cd kabu # ソースコードのディレクトリに移動
poetry install # ライブラリのインストール
# python3.10以上のバージョンがインストールされている必要があるかも

```

### API利用者登録
以下でアカウントを作成する
https://jpx-jquants.com/auth/signup

### 環境変数の準備
ここで使用したメールアドレスとパスワードを `.env` に記述する
このディレクトリのトップに `.env` というファイルを作り、環境変数を記述する

```filename=.env
JQUANTS_EMAIL=xxxx@xxx.xxx
JQUANTS_PASSWORD=xxxxxx
```


## 実行方法
コマンド実行やウェブアプリ化の案もあったが、まだ早すぎる
一旦、テスト実行によってプログラムの実行を代用する

```bash
poetry run pytest # テストの実行, テストに調査用のコードを書いて実行する
poetry run ptw # ファイルを変更する都度、テストを実行する
```

test_xxx.py という testから始まるファイル名に書かれた
testから始まる関数がテストで実行される


## ディレクトリ構成
- features/ ディレクトリ: 機能単位でまとめる
  - features/undervalued_search/test_undervalued.py でプログラムを実行
- shared/ ディレクトリ: 共通部分をまとめる
- kabu_cache/ APIで取得するデータをファイルとして保存しとくことでAPI連打を減らす
  API連打しすぎると、yahoo finance に一時的にBANされる可能性があるらしい
- pyproject.toml: 使用するライブラリ一覧などのプロジェクトの情報が含まれる








