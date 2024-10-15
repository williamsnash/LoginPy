from auth import database, passwd_hash


if __name__ == '__main__':

  # username = input("Enter username: ")
  password = input("Enter password: ")
  username = 'wsnash'
  # password = '123456'

  db = database()
  user = db.get_user(username=username)

  verified = passwd_hash.verify_password(
    password=password, hashed_password=user[2])

  if not verified:
    print("Invalid credentials")
    exit(0)

  print(f"Welcome {user[3]}")
  print("What would you like to do?")
  print("1. Change password")
  print("2. Update profile picture")
  print("3. Logout")
  choice = input("Enter choice: ")

  if choice == '1':
    print(1)
    new_password = input("Enter new password: ")
    new_password_hash = passwd_hash.hash_password(new_password)
    db.update_user(id=user[0], password_hash=new_password_hash)
  elif choice == '2':
    print(2)
  elif choice == '3':
    print(3)
    exit(0)
