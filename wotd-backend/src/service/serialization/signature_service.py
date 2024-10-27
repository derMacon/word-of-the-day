import os

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
            HeaderType.SIGNED_USERNAME.value: self.sign(username),
            HeaderType.SIGNED_UUID.value: self.sign(uuid)
        }

    def sign(self, input: str) -> str:
        return self.signer.sign(input).decode('utf-8')

    def unsign(self, signed_value) -> bool:
        return self.signer.unsign(signed_value).decode('utf-8')
