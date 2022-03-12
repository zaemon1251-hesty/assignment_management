import datetime
import uuid
import json
from logging import config, getLogger

with open("src/logging.json", "r") as f:
    log_conf = json.load(f)
config.dictConfig(log_conf)
logger = getLogger(__name__)


# openssl genrsa 2048 > private_key.pem
PRIVATE_PEM = open("src/infrastructure/cert/private_key.pem", "r").read()

TOKEN_EXPIRE = datetime.datetime.utcnow() + datetime.timedelta(days=7)

# openssl rand -hex 32
SECRET_KEY = "EXAMPLE"

# openssl rsa -in private_key.pem -pubout -out public_key.pem
# npm install -g pem-jwk
# pem-jwk public_key.pem
# 出力された json から該当する項目をコピーして、EXAMPLEの部分にペーストする
JWK = {
    "keys": [
        {
            "alg": "RS256",
            "kid": SECRET_KEY,
            "n": "EXAMPLE",
            "use": "sig",
            "e": "EXAMPLE",
            "kty": "EXAMPLE"
        }
    ]
}
