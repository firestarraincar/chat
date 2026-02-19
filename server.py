from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import os

app = Flask(__name__)
CORS(app)

messages = []
message_id = 0


@app.route('/')
def home():
    return "✅ Чат сервер работает на Render!"


@app.route('/api/messages', methods=['GET'])
def get_messages():
    return jsonify({
        'messages': messages,
        'count': len(messages)
    })

@app.route('/api/messages', methods=['POST'])
def post_message():
    global message_id, messages

    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Нет текста'}), 400

    message = {
        'id': message_id,
        'text': data['text'],
        'author': data.get('author', 'Аноним'),
        'timestamp': datetime.datetime.now().strftime('%H:%M:%S')
    }

    messages.append(message)
    message_id += 1

    return jsonify({'success': True, 'message': message})


@app.route('/api/messages/latest', methods=['GET'])
def get_latest():
    latest = messages[-50:] if len(messages) > 50 else messages
    return jsonify({'messages': latest})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port)


