from encoder import Encoder
from decoder import Decoder

imgEncoder = Encoder("../cover_assets/doge.jpg")
imgEncoder.setBitNumber(1)
imgEncoder.encode(1122334455)
imgEncoder.generateNewPic("../results/img/imgResult.png")


imgEncoder = Decoder("../results/img/imgResult.png")
