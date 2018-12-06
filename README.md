# Voice Mimicry

Flow

1. Navigate to voice_mimicry subdirectory.
2. Run Lyrebird.py
3. Type into the console what you want to hear in my voice_mimicry
4. Check the same directory and open the resulting .wav file.

No external dependencies are required for this. We use the Lyrebird API. I have
an account and provided a number of recordings of my voice to allow it to mimic.
I generated an access token for my account. Simply run Lyrebird.py and type in what
you want to hear in my voice. It will generate a wav file with the text in the same directory.
If you wanted to use a different voice, you'd have to create an account, provide
voice recordings, and then generate an access token for that account. So for now
we just stick to my voice.

# Audio Interpolation

## Dependencies

The dependencies are listed in the requirement.txt file. Navigate to the root
directory, create and activate a python environment and run "pip install -r requirements.txt".

## Project Layout

The project is organized as follows. Keep this layout.

* project root
  * voice_mimicry
    * **Lyrebird.py**
  * audio_synthesis
    * **record_audio.py**
    * **synthesize_audio.py**
    * **RecordAndInterpolate.py**
    * mixes
    * sounds
      * encodings
        * instrument_encodings
          * **drums.npy**
          * **cello.npy**
        * voice_encodings
      * recordings
        * instrument_recordings
          * **drums.wav**
          * **cello.wav**
        * voice_recordings
  * wavenet-ckpt

  This program allows you to record your voice, and then mix it with an instrument.

  Example Flow:

  1. Navigate to audio_synthesis subdirectory.
  2. Run RecordAndInterpolate.py
  3. When it says, "Recording Audio", say something like, "Hey Shimi, mix my voice with the (**drums** or **cello**)." As long as it has either "drums" or "cello", it will work.
  4. Let the program execute. Depending on your computing power, it could take 10 minutes plus.
  5. Check the mixes subdirectory for the resulting mix and listen to it.

  If I say, "Hey Shimi, mix the **drums** with my voice", it will
  create a new encoding for that particular voice recording, use the drumps.npy
  encoding in the encodings folder, and then interpolate the two encodings. The
  result will be .wav file stored in the mixes folder. The most recent mix will
  have the highest number attached to it. However, you must say the exact word
  that corresponds to the encoding in the encodings folder. If you say drum instead
  of drums, it will default to use the cello encoding as of now. For now, we only
  use drums and cello.
