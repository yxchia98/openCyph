from picture import Encoder
from filestream import get_stream

sneakyBits = get_stream("cover_assets/audio.wav")

imagecoder = Encoder("./cover_assets/mountain.jpeg", "01")

imagecoder.setBitNumber(6)
imagecoder.encode(sneakyBits)
# imagecoder.writeText()
imagecoder.generateNewPic("./results./img./imgResult.png")
