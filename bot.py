import os
import random
from mastodon import Mastodon

# 環境変数の取得
MASTODON_ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")
MASTODON_INSTANCE_URL = os.getenv("MASTODON_INSTANCE_URL")

# アクセストークンとインスタンスURLの確認
if not MASTODON_ACCESS_TOKEN or not MASTODON_INSTANCE_URL:
    raise ValueError("アクセストークンまたはインスタンスURLが設定されていません！")

# Mastodonに接続
mastodon = Mastodon(
    access_token=MASTODON_ACCESS_TOKEN,
    api_base_url=MASTODON_INSTANCE_URL
)

# 朝の言葉リスト（ランダムに選ばれる）
morning_quotes = [
    "おはよ～。ログボ取った～？",
    "おはよ！ ログボのお時間です",
    ":kb_ohayo2: ログボ取ってね～",
    ":kb_ohayo2: ログボ取って偉い",
    ":kb_ohayo2: 今日もログボってこ！"
]

# ランダムに一つの言葉を選ぶ
message = random.choice(morning_quotes)

# 投稿
status = mastodon.status_post(message)

print(f"投稿成功: {status.url}")
