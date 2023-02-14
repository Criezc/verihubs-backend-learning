from ...modules.user.domain.entities import Users
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hashed(password):
    return bcrypt_context.hash(password)
