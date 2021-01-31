from flask import Flask
from flask_restful import Resource, Api
from flask_script import Manager
from orm import Base, Users, Secrets
from helpers import create_engine, create_all_tables
from repository import SqlSession
from dotenv import load_dotenv
from exceptions import DatabaseError

load_dotenv()

engine = create_engine()

app = Flask(__name__)

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

if __name__ == "__main__":
    manager.run()
