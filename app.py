import os
import re
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

# Ladda miljövariabler
load_dotenv()

API_KEY = os.environ.get("OPENAI_API_KEY")
ASSISTANT_ID = os.environ.get("ASSISTANT_ID")

client = OpenAI(api_key=API_KEY)

# Flask-app
app = Flask(__name__)
CORS(app)  # Tillåt anrop från frontend (t.ex. från Squarespace)

# Hämta/återställ tråd
_thread = None
def get_thread():
    global _thread
    if _thread is None:
        _thread = client.beta.threads.create()
        print(f"Created new thread: {_thread.id}")
    return _thread

def reset_thread():
    global _thread
    _thread = None
    print("Thread reset.")

def clean_response(text: str) -> str:
    # Tar bort alla citationer i formatet:  
    return re.sub(r"【.*?†.*?】", "", text).strip()

# Hämta versionsnummer
def get_git_commit_hash():
    try:
        with open("version.txt", "r") as f:
            return f.read().strip()
    except Exception:
        return "okänd"

# Generera svar
def generate_response(user_input: str) -> str:
    thread = get_thread()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input,
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
    )
    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    try:
        raw_text = messages[0].content[0].text.value
        return clean_response(raw_text)
    except Exception as e:
        return "Kunde inte tolka svaret."

# Route för frontend att anropa
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    print("🟡 Fick POST-anrop:", data)  # <-- Lägg till denna rad

    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "Tomt meddelande"}), 400

    try:
        reply = generate_response(user_message)
        print("🟢 Svar från OpenAI:", reply)  # <-- och denna
        return jsonify({"reply": reply})
    except Exception as e:
        print("❌ Fel i generate_response:", e)
        return jsonify({"error": "Serverfel", "details": str(e)}), 500

@app.route("/")
def index():
    version = get_git_commit_hash()
    return render_template("index.html", version=version)

if __name__ == "__main__":
    app.run(debug=True)
