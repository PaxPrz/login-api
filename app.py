import os
import json

from dotenv import load_dotenv
load_dotenv()

# from flask import Flask, Response
from myflask import MyFlask as Flask
from flask_restful import Resource, Api
from flask_script import Manager
from orm import Base, Users, Secrets
from helpers import create_all_tables
from repository import SqlSession, engine
from exceptions import DatabaseError
from settings import create_app_settings
from login import login_blueprint
from werkzeug.exceptions import HTTPException


settings = create_app_settings(
    database=os.getenv("DATABASE"),
    jwt_secret=os.getenv("SECRET"),
)

app = Flask(__name__)
app.config["settings"] = settings
app.register_blueprint(login_blueprint)

manager = Manager(app)


@manager.command
def makedb():
    "Generates table in database if not exist"
    create_all_tables(Base, engine=engine)


@manager.option("-u", "--username", dest="name", default="admin")
@manager.option("-p", "--password", dest="password", default="password")
@manager.option("-s", "--secret", dest="flag", default="flag{test_flag}")
def add_user_secret(name, password, flag):
    "Add user with new secret"
    with SqlSession(engine) as sess:
        u = Users(username=name)
        u.set_password(password)
        sess.add(u)
        admin_id = sess.query(Users.id).filter(Users.username==name).one()
        if admin_id is None:
            raise DatabaseError()
        s = Secrets(data=flag, user_id=admin_id[0])
        sess.add(s)


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "status": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.context_type = "application/json"
    return response


if __name__ == "__main__":
    manager.run()
