import praw
import requests
from requests_html import HTMLSession
from time import sleep

url = 'https://old.reddit.com/r/{}/about/moderators'
session = HTMLSession()


def remove_from_blacklist(**kwargs):
    sub_name = kwargs['sub_name']
    kwargs['sql_cursor'].execute('DELETE FROM Blacklist WHERE SubName = ?', (sub_name,))
    kwargs['sql_connection'].commit()


def add_to_blacklist(**kwargs):
    sub_name = kwargs['sub_name']
    kwargs['sql_cursor'].execute('INSERT INTO Blacklist(SubName) VALUES (?)', (sub_name,))
    kwargs['sql_connection'].commit()


def get_moderator_set(sub):
    mods = set()

    response = None
    while response is None:
        try:
            response = session.get(url.format(sub))
            response.raise_for_status()
            users = response.html.find('span.user')
            for user in users[1:]:
                mod = user.text.split('\xa0')[0]
                mods.add(mod)
        except (requests.exceptions.HTTPError, ConnectionError) as exc:
            sleep(5)
    return mods




