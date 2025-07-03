# from flask import Flask, request
# import requests
# import assemblyai as aai
# import google.generativeai as genai
# import os
# # from pydub import AudioSegment
# import time

# app = Flask(__name__)

# # Telegram Bot Token
# TOKEN = '7314700145:AAFW_LqFEygBPeo0iKP9DyWSM7g2MC8TJCw'

# # Gemini API Key Configuration
# genai.configure(api_key="AIzaSyBoz2JBZ0xm7xMttzt2SZoMiXV2PRu60g4")

# # AssemblyAI API Key
# ASSEMBLYAI_API_KEY = "71e624cdbb0a426b816abd874dc1cc8a"

# # Initialize Gemini model
# model = genai.GenerativeModel('gemini-1.5-flash')

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     data = request.get_json()
#     print("Incoming data:", data)

#     try:
#         chat_id = data['message']['chat']['id']

#         # If it's a text message
#         if 'text' in data['message']:
#             user_message = data['message']['text']
#             response = model.generate_content(user_message)
#             reply_text = response.text.strip()
#             send_message(chat_id, reply_text)

#         # If it's a voice message
#         elif 'voice' in data['message']:
#             file_id = data['message']['voice']['file_id']

#             # Get file path from Telegram
#             file_info = requests.get(f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}").json()
#             file_path = file_info['result']['file_path']

#             # Download the voice file
#             voice_file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
#             voice_file_response = requests.get(voice_file_url)
#             with open("voice.ogg", "wb") as f:
#                 f.write(voice_file_response.content)

#             aai.settings.api_key = ASSEMBLYAI_API_KEY

#             transcriber = aai.Transcriber()
#             transcript = transcriber.transcribe("voice.ogg")

#             print(transcript.text)

#             # Send transcription text back
#             send_message(chat_id, f"📝 You said: {transcript.text}")
            
#             # Clean up files
#             os.remove("voice.ogg")
#             # os.remove("voice.wav")

#     except Exception as e:
#         print("Error:", e)

#     return "ok"



# def send_message(chat_id, text):
#     url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
#     payload = {"chat_id": chat_id, "text": text}
#     r = requests.post(url, json=payload)
#     print("Telegram response:", r.text)

# if __name__ == '__main__':
#     app.run(port=8000)


##django

# telegrambot/views.py
import os
import requests
import assemblyai as aai
import google.generativeai as genai
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Telegram Bot Token
TOKEN = '7314700145:AAFW_LqFEygBPeo0iKP9DyWSM7g2MC8TJCw'

# Gemini API Key
genai.configure(api_key="AIzaSyBoz2JBZ0xm7xMttzt2SZoMiXV2PRu60g4")
model = genai.GenerativeModel('gemini-1.5-flash')

# AssemblyAI Key
aai.settings.api_key = "71e624cdbb0a426b816abd874dc1cc8a"
transcriber = aai.Transcriber()

@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Incoming Data:", data)

            message = data.get('message', {})
            chat_id = message['chat']['id']

            if 'text' in message:
                user_message = message['text']
                response = model.generate_content(user_message)
                reply_text = response.text.strip()
                send_message(chat_id, reply_text)

            elif 'voice' in message:
                file_id = message['voice']['file_id']

                file_info = requests.get(f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}").json()
                file_path = file_info['result']['file_path']

                voice_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
                voice_data = requests.get(voice_url).content

                with open("voice.ogg", "wb") as f:
                    f.write(voice_data)

                transcript = transcriber.transcribe("voice.ogg")
                send_message(chat_id, f"📝 You said: {transcript.text}")
                os.remove("voice.ogg")

        except Exception as e:
            print("Error:", e)

    return JsonResponse({"status": "ok"})

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    r = requests.post(url, json=payload)
    print("Telegram Response:", r.text)



