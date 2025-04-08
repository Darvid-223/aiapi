import json
import re

# Funktion för att läsa en JSON-fil och returnera dess innehåll som en sträng
# med ett begränsat antal objekt (om max_items anges)
# Om max_items inte anges returneras hela filen
def read_json_file(filepath, max_items=None):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return json.dumps(data if max_items is None else data[:max_items], indent=2, ensure_ascii=False)
    except Exception as e:
        return f"⚠️ Kunde inte läsa filen {filepath}: {e}"

# Tar bort referenser till källor i svaret
# Exempel: "Enligt [1†källa] är..."
def clean_response(text: str) -> str:
    return re.sub(r"【.*?†.*?】", "", text).strip()
