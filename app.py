import requests
import uuid
from flask import Flask, request, render_template, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Session ke liye zaroori

# In-memory history store karne ke liye (optional)
translation_history = []

@app.route('/', methods=['GET'])
def index():
    # Agar history dikhana ho to pass kar do
    return render_template('index.html', myresult=translation_history)

@app.route('/', methods=['POST'])
def index_post():
    original_text = request.form['text']
    target_language = request.form['language']

    # Translator API credentials
    key = "8DfZONdICWMhbwlKQ1zei3FYA73eJhu91bh4SezHZh09CBxelNWRJQQJ99CAACYeBjFXJ3w3AAAbACOGbCWv"
    endpoint = "https://api.cognitive.microsofttranslator.com/"
    location = "eastus"

    path = '/translate?api-version=3.0'
    target_language_parameter = '&to=' + target_language
    constructed_url = endpoint + path + target_language_parameter

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': original_text}]
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    translator_response = translator_request.json()
    translated_text = translator_response[0]['translations'][0]['text']

    # History store karna (optional)
    translation_history.append({
        'original_text': original_text,
        'translated_text': translated_text,
        'target_language': target_language
    })

    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )

if __name__ == '__main__':
    app.run(debug=True)
