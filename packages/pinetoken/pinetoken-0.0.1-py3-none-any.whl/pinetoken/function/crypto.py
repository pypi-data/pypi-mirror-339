from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib
import json

BLOCK_SIZE = AES.block_size  # 16 bytes

def pad(s):
    padding = BLOCK_SIZE - len(s) % BLOCK_SIZE
    return s + (chr(padding) * padding)

def unpad(s):
    padding = ord(s[-1])
    return s[:-padding]

def get_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()

def encrypt_token(raw_token: str, password: str) -> str:
    raw = pad(raw_token)
    key = get_key(password)
    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(raw.encode())
    return base64.b64encode(iv + encrypted).decode("utf-8")

def decrypt_token(enc_token: str, password: str) -> str:
    enc = base64.b64decode(enc_token)
    iv = enc[:BLOCK_SIZE]
    key = get_key(password)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(enc[BLOCK_SIZE:]).decode("utf-8")
    return unpad(decrypted)

def encrypt_data(data, password):
    key = get_key(password)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    result = {
        'nonce': base64.b64encode(cipher.nonce).decode(),
        'tag': base64.b64encode(tag).decode(),
        'ciphertext': base64.b64encode(ciphertext).decode()
    }
    return json.dumps(result)

def decrypt_data(json_data, password):
    key = get_key(password)
    try:
        b64 = json.loads(json_data)
        nonce = base64.b64decode(b64['nonce'])
        tag = base64.b64decode(b64['tag'])
        ciphertext = base64.b64decode(b64['ciphertext'])

        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        return data.decode()
    except Exception as e:
        print("❌ Gagal dekripsi:", str(e))
        return None
    
        # Copyright (c) 2025 openpineaplehub

    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions: