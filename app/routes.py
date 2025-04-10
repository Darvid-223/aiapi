from flask import request, jsonify, render_template
from app import app
from app.agents import generate_response
import asyncio
from app.memory import save_message, get_full_log

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
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        save_message("user", user_input)

        reply = loop.run_until_complete(generate_response(user_input))

        save_message("bot", reply)

        # 🔽 Test: skriv ut hela loggen till terminalen
        print("🧠 FULL LOGG:")
        for entry in get_full_log():
            print(f"{entry['role']}: {entry['content']}")

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": "Serverfel", "details": str(e)}), 500