import os
import random
import sys
from datetime import datetime, date, timedelta, timezone
from mastodon import Mastodon

# ========= 設定 =========
START_DATE = date(2025, 12, 16)
END_DATE   = date(2026, 1, 26)

# ========= JST =========
JST = timezone(timedelta(hours=9))

# ========= 現在時刻 =========
now = datetime.now(timezone.utc).astimezone(JST)
today = now.date()
hour = now.hour
minute = now.minute

# ========= 期間チェック =========
if not (START_DATE <= today <= END_DATE):
    print("期間外なので投稿なし")
    sys.exit(0)

# ========= 時間帯判定 =========
if hour == 10 and 0 <= minute <= 31: # 10:00〜8:30
    slot = "morning"
elif hour == 20 and 0 <= minute <= 31: # 20:00〜20:30
    slot = "evening"
else:
    print("投稿時間帯外")
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

# ========= Mastodon側で二重防止 =========
last = mastodon.account_statuses(mastodon.me()["id"], limit=1)

if last:
    last_time = last[0]["created_at"].astimezone(JST)

    if last_time.date() == today:
        if slot == "morning" and last_time.hour == 10:
            print("既に朝投稿済み")
            sys.exit(0)
        if slot == "evening" and last_time.hour == 20:
            print("既に夜投稿済み")
            sys.exit(0)

# ========= 投稿文 =========
morning_messages = [
    "おはよ～。ログボ取った～？",
    "おはよ！ ログボのお時間です。",
    ":kb_ohayo2: ログボ取ってね～:ablobcatpnd_yurayura:",
    ":kb_ohayo2: ログボ取って偉い！:ablobcatcheersparkles:",
    ":kb_ohayo2: 今日もログボってこ！:ablobcatbongotap:"
]

evening_messages = [
    "こんばんは～。ログボ取りました？:blobcatpeek2:",
    "夜ログボのお時間です🌙",
    ":kb_otukare: ログボ取りましょ:blobhai:",
    ":kb_otukare: ログボ取れたね！",
    "ログボ取って寝 :blobcat_ofton:"
]

message = random.choice(
    morning_messages if slot == "morning" else evening_messages
)

# ========= 投稿 =========
status = mastodon.status_post(message)
print("投稿成功:", status.url)
