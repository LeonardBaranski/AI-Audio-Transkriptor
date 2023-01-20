from flask import Flask, request, jsonify
from flask_cors import CORS
import paramiko
from scp import SCPClient


app = Flask(__name__)
CORS(app)

@app.route("/receive", methods=['POST'])
def form():
    files = request.files
    filetype = type(files.getlist("audio")[0])
    file = files.getlist("audio")[0]

    file.save("audio.wav")

    transcribe_audio()
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

    print(scp.put("audio.wav", remote_path="/home/ai-transkriptor/whisper"))

    return 'result["text"]'