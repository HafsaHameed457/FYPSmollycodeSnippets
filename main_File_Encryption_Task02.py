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

        cipher = AES.new(key, AES.MODE_ECB)
        encrypted_text=[]
        plaintext = file.read()
        words=plaintext.split()
        for word in words:
            padded_text = pad(word, 16)

            encrypted_word = cipher.encrypt(padded_text)
            encrypted_word=base64.b64encode(encrypted_word).decode()
            encrypted_text.append(encrypted_word)
        print(encrypted_text)


        with open('encrypted.txt', 'wb') as encrypted_file:
            for encrypted_word in encrypted_text:
                encrypted_file.write(encrypted_word.encode('utf-8') + b" ")

                # encrypted_file.write(encrypted_word+b" ")

        # Specify an absolute path for 'encryption_key.key'
        with open('encryption_key.key', 'wb') as key_file:
            key_file.write(key)
    return 'Encrypted text stored in file'



if __name__ == '__main__':
    app.run(debug=True)