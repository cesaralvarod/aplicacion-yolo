# https://api.telegram.org/
# https://core.telegram.org/bots/api/


from dotenv import load_dotenv, dotenv_values
import requests

load_dotenv()

config = dotenv_values(".env")

# Telegram token
TOKEN_BOT = config['TELEGRAM_TOKEN_BOT']
CHAT_ID = config['TELEGRAM_CHAT_ID']


def sendImageTelegram(filename, caption):

    API_TELEGRAM = "https://api.telegram.org/bot"

    URL_REQUEST = API_TELEGRAM + TOKEN_BOT + "/sendPhoto"

    data = {
        'chat_id': CHAT_ID, 'caption': caption}

    files = {'photo': (filename, open(filename, 'rb'))}

    try:
        res = requests.post(URL_REQUEST, data=data, files=files).json()

        if(res['ok']):
            print("Message sent")
        else:
            print(res)
    except Exception as exception:
        print(exception)
