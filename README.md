**📂 Projektstruktur – Översikt av filer och mappar**

Här är en översikt av de viktigaste delarna i projektet:

- `app/` – Själva applikationsmappen:
  - `__init__.py` – Initierar Flask-appen.
  - `agents.py` – Skapar och kör agenten, samt laddar datan från JSON.
  - `routes.py` – Flask-routes för startsidan och API-anrop (`/`, `/chat`).
  - `utils.py` – Hjälpfunktioner, t.ex. för att läsa filer och rensa svar.
  - `templates/index.html` – HTML-sida som innehåller chattens gränssnitt.
  - `static/style.css` – Styling för chattens utseende.
  - `static/script.js` – JavaScript som hanterar chattlogik och anrop till API:t.

- `db/` – Mapp med datafiler:
  - `employees.json` – Lista med fiktiva anställda.
  - `brukare.json` – Lista med fiktiva brukare.

- `main.py` – Startar Flask-servern.
- `requirements.txt` – Alla Python-paket som projektet använder.
- `Procfile` – Säger åt Render hur projektet ska startas.
- `.env` – Innehåller API-nycklar (används lokalt, inte i Git).
- `.gitignore` – Anger vilka filer och mappar som ska ignoreras i Git.

