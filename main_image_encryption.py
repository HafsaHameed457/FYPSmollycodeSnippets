from flask import Flask, request,send_file,jsonify
import os
import datetime
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad,unpad
from PIL import Image
import io

import base64

app = Flask(__name__)


# Ensure the 'uploads' directory exists
@app.route('/')
def hello_world():
    return 'Send me a file and I will check if you have send it or not.'

@app.route('/', methods=['POST'])
def file():
    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_ECB)
    aes_key = base64.b64encode(key).decode()
    aes_key = aes_key.encode('utf-8')


    if 'image' not in request.files:
        return 'No file part'
    file = request.files['image']
    if file.filename == '':
        return 'No selected file'
    if file:
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d")
        file_name = os.path.splitext(file.filename)
        store_image = file_name[0] + "_" + current_datetime + ".png"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], store_image)

        file.save(file_path)  # Save the file to the 'uploads' directory

        image = Image.open(file_path)
        with io.BytesIO() as buffer:
            image.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()
        print(image_bytes)
        block_size = 16
        remainder = len(image_bytes) % block_size
        if remainder:
            padding = b' ' * (block_size - remainder)
            image_bytes += padding
            
        encrypted_image = cipher.encrypt(image_bytes)
        encrypt_image = base64.b64encode(encrypted_image).decode()

        store_encrypted_image=file_name[0]+"_encrypted_"+current_datetime+'.txt'
        store_encrypted_key = file_name[0] + "_encrypted_" + current_datetime + '.key'

        key_path = os.path.join(app.config['UPLOAD_FOLDER'], store_encrypted_key)
        encrypt_path = os.path.join(app.config['UPLOAD_FOLDER'], store_encrypted_image)

        with open(key_path, 'wb') as key_file:
            key_file.write(aes_key)

        with open(encrypt_path, 'wb') as encrypted_image:
            encrypted_image.write(encrypt_image.encode('utf-8') + b" ")

        return 'Image uploaded and encrypted successfully'




if __name__ == '__main__':
    app.run(debug=True)