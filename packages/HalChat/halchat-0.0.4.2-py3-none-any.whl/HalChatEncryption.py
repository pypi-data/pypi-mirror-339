import base64
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256
from HalEncryption import HalEncryption

class HalChatEncryption:
    """
    Класс-обёртка над HalEncryption + RSA для удобства:
    - Генерация ключей RSA
    - Шифрование/дешифрование сообщений
    - Хеширование строк
    """
    def __init__(self):
        self.he = HalEncryption()

    def generate_rsa_key(self):
        """Создаёт пару ключей RSA и возвращает (private_key, PKCS1_OAEP encryptor, public_key_base64)."""
        key = RSA.generate(2048)
        encryptor = PKCS1_OAEP.new(key, hashAlgo=SHA256)
        public_key = base64.b64encode(key.publickey().exportKey()).decode('utf-8')
        return key, encryptor, public_key

    def encrypt_hex(self, plain_data: bytes, password: str, rounds: int=10) -> str:
        """
        Шифрует plain_data (bytes) с помощью halEncryption + password, 
        результат возвращает в hex-строке.
        """
        encrypted = self.he.encodeByHash(plain_data, password, rounds)
        return encrypted.hex()

    def decrypt_hex(self, encrypted_hex: str, password: str, rounds: int=10) -> str:
        """
        Принимает на вход hex-строку, декодирует её обратно в bytes,
        дешифрует с помощью halEncryption + password, возвращает str.
        """
        encrypted_bytes = bytes.fromhex(encrypted_hex)
        decrypted = self.he.decodeByHash(encrypted_bytes, password, rounds)
        return decrypted.decode("utf-8")

    def str2hash(self, s: str, length: int=16, rounds: int=16) -> str:
        """Обёртка для Str2Hash из halEncryption.hh."""
        return self.he.hh.Str2Hash(s, length, rounds)