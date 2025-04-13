from app import app
import os
from dotenv import load_dotenv

load_dotenv()

debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
local_dev = os.getenv("LOCAL_DEV", "false").lower() == "true"

# 🔁 Använd Render-port om den finns, annars standardport 8080 lokalt
port = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    app.run(debug=debug_mode, host="0.0.0.0", port=port)

