""" Dieses Skript läuft auf der VM und ist hier nur zur Veranschaulichung """

import whisper
import smtplib
import os 
import time
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def check_for_file():
    check = os.path.isfile("./audio.wav")
    return check

def check_json():
    jsonFile = open("./language.json", "r")
    language_json = json.load(jsonFile)
    jsonFile.close
    language = language_json["language"]
    email = language_json["email"]

    print(language, email)
    return language, email

def transcribe_file(language):
    if language != "base.en":
        language = "medium"
    model = whisper.load_model(language)

    audio_file = "./audio.wav"

    try:
        result = model.transcribe(audio_file, fp16=False)
        transcription = result["text"]
        transcription = transcription.replace(". ", ". \n")
        print(transcription)
    except:
        return
    return transcription


def delete_file(file_path):
    os.remove(file_path)
    return print(f"File: {file_path} removed")


webmail = "transkriptor-ai@web.de"
passwort = "5ai-T6ra1ns!"

def send_mail(transcribed_text, email):
    s = smtplib.SMTP(host="smtp.web.de", port=587)
    s.starttls()
    s.login(webmail, passwort)

    msg = MIMEMultipart()

    message = transcribed_text

    msg["From"] = webmail
    msg["To"] = email
    msg["Subject"] = "Your transcribed text"
    msg.attach(MIMEText(message,"plain"))

    s.send_message(msg)

    del msg

def create_text_file(text):
    text_file = open("./transcription.txt", "w")
    text_file.write(text)
    text_file.close()

if __name__ == "__main__":
    while True:
        if check_for_file() == True:
            print("New transcription request")
            json_content = check_json()
            language = json_content[0]
            email = json_content[1]
            text = transcribe_file(language)
            if text != None:
                create_text_file(text)
                delete_file("./audio.wav")
                try: 
                    send_mail(text, email)
                except:
                    pass
                time.sleep(2.0)
                delete_file("./transcription.txt")
            else:
                print("Error with transcription or mailserver")
        else:
            print("No such file")
            time.sleep(2.0)

