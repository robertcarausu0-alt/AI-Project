import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE, 'frontend', 'templates'),
    static_folder=os.path.join(BASE, 'frontend', 'static')
)

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434/api/chat')
MODEL      = os.getenv('OLLAMA_MODEL', 'llama3.2')

chat_history = []


def ask_ai(user_input):
    global chat_history
    chat_history.append({'role': 'user', 'content': user_input})

    try:
        response = requests.post(OLLAMA_URL, json={
            'model': MODEL,
            'messages': chat_history,
            'stream': False
        }, timeout=60)

        data  = response.json()
        reply = data['message']['content']
        chat_history.append({'role': 'assistant', 'content': reply})
        return reply

    except requests.exceptions.ConnectionError:
        chat_history.pop()
        return 'ERROR: Cannot connect to Ollama. Make sure it is running.'
    except KeyError as e:
        chat_history.pop()
        return f'ERROR: Unexpected Ollama response: {e}'
    except Exception as e:
        chat_history.pop()
        return f'ERROR: {e}'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/main_menu')
def main_menu():
    return render_template('main_menu.html')

@app.route('/main_selection')
def main_selection():
    return render_template('main_selection.html')

@app.route('/AI_unique')
def ai_unique():
    return render_template('AI_unique.html')

@app.route('/AI_useful')
def ai_useful():
    return render_template('AI_useful.html')

@app.route('/pros_cons')
def pros_cons():
    return render_template('pros_cons.html')

@app.route('/Where_AI_used')
def where_ai_used():
    return render_template('Where_AI_used.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data       = request.get_json(force=True)
        user_input = data['message']
        reply      = ask_ai(user_input)
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'reply': f'Error: {e}'})


if __name__ == '__main__':
    app.run(debug=True)
