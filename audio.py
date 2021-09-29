import os.path
import pathlib
import sys

import numpy as np
import wave
from pydub import AudioSegment
import filestream

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


    def convert_audio(self, source, dest):
        # (
        #     ffmpeg
        #     .input(source)
        #     .output(dest)
        #     .overwrite_output()
        #     .run()
        # )
        print('[*] Converting', source[-3:], 'to', dest[-3:], '...')
        if source[-4:] == '.mp3':
            AudioSegment.from_mp3(source).export(dest, format=dest[-3:])
            return
        if source[-4:] == '.wav':
            AudioSegment.from_mp3(source).export(dest, format=dest[-3:])
            # AudioSegment.from_wav(source).export(dest, format=dest[-3:])
        return

    def limit_check(self, payload, cover, bitrange):
        payload_length = len(payload)
        cover_length = len(cover)
        if(payload_length > (cover_length * bitrange)):
            return 1
        return 0


    def generate_wav(self, data, dest):
        print('[*] Writing new data to file...')
        file = open(dest, "wb")
        file.write(data)
        file.close


    def encode_audio(self, source, dest, payload, bitrange):
        # error checking, and checking if file exists
        print('[*] Cover image URI is:', source, 'using', bitrange, 'bits.')
        if source[-4:] != '.wav':
            # convert mp3 to wav
            if source[-4:] == '.mp3':
                # convert current mp3 source into wav, as this method expects source to be of .wav type
                source_mp3 = source
                source = source[:-4]
                source += '.wav'
                self.convert_audio(source_mp3, source)      # convert mp3 to wav
            else:
                print('[!] Only .wav and .mp3 files are supported.')
                return
        if dest[-4:] != '.wav':
            dest += '.wav'
        if not os.path.exists(source):
            print('[!] Source file does not exist, only .wav files are accepted for encoding')
            return
        # check if payload is a file or plaintext
        if os.path.exists(payload):
            bin_payload = filestream.get_stream(payload)
            # Append delimiter 5= to payload
            bin_payload += self.to_bin('5=')
        else:
            print('[*] Payload is not a file, encoding as plaintext')
            # Append delimiter 5= to payload
            payload += "5="
            # Convert payload to binary
            bin_payload = self.to_bin(payload)


        print('[*] Encoding...')
        song = wave.open(source, 'rb')
        print('Channels: ', song.getnchannels(), '\nSample width:', song.getsampwidth(), '\nFramerate: ',
              song.getframerate(), '\nFrames: ', song.getnframes())
        # print(song.getparams())
        # Get all frames in wav
        frames = song.readframes(song.getnframes())
        frames = list(frames)
        frames = bytearray(frames)
        print('length of frames:', len(frames))


        print('binary length of payload:', len(bin_payload))
        # apply payload padding
        # Split the payload into specified bitrange slices
        bin_payload = [bin_payload[index: index + bitrange] for index in range(0, len(bin_payload), bitrange)]

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
        print('[*] Successfully encoded and exported to:', dest)

    def decode_audio(self, source, dest, bitrange):
        print('[*] Attempting to decode:', source, 'using', bitrange, 'bits.')
        # error handling
        type = 'wav'
        prev_char = ''
        current_char = ''
        if source[-4:] != '.wav':
            # convert mp3 to wav
            if source[-4:] == '.mp3':
                # convert current mp3 source into wav, as this method expects source to be of .wav type
                source_mp3 = source
                source = source[:-4]
                source += '.wav'
                self.convert_audio(source_mp3, source)      # convert mp3 to wav
                type = 'mp3'

        if dest[-4:] != '.txt':
            dest += '.txt'
        if not os.path.exists(source):
            print('[!] Source file', source,'does not exist, only .wav and .mp3 files are accepted for decoding')
            return
        # Read frames from specified file
        print('[*] Decoding...')
        song = wave.open(source, 'rb')
        frames = song.readframes(song.getnframes())
        frames = bytearray(frames)
        decoded_bin = ''
        decoded_string = ''
        for byte in frames:
            decoded_bin += self.to_bin(byte)[-bitrange:]
        decoded_bin = [decoded_bin[index: index + 8] for index in range(0, len(decoded_bin), 8)]
        for byte in decoded_bin:
            val = int(byte, 2)
            if 31 < val < 128:
                current_char = format(val, 'c')
                if prev_char == '5' and current_char == '=':
                    decoded_string = decoded_string[:-1]
                    break
                prev_char = current_char
                decoded_string += current_char

        with open(dest, 'w') as newfile:
            newfile.write(decoded_string)
            newfile.close()
        print('[*] Successfully decoded and exported to', dest)
        return decoded_string



if __name__ == '__main__':
    audio = AudioCoder()
    source_file = './cover_assets/audio.wav'
    embedded_file = './stego_assets/audio_embedded.wav'
    decoded_text = './stego_assets/decoded_audio.txt'
    bitrange = 1
    payload = 'NOT SO SECRET'
    audio.encode_audio(source_file, embedded_file, payload, bitrange)
    audio.decode_audio(embedded_file, decoded_text, bitrange)

    # audio.get_stream(source_file)






