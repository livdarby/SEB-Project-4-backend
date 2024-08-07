from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    invite_code = db.Column(db.Text, unique=False, nullable=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=True)
    total_score = db.Column(db.Integer, unique=False, nullable=True)
    accuracy_score = db.Column(db.Integer, unique=False, nullable=True)
    permissions = db.Column(db.Text, unique=False, nullable=True)

    @hybrid_property
    def password(self):
        pass

    @password.setter
    def password(self, password_plaintext):
        encoded_hashed_pw = bcrypt.generate_password_hash(password_plaintext)
        self.password_hash = encoded_hashed_pw.decode("utf-8")

    def validate_password(self, login_password):
        return bcrypt.check_password_hash(self.password_hash, login_password)
