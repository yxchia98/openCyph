import cv2, numpy as np
import os
import shutil
from subprocess import call, STDOUT
import sys

class VideoCoder:
    def __init__(self):
        self.source = ''
        self.payload = ''
        self.dest = ''

    def convert_to_bin(self, data):
        #Convert 'data' to binary format as string
        if isinstance(data, str):
            return ''.join([ format(ord(i), "08b") for i in data ])
        elif isinstance(data, bytes) or isinstance(data, np.ndarray):
            return [ format(i, "08b") for i in data ]
        elif isinstance(data, int) or isinstance(data, np.uint8):
            return format(data, "08b")
        else:
            raise TypeError("Type not supported.")

    def extract_frames(self, videoName):
        if not os.path.exists("./temp"):
            os.makedirs("temp")
        print("[INFO] temp directory created")

        #Loads video and capture it's frames
        vidframecap = cv2.VideoCapture(videoName)
        #Create a loop to capture all frames then save each to unique filename for sorting later on
        framesgenerated = 0
        while True:
            success, image = vidframecap.read()
            if not success:
                break
            cv2.imwrite(os.path.join("./temp", "frame{:d}.png".format(framesgenerated)), image)
            framesgenerated += 1

        return framesgenerated

    def clean(self, path):
        if os.path.exists("./" + path):
            shutil.rmtree("./" + path)
            print("[INFO] " + path + " files cleaned up")

    def encode_video(self, videoName, secretData, bitRange):
        if os.path.exists("./encoded_assets/decoded_video.txt"):
            os.remove("./encoded_assets/decoded_video.txt")
        if os.path.exists("./encoded_assets/stegoVideo.avi"):
            os.remove("./encoded_assets/stegoVideo.avi")

        framecount = self.extract_frames(videoName)
        #Check total number of frames generated
        print("Total Number of Frames Generated from Video:", framecount)

        totalbytes = 0
        secretData += "=====" #Add stopping criteria

        #Checking if there is sufficient bytes in video to encode data
        for frame in range(0, framecount, 1):
            framepath = (os.path.join("./temp", "frame{:d}.png".format(frame)))
            image = cv2.imread(framepath)  #Read the image
            totalbytes += image.shape[0] * image.shape[1] * 3 // 8  #Maximum bytes to encode
        print("[*] Bytes available for encoding:", totalbytes)
        if len(secretData) > totalbytes:
            raise ValueError("[!] Insufficient bytes to encode data of %d bytes, need bigger image or less data." % len(secretData))
        else:
            print("[*] Sufficient bytes to encode data of %d bytes." % len(secretData))

        #Extract audio from video
        call(["ffmpeg", "-i", videoName, "-q:a", "0", "-map", "a", "temp/audio.mp3", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)

        #Start encoding process
        dataencoded = False
        iterations = 1
        dataindex = 0
        binarysecretdata = self.convert_to_bin(secretData) #Convert data to binary
        datalen = len(binarysecretdata) #Size of data to hide
        pixelarray = np.zeros((1,3))
        while dataencoded == False:
            for frame in range(0, framecount, 1):
                framepath = (os.path.join("./temp", "frame{:d}.png".format(frame)))
                image = cv2.imread(framepath)  #Read the image

                print("[*] Encoding data...")
                if dataindex < datalen:
                    for row in image:
                        if np.isin(np.array(row), np.array(pixelarray)).all():
                            continue #All pixels in row is already encoded with data, go next row

                        i = 1
                        for pixel in row:
                            if i < iterations:
                                i += 1
                                continue

                            r, g, b = self.convert_to_bin(pixel) #Convert RGB values to binary format
                            if dataindex < datalen: #Modify the red pixel bits depending on bitRange only if there is still data to store
                                if (datalen - dataindex) < bitRange: #If data left to store is less than the bitRange, left shift the data accordingly then store so that it can be decoded correctly later
                                    pixel[0] = int(r[:-bitRange] + self.convert_to_bin(int(binarysecretdata[dataindex:(dataindex + (datalen - dataindex))]) << (bitRange-(datalen-dataindex))), 2)
                                    dataindex += (datalen - dataindex)
                                else:
                                    pixel[0] = int(r[:-bitRange] + binarysecretdata[dataindex:(dataindex + bitRange)], 2)
                                    dataindex += bitRange
                            if dataindex < datalen: #Modify the green pixel bits depending on bitRange only if there is still data to store
                                if (datalen - dataindex) < bitRange: #If data left to store is less than the bitRange, left shift the data accordingly then store so that it can be decoded correctly later
                                    pixel[1] = int(g[:-bitRange] + self.convert_to_bin(int(binarysecretdata[dataindex:(dataindex + (datalen - dataindex))]) << (bitRange-(datalen-dataindex))), 2)
                                    dataindex += (datalen - dataindex)
                                else:
                                    pixel[1] = int(g[:-bitRange] + binarysecretdata[dataindex:(dataindex + bitRange)], 2)
                                    dataindex += bitRange
                            if dataindex < datalen: #Modify the blue pixel bits depending on bitRange only if there is still data to store
                                if (datalen - dataindex) < bitRange: #If data left to store is less than the bitRange, left shift the data accordingly then store so that it can be decoded correctly later
                                    pixel[2] = int(b[:-bitRange] + self.convert_to_bin(int(binarysecretdata[dataindex:(dataindex + (datalen - dataindex))]) << (bitRange-(datalen-dataindex))), 2)
                                    dataindex += (datalen - dataindex)
                                else:
                                    pixel[2] = int(b[:-bitRange] + binarysecretdata[dataindex:(dataindex + bitRange)], 2)
                                    dataindex += bitRange
                            print("Data encoded in Frame " + str(frame))

                            pixelarray = np.append(pixelarray, [pixel], axis=0)

                            if dataindex >= datalen: #If data is encoded, just break out of the Loop
                                dataencoded = True #All data encoded, change variable to True to end While Loop
                                break

                            if len(row) + 1 == iterations:  # If all pixels in a row of a frame is encoded, go next row
                                iterations = 0

                            if frame + 1 == framecount: #All frames have that certain pixel encoded e.g. 1st pixel)
                                if len(row) + 1 == iterations: #If last pixels of the row encoded
                                    iterations = 1 #Restart the iteration variable
                                elif len(row) + 1 > iterations: #If not all pixels of the row encoded
                                    iterations += 1 #The loop restarts from first frame and now encode the next pixel available

                            break
                        break
                cv2.imwrite(os.path.join("./temp", "frame{:d}.png".format(frame)), image) #Replace old frame with new frame
                if dataindex >= datalen: #If data is encoded, just break out of the Loop
                    break
                #If not all data encoded, program will continue looping

        call(["ffmpeg", "-i", "temp/frame%d.png", "-vcodec", "png", "temp/noAudioStegoVid.avi", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)
        call(["ffmpeg", "-i", "temp/noAudioStegoVid.avi", "-i", "temp/audio.mp3", "-codec", "copy", "temp/audioStegoVid.avi", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)
        call(["ffmpeg", "-i", "temp/audioStegoVid.avi", "-f", "avi", "-c:v", "rawvideo", "-pix_fmt", "rgb32", "./encoded_assets/stegoVideo.avi"], stdout=open(os.devnull, "w"), stderr=STDOUT)
        self.clean("temp")

    def decode_video(self, videoName, decodedText, bitRange):
        framecount = self.extract_frames(videoName)

        #Check total number of frames generated
        print("Total Number of Frames Generated from Video:", framecount)

        datadecoded = False
        iterations = 1
        binarydata = ""
        pixelarray = np.zeros((1, 3))
        while datadecoded == False:
            for frame in range(0, framecount, 1):
                framepath = (os.path.join("./temp", "frame{:d}.png".format(frame)))
                image = cv2.imread(framepath)  #Read the image

                print("[+] Decoding...")
                for row in image:
                    if np.isin(np.array(row), np.array(pixelarray)).all():
                        continue  #All pixels in row is already encoded with data, go next row

                    i = 1
                    for pixel in row:
                        if i < iterations:
                            i += 1
                            continue

                        r, g, b = self.convert_to_bin(pixel)
                        binarydata += r[-bitRange:]
                        binarydata += g[-bitRange:]
                        binarydata += b[-bitRange:]

                        pixelarray = np.append(pixelarray, [pixel], axis=0)

                        if frame + 1 == framecount:  # All frames have that certain pixel encoded e.g. 1st pixel)
                            if len(row) + 1 == iterations:  # If last pixels of the row encoded
                                iterations = 1  # Restart the iteration variable
                            elif len(row) + 1 > iterations:  # If not all pixels of the row encoded
                                iterations += 1  # The loop restarts from first frame and now encode the next pixel available

                        break
                    break

            #Split by 8-bits
            allbytes = [binarydata[i: i+8] for i in range(0, len(binarydata), 8)]
            #Convert from bits to characters
            decodeddata = ""
            for byte in allbytes:
                decodeddata += chr(int(byte, 2))
                if decodeddata[-5:] == "=====":
                    datadecoded = True
                    break

        self.clean("temp")
        with open(decodedText, 'w') as newfile:
            newfile.write(decodeddata[:-5])
            newfile.close()

# Video Encoder
video = VideoCoder()
source_file = "./cover_assets/coverWaterfall.mp4"
embedded_file = "./encoded_assets/stegoVideo.avi"
decoded_text = "./encoded_assets/decoded_video.txt"
bitRange = 3
payload = "There are many variations of passages of Lorem Ipsum available"
video.encode_video(source_file, payload, bitRange)
video.decode_video(embedded_file, decoded_text, bitRange)