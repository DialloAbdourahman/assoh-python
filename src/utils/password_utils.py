from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class PasswordUtils:
    @staticmethod
    def hash_password(password:str) -> str:
        return bcrypt_context.hash(password)
    
    @staticmethod
    def verify_password(plane_password:str, hashed_password:str) -> bool:
        return bcrypt_context.verify(plane_password, hashed_password)

