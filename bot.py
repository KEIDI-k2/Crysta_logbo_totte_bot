from mastodon import Mastodon
import os
import datetime

# GitHub Secretsから環境変数を取得
ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")
INSTANCE_URL = os.getenv("MASTODON_INSTANCE_URL")

# Mastodon API クライアントのセットアップ
mastodon = Mastodon(access_token=ACCESS_TOKEN, api_base_url=INSTANCE_URL)

# 投稿するメッセージ
now = datetime.datetime.now()
message = f"テストだよ～。 クリスタのログボの時取ってっていう奴。"

# 投稿
mastodon.status_post(message)
print("投稿完了！")
