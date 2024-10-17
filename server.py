from datetime import timedelta, datetime
from flask import Flask, request, jsonify, render_template, redirect, send_from_directory, url_for, session

from auth import database, passwd_hash
from server_helper import *

app = Flask(__name__)
app.secret_key = 'cb7da859c508a40d17764bf9217db602'
app.permanent_session_lifetime = timedelta(minutes=30)


@app.route("/", methods=["GET", "POST"])
def index():
  if session.get("logged_in"):
    return render_template("home.html",
                           name=session.get("name"),
                           last_login=session.get("last_login"),
                           profile_pic=session.get("profile_pic"),
                           folders=list(FOLDER_PATHS.keys())
                           )

  if request.method == "POST":
    # Access form data using request.form
    username = request.form.get('username')
    password = request.form.get('password')

    verified, user = get_user(username, password)

    if verified:
      # Allows the user to close the page but the session remain (until the TLL runs out)
      register_session(user)
      return render_template("home.html",
                             name=session.get("name"),
                             last_login=session.get("last_login"),
                             profile_pic=session.get("profile_pic"),
                             folders=list(FOLDER_PATHS.keys())
                             )

    return render_template("login.html", message="Invalid credentials", color="red")

  url_color = request.args.get("color")
  color = ""
  if url_color == "success":
    color = "green"
  elif url_color == "danger":
    color = "red"

  return render_template("login.html", message=request.args.get("message", ""), color=color)


@app.route("/register", methods=["GET", "POST"])
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


@app.route("/logout")
def logout():
  session["logged_in"] = False
  now = datetime.now()
  formatted_date = now.strftime("%Y-%m-%d | %I:%M.%S %p")
  db = database()
  db.update_user(session.get("username"), last_login=formatted_date)
  session.clear()
  return redirect(url_for('index', message="Logged out successfully", color="success"))


@app.route("/delete_account")
def delete_account():
  db = database()
  username = session.get("username")
  print(f"Deleting account for {username}")
  db.delete_user(username=username)
  db.close()
  session.clear()
  return redirect(url_for('index', message="Account deleted successfully", color="success"))


@app.route("/masonry/<style>")
@login_required
def masonry_parent(style):
  path = request.args.get("path", "")

  # Default to page 1
  page = request.args.get('page', 1, type=int)

  # Default to 10 items per page
  per_page = request.args.get('per_page', 100, type=int)

  resp, _ = list_images(path, page, per_page)

  html = "masonry/gutterless.html"

  if style == "gutterless":
    html = "masonry/gutterless.html"
  elif style == "bordered":
    html = "masonry/bordered.html"
  elif style == "with-gutter":
    html = "masonry/with_gutter.html"

  return render_template(html, path=path, images=resp.get("images"), page=page, total_pages=resp.get("total_pages"))


# @app.route("/test")
# def test():
#   return render_template("test.html")

@app.route('/list-images/<path>', methods=['GET'])
@login_required
def API_list_images(path):

  page = request.args.get('page', 1, type=int)  # Default to page 1
  # Default to 10 items per page
  per_page = request.args.get('per_page', 100, type=int)

  resp, code = list_images(path, page, per_page)
  return resp, code


@app.route('/images/<folder>/<filename>', methods=['GET'])
@login_required
def serve_image(folder, filename):
  if folder not in FOLDER_PATHS:
    return jsonify([]), 404
  try:
    return send_from_directory(FOLDER_PATHS[folder], filename)
  except FileNotFoundError:
    return jsonify([]), 404


@app.route("/test-api", methods=["POST"])
@login_required
def API_test():
  return jsonify({"message": "API is working"})


if __name__ == "__main__":
  db = database()
  db.create_table()
  app.run(debug=True)
