from flask import Flask, request
import requests
import assemblyai as aai
import google.generativeai as genai
import os
import json
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mr_optimizer_db.settings')
application = get_wsgi_application()

from optimizer.models import Voice_assist, MR
from django.utils import timezone
# from pydub import AudioSegment
import time

app = Flask(__name__)

# Telegram Bot Token
TOKEN = '7314700145:AAFW_LqFEygBPeo0iKP9DyWSM7g2MC8TJCw'

# Gemini API Key Configuration
genai.configure(api_key="AIzaSyBoz2JBZ0xm7xMttzt2SZoMiXV2PRu60g4")

# AssemblyAI API Key
ASSEMBLYAI_API_KEY = "71e624cdbb0a426b816abd874dc1cc8a"

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

def determine_input_type(text):
    """Determine the type of input based on the transcribed text"""
    text_lower = text.lower()
    if any(word in text_lower for word in ['plan', 'schedule', 'visit', 'meet']):
        return 'PLAN'
    elif any(word in text_lower for word in ['achieve', 'accomplished', 'completed', 'success']):
        return 'ACHIEVEMENT'
    elif any(word in text_lower for word in ['challenge', 'problem', 'issue', 'difficulty']):
        return 'CHALLENGE'
    elif any(word in text_lower for word in ['expense', 'spent', 'cost', 'payment']):
        return 'EXPENSE'
    return 'OTHER'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Incoming data:", data)

    try:
        chat_id = data['message']['chat']['id']
        user_id = data['message'].get('from', {}).get('id')

        # Try to find the MR based on Telegram user ID
        try:
            mr = MR.objects.get(telegram_id=user_id)
        except MR.DoesNotExist:
            send_message(chat_id, "❌ Error: Your Telegram account is not linked to any MR profile. Please contact admin.")
            return "ok"

        # If it's a text message
        if 'text' in data['message']:
            user_message = data['message']['text']
            response = model.generate_content(user_message)
            reply_text = response.text.strip()
            send_message(chat_id, reply_text)

        # If it's a voice message
        elif 'voice' in data['message']:
            file_id = data['message']['voice']['file_id']
            duration = data['message']['voice'].get('duration', 0)

            # Get file path from Telegram
            file_info = requests.get(f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}").json()
            if not file_info.get('ok'):
                raise Exception("Failed to get file info from Telegram")
            
            file_path = file_info['result']['file_path']

            # Download the voice file
            voice_file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
            voice_file_response = requests.get(voice_file_url)
            if voice_file_response.status_code != 200:
                raise Exception("Failed to download voice file")

            temp_file = f"voice_{int(time.time())}.ogg"
            with open(temp_file, "wb") as f:
                f.write(voice_file_response.content)

            try:
                # Transcribe voice
                aai.settings.api_key = ASSEMBLYAI_API_KEY
                transcriber = aai.Transcriber()
                transcript = transcriber.transcribe(temp_file)

                if not transcript.text:
                    raise Exception("Transcription failed or returned empty text")

                # Determine input type
                input_type = determine_input_type(transcript.text)

                # Save to Voice_assist model
                voice_record = Voice_assist.objects.create(
                    mr=mr,
                    voice_input=transcript.text,
                    processed_text=transcript.text,  # You might want to process this further
                    input_type=input_type,
                    created_at=timezone.now()
                )

                # Send confirmation with type
                send_message(chat_id, f"📝 Voice message processed:\nType: {input_type}\nText: {transcript.text}")

            except Exception as e:
                send_message(chat_id, f"❌ Error processing voice message: {str(e)}")
                raise e

            finally:
                # Clean up temp file
                if os.path.exists(temp_file):
                    os.remove(temp_file)

    except Exception as e:
        print("Error:", e)
        try:
            send_message(chat_id, "❌ An error occurred while processing your message")
        except:
            pass

    return "ok"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    r = requests.post(url, json=payload)
    print("Telegram response:", r.text)

if __name__ == '__main__':
    app.run(port=5000)
