# app/utils.py

import re

# Tar bort referenser till källor i svaret
# Exempel: "Enligt [1†källa] är..."
def clean_response(text: str) -> str:
    return re.sub(r"【.*?†.*?】", "", text).strip()
