import sqlite3
import fitz  # PyMuPDF
import re

# Connexion / création de la base
conn = sqlite3.connect('ccc.db')
c = conn.cursor()

# Création de la table si elle n'existe pas
c.execute('''
CREATE TABLE IF NOT EXISTS ccc (
    para INTEGER PRIMARY KEY,
    text TEXT
)
''')
conn.commit()

# Lecture du PDF
pdf = fitz.open("cec.pdf")
text = ""
for page in pdf:
    text += page.get_text()

# Regex pour trouver tous les paragraphes
pattern = re.compile(r"(\d+)\s+([^\d]+?)(?=\n\d+\s+|$)", re.DOTALL)
matches = pattern.findall(text)

print(f"➡️ {len(matches)} paragraphes trouvés")

# Insertion dans la base
for para, para_text in matches:
    try:
        c.execute("INSERT OR IGNORE INTO ccc (para, text) VALUES (?, ?)", (int(para), para_text.strip()))
    except Exception as e:
        print(f"Erreur sur le paragraphe {para}: {e}")

conn.commit()
conn.close()
print("✅ Import terminé")
