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
    #print(files, filetype)
    #npimg = np.fromstring(file.read(), np.float32)
    #print(npimg)
    file.save("audio.wav")
    #audio_file = file.read()
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
    return "request"


def transcribe_audio():
    #model = whisper.load_model("base.en")

    #result = model.transcribe("test.wav", fp16=False)



    def createSSHClient(server, port, user, password):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server, port, user, password)
        return client

    ssh = createSSHClient("141.62.117.240", 22, "ai-transkriptor", "5ai-T6ra1ns!")
    scp = SCPClient(ssh.get_transport())

    print(scp.put("audio.wav", remote_path="/home/ai-transkriptor/whisper"))

    #print(result["text"])

    #with open("transcript.txt", "w") as text_file:
    #    text_file.write(result["text"])

    return 'result["text"]'