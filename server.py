from flask import Flask, request, Response
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

        if "choices" in response_json:
            ai_response = response_json["choices"][0]["message"]["content"]
            
            # ✅ מחזירים טקסט נקי בלבד
            return Response(ai_response, mimetype="text/plain; charset=utf-8")
        
        else:
            return Response("לא התקבלה תשובה מהשרת.", mimetype="text/plain; charset=utf-8", status=500)
    
    except Exception as e:
        return Response(f"שגיאה: {str(e)}", mimetype="text/plain; charset=utf-8", status=500)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
