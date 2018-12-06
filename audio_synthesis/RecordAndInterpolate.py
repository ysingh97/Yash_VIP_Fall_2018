from record_sound import *
from synthesize_audio import *
import sys


def record():
    recorder = AudioRecorder()
    voiceFile,  instrumentType = recorder.record()
    interpolate(voiceFile, instrumentType)

if __name__ == '__main__':
    print(sys.argv)
    record()



# recorder = AudioRecorder()
#
# voiceFile, instrumentType = recorder.record()
#
# interpolate(voiceFile, instrumentType)