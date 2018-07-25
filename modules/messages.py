signature = '''---\n\n''' + \
            '''^(Beep boop, I'm a bot. |) ^[Creator](https://www.reddit.com/user/Carlos_Menezes/) ^· ^Source ^· ^[Blacklist](https://pastebin.com/MEDMa0Xp)'''


def syntax_error(user):
    '''
    Make a message to send to the user informing them of a syntax error.
    :param user: str, a username
    :return: A formatted str to send to user.
    '''
    message = f'''Hello, **{user}**!\n\n''' + \
               '''It seems that you tried to use my services. However, you did not pass the correct parameters to the command `@translate`.\n\n''' + \
               '''The correct usage is: `@translate [lang] [message]`.\n\n''' + \
               '''The following is an example of how to use this command: `!translate ru Hello! I'm feeling very good today. Thanks for using this bot.`.\n\n''' + \
               '''For a list of available languages, please refer to [Supported Languages of the Yandex API](https://tech.yandex.com/translate/doc/dg/concepts/api-overview-docpage/#languages) list.\n\n''' + \
              f'''{signature}'''
    return message


def blacklist_action(moderator, subreddit, action):
    '''
    :param moderator: str, moderator name
    :param subreddit: str, subreddit of moderator
    :param action: str, either 'blacklisted' or 'unblacklisted'
    :return: A formatted str to send to the moderator of the subreddit
    '''
    message = f'''Hello, **{moderator}**!\n\n''' + \
              f'''Your subreddit, [{subreddit}](https://reddit.com/r/{subreddit}) has been {action}. If you wish to undo this action, check the link below\n\n''' + \
               '''([blacklist](https://pastebin.com/MEDMa0Xp)).\n\n''' + \
              f'''{signature}'''
    return message


def translated_comment(orignal_text, **kwargs):
    '''
    :param orignal_text: original comment body, pre-translation
    :param kwargs: the translation dictionary from yandex
    :return: A formatted str to make a comment reply
    '''
    message = f'''**Original text:** {orignal_text}\n\n''' + \
              f'''**Translated text ({kwargs["lang"]}):** {kwargs["text"][0]}\n\n''' + \
              f'''{signature}'''
    return message

