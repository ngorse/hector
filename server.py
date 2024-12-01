import json
import requests
from flask import Flask, render_template, request

URL = "http://localhost:11434/api/generate"
app = Flask(__name__)

def get_answer(prompt, model="openchat", stream=False):
    input = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }

    output = requests.post(URL, json=input)
    response = json.loads(output.text)["response"]
    print(response)
    return response.replace("\n", "<br>")

@app.route("/")
def home():    
    return render_template("index.html")

@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg')  
    return get_answer(userText)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
