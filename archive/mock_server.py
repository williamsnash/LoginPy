from auth import database, passwd_hash

if __name__ == '__main__':

  db = database()
  db.create_db()

  # username = input("Enter a username: ")
  # password = input("Enter a password: ")
  # name = input("Enter a name: ")
  username = "wsnash"
  password = "123456"
  name = "William Nash"
  profile_icon = "default.png"
  last_password_change = "2021-01-01"
  last_login = "2021-01-01"

  password_hash = passwd_hash.hash_password(password)


  db.insert_user(username, password_hash, name, profile_icon, last_password_change, last_login)

