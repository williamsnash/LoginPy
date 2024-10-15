@api.route("/home")
def home_page():
  name = session.get("name")
  last_login = session.get("last_login")
  return render_template("home.html", name=name, last_login=last_login, profile_pic=session.get("profile_pic"))


@api.route("/login", methods=["POST"])
def verify_login_creds():
  auth_header = request.headers.get("Authorization")

  # Extract username and password from the Authorization header
  auth_data = get_basic_auth_data(auth_header)

  if auth_data is None:
    return jsonify({"error": "Missing or invalid Authorization header"}), 401

  username, password = auth_data
  db = database()
  user = db.get_user(username=username)
  db.close()

  if user is None:
    return jsonify({"error": "Invalid credentials"}), 401

  verified = passwd_hash.verify_password(
    password=password, hashed_password=user[2])

  if not verified:
    return jsonify({"error": "Invalid credentials"}), 401

  return jsonify({"message": f"Welcome {user[3]}"})


@app.route("/masonry-with-gutter")
@login_required
def masonry_with_gutter():
  path = request.args.get("path", "")
  return render_template("masonry/with_gutter.html", path=path, images=get_images(path))


def list_images_backup(path):
  if path not in FOLDER_PATHS:
    return [], 405
  try:
    print(FOLDER_PATHS[path])
    files = os.listdir(FOLDER_PATHS[path])
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    images = [f for f in files if f.lower().endswith(image_extensions)]
    return images, 200
  except FileNotFoundError:
    return [], 404


def api_auth_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
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


@app.route("/masonry-bordered")
@login_required
def masonry_bordered():
  path = request.args.get("path", "")

  page = request.args.get('page', 1, type=int)  # Default to page 1
  # Default to 10 items per page
  per_page = request.args.get('per_page', 100, type=int)

  resp, _ = list_images(path, page, per_page)

  return render_template("masonry/bordered.html", path=path, images=resp.get("images"), total_pages=resp.get("total_pages"))


@app.route("/masonry-gutterless")
@login_required
def masonry_gutterless():
  path = request.args.get("path", "")

  page = request.args.get('page', 1, type=int)  # Default to page 1
  # Default to 10 items per page
  per_page = request.args.get('per_page', 100, type=int)

  resp, _ = list_images(path, page, per_page)

  return render_template("masonry/gutterless.html", path=path, images=resp.get("images"), total_pages=resp.get("total_pages"))


@app.route("/masonry-with-gutter")
@login_required
def masonry_with_gutter():
  path = request.args.get("path", "")

  page = request.args.get('page', 1, type=int)  # Default to page 1
  # Default to 10 items per page
  per_page = request.args.get('per_page', 100, type=int)

  resp, _ = list_images(path, page, per_page)

  return render_template("masonry/with_gutter.html", path=path, images=resp.get("images"), total_pages=resp.get("total_pages"))


def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if not session.get("logged_in"):
      return redirect(url_for('index', message="You need to login first", color="danger"))
    return f(*args, **kwargs)
  return decorated_function
