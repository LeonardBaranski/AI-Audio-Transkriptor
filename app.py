import whisper
import json, sys, os
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pydub
import ffmpeg
from scipy.io.wavfile import write
import wave


app = Flask(__name__)
CORS(app)

@app.route("/receive", methods=['POST'])
def form():
    files = request.files
    filetype = type(files.getlist("audio")[0])
    file = files.getlist("audio")[0]
    print(files, filetype)
    #npimg = np.fromstring(file.read(), np.float32)
    #print(npimg)
    file.save("test.wav")
    audio_file = file.read()
    #transcribe_audio(audio_file)
    #print(audio_file)
    #return "file"
    #a = pydub.AudioSegment.from_wav(file)
    #np_a = np.array(a.get_array_of_samples())
    #np_flattened = np_a.astype(np.float32, order='C') / 32768.0

    #audio_as_np_int16 = np.frombuffer(npimg, dtype=np.int16)
    #audio_as_np_float32 = audio_as_np_int16.astype(np.float32)

    # Normalise float32 array so that values are between -1.0 and +1.0                                                      
    #max_int16 = 2**15
    #audio_normalised = audio_as_np_float32 / max_int16
    
    #print(npimg)
    #rate = 47000
    #scaled = np.int16(np_flattened / np.max(np.abs(np_flattened)) * 32767)
    #write("create.wav", rate, scaled)
    #print(np_flattened)

    #load_audio(file.read())
    transcribe_audio()
    return "ok"
def load_audio(file:(bytes), sr: int = 16000):
    """
    Open an audio file and read as mono waveform, resampling as necessary

    Parameters
    ----------
    file: (str, bytes)
        The audio file to open or bytes of audio file

    sr: int
        The sample rate to resample the audio if necessary

    Returns
    -------
    A NumPy array containing the audio waveform, in float32 dtype.
    """

    if isinstance(file, bytes):
        inp = file
        file = 'pipe:'
    else:
        inp = None

    try:
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        out, _ = (
            ffmpeg.input(file, threads=0)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
            .run(cmd="ffmpeg", capture_stdout=True, capture_stderr=True, input=inp)
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    print(np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0)

    #transcribe_audio(np)
    return "file"

def transcribe_audio():
    model = whisper.load_model("base.en")

    result = model.transcribe("test.wav", fp16=False)

    print(result["text"])
    return result["text"]