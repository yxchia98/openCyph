from EncoderDecoder import Encoder, Decoder
from filestream import format_identifier, get_stream
from audio import AudioCoder

# Choose one file
# sneakyBits = get_stream("payload_assets/bloop.mp4")
# sneakyBits = get_stream("payload_assets/pinout.png")
# sneakyBits = get_stream("payload_assets/printer.pdf")
sneakyBits = get_stream("payload_assets/hass-lajv-lights.png")
# sneakyBits = get_stream("payload_assets/test.txt")

# Any Payload to Image Cover
imagecoder = Encoder("./cover_assets/TB1NAt.UEY1gK0jSZFC0.gwqXXa.jpg")
imagecoder.setBitNumber(6)
imagecoder.encode(sneakyBits)
# imagecoder.writeText()
imagecoder.generateNewPic("./results/img/imgResult.png")

# Audio Encoder
# audio = AudioCoder()
# source_file = './cover_assets/audio.wav'
# embedded_file = './stego_assets/audio_embedded.wav'
# decoded_text = './stego_assets/decoded_audio.txt'
# bitrange = 1
# payload = 'NOT SO SECRET'
# audio.encode_audio(source_file, embedded_file, payload, bitrange)
# audio.decode_audio(embedded_file, decoded_text, bitrange)

imagedecoder = Decoder("./results/img/imgResult.png")
imagedecoder.setBitNumber(6)
imagedecoder.readPayload()
imagedecoder.extractEmbeddedToFile()
