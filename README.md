# Translate Bot for Reddit
A Reddit bot that translate a message when queried.

---

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

1. Install [Python](https://python.org).
2. Clone this repository.
3. Open a terminal window inside the folder the project is located and create a virtual environment: `$ py -m venv venv`.
4. Activate the virtual environment: `$ cd venv/Scripts/activate`.
5. Install `requirements.txt`: `$ pip install -r requirements.txt`.
6. Open `praw.ini` and edit the values at the bottom. **Having trouble figuring out what to write?** Check [this](https://progur.com/2016/09/how-to-create-reddit-bot-using-praw4.html#registering-the-bot) link.
7. Run `$ py app.py`.
---

## How does it work?

Any user can use the following command syntax to summon this bot: `@translate lang message`. If the message does not contain the right parameters (to make it short: if length of `lang` > 2; if `message` < 1; if `lang` does not exist in the Yandex API), the bot will send a message to the user with clear instructions of how to use the bot.

![Instructions](https://i.imgur.com/s45F0eZ.png)
*The message containing the instructions.*

To comply with bottiquette, I've added an option to (un)blacklist subreddits on the fly (and you can read about how that works [here](https://pastebin.com/MEDMa0Xp)). This was a great opportunity to get some experience with databases.

![Blacklisted](https://i.imgur.com/Yp3irxH.png)
![Unblacklisted](https://i.imgur.com/0zJ3STJ.png)

If, however, the subreddit you summon the bot to isn't blacklisted; the language you provided is available in the Yandex API; and you provided a message with more than one character, the bot will reply to your comment in this fashion:

![Success](https://i.imgur.com/oygvnGE.png)
---


## Built With
* [PRAW](https://praw.readthedocs.io/en/latest/) — The Python Reddit API wrapper.
* [Regex101](https://regex101.com/) — Helped a lot with regular expressions. I had never worked with regular expressions and it took me 5 minutes to get the gist of it with the help of this tool.
* [Requests-HTML](https://github.com/kennethreitz/requests-html) — Used to scrape the list of moderators for the (un)blacklisting feature.
* [Requests](http://docs.python-requests.org/en/master/) — Used to GET and POST data.

---

## Authors
* **Carlos Menezes** — *Initial work* - [c-mnzs](https://github.com/c-mnzs)

