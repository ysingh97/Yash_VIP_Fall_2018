# adapted from https://stackoverflow.com/questions/892199/detect-record-audio-in-python

import pyaudio
import wave
import os
from sys import byteorder
from array import array
from struct import pack
import speech_recognition as sr


class AudioRecorder():
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.RECORD_SECONDS = 10
        self.CURRENT_DIRECTORY = os.getcwd()
        files = os.listdir("./sounds/recordings/voice_recordings")
        self.WAVE_OUTPUT_FILENAME = os.getcwd() + "/sounds/recordings/voice_recordings/recording" + str(len(files)) + ".wav"
        self.pyAudio = pyaudio.PyAudio()
        self.instruments = ['drums', 'cello']


    def normalize(snd_data):
        "Average the volume out"
        MAXIMUM = 16384
        times = float(MAXIMUM)/max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i*times))
        return r

    def find_input_device(self):
        device_index = None
        for i in range(self.pyAudio.get_device_count()):
            devinfo = (self.pyAudio.get_device_info_by_index(i))
            print("Device %d: %s" % (i, devinfo["name"]))

            for keyword in ["mic", "input"]:
                if keyword in devinfo["name"].lower():
                    print("Found an input: device %d - %s" % (i, devinfo["name"]))
                    device_index = i
                    return device_index

        if device_index == None:
            print("No preferred input found; using default input device.")

        return device_index

    def convertToSpeech(self):
        recognizer = sr.Recognizer()
        audioFile = sr.AudioFile(self.WAVE_OUTPUT_FILENAME)
        print(self.WAVE_OUTPUT_FILENAME)
        with audioFile as source:
            audio = recognizer.record(source)
        speech = recognizer.recognize_google(audio)
        print(speech)
        return speech


    def record(self):
        device_index = self.find_input_device()
        stream = self.pyAudio.open(format = self.FORMAT, channels = self.CHANNELS, rate = self.RATE, input = True, output = True, frames_per_buffer = self.CHUNK, input_device_index = device_index)
        frames = array('h')
        print("Recording audio...")
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = array('h', stream.read(self.CHUNK))
            frames.extend(data)
        stream.stop_stream()
        stream.close()
        print("done recording")
        self.pyAudio.terminate()
        width = self.pyAudio.get_sample_size(self.FORMAT)
        self.write_to_file(self.WAVE_OUTPUT_FILENAME, width, frames)
        speech = self.convertToSpeech()
        words = speech.lower().split()
        instrument = ""
        instrumentInRecording = False

        for word in words:
            if word in self.instruments:
                instrument = word
        return self.WAVE_OUTPUT_FILENAME, instrument

    def write_to_file(self, path, width, frames):
        sample_width = width
        data = frames
        data = pack('<' + ('h'*len(data)), *data)
        wf = wave.open(path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(self.RATE)
        wf.writeframes(data)
        wf.close()


