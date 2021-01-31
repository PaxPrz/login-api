from jose import jwt
from jose.exceptions import JWSSignatureError
from time import time
from exceptions import InvalidToken, ExpiredToken
import logging


def generate_user_token(user_id, username, secret="nephack", algo="HS256"):
    payload = {
        "iss": "com.nephack.paxprz",
        "iat": int(time()),
        "exp": int(time())+600,
        "user_id": user_id,
        "username": username
    }
    return jwt.encode(payload, secret, algorithm=algo)


def validate_user_token(token, secret="nephack", algo="HS256"):
    try:
        payload = jwt.decode(token, secret, algorithms=algo)
    except JWSSignatureError:
        logging.error("Invalid JWT Signature")
        raise InvalidToken()
    if payload["exp"] > int(time()):
        logging.error("JWT Token has Expired")
        raise ExpiredToken()
    return {
        "user_id": payload["user_id"],
        "username": payload["username"],
    }
