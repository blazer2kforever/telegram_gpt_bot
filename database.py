import sqlite3
from sqlite3 import Error
from datetime import datetime

INFO_SQL_CONNECT = 'Подключение SQL'
INFO_SQL_CREATE_TABLE = 'Создание таблицы SQL'
INFO_SQL_INSERT = 'Выполнение SQL INSERT'
INFO_SQL_DELETE = 'Выполнение SQL DELETE'
INFO_SQL_GET = 'Выполнение SQL GET'

ERROR_SQL_CONNECT = 'Невозможно установить соединение с SQL'
ERROR_SQL_CREATE_TABLE = 'Невозможно создать SQL таблицу'
ERROR_SQL_INSERT = 'Невозможно выполнить SQL INSERT'
ERROR_SQL_DELETE = 'Невозможно выполнить SQL DELETE'
ERROR_SQL_GET = 'Невозможно выполнить SQL SELECT'

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