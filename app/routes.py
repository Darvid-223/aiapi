from flask import request, jsonify, render_template
from app import app
from app.agents import generate_response
import asyncio

# Flask-rutter för att hantera HTTP-förfrågningar
# och svara med JSON-data eller HTML-sidor.
@app.route("/")
def index():
    return render_template("index.html")

# Flask-rutter för att hantera chat-meddelanden
# och svara med JSON-data.
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "Tomt meddelande"}), 400

    try:
        # Starta ny event loop för async funktion
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        reply = loop.run_until_complete(generate_response(user_input))
        return jsonify({"reply": reply})

    except Exception as e:
        print("❌ Fel:", e)
        return jsonify({"error": "Serverfel", "details": str(e)}), 500
