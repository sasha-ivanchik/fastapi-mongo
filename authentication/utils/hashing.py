from passlib.context import CryptContext
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from config import settings

password: bytes = settings.AUTH_JWT.TOKEN_ENCRYPTION_SECRET.encode("utf-8")
salt = settings.AUTH_JWT.TOKEN_ENCRYPTION_SALT.encode("utf-8")

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
)

key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


class Hasher:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(incoming_password: str) -> str:
        return pwd_context.hash(incoming_password)

    @staticmethod
    def encrypt(token: str) -> str:
        return f.encrypt(token.encode("utf-8")).decode("utf-8")

    @staticmethod
    def decrypt(token: str) -> str:
        return f.decrypt(token.encode("utf-8")).decode("utf-8")
