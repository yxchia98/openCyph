from EncoderDecoder import Encoder, Decoder
from filestream import format_identifier, get_stream
from audio import AudioCoder
from video import VideoCoder

# Choose one file
# sneakyBits = get_stream("payload_assets/bloop.mp4")
# sneakyBits = get_stream("payload_assets/pinout.png")
# sneakyBits = get_stream("payload_assets/printer.pdf")
sneakyBits = get_stream("payload_assets/doge.jpg")
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

# Video Encoder
#video = VideoCoder()
#source_file = "./cover_assets/coverWaterfall.mp4"
#embedded_file = "./encoded_assets/stegoVideo.avi"
#decoded_text = "./encoded_assets/decoded_video.txt"
#bitRange = 3
#payload = "There are many variations of passages of Lorem Ipsum available"
#video.encode_video(source_file, payload, bitRange)
#video.decode_video(embedded_file, decoded_text, bitRange)

imagedecoder = Decoder("./results/img/imgResult.png")
imagedecoder.setBitNumber(6)
imagedecoder.readPayload()
imagedecoder.extractEmbeddedToFile(123)
