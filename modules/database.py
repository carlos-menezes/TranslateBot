from itertools import chain
import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('./bot.db')
        self.c = self.conn.cursor()
        self.blacklisted_subs = set(chain(*self.c.execute('SELECT * from Blacklist').fetchall()))
        self.valid_langs = set(chain(*self.c.execute('SELECT * from CountryCodes').fetchall()))

    def add_to_blacklist(self, sub_name):
        self.blacklisted_subs.add(sub_name)
        self.c.execute('INSERT INTO Blacklist(SubName) VALUES (?)', (sub_name,))
        self.conn.commit()

    def remove_from_blacklist(self, sub_name):
        self.blacklisted_subs.remove(sub_name)
        self.c.execute('DELETE FROM Blacklist WHERE SubName = ?', (sub_name,))
        self.conn.commit()