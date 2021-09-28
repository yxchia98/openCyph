from encoder import Encoder

#import payload

#check payload filetype
#00 txt
# 01 mp3
# 10 mp4
# 11 tbc

#para1: url to cover
#para2: filetype of payload
filetype = "00"
imgEncoder = Encoder("../cover_assets/doge.jpg", filetype)
imgEncoder.setBitNumber(1)
imgEncoder.encode(100)
imgEncoder.generateNewPic("../results./img./imgResult.png")
