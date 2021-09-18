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


if __name__ == '__main__':
    image = cv2.imread("./cover_assets/8x8blackwhite.png")
    print(image.shape)
    for i in image[0]:
        print(to_bin(i))
    for i in image[1]:
        print(to_bin(i))
