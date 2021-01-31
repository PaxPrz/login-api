import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker
from hashlib import sha1



Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(20), unique=True)
    password = sa.Column(sa.String(100))
    # user_secrets = relationship("Secrets", backref="users", lazy=True)

    def set_password(self, password):
        self.password = sha1(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password == sha1(password.encode()).hexdigest()

    def __repr__(self):
        return f"< User[{self.id}]: {self.username} >"


class Secrets(Base):
    __tablename__ = "secrets"

    id = sa.Column(sa.Integer, primary_key=True)
    data = sa.Column(sa.String(200))
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    user_secrets = relationship("Users", backref="secrets", lazy=True)

    def __repr__(self):
        return f"< Secret[{self.id}]: {self.data[0:5]}.. >"
