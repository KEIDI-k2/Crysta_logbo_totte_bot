import os
import random
from datetime import datetime
from mastodon import Mastodon

# 現在の日付を取得
current_date = datetime.now().date()

# 休止期間の開始日と終了日を設定
start_date = datetime(current_date.year, 12, 16).date()  # 例12月7日
end_date = datetime(current_date.year + 1, 1, 26).date()  # 例1月30日（次の年）

# 実行範囲内かどうかを確認
if start_date <= current_date <= end_date:
    print("現在ログボ期間なので投稿しま！")

    # 環境変数の取得
    MASTODON_ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")
    MASTODON_INSTANCE_URL = os.getenv("MASTODON_INSTANCE_URL")

    # アクセストークンとインスタンスURLの確認
    if not MASTODON_ACCESS_TOKEN or not MASTODON_INSTANCE_URL:
        raise ValueError("アクセストークンかインスタンスURLが設定されてないっぽい。稀によくある")

    # kmyに接続
    mastodon = Mastodon(
        access_token=MASTODON_ACCESS_TOKEN,
        api_base_url=MASTODON_INSTANCE_URL
    )

    # ランダム選択
    morning_quotes = [
        "おはよ～。ログボ取った～？",
        "おはよ！ ログボのお時間です",
        ":kb_ohayo2: ログボ取ってね～",
        ":kb_ohayo2: ログボ取って偉い",
        ":kb_ohayo2: 今日もログボってこ！"
    ]

    message = random.choice(morning_quotes)

    # 投稿
    status = mastodon.status_post(message)

    print(f"投稿成功: {status.url}")

else:
    print("期間外なのでお休みです")

