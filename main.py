from app import app
import os
from dotenv import load_dotenv

load_dotenv()

debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
local_dev = os.getenv("LOCAL_DEV", "false").lower() == "true"

# Starta Flask-appen
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=debug_mode, host="0.0.0.0", port=port)

