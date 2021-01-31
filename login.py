from flask import Blueprint, current_app, escape, jsonify, request
from orm import Users
from repository import SqlSession, engine
from exceptions import UserNotExist, IncorrectPassword, DuplicateUser
from auth import generate_user_token
from sqlalchemy.orm.exc import NoResultFound


login_blueprint = Blueprint("login_blueprint", __name__, url_prefix="/user")

@login_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and request.is_json:
        username = request.json.get("username")
        password = request.json.get("password")
        with SqlSession(engine) as sess:
            try:
                user = sess.query(Users).filter(Users.username==username).one()
            except NoResultFound:
                raise UserNotExist
            if not user.check_password(password):
                raise IncorrectPassword
            return {
                "token": generate_user_token(
                    user_id=user.id,
                    username=username,
                    secret=current_app.config["settings"].jwt_secret,
                    algo=current_app.config["settings"].jwt_algo,
                ),
            }


@login_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST" and request.is_json:
        username = escape(request.json.get("username"))
        password = escape(request.json.get("password"))
        with SqlSession(engine) as sess:
            try:
                user = sess.query(Users).filter(Users.username==username).one()
                if user:
                    raise DuplicateUser
            except NoResultFound:
                pass
            user = Users(username=username)
            user.set_password(password)
            sess.add(user)
        return {"message": "New user successfully added"}


@login_blueprint.route("/", methods=["GET"])
def test():
    if request.method == "GET":
        return {"message": "success"}, 200
