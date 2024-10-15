import sqlite3


class database():

  def __init__(self):
    self.conn = sqlite3.connect('auth.db')
    self.cursor = self.conn.cursor()

  def create_db(self):
    """Creates the db (Really for testing purposes)
    """
    self.cursor.execute('''CREATE TABLE IF NOT EXISTS auth
             (id INTEGER PRIMARY KEY,
              username TEXT,
              password_hash TEXT,
              name TEXT,
              profile_icon TEXT,
              last_password_change TEXT,
              last_login TEXT)''')
    self.conn.commit()

  def insert_user(self, username, password_hash, name, profile_icon, last_password_change, last_login):
    """Inserts a user into the database.

    Args:
        username (string): Username of the user
        password_hash (string): Hashed password of the user
        name (string): Name of the user
        profile_icon (string): Profile icon of the user
        last_password_change (string): Date of the last password change
        last_login (string): Date of the last login
    """
    # sdfsd
    self.cursor.execute(
        """INSERT INTO auth
        (username, 
        password_hash,
        name,
        profile_icon,
        last_password_change,
        last_login)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (username, password_hash, name, profile_icon, last_password_change, last_login))
    self.conn.commit()

  def update_user(self, id, **kwargs):
    """
    Update a user in the database. Allows for any of the fields to be updated.

    Args:
        id (int): Id of the user to update
        kwargs: Any of the fields of the db to update
          (username, 
          password_hash,
          name,
          profile_icon,
          last_password_change,
          last_login)
    """
    # List comprehension to create a list of keys
    set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
    sql = f"UPDATE auth SET {set_clause} WHERE id = ?"

    # Add values and id to the list for the execute
    self.cursor.execute(sql, list(kwargs.values()) + [id])
    self.conn.commit()

  def delete_user(self, username):
    """Deletes a user from the database by username.

    Args:
        username (string): Username of the user to delete
    """
    self.cursor.execute("DELETE FROM auth WHERE username = ?", (username,))
    self.conn.commit()

  def get_user(self, username):
    """Gets the user from the database by username.

    Args:
        username (string): Username of the user to get

    Returns:
        Set: A single user from the database
    """
    self.cursor.execute("SELECT * FROM auth WHERE username = ?", (username,))
    return self.cursor.fetchone()

  def close(self):
    self.conn.close()
