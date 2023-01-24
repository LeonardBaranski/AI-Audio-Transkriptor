from flask import Flask, request, jsonify
from flask_cors import CORS
import paramiko
from scp import SCPClient
import json
import time


app = Flask(__name__)
CORS(app)

@app.route("/language", methods=["POST"])
def set_language():
    response = request.data
    print(response)

    if response != b"English":
        lang = {"language": "Not English"}
    else:
        lang = {"language": "base.en"}

    json_object = json.dumps(lang)
    with open("language.json", "w") as json_file:
        json_file.write(json_object)

    time.sleep(0.1)
    transcribe_audio()

    return "lang"

@app.route("/receive", methods=['POST'])
def form():
    files = request.files
    filetype = type(files.getlist("audio")[0])
    file = files.getlist("audio")[0]

    file.save("audio.wav")

    return "request"


def transcribe_audio():

    def createSSHClient(server, port, user, password):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server, port, user, password)
        return client

    ssh = createSSHClient("141.62.117.240", 22, "ai-transkriptor", "5ai-T6ra1ns!")
    scp = SCPClient(ssh.get_transport())

    print(scp.put("language.json", remote_path="/home/ai-transkriptor/whisper"))
    print(scp.put("audio.wav", remote_path="/home/ai-transkriptor/whisper"))
    

    return 'result["text"]'