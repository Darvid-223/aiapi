from flask import request, jsonify, render_template
from app import app
from app.generate_response import generate_response
from app.memory import reset_log, save_message, get_full_log
import asyncio

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reset_memory", methods=["POST"])
def reset_memory():
    data = request.get_json()
    user_type = data.get("user_type", "").lower()

    if user_type not in ["ledning", "verksamhet"]:
        return jsonify({"error": "Ogiltig användartyp"}), 400

    reset_log(user_type)
    return jsonify({"message": f"Minne för {user_type} rensat."})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    user_type = data.get("user_type", "verksamhet")  # standard till verksamhet

    if not user_input:
        return jsonify({"error": "Tomt meddelande"}), 400

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        save_message(user_type, "user", user_input)

        reply = loop.run_until_complete(generate_response(user_input, user_type))

        save_message(user_type, "assistant", reply)

        # 🔽 Test: skriv ut hela loggen till terminalen
        print(f"🧠 FULL LOGG ({user_type.upper()}):")
        for entry in get_full_log(user_type):
            print(f"{entry['role']}: {entry['content']}")

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": "Serverfel", "details": str(e)}), 500
