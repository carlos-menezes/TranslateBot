import praw
from praw.exceptions import APIException, ClientException
from prawcore.exceptions import PrawcoreException
import re
import requests
from requests_html import HTMLSession
import time
from modules import patterns
from modules.database import Database
import modules.messages as messages
import modules.translate as translate


class TranslateBot:
    def __init__(self):
        # Stores the current time in seconds since the Epoch. Used later to prevent the bot from replying to old comment every time it is executed.
        self.executed_timestamp = time.time()
        self.database = Database()
        # Authenticating with Reddit
        self.reddit = praw.Reddit('translate_bot')
        # Stream of comments
        self.comment_stream = self.reddit.subreddit('testingground4bots').stream.comments(pause_after=-1)
        # Stream of inbox messages
        self.inbox_stream = praw.models.util.stream_generator(self.reddit.inbox.unread, pause_after=-1)
        # Start
        self.main()

    def get_moderator_set(self, sub_name):
        url = f'https://old.reddit.com/r/{sub_name}/about/moderators'
        session = HTMLSession()
        mods = set()
        response = None
        while response is None:
            try:
                response = session.get(url)
                response.raise_for_status()
                users = response.html.find('span.user')
                for user in users[1:]:
                    mod = user.text.split('\xa0')[0]
                    mods.add(mod)
            except (requests.exceptions.HTTPError, ConnectionError) as exc:
                print(exc)
                time.sleep(5)
        return mods

    def read_comments(self):
        for comment in self.comment_stream:
            if comment is None:
                break
            if comment.created_utc > self.executed_timestamp:
                if comment.subreddit not in self.database.blacklisted_subs:
                    if comment.body.startswith(patterns.main_trigger):
                        if comment.parent_id == comment.link_id:
                            author = str(comment.author)
                            comment_match = re.match(patterns.full_trigger_pattern, comment.body)
                            try:
                                lang, query = comment_match.groups()
                                lang = lang.lower()
                                if lang in self.database.valid_langs:
                                    translation_response = translate.translate(f'{lang}', f'{query}')
                                    print(f'replying to: {author}')
                                    comment.reply(messages.translated_comment(query, **translation_response))
                                # If the parameters passed to "lang" is not recognized by Yandex, send a message to the user notifying him.
                                else:
                                    print(f'sending syntax error message to: {author}')
                                    self.reddit.redditor(author).message('Notification from TranslateService',
                                                                         messages.syntax_error(author))
                            # If the message does not match the pattern, send a syntax message to the user.
                            except AttributeError as e:
                                print(e)
                                self.reddit.redditor(author).message('Notification from TranslateService',
                                                                     messages.syntax_error(author))

    def read_messages(self):
        for msg in self.inbox_stream:
            if msg is None:
                break
            if msg.created_utc > self.executed_timestamp:
                msg_author = str(msg.author)
                msg_subject = msg.subject.lower()
                sub_name = msg.body.lower()
                sub_mods = self.get_moderator_set(sub_name)
                if msg_author in sub_mods:
                    if msg_subject == 'blacklist':
                        if sub_name not in self.database.blacklisted_subs:
                            self.database.add_to_blacklist(sub_name)
                            print(f'sending blacklist add message to: {msg_author}')
                            self.reddit.redditor(msg_author).message('Notification from TranslateService',
                                                                      messages.blacklist_action(msg_author, sub_name, 'blacklisted'))
                    elif msg_subject == 'unblacklist':
                        if sub_name in self.database.blacklisted_subs:
                            self.database.remove_from_blacklist(sub_name)
                            print(f'sending blacklist remove message to: {msg_author}')
                            self.reddit.redditor(msg_author).message('Notification from TranslateService',
                                                                     messages.blacklist_action(msg_author, sub_name, 'unblacklisted'))

    def main(self):
        while True:
            try:
                self.read_messages()
                self.read_comments()
            except (APIException, ClientException, PrawcoreException) as e:
                print(e)
                pass


if __name__ == '__main__':
    TranslateBot()
