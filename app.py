from itertools import chain
import praw
import re
import requests
import sqlite3
import time
from modules import patterns
from modules.blacklist import *
from modules.messages import syntax_message, signature, un_blacklist_message
from modules.translate import *


conn = sqlite3.connect('bot.db')
c = conn.cursor()

# Authenticating with Reddit
reddit = praw.Reddit('translate_bot')

# Stream of comments
comments = reddit.subreddit('all').stream.comments(pause_after=-1)

# Stream of inbox messages
inbox_stream = praw.models.util.stream_generator(reddit.inbox.unread, pause_after=-1)

# Defines
executed_timestamp = time.time() # Stores the current time in seconds since the Epoch. Used later to prevent the bot from replying to old comments everytime it is executed.

blacklisted = c.execute('SELECT * from Blacklist').fetchall()
blacklisted_subs = [row[0] for row in blacklisted]

lang_list = list(chain(*c.execute('SELECT * from CountryCodes').fetchall()))


while True:
    try:
        for comment in comments:
            if comment is None:
                break

            if comment.created_utc > executed_timestamp:
                if comment.subreddit not in blacklisted_subs:
                    if str(comment.body).startswith(patterns.main_trigger):
                        if comment.parent_id == comment.link_id:                    
                            author = str(comment.author)

                            comment_match = re.search(patterns.full_trigger_pattern, comment.body)
                            
                            try:
                                lang, query = comment_match.groups()
                                codes = [row[0] for row in lang_list]

                                if str(lang) not in codes: # If the parameters passed to "lang" is not recognized by Yandex, send a message to the user notifying him.
                                    reddit.redditor(author).message('Notification from TranslateService', syntax_message(author))

                                else:
                                    result = translate(f'{lang}', f'{query}')
                                    message = f"""**Original text:** {str(query)}


    **Translated text ({result['lang']}):** {result['text'][0]}


    {signature}
                                    """

                                    comment.reply(message)

                            except AttributeError as e: # If the message does not match the pattern, send a syntax message to the user.
                                print(e)
                                reddit.redditor(author).message('Notification from TranslateService', syntax_message(author))
        

        for msg in inbox_stream:
            if msg is None:
                break

            if msg.created_utc > executed_timestamp:
                if 'blacklist' == str(msg.subject).lower():
                    sub_name = str(msg.body).lower()
                    mods = get_mod_list(sub_name)
                    
                    if msg.author in mods:
                        if sub_name not in blacklisted_subs:
                            blacklisted_subs.append(sub_name)
                            c.execute('INSERT INTO Blacklist(SubName) VALUES (?)', (sub_name,))
                            conn.commit()

                            reddit.redditor(str(msg.author)).message('Notification from TranslateService', un_blacklist_message(str(msg.author), str(sub_name), 'blacklisted'))

                if 'unblacklist' == str(msg.subject).lower():
                    sub_name = str(msg.body).lower()
                    mods = get_mod_list(sub_name)

                    if msg.author in mods:
                        if sub_name in blacklisted_subs:
                            blacklisted_subs.remove(sub_name)

                            c.execute('DELETE FROM Blacklist WHERE SubName = ?', (sub_name,))
                            conn.commit()

                            reddit.redditor(str(msg.author)).message('Notification from TranslateService', un_blacklist_message(str(msg.author), str(sub_name), 'unblacklisted'))
    except Exception as e:
        continue
