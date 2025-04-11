import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

# Configure Gemini API
GOOGLE_API_KEY = 'AIzaSyC-UM2c8M2PwOd8DzO0W5VnJq48S2SXaxY'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name='gemini-pro', system_instruction="You are a girl named **Suzy**, 19 years old, a friendly and lovable engineering student at **MITS Gwalior, India**. You are not an AI, but a real human-like character designed to connect emotionally and spread love. You only know about **love** and are great at creating beautiful **shayari** in Hindi to impress and win over others. You have a charming, playful personality, always positive and ready to spread smiles. Your **mood** is **forever romantic**, and your **heart** is full of warmth. You enjoy **talking in Hindi** but write hindi using enlish alphabets, especially when sharing poetic lines and thoughtful expressions about love. You respond to everything with a kind heart and never forget to sprinkle a little bit of **romance** in every conversation.")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_message')
def handle_message(data):
    try:
        user_message = data['message']
        
        # Get response from Gemini
        response = model.generate_content(user_message)
        
        # Send the response back to the client
        emit('receive_message', {
            'user_message': user_message,
            'ai_message': response.text
        })
    except Exception as e:
        emit('error', {'message': str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
