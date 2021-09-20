import cv2
import numpy as np

def to_bin(data):
    # Convert 'data' to binary format as String
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type is not supported.")

def combineColorPlanes(blue, green, red):
    newimg = np.append([blue], [green], axis=0)
    newimg = np.append(newimg, [red], axis=0)
    newimg = np.moveaxis(newimg, 0, -1)
    return newimg

if __name__ == '__main__':
    img = cv2.imread("./cover_assets/doge.jpg")
    print(img.shape)
    copyimg = img.copy()
    count = 0
    # copyimg[:, :, :] = 0        # opencv uses B G R format
    # extract out all blue, green and red colors individually
    onlyblue = copyimg[:, :, 0]
    onlygreen = copyimg[:, :, 1]
    onlyred = copyimg[:, :, 2]
    # Combine back the planes
    newimg = combineColorPlanes(onlyblue, onlygreen, onlyred)

    # uncomment for each of the below functionalities
    # Take out all blue
    # newimg[:, :, 0] = 0
    # # Take out all green
    # newimg[:, :, 1] = 0
    # # Take out all red
    # newimg[:, :, 2] = 0

    print(newimg.shape)

    # for i in copyimg:
    #     for n in i:
    #         print(to_bin(n))
    #         count += 1

    print('Converted ' + str(count) + ' pixels')

    cv2.imshow('test', newimg)
    cv2.waitKey(0)
