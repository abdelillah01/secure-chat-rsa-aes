from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import HMAC, SHA256

def encrypt_message(key, message):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))

    # HMAC for integrity
    h = HMAC.new(key, digestmod=SHA256)
    h.update(iv + ciphertext)
    mac = h.digest()

    return iv + ciphertext + mac  # Send IV + Ciphertext + MAC

def decrypt_message(key, data):
    iv = data[:16]
    mac = data[-32:]  # Last 32 bytes are HMAC
    ciphertext = data[16:-32]

    # Verify HMAC
    h = HMAC.new(key, digestmod=SHA256)
    h.update(iv + ciphertext)
    h.verify(mac)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()
