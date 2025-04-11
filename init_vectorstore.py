from openai import OpenAI
from dotenv import load_dotenv
from app.utils import read_json_file

# Ladda miljövariabler (OPENAI_API_KEY)
load_dotenv()

# Initiera klient
client = OpenAI()

# Läs och kombinera data
employees = read_json_file("db/employees.json")
brukare = read_json_file("db/brukare.json")

combined_data = f"## Anställda:\n{employees}\n\n## Brukare:\n{brukare}"

# Spara till temporär fil
with open("combined_data.txt", "w", encoding="utf-8") as f:
    f.write(combined_data)

# Skapa vector store
vector_store = client.vector_stores.create(name="Eklunda-data")

# Ladda upp fil
file_upload = client.vector_stores.files.upload_and_poll(
    vector_store_id=vector_store.id,
    file=open("combined_data.txt", "rb")
)

print("✅ Klar! Vector Store ID:", vector_store.id)
