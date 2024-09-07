import os

from flask import Response
from itsdangerous import Signer
from singleton_decorator import singleton

from src.data.anki.token_type import HeaderType


@singleton
class SignatureService:

    def __init__(self):
        private_key_uuid_sign = os.environ.get('PRIVATE_KEY_UUID_SIGN', 'test-key')
        self.signer = Signer(private_key_uuid_sign)

    def create_signed_header_dict(self, username: str, uuid: str):
        return {
            HeaderType.USERNAME.value: self._sign(username),
            HeaderType.UUID.value: self._sign(uuid)
        }

    def _sign(self, input):
        return self.signer.sign(input)

    def _unsign(self, signed_value) -> bool:
        return self.signer.unsign(signed_value)

