import os
import anthropic
import requests
from datetime import datetime

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

STYLE_EXAMPLES = """
本気で人と仲間とお客様と向き合っているか？
死ぬ気で素直に本気で法人飛び込みに賭けたから。確実に強くなってきている。
数字欲しさの薄さとペラペラ具合が見透かされるから、結局数字も出ない、紹介も出ない。
今やらなければ、どうせ遅かれ早かれ詰む。
負け癖を絶対につけるな。下方修正癖を絶対につけるな。
抗え、逆らえ、歯向かえ、もがけ。自分の目標は落とすものでも妥協するものでもない。

うまくいかない時期は、才能がない時期じゃない。
結果が出る前に辞めるかどうかを試されてる時期だと思う。
悔しいなら、まだ終わってない。苦しいなら、まだ前に進もうとしてる。
人生は、楽をした人が勝つんじゃない。覚悟を決めた人が勝つ。

自分が本気でやろうとしているのは、ただAIを使って楽をすることじゃない。
AIを使って、仕事の質と人生そのものを変えること。
情報を知ってる営業は強い。でも、全部を自分で調べ続けるのは限界がある。だからこそAIを使う。
完璧になった人の話じゃなく、普通の営業マンがAIを使いながら試行錯誤してる過程の方がリアルで価値がある。
AIは魔法じゃない。でも、行動する人間にとっては武器になる。
"""

PROMPT = f"""あなたは保険営業×AI発信をしている日本人です。
以下の文体・熱量・思想で今日の投稿案を作ってください。

【文体のルール】
- 短い文をリズムよく並べる
- 「だから」「でも」「だからこそ」をよく使う
- 「〜か？」で問いかけを入れる
- きれいにまとめすぎない。本音・リアル感を出す
- 改行を多用する
- 「必ず」「絶対に」「どうせ」などの強い言葉を使う
- AIっぽい綺麗な文章にしない

【過去の投稿（文体の参考）】
{STYLE_EXAMPLES}

【今日の日付】{datetime.now().strftime('%Y年%m月%d日')}

【出力形式】
━━━━━━━━━━━━━━━━
📝 note投稿案（長文）
━━━━━━━━━━━━━━━━
（600〜1000文字）

━━━━━━━━━━━━━━━━
⚡ 短い投稿①
━━━━━━━━━━━━━━━━
（100〜200文字）

━━━━━━━━━━━━━━━━
⚡ 短い投稿②
━━━━━━━━━━━━━━━━
（100〜200文字）

━━━━━━━━━━━━━━━━
🎯 タイトル案3つ
━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━
🔥 フックになる一文
━━━━━━━━━━━━━━━━

毎回違うテーマで作ること。ジャンルはAI実践・営業・覚悟・失敗・成長・挑戦からランダムに選ぶ。"""


def generate_posts():
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        messages=[{"role": "user", "content": PROMPT}]
    )
    return message.content[0].text


def send_to_line(text):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['LINE_TOKEN']}"
    }
    data = {
        "to": os.environ["LINE_USER_ID"],
        "messages": [{"type": "text", "text": text[:5000]}]
    }
    response = requests.post(url, headers=headers, json=data)
    print(f"LINE送信結果: {response.status_code}")
    return response.status_code


if __name__ == "__main__":
    print("投稿案を生成中...")
    posts = generate_posts()
    print(posts)
    print("\nLINEに送信中...")
    send_to_line(posts)
    print("完了！")
