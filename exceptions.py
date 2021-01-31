from werkzeug.exceptions import HTTPException


class InvalidToken(HTTPException):
    code = 401
    description = "Token provided is Invalid"


class ExpiredToken(HTTPException):
    code = 401
    description = "Token has expired"


class DatabaseError(HTTPException):
    code = 503
    description = "Database operation failure"


class UserNotExist(HTTPException):
    code = 400
    description = "User doesn't exists"


class IncorrectPassword(HTTPException):
    code = 400
    description = "Incorrect Password"


class DuplicateUser(HTTPException):
    code = 400
    description = "User already exists"
