from itertools import chain
import praw
import re
import sqlite3
import time
from modules import patterns
import modules.blacklist as blacklist
import modules.messages as messages
import modules.translate as translate


conn = sqlite3.connect('bot.db')
c = conn.cursor()

# Authenticating with Reddit
reddit = praw.Reddit('translate_bot')

# Stream of comments
comment_stream = reddit.subreddit('all').stream.comments(pause_after=-1)

# Stream of inbox messages
inbox_stream = praw.models.util.stream_generator(reddit.inbox.unread, pause_after=-1)

# Defines
executed_timestamp = time.time() # Stores the current time in seconds since the Epoch. Used later to prevent the bot from replying to old comment every time it is executed.

blacklisted_subs = set(chain(*c.execute('SELECT * from Blacklist').fetchall()))
valid_langs = set(chain(*c.execute('SELECT * from CountryCodes').fetchall()))


def main():
    while True:
        try:
            for comment in comment_stream:
                if comment is None:
                    break

                if comment.created_utc > executed_timestamp:
                    if comment.subreddit not in blacklisted_subs:
                        if comment.body.startswith(patterns.main_trigger):
                            if comment.parent_id == comment.link_id:
                                author = str(comment.author)

                                comment_match = re.match(patterns.full_trigger_pattern, comment.body)

                                try:
                                    lang, query = comment_match.groups()
                                    lang = lang.lower()

                                    if lang in valid_langs:
                                        translation_response = translate.translate(f'{lang}', f'{query}')
                                        comment.reply(messages.translated_comment(query, **translation_response))
                                    # If the parameters passed to "lang" is not recognized by Yandex, send a message to the user notifying him.
                                    else:
                                        reddit.redditor(author).message('Notification from TranslateService', messages.syntax_error(author))
                                # If the message does not match the pattern, send a syntax message to the user.
                                except AttributeError as e:
                                    print(e)
                                    reddit.redditor(author).message('Notification from TranslateService', messages.syntax_error(author))

            for msg in inbox_stream:
                if msg is None:
                    break

                if msg.created_utc > executed_timestamp:
                    msg_author = str(msg.author)
                    msg_subject = msg.subject.lower()
                    sub_name = msg.body.lower()
                    sub_mods = blacklist.get_moderator_set(sub_name)

                    if msg_author in sub_mods:
                        if msg_subject == 'blacklist':
                            if sub_name not in blacklisted_subs:
                                blacklisted_subs.add(sub_name)
                                blacklist.add_to_blacklist(sub_name=sub_name, sql_connection=conn, sql_cursor=c)
                                reddit.redditor(msg_author).message('Notification from TranslateService',
                                                                    messages.blacklist_action(msg_author, sub_name, 'blacklisted'))
                        elif msg_subject == 'unblacklist':
                            if sub_name in blacklisted_subs:
                                blacklisted_subs.remove(sub_name)
                                blacklist.remove_from_blacklist(sub_name=sub_name, sql_connection=conn, sql_cursor=c)
                                reddit.redditor(msg_author).message('Notification from TranslateService',
                                                                    messages.blacklist_action(msg_author, sub_name, 'unblacklisted'))
        except Exception as e:
            continue


if __name__ == '__main__':
    main()
