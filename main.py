import requests
import json
import os

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Origin': 'https://webstatic-sea.mihoyo.com',
    'Connection': 'keep-alive',
    'Referer': 'https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id=e202102251931481&lang=en-us',
    'Cache-Control': 'max-age=0',
}

params = (
    ('lang', 'en-us'),
    ('act_id', "e202102251931481"),
)

cookies = {}


def parse_cookies(filename):
    file = open(filename)
    data = json.load(file)
    for cookie in data:
        cookies[cookie["name"]] = cookie["value"]

# get current status
def get_status():
    try:
        response = requests.get('https://hk4e-api-os.mihoyo.com/event/sol/info',
                                headers=headers, params=params, cookies=cookies)
        text = response.json()
        return text["message"], text["data"]["total_sign_day"], text["data"]["today"]
    except Exception as e:
        print(e)
        return e


def claim_daily():
    data = {'act_id': "e202102251931481"}

    try:
        response = requests.post('https://hk4e-api-os.mihoyo.com/event/sol/sign',
                                 headers=headers, params=params, cookies=cookies, json=data)
        text = response.json()
        return text["message"]
    except Exception as e:
        print(e)
        return

# telegram bot to send notification
def telegram_bot_send(bot_message, chat_id):
    bot_token = os.environ['TOKEN']
    bot_chat_id = chat_id
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chat_id + \
        '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

# main function lambda handler
def main(event, context):
    for cookie in [{"cookie": "cookie.json", "chat_id": "chat_id"}, {"cookie": "cookie.json", "chat_id": "chat_id"}]:
        parse_cookies(cookie["cookie"])
        text = str(get_status())
        text = text + "\n" + claim_daily()
        telegram_bot_send(text, cookie["chat_id"])
        print(cookie["cookie"], "success")
