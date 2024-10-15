from datetime import timedelta, datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, session

from auth import database, passwd_hash
from server_helper import *

api = Flask(__name__)
api.secret_key = 'cb7da859c508a40d17764bf9217db602'
api.permanent_session_lifetime = timedelta(minutes=30)

REG_OPEN = True


@api.route("/", methods=["GET", "POST"])
def index():
  if session.get("logged_in"):
    return render_template("home.html",
                           name=session.get("name"),
                           last_login=session.get("last_login"),
                           profile_pic=session.get("profile_pic")
                           )

  if request.method == "POST":
    # Access form data using request.form
    username = request.form.get('username')
    password = request.form.get('password')

    verified, user = get_user(username, password)

    if verified:
      # Allows the user to close the page but the session remain (until the TLL runs out)
      return register_session(user)

    return render_template("login.html", message="Invalid credentials", color="red")

  url_color = request.args.get("color")
  if url_color == "success":
    color = "green"
  elif url_color == "danger":
    color = "red"

  return render_template("login.html", message=request.args.get("message", ""), color=color)


@api.route("/register", methods=["GET", "POST"])
def register():
  if not REG_OPEN:
    return render_template("error.html", error_code="500", error_message="Registration is closed")

  if request.method == "POST":
    username = request.form.get("username")
    request.form.get("name")

    db = database()
    user = db.get_user(username=username)
    if user:
      return render_template("error.html", error_code="500", error_message="User already exists")
    password_hash = passwd_hash.hash_password(request.form.get("password"))
    db.insert_user(username=username,
                   password_hash=password_hash,
                   name=request.form.get("name"),
                   profile_icon="default.jpg",
                   last_password_change="Never",
                   last_login="Never"
                   )
    db.close()
    return redirect(url_for('index', message="Registration successful", color="success"))

  return render_template("register.html")


@api.route("/logout")
def logout():
  session["logged_in"] = False
  now = datetime.now()
  formatted_date = now.strftime("%Y-%m-%d | %I:%M.%S %p")
  db = database()
  db.update_user(session.get("username"), last_login=formatted_date)
  session.clear()
  return redirect(url_for('index', message="Logged out successfully", color="success"))


@api.route("/delete_account")
def delete_account():
  db = database()
  username = session.get("username")
  print(f"Deleting account for {username}")
  db.delete_user(username=username)
  db.close()
  session.clear()
  return redirect(url_for('index', message="Account deleted successfully", color="success"))


@api.route("/masonry-bordered")
@login_required
def masonry_bordered():
  path = request.args.get("path", "")
  return render_template("masonry/bordered.html", path=path, images=get_images(path))


@api.route("/masonry-gutterless")
@login_required
def masonry_gutterless():
  path = request.args.get("path", "")
  return render_template("masonry/gutterless.html", path=path, images=get_images(path))


@api.route("/masonry-with-gutter")
@login_required
def masonry_with_gutter():
  path = request.args.get("path", "")
  return render_template("masonry/with_gutter.html", path=path, images=get_images(path))


@api.route("/test-api", methods=["POST"])
@api_auth_required
def test_api():
  return jsonify({"message": "API is working"})


if __name__ == "__main__":
  api.run(debug=True)
