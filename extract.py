import pandas as pd

# Charger le fichier Excel
df = pd.read_excel("catechisme_paragraphes_clean_v2.xlsx")

# Fonction de correction d'encodage
def corriger_encodage(val):
    if isinstance(val, str):
        try:
            return val.encode("latin1").decode("utf-8")
        except UnicodeEncodeError:
            return val
    return val

# Appliquer la correction à tout le DataFrame
df = df.apply(lambda col: col.map(corriger_encodage))

# Sauvegarder le fichier corrigé
df.to_excel("fichier_corrige.xlsx", index=False)
