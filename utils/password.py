import hashlib

def gener_password(password: str, salt: str) -> str:
    b = (password + salt).encode('utf-8')
    return hashlib.md5(b).hexdigest()
