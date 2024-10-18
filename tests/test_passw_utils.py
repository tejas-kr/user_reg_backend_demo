"""
Test File for Password Utils
"""
from utils.passw_utils import PasswordUtils


class TestPasswUtils:
    """
    Password Util test methods
    """
    TEST_PASS = "thisispass12"

    def test_hash_passw(self):
        """
        Test hash method
        :return: None
        """
        pw_utils = PasswordUtils(passw=self.TEST_PASS)
        h_pw = pw_utils.hash_passw()
        assert isinstance(h_pw, bytes)

    def test_verify_passw(self):
        """
        Test Verify password
        :return: None
        """
        pw_utils = PasswordUtils(passw=self.TEST_PASS)
        assert pw_utils.verify_passw()
