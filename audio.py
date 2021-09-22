import os.path
import pathlib
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
        # error checking, and checking if file exists
        if source[-4:] != '.wav':
            source += '.wav'
        if dest[-4:] != '.wav':
            dest += '.wav'
        if not os.path.exists(source):
            print('[!] Source file does not exist, only .wav files are accepted')
            return
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
        # Split the payload into specified bitrange slices
        bin_payload = [bin_payload[index: index + bitrange] for index in range(0, len(bin_payload), bitrange)]
        print(bin_payload)

        # set bitmask clear to specified bitranges
        bitmask = 0
        for i in range(0, bitrange):
            bitmask += 1 << i
        bitmask = bitmask.to_bytes(1, byteorder=sys.byteorder)
        bitmask = bitmask[0]

        # embed payload into frames, payload slices determined by bitrange specified
        for i, bits in enumerate(bin_payload):
            # if binary slice is not the specified bitrange length (usually happens to the last bit), add trailing 0s
            if len(bits) < bitrange:
                bits = bits.ljust(bitrange, '0')
            # clear specified number of bits, and set bits according to payload
            frames[i] = (frames[i] & ~bitmask) | int(bits, 2)
        # convert bytearray into bytes, the format to write to a wav file
        modded_frames = bytes(frames)
        # write to a wav file on specified destination
        with wave.open(dest, 'wb') as newfile:
            newfile.setparams(song.getparams())
            newfile.writeframes(modded_frames)
            newfile.close()
        song.close()

    def decode_audio(self, source, dest, bitrange):
        # error handling
        if source[-4:] != '.wav':
            source += '.wav'
        if dest[-4:] != '.txt':
            dest += '.txt'
        if not os.path.exists(source):
            print('[!] Source file does not exist, only .wav files are accepted')
            return

        # Read frames from specified file
        song = wave.open(source, 'rb')
        frames = song.readframes(song.getnframes())
        frames = bytearray(frames)
        decoded_bin = ''
        decoded_string = ''
        for byte in frames:
            decoded_bin += self.to_bin(byte)[-bitrange:]
        decoded_bin = [decoded_bin[index: index + 8] for index in range(0, len(decoded_bin), 8)]
        print('decoded:', decoded_bin[0])
        for byte in decoded_bin:
            val = int(byte, 2)
            if 31 < val < 128:
                decoded_string += format(val, 'c')
        with open(dest, 'w') as newfile:
            newfile.write(decoded_string)
            newfile.close()
        return decoded_string



if __name__ == '__main__':
    audio = AudioCoder()
    source_file = './cover_assets/audio'
    embedded_file = './stego_assets/audio_embedded'
    decoded_text = './stego_assets/decoded_audio.txt'
    bitrange = 1
    # payload = str(input('Enter payload to be embedded: '))
    payload = 'PLEASE GIVE ME A+'
    audio.encode_audio(source_file, embedded_file, payload, bitrange)
    audio.decode_audio(embedded_file, decoded_text, bitrange)



