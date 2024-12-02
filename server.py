import json
import requests
from datetime import datetime
from flask import Flask, render_template, request

URL = "http://localhost:11434/api/chat"
app = Flask(__name__)

def get_answer(prompt, model="openchat", stream=False):
    input = {
        "model": model,
        "stream": stream,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    print(f"\nDATE  : {datetime.now()}")
    print(f"INPUT : {prompt}")
    try:
        output = requests.post(URL, json=input)
        response = json.loads(output.text)["message"]["content"]
    except json.JSONDecodeError as e:
        response = f"[SYSTEM ERROR]: Error decoding JSON: {e}"
    except KeyError as e:
        response = f"[SYSTEM ERROR]: Key error accessing response data: {e}"
    except requests.exceptions.RequestException as e:
        response = f"[SYSTEM ERROR]: An error occurred while making the POST request: {e}"
    except Exception as e:
        response = f"[SYSTEM ERROR]: An unexpected error occurred: {e}"

    print(f"OUTPUT:{response}\n")
    return response.replace("\n", "<br>")

@app.route("/")
def home():    
    return render_template("index.html")

@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg')  
    return get_answer(userText)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555, debug=True)
