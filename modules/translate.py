from modules.parseconfig import yandex_api
import requests
from time import sleep

def translate(lang, text):
    url = f'https://translate.yandex.net/api/v1.5/tr.json/translate?key={yandex_api}&lang={lang}&text={text}&format=plain'

    response = None
    while response is None:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except (requests.exceptions.HTTPError, ConnectionError) as exc:
            print(exc)
            sleep(5)
    return response.json()