import datetime
import sys
import os
import json
from logging import config, getLogger
from dotenv import load_dotenv

# load current directory
load_dotenv()

# load secret directory
load_dotenv(dotenv_path="/etc/secrets/.env")


with open("src/logging.json", "r") as f:
    log_conf = json.load(f)
config.dictConfig(log_conf)
logger = getLogger(__name__)

# openssl genrsa 2048 > private_key.pem
PRIVATE_PEM = open("src/infrastructure/cert/private_key.pem", "r").read()

TOKEN_EXPIRE = datetime.datetime.utcnow() + datetime.timedelta(days=7)

# openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY")

# openssl rsa -in private_key.pem -pubout -out public_key.pem
# npm install -g pem-jwk
# pem-jwk public_key.pem
# 出力された json から該当する項目をコピーして、EXAMPLEの部分にペーストする
JWK = {
    "keys": [
        {
            "alg": "RS256",
            "kid": SECRET_KEY,
            "n": os.getenv("SECRET_N"),
            "use": "sig",
            "e": os.getenv("SECRET_E"),
            "kty": os.getenv("SECRET_KTY")
        }
    ]
}
