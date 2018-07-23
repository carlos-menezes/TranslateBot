signature = """---
^(Beep boop, I'm a bot. |) ^[Creator](https://www.reddit.com/user/Carlos_Menezes/) ^· ^Source ^· ^[Blacklist](https://pastebin.com/MEDMa0Xp)"""    


def syntax_message(user):
    syntax_message = f"""Hello, **{user}**!
    
It seems that you tried to use my services. However, you did not pass the correct parameters to the command `@translate`.

The correct usage is: `@translate [lang] [message]`.

The following is an example of how to use this command: `!translate ru Hello! I'm feeling very good today. Thanks for using this bot.`.


For a list of available languages, please refer to [Supported Languages of the Yandex API](https://tech.yandex.com/translate/doc/dg/concepts/api-overview-docpage/#languages) list.


{signature}
"""
    return str(syntax_message)

    
def un_blacklist_message(user, sub, condition):
    un_blacklist_message = f"""Hello, **{user}**!

Your subreddit, [{sub}](https://reddit.com/r/{sub}) has been {condition}. If you wish to undo this action, check the link below ([blacklist](https://pastebin.com/MEDMa0Xp)).


{signature}"""

    return un_blacklist_message

