import bcrypt


def get_hash_password(password: str) -> str:
    """对密码进行加密"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """校验密码与哈希是否匹配"""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
