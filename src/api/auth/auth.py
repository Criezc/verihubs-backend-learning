import time
import jwt

from decouple import config


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

# Functions to return the token


def token_response(token: str):
    return {
        "access token": token
    }

# Function to sign the JWT Token


def signJWT(userID: str):
    payload = {
        "userID": userID,
        "expiration": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_SECRET)
        return decode_token if decode_token['expiration'] >= time.time() else None
    except:
        return {}
