import os
import json
import logging
import requests
from datetime import timedelta
from flask import Flask, render_template, request, jsonify, session, redirect

CONTEXT_LENGTH=int(os.environ.get('CONTEXT_LENGTH', '500'))

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
    session['llm_url'] = os.environ.get('LLM_PROTOCOL', 'http') + "://" + \
            os.environ.get('LLM_HOST', 'localhost') + ":" +  \
            os.environ.get('LLM_PORT', '11434')
    session['llm_url_chat'] = session['llm_url'] + "/api/chat"
    session['llm_url_pull'] = session['llm_url'] + "/api/pull"
    session['llm_model'] = os.environ.get('LLM_MODEL', 'llama3.2')

    logger.info(f"LLM_URL  : {session['llm_url']}")
    data = { "model": session['llm_model'] }
    response = requests.post(session['llm_url_pull'], json=data)
    if response.ok:
        logger.info(f"LLM_MODEL: {session['llm_model']}")
    else:
        logger.info(f"LLM_MODEL: Pull failed ({response.status_code}): {response.text}")

logger = logging.getLogger(__name__)
set_logger()

# --------------------------------------------------------------

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.permanent_session_lifetime = timedelta(days=30)

@app.route("/")
def home():
    set_llm()
    if 'context' not in session:
        session['context'] = []
    return render_template("index.html")

@app.route("/reset")
def reset():
    session['context'] = []
    logger.info(f"IP    : {request.remote_addr}")
    logger.info(f"ACTION: CONTEXT_RESET")
    return redirect("/", code=302)

@app.route("/chat", methods=["POST"])
def get_bot_response():
    message = request.json.get('msg')
    return get_answer(message=message)

# --------------------------------------------------------------

def append_to_context(role, content):
    if len(session['context']) >= CONTEXT_LENGTH:
        context = session['context']
        context = context[2:]
        session['context'] = context

    context = session['context']
    context.append({ "role": role, "content": content })
    session['context'] = context

def get_answer(message, stream=False):
    append_to_context(role="user", content=message)
    input = {
        "model": session['llm_model'] ,
        "messages": session['context'],
        "stream": stream
    }

    try:
        output = requests.post(session['llm_url_chat'], json=input)
        response = json.loads(output.text)["message"]["content"]
        role = json.loads(output.text)["message"]["role"]
        append_to_context(role=role, content=response)
    except json.JSONDecodeError as e:
        response = f"[SYSTEM ERROR]: Error decoding JSON: {e}"
    except KeyError as e:
        response = f"[SYSTEM ERROR]: Key error accessing response data: {e}"
    except requests.exceptions.RequestException as e:
        response = f"[SYSTEM ERROR]: An error occurred while making the POST request: {e}"
    except Exception as e:
        response = f"[SYSTEM ERROR]: An unexpected error occurred: {e}"

    logger.info(f"IP    : {request.remote_addr}")
    logger.info(f"INPUT : {message}")
    logger.info(f"OUTPUT: {response}")

    return jsonify({"response": response.replace("\n", "<br>")})

# --------------------------------------------------------------

if __name__ == "__main__":
    app.run(host=os.environ.get('FLASK_RUN_HOST', '127.0.0.1'),
            port=int(os.environ.get('FLASK_RUN_PORT', 5555)),
            debug=bool(os.environ.get('FLASK_DEBUG', True)))
