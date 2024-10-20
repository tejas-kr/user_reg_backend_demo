"""
Password Util Class and methods
"""
import bcrypt


class PasswordUtils:
    """
    Password Util methods
    """
    def __init__(self, passw: str):
        """
        Initialize Password Utils object
        :param passw: Str. raw password
        """
        self.passw = passw

    def hash_passw(self) -> bytes:
        """
        Hashes the password
        :return: Hashed password in bytes
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(self.passw.encode('utf-8'), salt)
        return hashed

    def verify_passw(self) -> bool:
        """
        Verifies the password
        :return: Bool. True if passw matches or vice versa
        """
        hashed_pass = self.hash_passw()
        return bcrypt.checkpw(self.passw.encode(), hashed_pass)
