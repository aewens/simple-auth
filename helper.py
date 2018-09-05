import hmac
import base64
import hashlib
from os import urandom
from datetime import datetime

def sha256(seed=None):
    m = hashlib.sha256()
    if seed is not None:
        m.update(seed.encode("utf-8"))
    else:
        m.update(urandom(32))
    return m.hexdigest()

def sign(message, secret):
    digest = hmac.new(
        secret.encode(), 
        msg=message.encode(), 
        digestmod=hashlib.sha256
    ).digest()
    signature = base64.b64encode(digest).decode()
    return signature

def timestamp(date_str=None):
    if date_str is None:
        return datetime.now().timestamp()

    date = datetime.strptime(date_str, "%Y-%m-%d %H-%M-S")
    return data.timestamp()