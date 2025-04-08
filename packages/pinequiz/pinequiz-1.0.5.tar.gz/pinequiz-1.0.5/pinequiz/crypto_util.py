import base64
import random
import string

KEY = "JBSWY3DPEHPK3PXP"

def xor_encrypt_with_salt(plain, key=KEY, salt_len=4):
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=salt_len))
    text = salt + plain
    encrypted = ''.join(
        chr(ord(c) ^ ord(key[i % len(key)]))
        for i, c in enumerate(text)
    )
    return base64.b64encode(encrypted.encode()).decode()

def xor_decrypt_with_salt(encoded, key=KEY):
    decoded = base64.b64decode(encoded).decode()
    decrypted = ''.join(
        chr(ord(c) ^ ord(key[i % len(key)]))
        for i, c in enumerate(decoded)
    )
    return decrypted[-1]  
