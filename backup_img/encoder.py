from PIL import Image


class Encoder:
    def __init__(self, url):
        self.originalArr = []
        self.resultArr = []
        image = Image.open(url)
        self.width = image.width
        self.height = image.height
        self.size = self.width * self.height
        self.bitNumber = 1
        pixel = image.load()

        # convert image to bits
        intValue = list(image.getdata())
        for i in range(len(intValue)):
            red = bin(intValue[i][0])
            green = bin(intValue[i][1])
            blue = bin(intValue[i][2])
            self.originalArr.append([red, green, blue])

        # save to file for debug
        file = open('./results/img/data.txt', 'w')

        for elements in self.originalArr:
            for data in elements:
                file.write(data + "  ")
            file.write("\n")

        file.close()

    def setPayload(self, payload):
        #import payload
        # calls self.checkPayload()
        # returns binary string array
        binary = bin(payload)
        check = self.checkPayload(len(binary))

        if(check == True):
            return binary
        else:
            sys.exit("Payload is larger than file")

    def checkPayload(self, payloadLength):
        # returns True or False
        bitNumber = self.bitNumber
        size = self.size
        if(bitNumber == 1 & payloadLength < (size*3)):
            return True
        elif(bitNumber == 2 & payloadLength < (size*6)):
            return True
        elif(bitNumber == 3 & payloadLength < (size*9)):
            return True
        elif(bitNumber == 4 & payloadLength < (size*12)):
            return True
        elif(bitNumber == 5 & payloadLength < (size*15)):
            return True
        elif(bitNumber == 6 & payloadLength < (size*18)):
            return True
        elif(bitNumber == 7 & payloadLength < (size*21)):
            return True
        elif(bitNumber == 8 & payloadLength < (size*24)):
            return True
        else:
            return False

    def setBitNumber(self, bitNumber):
        self.bitNumber = bitNumber

    def encode(self, userInput):
        counter = 0
        color = 0
        i = 2
        payload = self.setPayload(userInput)
        bitNumber = self.bitNumber
        pixArr = self.originalArr

        while(i < len(payload)):
            # modify red bit
            if(color == 0):
                temp = pixArr[counter][0][:-bitNumber]
                for j in range(bitNumber):
                    if((i+j) < len(payload)):
                        temp += payload[i+j]
                    else:
                        temp += "0"
                pixArr[counter][0] = temp
                i += bitNumber
                color += 1

            # modify green bit
            elif(color == 1):
                temp = pixArr[counter][1][:-bitNumber]
                for j in range(bitNumber):
                    if((i+j) < len(payload)):
                        temp += payload[i+j]
                    else:
                        temp += "0"
                pixArr[counter][1] = temp
                i += bitNumber
                color += 1

            # modify blue bit
            elif(color == 2):
                temp = pixArr[counter][2][:-bitNumber]
                for j in range(bitNumber):
                    if((i+j) < len(payload)):
                        temp += payload[i+j]
                    else:
                        temp += "0"
                pixArr[counter][2] = temp
                i += bitNumber
                color = 0
                counter += 1

            # return pixArr
            self.resultArr = pixArr

    def generateNewPic(self, saveUrl):
        pixArr = self.resultArr
        temp = []
        for i in range(len(pixArr)):
            red = int(pixArr[i][0], 2)
            green = int(pixArr[i][1], 2)
            blue = int(pixArr[i][2], 2)
            temp.append((red, green, blue))

        result = Image.new('RGB', (self.width, self.height))
        result.putdata(temp)
        result.save(saveUrl)
