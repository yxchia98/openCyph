from picture import Encoder
from filestream import get_stream
from audio import AudioCoder


# sneakyBits = get_stream("cover_assets/audio.wav")

# imagecoder = Encoder("./cover_assets/mountain.jpeg")

# imagecoder.setBitNumber(6)
# imagecoder.encode(sneakyBits)
# # imagecoder.writeText()
# imagecoder.generateNewPic("./results/img/imgResult.png")


audio = AudioCoder()
source_file = './cover_assets/audio.wav'
embedded_file = './stego_assets/audio_embedded.wav'
decoded_text = './stego_assets/decoded_audio.txt'
bitrange = 1
payload = 'NOT SO SECRET'
audio.encode_audio(source_file, embedded_file, payload, bitrange)
audio.decode_audio(embedded_file, decoded_text, bitrange)
