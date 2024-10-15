import base64
import os
from functools import wraps
from flask import jsonify, render_template, request, session, redirect, url_for
from config import *

from auth import passwd_hash
from auth.db import database


def get_basic_auth_data(auth_header):
  # Example of Basic auth: "Basic dXNlcm5hbWU6cGFzc3dvcmQ="
  if not auth_header or not auth_header.startswith("Basic "):
    return None

  # Decode the Base64 encoded part (after "Basic ")
  auth_str = auth_header.split(" ")[1]
  decoded_bytes = base64.b64decode(auth_str).decode("utf-8")
  # Split the decoded string into username and password
  username, password = decoded_bytes.split(":")
  return username, password


def get_user(username, password):
  """Takes a username and password and returns a tuple of (bool, user)
  where if it is a valid user, the bool is True and the user is the
  user's data. If the user is invalid, the bool is False and the user is None.

  Args:
      username (String): Username of the user
      password (String): Password entered by the user

  Returns:
      tuple: (bool, user->tuple)
  """
  db = database()
  user = db.get_user(username=username)
  db.close()

  if user is None:
    return False, None

  verified = passwd_hash.verify_password(
      password=password, hashed_password=user[2])

  if not verified:
    return False, None

  return True, user


def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):

    if not session.get("logged_in"): # If not user session (HTML login)

      # Do api auth
      auth_header = request.headers.get("Authorization")

      # Extract username and password from the Authorization header
      auth_data = get_basic_auth_data(auth_header)

      if auth_data is None:
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

      username, password = auth_data
      verified, user = get_user(username, password)

      if not verified:
        return jsonify({"error": "Invalid credentials"}), 401

    return f(*args, **kwargs)
  return decorated_function


def get_images(path):
  path = os.path.join("static", path)
  if os.path.exists(path):
    return [image for image in os.listdir(path) if image.endswith(".jpg")]
  return []


def register_session(user):
  session.permanent = True
  session["logged_in"] = True
  session["username"] = user[1]
  session["name"] = user[3]
  session["profile_pic"] = user[4]
  session["last_login"] = user[6]
  session["last_password_change"] = user[5]

  return render_template("home.html",
                         name=session.get("name"),
                         last_login=session.get("last_login"),
                         profile_pic=session.get("profile_pic")
                         )


def list_images(path, page=1, per_page=100):
  if path not in FOLDER_PATHS:
    return {}, 405

  try:
    files = os.listdir(FOLDER_PATHS[path])
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    images = [f for f in files if f.lower().endswith(image_extensions)]

    start = (page - 1) * per_page
    end = start + per_page

    paginated_images = images[start:end]

    return {
        "images": paginated_images,
        "total_images": len(images),
        "total_pages": (len(images) + per_page - 1) // per_page,
        "page": page,
        "per_page": per_page
    }, 200

  except FileNotFoundError:
    return {}, 404
