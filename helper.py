import hashlib
from os import urandom

def sha256(seed=None):
    m = hashlib.sha256()
    if seed is not None:
        m.update(seed.encode("utf-8"))
    else:
        m.update(urandom(32))
    return m.hexdigest()