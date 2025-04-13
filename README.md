## 📂 Projektstruktur – Översikt av filer och mappar

Här är en översikt av de viktigaste delarna i projektet:

### `app/` – Själva applikationsmappen:
- `__init__.py` – Initierar Flask-appen.
- `agents.py` – Skapar och kör agenten, använder OpenAI Agent SDK, FileSearchTool och vector store.
- `routes.py` – Flask-routes för startsidan och API-anrop (`/`, `/chat`).
- `utils.py` – Hjälpfunktioner, t.ex. för att läsa JSON-filer och rensa AI-svar.
- `memory.py` – Håller konversationsminne under pågående session.
- `templates/index.html` – HTML-sida som innehåller chattens gränssnitt.
- `static/style.css` – Styling för chattens utseende.
- `static/script.js` – JavaScript som hanterar UI och API-kommunikation.

### `db/` – Mapp med datafiler (används vid initiering av vector store):
- `employees.json` – Lista med fiktiva anställda.
- `brukare.json` – Lista med fiktiva brukare.

### Rotkatalog:
- `main.py` – Startar Flask-servern.
- `init_vectorstore.py` – Skript för att skapa och ladda upp innehåll till vector store (OpenAI Retrieval API).
- `requirements.txt` – Alla Python-paket som projektet använder.
- `.env` – Miljövariabler (API-nycklar etc., ingår inte i Git).
- `.gitignore` – Anger vilka filer och mappar som ska ignoreras i Git.
- `Dockerfile` – Definierar hur projektet byggs och körs i en container (används t.ex. av Render).
- `.dockerignore` – Anger vilka filer som ska uteslutas vid Docker-bygge (liknar `.gitignore`).


