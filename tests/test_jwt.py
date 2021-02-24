import time
import unittest

from auth.jwt_api import JwtApi


class TestAwt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self._jwt = JwtApi()

    def tearDown(self):
        del self._jwt

    def test_secret(self):
        # real, long duration token, valid
        token_1 = self._jwt.get_token('some_one')
        exp_1 = True
        output_1 = self._jwt.validate(token_1)
        self.assertEquals(exp_1, output_1)
        # real, but short-lived token, expired
        token_2 = self._jwt.get_token('some_one', duration=1)
        exp_2 = False
        time.sleep(2)
        output_2 = self._jwt.validate(token_2)
        self.assertEquals(exp_2, output_2)
        # invalid token
        token_3 = b'an invalid one'
        exp_3 = False
        output_3 = self._jwt.validate(token_3)
        self.assertEquals(exp_3, output_3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
