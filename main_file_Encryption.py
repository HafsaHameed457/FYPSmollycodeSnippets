from flask import Flask, request
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad,unpad
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
        encrypted_text = []
        plaintext = file.read()
        words = plaintext.split()
        aes_key = base64.b64encode(key).decode()
        aes_key = aes_key.encode('utf-8')
        print('key hun mai', key)
        for word in words:
            padded_text = pad(word, 16)

            encrypted_word = cipher.encrypt(padded_text)
            encrypted_word = base64.b64encode(encrypted_word).decode()
            encrypted_text.append(encrypted_word)

        with open('encrypted.txt', 'wb') as encrypted_file:
            for encrypted_word in encrypted_text:
                encrypted_file.write(encrypted_word.encode('utf-8') + b" ")

        with open('encryption_key.key', 'wb') as key_file:
            key_file.write(aes_key)
    return 'hehe'


@app.route('/search', methods=['POST'])
def search():
    text_to_search = request.json.get('text')
    padded_text=text_to_search.encode('utf-8')
    padded_text = pad(padded_text, 16)

    with open("encryption_key.key", "r") as key_file:
        key_contents = key_file.read()
        key = base64.b64decode(key_contents)

    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_word = cipher.encrypt(padded_text)


    with open("encrypted.txt", "rb") as file:
        file_contents = file.read()
        encoded_words=file_contents.split()
        decoded=[]
        for encoded_word in encoded_words:
            decode = base64.b64decode(encoded_word)
            decoded.append(decode)
        print('encoded_word',decoded)
        print('encrypted_word',encrypted_word)
        for decoded_word in decoded:
            if(decoded_word==encrypted_word):
                encrypted_word_decoded=base64.b64encode(encrypted_word).decode()
                return encrypted_word_decoded

@app.route('/decrypt', methods=['POST'])
def decrypt():
    text_to_decrypt = request.json.get('cipher_text')
    text_to_decrypt=base64.b64decode(text_to_decrypt)
    with open("encryption_key.key", "r") as key_file:
        key_contents = key_file.read()
        key = base64.b64decode(key_contents)

    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_text=cipher.decrypt(text_to_decrypt)
    decrypted_text=unpad(decrypted_text,16)
    return decrypted_text


if __name__ == '__main__':
    app.run(debug=True)
