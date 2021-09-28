from audio import AudioCoder
from picture import Encoder


audiocoder = AudioCoder()
audioBits = audiocoder.get_stream("cover_assets/audio.wav")

imagecoder = Encoder("./cover_assets/mountain.jpeg", "01")

imagecoder.setBitNumber(4)
imagecoder.encode(audioBits)
# imagecoder.writeText()
imagecoder.generateNewPic("./results./img./imgResult.png")
