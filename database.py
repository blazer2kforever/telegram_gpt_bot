import sqlite3
from sqlite3 import Error
from datetime import datetime

INFO_SQL_CONNECT = 'Connecting SQL'
INFO_SQL_CREATE_TABLE = 'Creating SQL table'
INFO_SQL_INSERT = 'Proceeding SQL INSERT'
INFO_SQL_DELETE = 'Proceeding SQL DELETE'
INFO_SQL_GET = 'Proceeding SQL GET'

ERROR_SQL_CONNECT = 'Cant connect to SQL'
ERROR_SQL_CREATE_TABLE = 'Cant create SQL table'
ERROR_SQL_INSERT = 'Cant proceed SQL INSERT'
ERROR_SQL_DELETE = 'Cant proceed SQL DELETE'
ERROR_SQL_GET = 'Cant proceed SQL SELECT'

class Database:
  def __init__(self, db_name, terminal):
      self.db_name = db_name
      self.db = None

      self.terminal = terminal

  def connect(self):
    try:
        self.terminal.p_system(INFO_SQL_CONNECT)
        self.db = sqlite3.connect(self.db_name, check_same_thread=False)
    except Error as e:
        self.terminal.p_error(f'{ERROR_SQL_CONNECT} : {e}')

  def create_history_table(self):
      try:
          self.terminal.p_system(INFO_SQL_CREATE_TABLE)
          cursorObj = self.db.cursor()
          cursorObj.execute(
              "CREATE TABLE IF NOT EXISTS history(id integer PRIMARY KEY, username text, user_id text, role text, content text, created_at date)")
          self.db.commit()
      except Error as e:
          self.terminal.p_error(f'{ERROR_SQL_CREATE_TABLE} : {e}')


  def insert_message(self, username, user_id, role, message):
      try:
          self.terminal.p_system(INFO_SQL_INSERT)
          cursorObj = self.db.cursor()
          sqlite_insert_query = f"""INSERT INTO history
                                    (username, user_id, role, content, created_at)
                                    VALUES
                                    ('{username}', '{user_id}', '{role}', '{message}', '{datetime.now()}');"""
          cursorObj.execute(sqlite_insert_query)
          self.db.commit()
      except Error as e:
          self.terminal.p_error(f'{ERROR_SQL_INSERT} : {e}')

  def get_history(self, user_id):
      try:
          self.terminal.p_system(INFO_SQL_GET)
          cursorObj = self.db.cursor()
          cursorObj.execute(
              f'SELECT * FROM history WHERE user_id = "{user_id}"')

          return cursorObj.fetchall()
      except Error as e:
          self.terminal.p_error(f'{ERROR_SQL_GET} : {e}')

  def delete_history(self, user_id):
      try:
          self.terminal.p_system(INFO_SQL_DELETE)
          cursorObj = self.db.cursor()
          cursorObj.execute(
              f"DELETE FROM history WHERE user_id = '{user_id}'")
          self.db.commit()
      except Error as e:
          self.terminal.p_error(f'{ERROR_SQL_DELETE} : {e}')

  def get_users(self):
      try:
          cursorObj = self.db.cursor()
          cursorObj.execute("SELECT DISTINCT user_id, username FROM history")
          rows = cursorObj.fetchall()
          users_dict = {'username': [], 'id': []}
          for row in rows:
              users_dict['id'].append(row[0])
              users_dict['username'].append(row[1])
          return users_dict
      except Error as e:
          self.terminal.p_error(f'{ERROR_SQL_GET} : {e}')