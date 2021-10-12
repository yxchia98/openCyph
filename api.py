from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import json
import os
from EncoderDecoder import Encoder, Decoder
from filestream import get_stream
from audio import AudioCoder
from video import VideoCoder


app = Flask(__name__)
CORS(app)

# API_ENDPOINT = 'http://localhost:9999'
API_ENDPOINT = 'https://stego-api.bongzy.me'


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


@app.get('/getAvi')
def getAvi(id=0):
    aviID = request.args.get('id')
    return send_file(f'./results/avi/aviResult{aviID}.avi', mimetype='video/x-msvideo')


@app.get('/getDecodedFile')
def getDecodedFile():
    outputId = request.args.get('id')
    fileType = request.args.get('fileType')
    # if fileType == '.txt':
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

    if 'optionObject' not in request.form:
        return jsonify({'error': f"Error: object not found"})
    optionObject = json.loads(request.form['optionObject'])
    print(optionObject)

    if optionObject['payloadType'] != 'plaintext':
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
    else:
        if 'coverFile' not in request.files:
            return jsonify({'error': f"Error: cover not found"})
        coverFile = request.files['coverFile']
        coverFile.save(os.path.join("./cover_assets/",
                                    secure_filename(coverFile.filename)))

    if optionObject['coverType'] == "image":
        try:
            if str(os.path.splitext(secure_filename(coverFile.filename))[1]) in ['.png', '.jpg', '.jpeg']:
                if optionObject['payloadType'] == 'plaintext':
                    plaintextToEncode = str(optionObject['payloadText'])
                    print(plaintextToEncode)
                    with open('./payload_assets/plaintext.txt', 'w') as f:
                        f.write(plaintextToEncode)
                    sneakyBits = get_stream('./payload_assets/plaintext.txt')
                else:
                    sneakyBits = get_stream(
                        f"./payload_assets/{secure_filename(payloadFile.filename)}")

                imagecoder = Encoder(
                    f"./cover_assets/{secure_filename(coverFile.filename)}")
                imagecoder.setBitNumber(int(optionObject['coverNumBits']))
                imagecoder.encode(sneakyBits)
                # # imagecoder.writeText()
                imagecoder.generateNewPic(
                    f"./results/img/imgResult{optionObject['id']}.png")
            else:
                raise Exception("NOT IMAGE FILE")
        except Exception as e:
            return jsonify({'error': f"{e}"})
        response = {
            'url': f"{API_ENDPOINT}/getImage?type=stegoObject&id={optionObject['id']}",
            'id': optionObject['id']
        }
    elif optionObject['coverType'] == "wav":
        try:
            if os.path.splitext(secure_filename(coverFile.filename))[1] == '.wav':
                audioencoder = AudioCoder()
                audioencoder.encode_audio(f"./cover_assets/{secure_filename(coverFile.filename)}",
                                          f"./results/wav/wavResult{optionObject['id']}.wav", f"./payload_assets/{secure_filename(payloadFile.filename)}", int(optionObject['coverNumBits']))
            else:
                raise Exception("NOT WAV")
        except Exception as e:
            return jsonify({'error': f"{e}"})
        response = {
            'url': f"{API_ENDPOINT}/getWav?id={optionObject['id']}",
            'id': optionObject['id']
        }
    elif optionObject['coverType'] == 'mp4':
        try:
            if os.path.splitext(secure_filename(coverFile.filename))[1] == '.mp4':
                videoencoder = VideoCoder()
                videoencoder.encode_video(f"./cover_assets/{secure_filename(coverFile.filename)}", str(
                    optionObject['payloadText']), int(optionObject['coverNumBits']), int(optionObject['id']))
            else:
                raise Exception("NOT MP4")
        except Exception as e:
            return jsonify({'error': f"{e}"})
        response = {
            'url': f"{API_ENDPOINT}/getAvi?id={optionObject['id']}",
            'id': optionObject['id']
        }

    return jsonify(response)


@ app.post('/decodeFile')
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
            if str(os.path.splitext(secure_filename(encodedFile.filename))[1]) in ['.png', '.jpg', '.jpeg']:
                imagedecoder = Decoder(
                    f"./encoded_assets/{secure_filename(encodedFile.filename)}")
                imagedecoder.setBitNumber(
                    int(decodeOptionsObject['coverNumBits']))
                imagedecoder.readPayload()
                fileType = imagedecoder.extractEmbeddedToFile(
                    decodeOptionsObject['id'])
            else:
                raise Exception("NOT IMAGE FILE")
        except Exception as e:
            return jsonify({'error': f"{e}"})
        response = {
            'url': f"{API_ENDPOINT}/getDecodedFile?&id={decodeOptionsObject['id']}&fileType={fileType}",
            'id': decodeOptionsObject['id']
        }
    elif decodeOptionsObject['coverType'] == 'wav':
        try:
            if str(os.path.splitext(secure_filename(encodedFile.filename))[1]) in ['.wav']:
                audiodecoder = AudioCoder()
                fileType = audiodecoder.decode_audio(f"./encoded_assets/{secure_filename(encodedFile.filename)}",
                                                     f"./results/decoded_assets/output{decodeOptionsObject['id']}", int(decodeOptionsObject['coverNumBits']), 'file')
            else:
                raise Exception("NOT WAV FILE")
        except Exception as e:
            return jsonify({'error': f"{e}"})
        response = {
            'url': f"{API_ENDPOINT}/getDecodedFile?&id={decodeOptionsObject['id']}&fileType={fileType}",
            'id': decodeOptionsObject['id']
        }
    elif decodeOptionsObject['coverType'] == 'avi':
        try:
            if str(os.path.splitext(secure_filename(encodedFile.filename))[1]) in ['.avi']:
                videodecoder = VideoCoder()
                videodecoder.decode_video(f"./encoded_assets/{secure_filename(encodedFile.filename)}",
                                          f"./results/decoded_assets/output{decodeOptionsObject['id']}.txt", int(decodeOptionsObject['coverNumBits']))
            else:
                raise Exception("NOT AVI FILE")
        except Exception as e:
            return jsonify({'error': f"{e}"})
        response = {
            'url': f"{API_ENDPOINT}/getDecodedFile?&id={decodeOptionsObject['id']}&fileType=.txt",
            'id': decodeOptionsObject['id']
        }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='9999')
