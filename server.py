import json
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
URL = "http://localhost:11434/api/chat"
MESSAGES = []


def get_answer(prompt, model="llama3.2", stream=False):
    global MESSAGES
    if len(MESSAGES) == 50:
        MESSAGES = MESSAGES[2:]
    MESSAGES.append({ "role": "user", "content": prompt })
    input = {
        "model": model,
        "messages": MESSAGES,
        "stream": stream
    }

    print(f"\nDATE  : {datetime.now()}")
    print(f"INPUT : {MESSAGES[-1]}")
    try:
        output = requests.post(URL, json=input)
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
    app.run(host='0.0.0.0', port=5555, debug=True)
