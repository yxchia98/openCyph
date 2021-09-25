from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


from img.encoder import Encoder
from img.decoder import Decoder


app = Flask(__name__)
CORS(app)


@app.get('/getImage')
def getImage():
    imgType = request.args.get('type')
    if imgType:
        if imgType == "coverObject":
            return send_file("./cover_assets/doge.jpg", mimetype='image/png')
        elif imgType == "stegoObject":
            return send_file('./results/img/imgResult.png', mimetype='image/png')


@app.post('/')
def receiveOptions():
    data = request.json

    imgEncoder = Encoder("./cover_assets/doge.jpg")
    imgEncoder.setBitNumber(int(data['numBits']))
    imgEncoder.encode(1122334455)
    # data['filetype']
    imgEncoder.generateNewPic("./results/img/imgResult.png")
    result = {
        'coverObject': './cover_assets/doge.jpg',
        'stegoObject': './results/img/imgResult.png'
    }

    return jsonify(result)


@app.post('/uploadFile')
def uploadFile():
    if 'file' not in request.files:
        return "nofile"
    file = request.files['file']
    if file.filename == '':
        return 'no filename'

    print(file)
    return "File saved successfully"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='9999')
