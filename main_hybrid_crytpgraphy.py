from flask import Flask, request
import base64
import rsa

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

publicKey, privateKey = rsa.newkeys(512)
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Here you can encrypt and decrypt your message'


@app.route('/encrypt', methods=['POST'])
def encrypt():
    # text is encrypted and iv is generated
    message_string = request.json.get('message')
    password = get_random_bytes(16)
    message = message_string.encode('utf-8')
    iv = get_random_bytes(16)
    cipher = AES.new(password, AES.MODE_CBC, iv)
    padded_message = message + b' ' * (16 - len(message) % 16)

    ciphertext = cipher.encrypt(padded_message)
    # encrypting aes password using rsa
    encrypt_password = rsa.encrypt(password, publicKey)

    iv_64 = base64.b64encode(iv).decode()
    password_64 = base64.b64encode(encrypt_password).decode()
    ciphertext_64 = base64.b64encode(ciphertext).decode()

    return {
        "Encrypted_password": password_64,
        "Encrypted_Data": ciphertext_64,
        "IV_64": iv_64
    }


@app.route('/decrypt', methods=['POST'])
def decrypt():
    # try:
    password_64 = request.json.get('Encrypted_password')

    cipher_text_64 = request.json.get('Encrypted_Data')
    iv_64 = request.json.get('IV_64')

    # decoded and decrypted password
    decoded = base64.b64decode(password_64)
    decrypt_password = rsa.decrypt(decoded, privateKey)

    print(decrypt_password)
    # decoded iv and cipher text
    iv = base64.b64decode(iv_64)
    ciphertext = base64.b64decode(cipher_text_64)
    # created new cipher
    cipher = AES.new(decrypt_password, AES.MODE_CBC, iv)

    decrypted_message = cipher.decrypt(ciphertext)

    unpadded_data = decrypted_message.rstrip(b' ')

    decrypted_message_str = unpadded_data.decode('utf-8')

    return decrypted_message_str


if __name__ == '__main__':
    app.run(debug=True)
