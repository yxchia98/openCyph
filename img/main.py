from encoder import Encoder

imgEncoder = Encoder("../cover_assets/doge.jpg")
imgEncoder.setBitNumber(1)
imgEncoder.encode(100)
imgEncoder.generateNewPic("../results./img./imgResult.png")
