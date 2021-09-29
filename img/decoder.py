from PIL import Image


class Decoder:
    def __init__(self, url):
        self.originalArr = []
        image = Image.open(url)
        self.width = image.width
        self.height = image.height
        self.size = self.width * self.height
        pixelList = list(image.getdata())

        newArray = ''
        for i in pixelList:
            newArray += bin(i[0])[-1] + bin(i[1])[-1] + bin(i[2])[-1]

        print(newArray)
        file = open('../output.txt', 'w')
        file.write(newArray)
        file.close()
