from flask import Flask, request
import os
import datetime
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import PyPDF2
import base64
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'pdf'}

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
    if 'pdf' not in request.files:
        return 'No file part'
    file = request.files['pdf']
    if file.filename == '':
        return 'No selected file'

    if file:
        check_file = file.filename.split('.')

        if check_file[1] in ALLOWED_EXTENSIONS:
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d")
            file_name = os.path.splitext(file.filename)
            store_pdf = file_name[0] + "_" + current_datetime + "." + check_file[1]

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], store_pdf)
            file.save(file_path)
            pdf_text = ''
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                num_pages = len(pdf_reader.pages)
                print(num_pages)

                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    pdf_text += page.extract_text()
            pdf_text = pdf_text.split()
            encrypted_text = ''
            for pdf_words in pdf_text:
                pdf_words=pdf_words.split(',')
                for word in pdf_words:
                    if(word):
                        word = word.encode('utf-8')
                        padded_value = pad(word, 16)
                        encrypted_word = cipher.encrypt(padded_value)
                        encrypted_word = base64.b64encode(encrypted_word).decode()
                        print(encrypted_word)
                        if encrypted_text == '':
                            encrypted_text = encrypted_word
                        else:
                            encrypted_text+=' '+encrypted_word
            print(encrypted_text)
            store_encrypted_pdf = file_name[0] + "_encrypted_" + current_datetime + '.txt'
            store_encrypted_key = file_name[0] + "_encrypted_" + current_datetime + '.key'
            key_path = os.path.join(app.config['UPLOAD_FOLDER'], store_encrypted_key)
            encrypt_path = os.path.join(app.config['UPLOAD_FOLDER'], store_encrypted_pdf)
            with open(key_path, 'wb') as key_file:
                key_file.write(aes_key)

            with open(encrypt_path, 'wb') as encrypted_csv:
                encrypted_csv.write(encrypted_text.encode('utf-8') + b"")
            return {"key_path": key_path, "encrypt_path": encrypt_path}

        else:
            return 'File uploaded is not pdf type'

@app.route('/search', methods=['POST'])
def search():
    text_to_search = request.json.get('text')
    encrypt_path=request.json.get('encrypt_path')
    key_path=request.json.get('key_path')
    padded_text = text_to_search.encode('utf-8')
    padded_text = pad(padded_text, 16)

    with open(key_path, "r") as key_file:
        key_contents = key_file.read()
        key = base64.b64decode(key_contents)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_word = cipher.encrypt(padded_text)
    encrypted_word=base64.b64encode(encrypted_word).decode()
    print(encrypted_word)
    with open(encrypt_path, "rb") as file:
        file_contents = file.read()
        file_contents=file_contents.split()

    for word in file_contents:
        word=word.decode('utf-8')
        if(encrypted_word==word):
            return 'word found'
    return 'Not Found'


if __name__ == '__main__':
    app.run(debug=True)
