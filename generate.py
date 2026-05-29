import os
import requests

token = os.environ["LINE_TOKEN"]
user_id = os.environ["LINE_USER_ID"]

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
}

data = {
    "to": user_id,
    "messages": [{"type": "text", "text": "テスト：LINEに届きました！"}]
}

r = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=data)
print(r.status_code)
print(r.text)
