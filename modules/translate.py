from modules.parseconfig import yandex_api
import requests

def translate(lang, text):
    url = f'https://translate.yandex.net/api/v1.5/tr.json/translate?key={str(yandex_api)}&lang={lang}&text={text}&format=plain'

    r = requests.get(url)

    if r.status_code == 200:
        r = r.json()
        return r