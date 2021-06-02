import sqlite3
import os
from collections import namedtuple as _nt

AnimeDescriptor = _nt("AnimeDescriptor", 'name src episode_count')
MAX_UNCOMMITED_ISERTIONS = 1
MAX_UNCOMMITED_UPDATES = 1

class Cacher(sqlite3.Connection):
	FILE = os.getenv("HOME") + '/anime.db'
	def __init__(self):
		first_time = not os.path.isfile(self.FILE)
		sqlite3.Connection.__init__(self, self.FILE)
		self.__cache = CacheDict()
		self.__uncommited_ins = 0
		self.__uncommited_upd = 0
		if first_time:
			self.setup()
	def __exit__(self, type, value, traceback):
		sqlite3.Connection.close(self)
	def close(self):
		self.commit()
		sqlite3.Connection.close(self)
	def register_anime(self, name: str, source: str, ep_count: int, cache=True):
		cursor = self.execute(f"""
		INSERT INTO ANIME_DATA
		VALUES ('{name}', '{source}', {ep_count})
		""")
		if cache:
			self.__cache[name] = AnimeDescriptor(name, source, ep_count)
		self.__uncommited_ins += 1
		if self.__uncommited_ins >= MAX_UNCOMMITED_ISERTIONS:
			self.commit()
			self.__uncommited_ins = 0
	def update_anime(self, iname: str, new_data: AnimeDescriptor = None,
									 source: str = None, ep_count: int = None):
		sql_statement = "UPDATE ANIME_DATA\n"
		if new_data is not None:
			_, source, ep_count = new_data
		if iname in self.__cache:
			anime = self.__cache[iname]
			if source is not None:
				anime.src = source
				sql_statement += f"SET SOURCE = '{source}'"
			if ep_count is not None:
				anime.episode_count = ep_count
				sql_statement += f"""{'SET'
															if source is not None
															else ','} EP_COUNT {ep_count}\n"""
			if (name, ep_count) == (None, None):
				return
			else:
				sql_statement += f"WHERE LOWER(NAME) = '{iname.lower()}'"
				cursor = self.execute(sql_statement)
				cursor.close()
				self.__uncommited_ins += 1
				if self.__uncommited_upd >= MAX_UNCOMMITED_UPDATES:
					self.commit()
					self.__uncommited_upd = 0
	def get_anime_data(self, iname: str, cache=True) -> AnimeDescriptor:
		if cache and iname in self.__cache:
			return self.__cache[iname]
		else:
			cursor = self.execute(f"""
			SELECT NAME, SOURCE, EP_COUNT
			FROM ANIME_DATA
			WHERE LOWER(NAME) = '{iname.lower()}'
			""")
			data = cursor.fetchall()
			if len(data) == 0:
				return None
			if cache:
				anime = AnimeDescriptor(*data[0])
				self.__cache[iname] = anime
				return anime

	def setup(self):
		cursor = self.execute("""
		CREATE TABLE ANIME_DATA
		(NAME TEXT,
		SOURCE TEXT,
		EP_COUNT INTEGER)
		""")
		self.register_anime('Naruto-Shippuden', 'v5.4animu.me', 750)

class CacheDict(dict):
	def __setitem__(self, key: str, value: AnimeDescriptor):
		dict.__setitem__(self, key.lower(), value)
	def __getitem__(self, key: str) -> AnimeDescriptor:
		dict.__getitem__(self, key.lower())
	def __contains__(self, key: str) -> bool:
		return dict.__contains__(self, key.lower())
