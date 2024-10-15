import bcrypt


class passwd_hash:
  @staticmethod
  def hash_password(password):
    """Hashes a given password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

  @staticmethod
  def verify_password(password, hashed_password):
    """Verifies a given password against a stored hash."""
    return bcrypt.checkpw(password.encode(), hashed_password)
