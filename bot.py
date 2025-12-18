import os
import random
from datetime import datetime, date
from mastodon import Mastodon
import sys

# ========= 現在時刻（UTC） =========
now = datetime.utcnow()
today = now.date()
hour = now.hour
minute = now.minute

# ========= 実行期間 =========
START_DATE = date(2025, 12, 16)
END_DATE   = date(2026, 1, 26)

# ========= 期間チェック =========
if not (START_DATE <= today <= END_DATE):
    print("期間外なので投稿しません")
    sys.exit(0)

# ========= 投稿タイミング判定 =========
post_type = None

# 朝10時（JST）= UTC 01:00
if hour == 1 and minute == 0:
    post_type = "morning"

# 夜20時（JST）= UTC 11:00
elif hour == 11 and minute == 0:
    post_type = "evening"

else:
    print("投稿時間ではないのでスキップ")
    sys.exit(0)

print(f"投稿時間一致：{post_type}")

# ========= 環境変数 =========
ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")
INSTANCE_URL = os.getenv("MASTODON_INSTANCE_URL")

if not ACCESS_TOKEN or not INSTANCE_URL:
    raise ValueError("環境変数が設定されていません")

# ========= Mastodon接続 =========
mastodon = Mastodon(
    access_token=ACCESS_TOKEN,
    api_base_url=INSTANCE_URL
)

# ========= 投稿文 =========
morning_messages = [
    "おはよ～。ログボ取った～？",
    "おはよ！ ログボのお時間です",
    ":kb_ohayo2: ログボ取ってね～",
    ":kb_ohayo2: ログボ取って偉い",
    ":kb_ohayo2: 今日もログボってこ！"
]

evening_messages = [
    "こんばんは～。ログボ取りました？",
    "夜ログボのお時間です 🌙",
    ":kb_otukare: ログボ取りましょ",
    ":kb_otukare: ログボ取れたね！",
    "一日の締めにログボ取っとこ～"
]

# ========= 文言選択 =========
if post_type == "morning":
    message = random.choice(morning_messages)
else:
    message = random.choice(evening_messages)

# ========= 投稿 =========
status = mastodon.status_post(message)
print("投稿成功:", status.url)
