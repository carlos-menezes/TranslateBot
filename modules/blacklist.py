import praw
from requests_html import HTMLSession

url = "https://old.reddit.com/r/{}/about/moderators"
session = HTMLSession()

def get_mod_list(sub):
    
    mods = []

    r = session.get(url.format(sub))

    if r.status_code == 200:
        users = r.html.find('span.user')
        for user in users[1:]:
            moderator = user.text.split("\xa0")[0]
            mods.append(moderator)

        return mods
