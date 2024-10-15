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
