#!/usr/bin/nv python3
"""auth module"""
import bcrypt
from db import DB
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """returns hashed password"""
    hashed_psw = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt(4))
    return hashed_psw


def _generate_uuid() -> str:
    """returns uuid4 string"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """initialization"""
        self._db = DB()

    def register_user(self, email:str, password: str) -> User:
        """function doc string"""
        user_exists = False
        try:
            existing_user = self._db.find_user_by(email=email)
            user_exists = True
        except Exception:
            pass
        if user_exists:
            raise ValueError(f"User {email} already exists")
        hashed_passwd = _hash_password(password)
        return self._db.add_user(email=email, hashed_password=hashed_passwd)

    def valid_login(self, email: str, password: str) -> bool:
        """validates login details"""
        try:
            user = self._db.find_user_by(email=email)
            p = bytes(password, 'utf-8')
            if bcrypt.checkpw(p, user.hashed_password):
                return True
            return False
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """creates a new session for user"""
        try:
            user = self._db.find_user_by(email=email)
            s_id = _generate_uuid()
            self.__db.update_user(user.id, session_id=s_id)
            return s_id
        except Exception:
            pass

    def destroy_session(self, user_id: str) -> User:
        """removes user session_id"""
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """updates users reset token"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError
        hashed_p = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_p, reset_token=None)
