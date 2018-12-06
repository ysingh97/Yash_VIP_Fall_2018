from record_sound import *
import os
import numpy as np
import matplotlib.pyplot as plt
from magenta.models.nsynth import utils
from magenta.models.nsynth.wavenet import fastgen
import pickle
from IPython.display import Audio

voiceWeight = 1.0
defaultInstrumemt = "cello"

def fade(encoding, mode='in'):
    length = encoding.shape[1]
    fadein = (0.5 * (1.0 - np.cos(3.1415 * np.arange(length) /
                                  float(length)))).reshape(1, -1, 1)
    if mode == 'in':
        return fadein * encoding
    else:
        return (1.0 - fadein) * encoding

def crossfade(encoding1, encoding2):
    return fade(encoding1, 'out') + fade(encoding2, 'in')

def load_encoding(fname, sample_length=None, sr=16000, ckpt='../wavenet-ckpt/model.ckpt-200000'):
    audio = utils.load_audio(fname, sample_length=sample_length, sr=sr)
    encoding = fastgen.encode(audio, ckpt, sample_length)
    return audio, encoding

def checkAudio(filename):
    files = os.listdir('sounds/encodings/instrument_encodings')
    print(files)
    if(filename not in files):
        return False
    else:
        return True


def interpolate(recordedAudio, instrument):
    global voiceWeight, defaultInstrument

    sample_length = 80000

    instrumentType = defaultInstrumemt
    if(instrument != ""):
        instrumentType = instrument

    instrumentFile = "./sounds/recordings/instrument_recordings/" + instrumentType + ".wav"
    instrumentEncoding = "./sounds/encodings/instrument_encodings/" + instrumentType + ".npy"

    aud1, enc1 = load_encoding(recordedAudio, sample_length)
    #check if encoding already exists
    enc2 = None
    print("encoding path", instrumentEncoding)
    if(checkAudio(instrument + ".npy")):
        print("encoding exists")
        enc2 = np.load(instrumentEncoding)
    else:
        print("encoding does not exist")
        aud2, enc2 = load_encoding(instrumentFile, sample_length)
        np.save(instrumentEncoding, enc2)

    enc_mix = (1.5 * enc1 + enc2)/2.0
    outputPath = './mixes/mix' + str(len(os.listdir('./mixes'))) + '.wav'
    fastgen.synthesize(enc_mix, checkpoint_path='../wavenet-ckpt/model.ckpt-200000', save_paths=[outputPath])

# used for my own experimentation purposes, provides more detailed file names
def synthesizeEncodings(encoding1Name, encoding2Name, encoding1, encoding2, encoding1Weight, encoding2Weight):
    global voiceWeight, defaultInstrument

    sample_length = 80000
    voiceEncodingPath = "./sounds/encodings/voice_encodings/recording3_encoding.npy"
    instrumentEncodingPath = "./sounds/encodings/instrument_encodings/cello.npy"

    enc_mix = (encoding1Weight * encoding1 + encoding2Weight * encoding2) / 2.0
    outputFile = encoding1Name + "_" + str(encoding1Weight) + "_" + encoding2Name + "_" + str(encoding2Weight)
    outputPath = './mixes/weight_experiments/' + outputFile + '.wav'
    fastgen.synthesize(enc_mix, checkpoint_path='../wavenet-ckpt/model.ckpt-200000', save_paths=[outputPath])

def encodeAndDecode(recordingName, recordingPath):
    aud1, enc1 = load_encoding(recordingPath, 80000)
    encodeOutputPath = './sounds/encodings/voice_encodings/' + recordingName + '_encoding' + str(len(os.listdir('./sounds/encodings/voice_encodings')))
    decodeOutputPath = './mixes/single_voice_decoding/' + recordingName + '_decoding' + str(len(os.listdir('./mixes/single_voice_decoding'))) + '.wav'
    np.save(encodeOutputPath, enc1)
    fastgen.synthesize(enc1, checkpoint_path='../wavenet-ckpt/model.ckpt-200000', save_paths=[decodeOutputPath])

def testDecoding():
    encodeAndDecode("recording3", './sounds/recordings/voice_recordings/recording3.wav')
    encodeAndDecode("recording4", './sounds/recordings/voice_recordings/recording4.wav')

def experiment():
    voiceEncodingPath = './sounds/encodings/voice_encodings/recording3_encoding.npy'
    drumEncodingPath = './sounds/encodings/instrument_encodings/drums.npy'
    celloEncodingPath = './sounds/encodings/instrument_encodings/cello.npy'
    voiceEncoding = np.load(voiceEncodingPath)
    celloEncoding = np.load(celloEncodingPath)
    drumEncoding = np.load(drumEncodingPath)
    synthesizeEncodings("recording3", "cello", voiceEncoding, celloEncoding, 1.8, 1.0)
    synthesizeEncodings("recording3", "cello", voiceEncoding, celloEncoding, 1.9, 1.0)
    synthesizeEncodings("recording3", "cello", voiceEncoding, celloEncoding, 2.0, 1.0)
    synthesizeEncodings("recording3", "drums", voiceEncoding, drumEncoding, 1.8, 1.0)
    synthesizeEncodings("recording3", "drums", voiceEncoding, drumEncoding, 1.9, 1.0)
    synthesizeEncodings("recording3", "drums", voiceEncoding, drumEncoding, 2.0, 1.0)







# fname = "recording.wav"
# sr = 16000
# audio = utils.load_audio(fname, sample_length=40000, sr=sr)
# sample_length = audio.shape[0]
# print('{} samples, {} seconds'.format(sample_length, sample_length / float(sr)))




