import cv2, numpy as np
import os
import shutil
from subprocess import call, STDOUT
import sys

def convertToBin(data):
    """Convert 'data' to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def extractFrames(videoName):
    if not os.path.exists("./temp"):
        os.makedirs("temp")
    print("[INFO] temp directory created")

    # Loads video and capture it's frames
    vidFrameCap = cv2.VideoCapture(videoName)
    # Create a loop to capture all frames then save each to unique filename for sorting later on
    framesGenerated = 0
    while True:
        success, image = vidFrameCap.read()
        if not success:
            break
        cv2.imwrite(os.path.join("./temp", "frame{:d}.png".format(framesGenerated)), image)
        framesGenerated += 1

    return framesGenerated

def clean(path):
    if os.path.exists("./" + path):
        shutil.rmtree("./" + path)
        print("[INFO] " + path + " files cleaned up")

def encode(videoName, secretData):
    frameCount = extractFrames(videoName)

    # Check total number of frames generated
    print("Total Number of Frames Generated from Video: ", frameCount)

    call(["ffmpeg", "-i", videoName, "-q:a", "0", "-map", "a", "temp/audio.mp3", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)

    totalBytes = 0
    secretData += "=====" # add stopping criteria
    print(convertToBin(secretData))

    dataIndex = 0
    binarySecretData = convertToBin(secretData) # Convert data to binary
    dataLen = len(binarySecretData) # size of data to hide
    for frame in range(0, frameCount, 1):
        framePath = (os.path.join("./temp", "frame{:d}.png".format(frame)))
        image = cv2.imread(framePath)  # read the image
        totalBytes += image.shape[0] * image.shape[1] * 3 // 8  # maximum bytes to encode
        print("[*] Bytes available for encoding:", totalBytes)
        if len(secretData) > totalBytes:
            raise ValueError("[!] Insufficient bytes, need bigger image or less data.")

        print("[*] Encoding data...")
        if dataIndex < dataLen:
            for row in image:
                for pixel in row:
                    r, g, b = convertToBin(pixel) # convert RGB values to binary format
                    if dataIndex < dataLen: # modify the Least Significant bit only if there is still data to store
                        pixel[0] = int(r[:-1] + binarySecretData[dataIndex], 2) # Least significant red pixel bit
                        dataIndex += 1
                    if dataIndex < dataLen:
                        pixel[1] = int(g[:-1] + binarySecretData[dataIndex], 2)  # Least significant green pixel bit
                        dataIndex += 1
                    if dataIndex < dataLen:
                        pixel[2] = int(b[:-1] + binarySecretData[dataIndex], 2)  # Least significant blue pixel bit
                        dataIndex += 1
                    print("Data encoded in Frame " + str(frame))
                    if dataIndex >= dataLen: # if data is encoded, just break out of the Loop
                        break
                    break
                break
        cv2.imwrite(os.path.join("./temp", "encFrame{:d}.png".format(frame)), image)
        continue

    call(["ffmpeg", "-i", "temp/encFrame%d.png", "-vcodec", "png", "temp/noAudioStegoVid.mp4", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)
    call(["ffmpeg", "-i", "temp/noAudioStegoVid.mp4", "-i", "temp/audio.mp3", "-codec", "copy", "temp/audioStegoVid.mp4", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)
    call(["ffmpeg", "-i", "temp/audioStegoVid.mp4", "-f", "avi", "-c:v", "huffyuv", "stegoVideo.avi"], stdout=open(os.devnull, "w"), stderr=STDOUT)
    clean("temp")

def decode(videoName):
    frameCount = extractFrames(videoName)

    # Check total number of frames generated
    print("Total Number of Frames Generated from Video: ", frameCount)

    binaryData = ""
    for frame in range(0, frameCount, 1):
        framePath = (os.path.join("./temp", "frame{:d}.png".format(frame)))
        image = cv2.imread(framePath)  # read the image

        print("[+] Decoding...")
        for row in image:
            for pixel in row:
                r, g, b = convertToBin(pixel)
                binaryData += r[-1]
                binaryData += g[-1]
                binaryData += b[-1]
                break
            break
        continue

    # split by 8-bits
    allBytes = [binaryData[i: i+8] for i in range(0, len(binaryData), 8)]
    # convert from bits to characters
    decodedData = ""
    for byte in allBytes:
        decodedData += chr(int(byte, 2))
        if decodedData[-5:] == "=====":
            break
    clean("temp")
    return decodedData[:-5]

#Main Program
while True:
    userInput = input("Enter 1 to Encode, 2 to Decode, 3 to Restore Video to Playable Format and anything else to end program: ")

    #Encode
    if userInput == "1":
        videoName = input("Enter video name with its format to encode: ")
        textToHide = input("Enter the text you want to hide: ")
        print("Video to encode: ", videoName)
        print("Text to Hide: ", textToHide)

        #Encode and create new video file
        encode(videoName, textToHide)

    #Decode
    elif userInput == "2":
        videoName = input("Enter video name with its format to decode: ")
        print("Video to decode: ", videoName)

        #Decode and display hidden text
        decodedText = decode(videoName)
        print("The hidden text in the video was: ", decodedText)

    #Restore Video to Playable Format
    elif userInput == "3":
        print("Function for ltr (Ignore)")

    #End Program
    else:
        sys.exit("Program has been terminated")

