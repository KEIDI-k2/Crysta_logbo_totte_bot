import os
import random
from datetime import datetime, date
from mastodon import Mastodon
import sys
import json

# ========= 設定 =========
START_DATE = date(2025, 12, 16)
END_DATE   = date(2026, 1, 26)

POST_TIMES = {
    10: "morning",
    20: "evening",
}

LOG_FILE = "last_post.json"

# ========= 現在時刻（UTC → JST） =========
now = datetime.utcnow()
today = now.date()
hour = now.hour + 9  # JST
if hour >= 24:
    hour -= 24

# ========= 期間チェック =========
if not (START_DATE <= today <= END_DATE):
    print("期間外なので投稿なし")
    sys.exit(0)

# ========= 時刻チェック =========
if hour not in POST_TIMES:
    print("投稿時間外")
    sys.exit(0)

slot = POST_TIMES[hour]

# ========= 二重投稿防止 =========
key = f"{today}_{slot}"

if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        if data.get("last_post") == key:
            print("既に投稿済みです")
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
    "夜ログボのお時間です🌙",
    ":kb_otukare: ログボ取りましょ",
    ":kb_otukare: ログボ取れたね！",
    "ログボ取ってね :blobcat_ofton: "
]

if slot == "morning":
    message = random.choice(MORNING_MESSAGES)
else:
    message = random.choice(EVENING_MESSAGES)

# ========= 投稿 =========
status = mastodon.status_post(message)
print("投稿成功:", status.url)

# ========= 記録 =========
with open(LOG_FILE, "w", encoding="utf-8") as f:
    json.dump({"last_post": key}, f, ensure_ascii=False)

print("投稿記録更新完了")
