import hashlib
import os
import secrets
import time
import base64
import requests
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecurityManager:
    @staticmethod
    def generate_salt() -> str:
        return os.urandom(16).hex()

    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        salted = (password + salt).encode('utf-8')
        return hashlib.sha256(salted).hexdigest()

    # --- AES-256 ŞİFRELEME (MASTER PASSWORD DERIVATION) ---
    @staticmethod
    def derive_key(master_password: str, salt_bytes: bytes) -> bytes:
        """Kullanıcının ana şifresinden 256-bit AES anahtarı türetir."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt_bytes,
            iterations=100_000,
        )
        return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

    @staticmethod
    def encrypt_data(data: str, master_password: str, salt: str) -> str:
        """Metni AES-256 ile şifreler."""
        if not data:
            return ""
        key = SecurityManager.derive_key(master_password, bytes.fromhex(salt))
        fernet = Fernet(key)
        return fernet.encrypt(data.encode()).decode()

    @staticmethod
    def decrypt_data(encrypted_data: str, master_password: str, salt: str) -> str:
        """AES-256 ile şifrelenmiş metni çözer."""
        if not encrypted_data:
            return ""
        try:
            key = SecurityManager.derive_key(master_password, bytes.fromhex(salt))
            fernet = Fernet(key)
            return fernet.decrypt(encrypted_data.encode()).decode()
        except Exception:
            return "⚠️ [Şifre Çözülemedi]"

    # --- ŞİFRE SIZINTI KONTROLÜ (HAVEIBEENPWNED API) ---
    @staticmethod
    def check_pwned_password(password: str) -> int:
        """
        k-Anonymity modelini kullanarak şifrenin sızıp sızmadığını sorgular.
        Gerçek şifre asla internete gönderilmez, sadece SHA-1 hash'inin ilk 5 karakteri gönderilir.
        """
        sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = sha1_password[:5], sha1_password[5:]
        
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                hashes = (line.split(':') for line in response.text.splitlines())
                for h, count in hashes:
                    if h == suffix:
                        return int(count)  # Kaç kez sızdırıldığı
        except Exception:
            pass
        return 0  # Sızdırılmamış