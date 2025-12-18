import os
import random
from datetime import datetime, date, timedelta
from mastodon import Mastodon
import sys

# ========= 設定 =========
START_DATE = date(2025, 12, 16)
END_DATE   = date(2026, 1, 26)

# GitHub Actions は UTC
TARGET_TIMES = {
    "morning": (1, 0),   # 10:00 JST
    "evening": (11, 0),  # 20:00 JST
}

LAST_POST_FILE = "last_post.txt"

# ========= 現在時刻 =========
now = datetime.utcnow()
today = now.date()
hour = now.hour
minute = now.minute

print(f"UTC現在時刻: {hour:02}:{minute:02}")

# ========= 期間チェック =========
if not (START_DATE <= today <= END_DATE):
    print("期間外なので投稿しません")
    sys.exit(0)

# ========= 時刻判定 =========
post_type = None
for key, (h, m) in TARGET_TIMES.items():
    if hour == h and minute == m:
        post_type = key
        break

if not post_type:
    print("投稿時刻ではありません")
    sys.exit(0)

# ========= 二重投稿防止 =========
today_key = f"{today}_{post_type}"

if os.path.exists(LAST_POST_FILE):
    with open(LAST_POST_FILE, "r") as f:
        last = f.read().strip()
        if last == today_key:
            print("すでに投稿済みです")
            sys.exit(0)

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
    "ログボ取ってね :blobcat_ofton: "
]

if post_type == "morning":
    message = random.choice(morning_messages)
else:
    message = random.choice(evening_messages)

# ========= 投稿 =========
status = mastodon.status_post(message)
print("投稿成功:", status.url)

# ========= 投稿記録 =========
with open(LAST_POST_FILE, "w") as f:
    f.write(today_key)
