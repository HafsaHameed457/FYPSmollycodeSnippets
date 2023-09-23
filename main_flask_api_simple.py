from flask import Flask, request

app = Flask(__name__)
info = {
    1: {'name': 'Hafsa',
        'primary address': 'Wazirabad',
        'secondary address': 'Lower Topa'},
    2: {'name': 'NotHafsa',
        'primary address': 'Wazirabad',
        'secondary address': 'Lower Topa'}
}


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/getinfo/<int:info_id>', methods=['GET'])
def journey(info_id):
    return info[info_id]


@app.route('/postinfo', methods=['POST'])
def receive_json():
    data = request.get_json()
    name = data['name']
    return name


if __name__ == '__main__':
    app.run(debug=True)
