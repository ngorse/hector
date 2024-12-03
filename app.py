import os
import json
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
MESSAGES = []
LLM_URL = os.environ.get('LLM_PROTOCOL', 'http') + "://" + \
        os.environ.get('LLM_HOST', 'localhost') + ":" +  \
        os.environ.get('LLM_PORT', '11434') + "/api/chat"
LLM_MODEL= os.environ.get('LLM_MODEL', 'llama3.2')
print(f'LLM_URL  : {LLM_URL}')
print(f'LLM_MODEL: {LLM_MODEL}')


def get_answer(prompt, stream=False):
    global MESSAGES
    if len(MESSAGES) >= 200:
        MESSAGES = MESSAGES[2:]
    MESSAGES.append({ "role": "user", "content": prompt })
    input = {
        "model": LLM_MODEL,
        "messages": MESSAGES,
        "stream": stream
    }

    print(f"\nDATE  : {datetime.now()}")
    print(f"INPUT : {MESSAGES[-1]}")
    try:
        output = requests.post(LLM_URL, json=input)
        response = json.loads(output.text)["message"]["content"]
        role = json.loads(output.text)["message"]["role"]
        MESSAGES.append({ "role": role, "content:": response})
    except json.JSONDecodeError as e:
        response = f"[SYSTEM ERROR]: Error decoding JSON: {e}"
    except KeyError as e:
        response = f"[SYSTEM ERROR]: Key error accessing response data: {e}"
    except requests.exceptions.RequestException as e:
        response = f"[SYSTEM ERROR]: An error occurred while making the POST request: {e}"
    except Exception as e:
        response = f"[SYSTEM ERROR]: An unexpected error occurred: {e}"

    print(f"OUTPUT: {MESSAGES[-1]}\n")
    return jsonify({"response": response.replace("\n", "<br>")})


@app.route("/")
def home():    
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def get_bot_response():
    userText = request.json.get('msg')
    return get_answer(userText)


if __name__ == "__main__":
    app.run(host=os.environ.get('FLASK_RUN_HOST', '127.0.0.1'),
            port=int(os.environ.get('FLASK_RUN_PORT', 5555)),
            debug=bool(os.environ.get('FLASK_DEBUG', True)))
