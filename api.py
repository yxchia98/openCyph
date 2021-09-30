from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import json
import os
from EncoderDecoder import Encoder, Decoder
from filestream import get_stream


app = Flask(__name__)
CORS(app)


@app.get('/getImage')
def getImage(id=0):
    imgType = request.args.get('type')
    if imgType:
        if imgType == "coverObject":
            return send_file("./cover_assets/doge.jpg", mimetype='image/png')
        elif imgType == "stegoObject":
            imgID = request.args.get('id')
            if imgID:
                return send_file(f'./results/img/imgResult{imgID}.png', mimetype='image/png')


@app.post('/')
def receiveOptions():
    data = request.json

    result = {
        'coverObject': './cover_assets/doge.jpg',
        'stegoObject': './results/img/imgResult.png'
    }

    return jsonify(result)


@app.post('/uploadFile')
def uploadFile():
    if 'payloadFile' not in request.files:
        return jsonify({'error': f"Error: payload not found"})
    payloadFile = request.files['payloadFile']
    payloadFile.save(os.path.join("./payload_assets/",
                                  secure_filename(payloadFile.filename)))
    if 'coverFile' not in request.files:
        return jsonify({'error': f"Error: cover not found"})
    coverFile = request.files['coverFile']
    coverFile.save(os.path.join("./cover_assets/",
                                secure_filename(coverFile.filename)))
    if 'optionObject' not in request.form:
        return jsonify({'error': f"Error: object not found"})
    optionObject = json.loads(request.form['optionObject'])
    print(optionObject)

    try:
        sneakyBits = get_stream(
            f"./payload_assets/{secure_filename(payloadFile.filename)}")

        imagecoder = Encoder(
            f"./cover_assets/{secure_filename(coverFile.filename)}")
        imagecoder.setBitNumber(int(optionObject['coverNumBits']))
        imagecoder.encode(sneakyBits)
        # # imagecoder.writeText()
        imagecoder.generateNewPic(
            f"./results/img/imgResult{optionObject['id']}.png")
    except Exception as e:
        return jsonify({'error': f"{e}"})
    response = {
        'url': f"http://localhost:9999/getImage?type=stegoObject&id={optionObject['id']}",
        'id': optionObject['id']
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='9999')
