import sqlite3
import os

class Cacher(sqlite3.Connection):
    FILE = os.getenv("PREFIX")
    def __init__(self):
        first_time = os.path.isfile(self.FILE)
        sqlite3.Connection.__init__(self, self.FILE)
        if first_time:
            self.setup()
    def setup(self):
        self.execute("""
        CREATE TABLE ANIME_DATA
        (NAME CHAR(30),
        SOURCE CHAR(15),
        EP_COUNT NUMBER)""")
        # TODO: Add logic fir ading and searching
