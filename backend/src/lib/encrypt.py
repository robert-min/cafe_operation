import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from . import ENCRYTION_KEY


class EncryptManager:
    def __init__(self) -> None:
        self.dek = bytes(ENCRYTION_KEY, "utf-8")
        self.Block_size = 16
    
    def encrypt_password(self, origin_pw: str) -> bytes:
        """Encrypt password.
        Args:
            origin_pw: user password
        
        Return:
            encrypt_pw
            
        Raise:
            Failed to encrypt password.
        """
        try:
            encoding_pw = origin_pw.encode()
            aes = AES.new(self.dek, AES.MODE_ECB)
            padding_pw = pad(encoding_pw, self.Block_size)
            encrypt_pw = aes.encrypt(padding_pw)
            return base64.b64encode(encrypt_pw)
        except Exception:
            raise EncryptManagerError("Failed to encrypt password.")
    
    def decrypt_password(self, encrypt_pw: bytes) -> str:
        """Decrypt password.
        Args:
            encrypt_pw: user encrypt password
        
        Return:
            origin_pw
            
        Raise:
            Failed to decrypt password.
        """
        try:
            aes = AES.new(self.dek, AES.MODE_ECB)
            decrypt_pw = aes.decrypt(base64.b64decode(encrypt_pw))
            unpadding_pw = unpad(decrypt_pw, self.Block_size)
            return unpadding_pw.decode()
        except Exception:
            raise EncryptManagerError("Failed to decrypt password.")
            
            
class EncryptManagerError(Exception):
    """All EncryptManager Error"""