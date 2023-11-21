# import secrets
import jwt
from datetime import datetime, timedelta
from src.utils.config import JWT_SECRET_KEY


# Function to form random secret key
# def get_secret_key():
#     # Generates a 64-character hexadecimal string (32 bytes)
#     secret_key = secrets.token_hex(32)
#     print("Secret Key:", secret_key)
#     return secret_key


def construct_jwt(payload):
    expiration_time = datetime.utcnow() + timedelta(minutes=30)
    payload["exp"] = expiration_time
    encoded = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return encoded


def de_construct_jwt(jwt_token):
    try:
        payload = jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except Exception as e:
        raise Exception("Error in decoding jwt token")
