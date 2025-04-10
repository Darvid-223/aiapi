from app import app
import os
from dotenv import load_dotenv

load_dotenv()

debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
local_dev = os.getenv("LOCAL_DEV", "false").lower() == "true"

# Starta Flask-appen
if __name__ == "__main__":
    if local_dev:
        app.run(debug=debug_mode, host="0.0.0.0")
    else:
        app.run(debug=debug_mode)
