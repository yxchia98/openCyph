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


    def encode_audio(self, source, dest, payload):
        song = wave.open(source, 'rb')
        print('Channels: ', song.getnchannels(), '\nSample width:', song.getsampwidth(), '\nFramerate: ',
              song.getframerate(), '\nFrames: ', song.getnframes())
        frames = song.readframes(song.getnframes())
        frames = list(frames)
        frames = bytearray(frames)
        bin_payload = self.to_bin(payload)
        for i, bit in enumerate(bin_payload):
            frames[i] = (frames[i] & ~1) | int(bit)
        moddedFrames = bytes(frames)
        with wave.open(dest, 'wb') as newfile:
            newfile.setparams(song.getparams())
            newfile.writeframes(moddedFrames)
            newfile.close()
        song.close()

    def decode_audio(self, source):
        song = wave.open(source, 'rb')
        frames = song.readframes(song.getnframes())
        frames = bytearray(frames)
        decoded_bin = ''
        decoded_string = ''
        for byte in frames:
            decoded_bin += self.to_bin(byte)[-1]
        decoded_bin = [decoded_bin[index: index + 8] for index in range(0, len(decoded_bin), 8)]
        for byte in decoded_bin:
            val = int(byte, 2)
            if 31 < val < 128:
                decoded_string += format(val, 'c')

        return decoded_string



if __name__ == '__main__':

    audio = AudioCoder()
    print(audio.decode_audio('./stego_assets/audio_embedded.wav'))
    # sourcefile = './cover_assets/audio.wav'
    # destfile = './stego_assets/audio_embedded.wav'
    # # payload = str(input('Enter payload to be embedded: '))
    #
    # payload = 'THIS IS A SECRET TEXT'
    # encode_audio(sourcefile, destfile, payload)
    # with open('./stego_assets/decoded_audio.txt', 'w') as newfile:
    #     newfile.write(decode_audio(destfile))
    #     newfile.close()

