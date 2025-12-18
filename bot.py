import os
import random
from datetime import datetime, date
from mastodon import Mastodon
import sys

# ========= 現在時刻（日本時間） =========
now = datetime.now()
today = now.date()
hour = now.hour
minute = now.minute

# ========= 実行期間 =========
START_DATE = date(2025, 12, 16)
END_DATE   = date(2026, 1, 26)

# ========= 誤爆・多重投稿回避用 =========
if not (START_DATE <= today <= END_DATE):
    print("期間外なので投稿しません")
    sys.exit(0)

if not (hour == 10 and minute == 0):
    print("10時丁度の投稿重複の為投稿しません")
    sys.exit(0)

print("条件一致：投稿します")

# ========= 環境変数 =========
ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")
INSTANCE_URL = os.getenv("MASTODON_INSTANCE_URL")

if not ACCESS_TOKEN or not INSTANCE_URL:
    raise ValueError("環境変数が設定されてないエラー")

# ========= Mastodon接続 =========
mastodon = Mastodon(
    access_token=ACCESS_TOKEN,
    api_base_url=INSTANCE_URL
)

# ========= 投稿文 =========
messages = [
    "おはよ～。ログボ取った～？",
    "おはよ！ ログボのお時間です",
    ":kb_ohayo2: ログボ取ってね～",
    ":kb_ohayo2: ログボ取って偉い",
    ":kb_ohayo2: 今日もログボってこ！"
]

message = random.choice(messages)

status = mastodon.status_post(message)
print("投稿成功:", status.url)
