import os
import json
import logging
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify

def set_logger():
    if bool(os.environ.get('FLASK_DEBUG', True)):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

def set_llm():
    global LLM_URL
    global LLM_MODEL
    
    LLM_URL = os.environ.get('LLM_PROTOCOL', 'http') + "://" + \
            os.environ.get('LLM_HOST', 'localhost') + ":" +  \
            os.environ.get('LLM_PORT', '11434') + "/api/chat"
    LLM_MODEL= os.environ.get('LLM_MODEL', 'llama3.2')
    logger.info(f'LLM_URL  : {LLM_URL}')
    logger.info(f'LLM_MODEL: {LLM_MODEL}')

logger = logging.getLogger(__name__)
set_logger()

MESSAGES = []
LLM_MODEL = ""
LLM_URL = ""
set_llm()

# --------------------------------------------------------------

app = Flask(__name__)

@app.route("/")
def home():    
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def get_bot_response():
    userText = request.json.get('msg')
    return get_answer(userText)

# --------------------------------------------------------------

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

    logger.info(f"\nDATE  : {datetime.now()}")
    logger.info(f"INPUT : {MESSAGES[-1]}")
    try:
        output = requests.post(LLM_URL, json=input)
        logger.info(f'IP: {request.remote_addr}')
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

    logger.info(f"OUTPUT: {MESSAGES[-1]}\n")
    return jsonify({"response": response.replace("\n", "<br>")})

# --------------------------------------------------------------

if __name__ == "__main__":
    app.run(host=os.environ.get('FLASK_RUN_HOST', '127.0.0.1'),
            port=int(os.environ.get('FLASK_RUN_PORT', 5555)),
            debug=bool(os.environ.get('FLASK_DEBUG', True)))
