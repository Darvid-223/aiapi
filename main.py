from app import app
import os
from dotenv import load_dotenv

load_dotenv()

debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"

if __name__ == "__main__":
    app.run(debug=debug_mode)
