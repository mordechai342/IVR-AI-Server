from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# קריאת מפתח ה-API מהסביבה
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route('/api/ivr', methods=['GET'])
def ivr_response():
    try:
        user_input = request.args.get('text', 'שלום')

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "system", "content": "אתה עוזר טלפוני חכם"},
                         {"role": "user", "content": user_input}]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
        response_json = response.json()

        # בדיקת שגיאות
        if "choices" in response_json:
            ai_response = response_json["choices"][0]["message"]["content"]
            return jsonify({"text": ai_response})
        else:
            return jsonify({"error": response_json}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
