from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# קריאת מפתח ה-API מהסביבה
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/api/ivr', methods=['GET'])
def ivr_response():
    user_input = request.args.get('text', 'שלום')

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "אתה עוזר טלפוני חכם"},
                  {"role": "user", "content": user_input}]
    )
    ai_response = response["choices"][0]["message"]["content"]

    return jsonify({"text": ai_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
@app.route('/api/ivr', methods=['GET'])
