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

    #Loads video and capture it's frames
    vidFrameCap = cv2.VideoCapture(videoName)
    #Create a loop to capture all frames then save each to unique filename for sorting later on
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
    #Check total number of frames generated
    print("Total Number of Frames Generated from Video:", frameCount)

    totalBytes = 0
    secretData += "=====" #Add stopping criteria

    #Checking if there is sufficient bytes in video to encode data
    for frame in range(0, frameCount, 1):
        framePath = (os.path.join("./temp", "frame{:d}.png".format(frame)))
        image = cv2.imread(framePath)  #Read the image
        totalBytes += image.shape[0] * image.shape[1] * 3 // 8  #Maximum bytes to encode
    print("[*] Bytes available for encoding:", totalBytes)
    if len(secretData) > totalBytes:
        raise ValueError("[!] Insufficient bytes to encode data of %d bytes, need bigger image or less data." % len(secretData))
    else:
        print("[*] Sufficient bytes to encode data of %d bytes." % len(secretData))

    #Extract audio from video
    call(["ffmpeg", "-i", videoName, "-q:a", "0", "-map", "a", "temp/audio.mp3", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)

    #Start encoding process
    dataIndex = 0
    binarySecretData = convertToBin(secretData) #Convert data to binary
    dataLen = len(binarySecretData) #Size of data to hide
    for frame in range(0, frameCount, 1):
        framePath = (os.path.join("./temp", "frame{:d}.png".format(frame)))
        image = cv2.imread(framePath)  #Read the image

        print("[*] Encoding data...")
        if dataIndex < dataLen:
            for row in image:
                for pixel in row:
                    r, g, b = convertToBin(pixel) # convert RGB values to binary format
                    if dataIndex < dataLen: #Modify the red pixel bits depending on bitRange only if there is still data to store
                        if (dataLen - dataIndex) < bitRange: #If data left to store is less than the bitRange, left shift the data accordingly then store so that it can be decoded correctly later
                            pixel[0] = int(r[:-bitRange] + convertToBin(int(binarySecretData[dataIndex:(dataIndex + (dataLen - dataIndex))]) << (bitRange-(dataLen-dataIndex))), 2)
                            dataIndex += (dataLen - dataIndex)
                        else:
                            pixel[0] = int(r[:-bitRange] + binarySecretData[dataIndex:(dataIndex + bitRange)], 2)
                            dataIndex += bitRange
                    if dataIndex < dataLen: #Modify the green pixel bits depending on bitRange only if there is still data to store
                        if (dataLen - dataIndex) < bitRange: #If data left to store is less than the bitRange, left shift the data accordingly then store so that it can be decoded correctly later
                            pixel[1] = int(g[:-bitRange] + convertToBin(int(binarySecretData[dataIndex:(dataIndex + (dataLen - dataIndex))]) << (bitRange-(dataLen-dataIndex))), 2)
                            dataIndex += (dataLen - dataIndex)
                        else:
                            pixel[1] = int(g[:-bitRange] + binarySecretData[dataIndex:(dataIndex + bitRange)], 2)
                            dataIndex += bitRange
                    if dataIndex < dataLen: #Modify the blue pixel bits depending on bitRange only if there is still data to store
                        if (dataLen - dataIndex) < bitRange: #If data left to store is less than the bitRange, left shift the data accordingly then store so that it can be decoded correctly later
                            pixel[2] = int(b[:-bitRange] + convertToBin(int(binarySecretData[dataIndex:(dataIndex + (dataLen - dataIndex))]) << (bitRange-(dataLen-dataIndex))), 2)
                            dataIndex += (dataLen - dataIndex)
                        else:
                            pixel[2] = int(b[:-bitRange] + binarySecretData[dataIndex:(dataIndex + bitRange)], 2)
                            dataIndex += bitRange
                    print("Data encoded in Frame " + str(frame))
                    if dataIndex >= dataLen: #If data is encoded, just break out of the Loop
                        break
                    break
                break
        cv2.imwrite(os.path.join("./temp", "encFrame{:d}.png".format(frame)), image)
        continue

    call(["ffmpeg", "-i", "temp/encFrame%d.png", "-vcodec", "png", "temp/noAudioStegoVid.avi", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)
    call(["ffmpeg", "-i", "temp/noAudioStegoVid.avi", "-i", "temp/audio.mp3", "-codec", "copy", "temp/audioStegoVid.avi", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)
    call(["ffmpeg", "-i", "temp/audioStegoVid.avi", "-f", "avi", "-c:v", "rawvideo", "-pix_fmt", "rgb32", "stegoVideo.avi"], stdout=open(os.devnull, "w"), stderr=STDOUT)
    clean("temp")

def decode(videoName):
    frameCount = extractFrames(videoName)

    #Check total number of frames generated
    print("Total Number of Frames Generated from Video:", frameCount)

    binaryData = ""
    for frame in range(0, frameCount, 1):
        framePath = (os.path.join("./temp", "frame{:d}.png".format(frame)))
        image = cv2.imread(framePath)  #Read the image

        print("[+] Decoding...")
        for row in image:
            for pixel in row:
                r, g, b = convertToBin(pixel)
                binaryData += r[-bitRange:]
                binaryData += g[-bitRange:]
                binaryData += b[-bitRange:]
                break
            break
        continue

    #Split by 8-bits
    allBytes = [binaryData[i: i+8] for i in range(0, len(binaryData), 8)]
    #Convert from bits to characters
    decodedData = ""
    for byte in allBytes:
        decodedData += chr(int(byte, 2))
        if decodedData[-5:] == "=====":
            break
    clean("temp")
    return decodedData[:-5]

#Main Program
while True:
    userInput = input("Enter 1 to Encode, 2 to Decode and anything else to end program: ")

    #Encode
    if userInput == "1":
        bitRange = int(input("Please specific Bitrange to encode video by: "))
        videoName = input("Enter video name with its format to encode: ")
        textToHide = input("Enter the text you want to hide: ")
        print("Video to encode:", videoName)
        print("Text to Hide:", textToHide)

        #Encode and create new video file
        encode(videoName, textToHide)

    #Decode
    elif userInput == "2":
        bitRange = int(input("Please specific Bitrange to decode video by: "))
        videoName = input("Enter video name with its format to decode: ")
        print("Video to decode:", videoName)

        #Decode and display hidden text
        decodedText = decode(videoName)
        print("The hidden text in the video was:", decodedText)

    #End Program
    else:
        sys.exit("Program has been terminated")