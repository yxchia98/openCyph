import sys

import numpy as np
import wave
import re

class AudioCoder:
    def __init__(self):
        self.source = ''
        self.payload = ''
        self.dest = ''


    def to_bin(self, data):
        # Convert 'data' to binary format as String
        if isinstance(data, str):
            return ''.join([format(ord(i), "08b") for i in data])
        elif isinstance(data, bytes) or isinstance(data, np.ndarray):
            return [format(i, "08b") for i in data]
        elif isinstance(data, int) or isinstance(data, np.uint8):
            return format(data, "08b")
        else:
            raise TypeError("Type is not supported.")


    def encode_audio(self, source, dest, payload, bitrange):
        song = wave.open(source, 'rb')
        print('Channels: ', song.getnchannels(), '\nSample width:', song.getsampwidth(), '\nFramerate: ',
              song.getframerate(), '\nFrames: ', song.getnframes())
        print(song.getparams())
        # Get all frames in wav
        frames = song.readframes(song.getnframes())
        frames = list(frames)
        frames = bytearray(frames)

        # Convert payload to binary
        bin_payload = self.to_bin(payload)
        # apply payload padding
        # Split the payload into specified bitranges
        bin_payload = [bin_payload[index: index + bitrange] for index in range(0, len(bin_payload), bitrange)]

        # set bitmask clear to specified bitranges
        bitmask = 0
        for i in range(0, bitrange):
            bitmask += 1 << i
        bitmask = bitmask.to_bytes(1, byteorder=sys.byteorder)
        bitmask = bitmask[0]
        print('bitmask: ', bitmask)

        for i, bits in enumerate(bin_payload):
            frames[i] = (frames[i] & ~bitmask) | int(bits, 2)
        modded_frames = bytes(frames)
        with wave.open(dest, 'wb') as newfile:
            newfile.setparams(song.getparams())
            newfile.writeframes(modded_frames)
            newfile.close()
        song.close()

    def decode_audio(self, source, bitrange):
        song = wave.open(source, 'rb')
        frames = song.readframes(song.getnframes())
        frames = bytearray(frames)
        decoded_bin = ''
        decoded_string = ''
        # counter = 8
        # for byte in frames:
        #     counter -= bitrange
        #     if counter >= 0:
        #         decoded_bin += self.to_bin(byte)[-bitrange:]
        #     else:
        #         decoded_bin += self.to_bin(byte)[-(bitrange - 1):]
        #         counter = 8
        for byte in frames:
            decoded_bin += self.to_bin(byte)[-bitrange:]
        decoded_bin = [decoded_bin[index: index + 8] for index in range(0, len(decoded_bin), 8)]
        for byte in decoded_bin:
            val = int(byte, 2)
            if 31 < val < 128:
                decoded_string += format(val, 'c')

        return decoded_string



if __name__ == '__main__':
    audio = AudioCoder()
    sourcefile = './cover_assets/audio.wav'
    destfile = './stego_assets/audio_embedded.wav'
    # payload = str(input('Enter payload to be embedded: '))
    payload = 'TESTING3'
    audio.encode_audio(sourcefile, destfile, payload, 3)
    with open('./stego_assets/decoded_audio.txt', 'w') as newfile:
        newfile.write(audio.decode_audio(destfile, 3))
        newfile.close()

