from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# קריאת מפתח ה-API מהסביבה
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/api/ivr', methods=['GET'])
def ivr_response():
    try:
        user_input = request.args.get('text', 'שלום')

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "אתה עוזר טלפוני חכם"},
                      {"role": "user", "content": user_input}]
        )

        # ✅ שימוש בפורמט החדש של OpenAI
        ai_response = response["choices"][0]["message"]["content"]

        return jsonify({"text": ai_response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
