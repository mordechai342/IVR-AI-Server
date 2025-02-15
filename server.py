from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Flask עובד!"})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # שימוש בפורט של Render
    app.run(host='0.0.0.0', port=port)

