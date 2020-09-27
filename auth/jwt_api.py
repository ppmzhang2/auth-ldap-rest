import random
import string
from datetime import datetime
from typing import Tuple

import jwt
from jwt.exceptions import InvalidTokenError

from auth import cfg
from auth.singleton_meta import SingletonMeta

__all__ = ['JwtApi']


class JwtApi(metaclass=SingletonMeta):
    _SECRET_LEN = 30
    _ALGORITHM = 'HS256'

    __slots__ = ['_secret']

    @staticmethod
    def _random_alphanumeric_string(length: int):
        alphabet = string.ascii_letters + string.digits
        result_str = ''.join((random.sample(alphabet, length)))
        return result_str

    @staticmethod
    def _timestamps(duration: int) -> Tuple[int, int]:
        """unix timestampes for payload

        :param duration: effective time in second
        :return: iat (Issued At), nbf (Not Before) and exp (expiration time)
        """
        iat = int(datetime.now().timestamp())
        nbf = iat
        exp = iat + duration
        return iat, nbf, exp

    @classmethod
    def _headers(cls):
        return {"alg": cls._ALGORITHM, "typ": "JWT"}

    def __init__(self):
        self._secret = JwtApi._random_alphanumeric_string(JwtApi._SECRET_LEN)

    def get_token(self, user_id: str, duration: int = 86400) -> str:
        """create token for a user

        :param user_id: user to receive the token, store in payload
        :param duration: effective time in second, default 86400 (one day)
        :return bytes token
        """
        iat, nbf, exp = self._timestamps(duration)
        headers = self._headers()
        payload = {'user': user_id, 'iat': iat, 'nbf': nbf, 'exp': exp}
        return jwt.encode(payload=payload,
                          key=self._secret,
                          algorithm=self._ALGORITHM,
                          headers=headers).decode()

    def validate(self, token: str):
        try:
            jwt.decode(token,
                       key=self._secret,
                       verify=True,
                       algorithms=self._ALGORITHM)
            return True
        except InvalidTokenError:
            return False
