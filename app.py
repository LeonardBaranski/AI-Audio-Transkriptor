import whisper
import json, sys, os
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/receive", methods=['POST'])
def form():
    files = request.files
    filetype = type(files.getlist("audio")[0])
    file = files.getlist("audio")[0]
    print(file)

    return "file"

def transcribe_audio(wav):
    model = whisper.load_model("base.en")

    result = model.transcribe(wav, fp16=False)

    print(result["text"])
    return result["text"]