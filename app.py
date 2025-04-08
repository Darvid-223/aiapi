import os
import re
import uuid
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from agents import Agent, Runner
import asyncio
import json

# Miljövariabler
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Flask-app
app = Flask(__name__)
CORS(app)

# Agent-definition
chat_agent = Agent(
    name="Navigator",
    instructions="""
    Du är en assistent för Eklunda kommun. 
    Du kan svara på frågor om organisationen, anställda eller brukare. 
    Du baserar dina svar på datan du får presenterad i prompten. 
    Du är artig och professionell, och svarar som om du vore en anställd.
    """,
    model="gpt-4-turbo",
)

# Hjälp: läs JSON och returnera en textsnutt

def read_json_file(filepath, max_items=None):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return json.dumps(data if max_items is None else data[:max_items], indent=2, ensure_ascii=False)
    except Exception as e:
        return f"⚠️ Kunde inte läsa filen {filepath}: {e}"


def clean_response(text: str) -> str:
    return re.sub(r"【.*?†.*?】", "", text).strip()


# Async körning av agent
async def async_generate_response(user_input):
    employees_data = read_json_file("db/employees.json")
    brukare_data = read_json_file("db/brukare.json")

    system_context = f"Information om anställda: {employees_data}. Information om brukare: {brukare_data}"

    messages = [
        {"role": "system", "content": system_context},
        {"role": "user", "content": user_input}
    ]

    result = await Runner.run(chat_agent, input=messages)
    return clean_response(result.final_output)


# API endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "Tomt meddelande"}), 400

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        reply = loop.run_until_complete(async_generate_response(user_input))
        return jsonify({"reply": reply})
    except Exception as e:
        print("❌ Fel:", e)
        return jsonify({"error": "Serverfel", "details": str(e)}), 500


@app.route("/")
def index():
    return render_template("index.html")


debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"

if __name__ == "__main__":
    app.run(debug=debug_mode)