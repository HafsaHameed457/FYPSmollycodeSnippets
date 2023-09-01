from flask import Flask, request
import base64
import rsa

publicKey, privateKey = rsa.newkeys(512)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Here you can encrypt and decrypt your message'


@app.route('/encrypt', methods=['POST'])
def encrypt():
    message = request.json.get('message')
    encMessage = rsa.encrypt(message.encode(),
                             publicKey)
    encMessageBase64 = base64.b64encode(encMessage).decode()

    return encMessageBase64



@app.route('/decrypt', methods=['POST'])
def receive_json():
    message = request.json.get('message')
    message=base64.b64decode(message)

    decMessage = rsa.decrypt(message, privateKey).decode()

    return {

        "decMessage": decMessage

    }


if __name__ == '__main__':
    app.run(debug=True)
