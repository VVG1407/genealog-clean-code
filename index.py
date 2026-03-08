import requests
import os
from flask import Flask, request

app = Flask(__name__)

TOKEN = "8646119174:AAH6YtktbUpHRy52qHnzx_TcRYMpUhRvnQE"
DIFY_API_KEY = "app-dP3PB2kM1fnSYrvl2IlTJ2Yv"

session_storage = {}

@app.route('/api', methods=['POST'])
def webhook():
    update = request.get_json()
    if not update or 'message' not in update:
        return "OK", 200
    
    chat_id = update['message']['chat']['id']
    text = update['message'].get('text')
    
    if text:
        last_conv_id = session_storage.get(chat_id, "")
        
        try:
            response = requests.post(
                "https://api.dify.ai/v1/chat-messages",
                headers={"Authorization": f"Bearer {DIFY_API_KEY}"},
                json={
                    "inputs": {},
                    "query": text,
                    "response_mode": "blocking",
                    "user": str(chat_id),
                    "conversation_id": last_conv_id
                },
                timeout=25
            )
            
            result = response.json()
            
            new_conv_id = result.get('conversation_id')
            if new_conv_id:
                session_storage[chat_id] = new_conv_id
            
            answer = result.get('answer', 'Мира задумалась...')
            
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": answer}
            )
            
        except Exception as e:
            print(f"Ошибка: {e}")
            
    return "OK", 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return "Mira Status: Working", 200
