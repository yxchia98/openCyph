from PIL import Image

#choose image
im = Image.open("../cover_assets/doge.jpg")
width = im.width
height = im.height
px = im.load()

#extract pixel value
value = list(im.getdata())

pixArr = []
testArr = []

#convert to binary
for i in range(len(value)):
    red = bin(value[i][0])
    green = bin(value[i][1])
    blue = bin(value[i][2])
    pixArr.append([red, green, blue])

#initial file for debug
file = open('../results/img/data.txt', 'w')
for elements in pixArr:
    for data in elements:
        file.write(data + "  ")
    file.write("\n")
file.close()

#user var
payload = "the password is password"
tempArr = bytearray(payload, "utf-8")
payloadArr = []
for i in range(len(tempArr)):
    payloadArr.append(format(tempArr[i], "08b"))
payloadArr = "".join(payloadArr)
print("payload: ", payloadArr)

#bit number cannnot be > 8
bitNumber = 8

#set limits


counter = 0
color = 0
i = 2

while(i < len(payload)):
    #modify red bit
    if(color == 0):
        temp = pixArr[counter][0][:-bitNumber]
        for j in range(bitNumber):
            if((i+j)<len(payloadArr)):
                temp += payloadArr[i+j]
            else:
                temp += "0"
        pixArr[counter][0] = temp
        i += bitNumber
        color += 1

    #modify green bit
    elif(color == 1):
        temp = pixArr[counter][1][:-bitNumber]
        for j in range(bitNumber):
            if((i+j)<len(payloadArr)):
                temp += payloadArr[i+j]
            else:
                temp += "0"
        pixArr[counter][1] = temp
        i += bitNumber
        color += 1

    #modify blue bit
    elif(color == 2):
        temp = pixArr[counter][2][:-bitNumber]
        for j in range(bitNumber):
            if((i+j)<len(payloadArr)):
                temp += payloadArr[i+j]
            else:
                temp += "0"
        pixArr[counter][2] = temp
        i += bitNumber
        color = 0
        counter += 1

#save to data2.txt for debug
file = open("../results/img/data2.txt", 'w')
for i in pixArr:
    for j in i:
        file.write(j + " ")
    file.write('\n')
file.close()



#generate new pic
for i in range(len(pixArr)):
    red = int(pixArr[i][0], 2)
    green = int(pixArr[i][1], 2)
    blue = int(pixArr[i][2], 2)
    testArr.append((red, green, blue))

result = Image.new('RGB', (width, height))
result.putdata(testArr)

result.save('../results/img/imgResult.png')
