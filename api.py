from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import json
import os
from EncoderDecoder import Encoder, Decoder
from filestream import get_stream
from audio import AudioCoder


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

@app.get('/getWav')
def getWav(id=0):
    wavID = request.args.get('id')
    return send_file(f'./results/wav/wavResult{wavID}.wav', mimetype='audio/wav')


@app.get('/getDecodedFile')
def getDecodedFile():
    outputId = request.args.get('id')
    fileType = request.args.get('fileType')
    return send_file(f'./results/decoded_assets/output{outputId}{fileType}')

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

    if optionObject['coverType'] == "image":
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
    elif optionObject['coverType'] == "wav":
        try:
            audioencoder = AudioCoder()
            audioencoder.encode_audio(f"./cover_assets/{secure_filename(coverFile.filename)}", f"./results/wav/wavResult{optionObject['id']}.wav", f"./payload_assets/{secure_filename(payloadFile.filename)}", int(optionObject['coverNumBits']))
        except Exception as e:
            return jsonify({'error': f"{e}"})
        response = {
            'url': f"http://localhost:9999/getWav?id={optionObject['id']}",
            'id': optionObject['id']
        }

    return jsonify(response)

@app.post('/decodeFile')
def decodeFile():
    if 'encodedFile' not in request.files:
        return jsonify({'error': f"Error: encoded not found"})
    encodedFile = request.files['encodedFile']
    encodedFile.save(os.path.join("./encoded_assets/",
                                  secure_filename(encodedFile.filename)))
    if 'decodeOptionsObject' not in request.form:
        return jsonify({'error': f"Error: object not found"})
    decodeOptionsObject = json.loads(request.form['decodeOptionsObject'])
    print(decodeOptionsObject)

    if decodeOptionsObject['coverType'] == 'image':
        try:
            imagedecoder = Decoder(
                f"./encoded_assets/{secure_filename(encodedFile.filename)}")
            imagedecoder.setBitNumber(int(decodeOptionsObject['coverNumBits']))
            imagedecoder.readPayload()
            fileType = imagedecoder.extractEmbeddedToFile(decodeOptionsObject['id'])
        except Exception as e:
            return jsonify({'error': f"{e}"})
        response = {
            'url': f"http://localhost:9999/getDecodedFile?&id={decodeOptionsObject['id']}&fileType={fileType}",
            'id': decodeOptionsObject['id']
        }
    elif decodeOptionsObject['coverType'] == 'wav':
        try:
            audiodecoder = AudioCoder()
            fileType = audiodecoder.decode_audio(f"./encoded_assets/{secure_filename(encodedFile.filename)}", f"./results/decoded_assets/output{decodeOptionsObject['id']}", int(decodeOptionsObject['coverNumBits']), 'file')
        except Exception as e:
            return jsonify({'error': f"{e}"})
        response = {
            'url': f"http://localhost:9999/getDecodedFile?&id={decodeOptionsObject['id']}&fileType={fileType}",
            'id': decodeOptionsObject['id']
        }
    
    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='9999')
