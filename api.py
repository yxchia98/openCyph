from flask import Flask, send_file, request, jsonify
from flask_cors import CORS

from img.encoder import Encoder
from img.decoder import Decoder


app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    imgEncoder = Encoder("./cover_assets/doge.jpg")
    imgEncoder.setBitNumber(1)
    imgEncoder.encode(1122334455)
    imgEncoder.generateNewPic("./results/img/imgResult.png")

    filename = './results/img/imgResult.png'
    return send_file(filename, mimetype='image/jpg')


@app.post('/')
def receiveOptions():
    data = request.json
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='9999')
