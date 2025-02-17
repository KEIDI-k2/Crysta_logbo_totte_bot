from mastodon import Mastodon
import os
import datetime

# GitHub Secretsから環境変数を取得
ACCESS_TOKEN = os.getenv("U69q6ggIQHsW15ggKcfp5TkSL3GJzHadCuDEmSbde4E")
INSTANCE_URL = os.getenv("https://kmy.blue/@keidi")

# Mastodon API クライアントのセットアップ
mastodon = Mastodon(access_token=ACCESS_TOKEN, api_base_url=INSTANCE_URL)

# 投稿するメッセージ
now = datetime.datetime.now()
message = f"テストだよ～。 クリスタのログボの時取ってっていう奴。"

# 投稿
mastodon.status_post(message)
print("投稿完了！")
