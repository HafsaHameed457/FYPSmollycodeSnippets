from flask import Flask, request
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import base64

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Send me a file and I will check if you have send it or not.'

@app.route('/file', methods=['POST'])
def file():
    file = request.files['file']
    if file:
        # Generate a random encryption key
        key = get_random_bytes(16)

        cipher_suite = AES.new(key, AES.MODE_ECB)

        plaintext = file.read()
        plaintext = pad(plaintext, 16)

        encrypted_text = cipher_suite.encrypt(plaintext)
        encrypted_text = base64.b64encode(encrypted_text).decode()

        with open('encrypted.txt', 'wb') as file:
            file.write(encrypted_text.encode('utf-8'))

        # Specify an absolute path for 'encryption_key.key'
        with open('encryption_key.key', 'wb') as key_file:
            key_file.write(key)
    return 'file send'



if __name__ == '__main__':
    app.run(debug=True)