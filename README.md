# Bot Telegram « Catéchisme » — Clé en main (gabarit)

> ⚠️ Ce dépôt est un **gabarit technique**. Il n'inclut PAS le texte complet du CCC pour des raisons de droits d'auteur. Ajoutez vos propres données (sources autorisées, éditions libres de droits, ou usage interne autorisé).

## Fonctionnalités

- `/para 123` : affiche le paragraphe n°123
- `/range 100 110` : affiche une plage (max 15)
- `/search miséricorde` : recherche plein texte (FTS5)
- `/random` : paragraphe aléatoire
- Requêtes **inline** : tapez `@NomDuBot` puis un mot-clé dans n'importe quel chat

## Démarrage rapide

1. **Créer un bot** : via Telegram @BotFather → obtenez un *token*.
2. **Cloner/copier** ce dossier sur votre machine/serveur.
3. **Installer** Python 3.10+ puis :
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   # Éditez .env et renseignez TELEGRAM_BOT_TOKEN
   ```
4. **Préparer vos données** :
   - Placez un CSV au format : `id,text,topics`
   - Exemple fourni : `data/sample_ccc.csv` (texte factice).
   - Construisez la base :
     ```bash
     python scripts/build_db.py data/sample_ccc.csv data/ccc.db
     ```
5. **Lancer le bot** :
   ```bash
   python bot.py
   ```

## Format des données

- `id` : numéro de paragraphe (entier)
- `text` : contenu du paragraphe en texte brut (UTF-8)
- `topics` : mots-clés séparés par `;` (optionnel)

> Astuce : vous pouvez aussi créer des colonnes supplémentaires dans un CSV à part, puis fusionner en amont.

## Déploiement (Docker, optionnel)

```dockerfile
# Dockerfile minimal
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

Build & run:
```bash
docker build -t ccc-bot .
docker run --rm -it --env-file .env -v $(pwd)/data:/app/data ccc-bot
```

## Avertissements juridiques

- Le **Catéchisme de l’Église catholique (1992)** est protégé par des droits de la Libreria Editrice Vaticana selon les juridictions et traductions.
- Vérifiez les droits d'usage de l'édition/translation que vous employez (ex: autorisation du détenteur, domaine public, licence compatible, usage interne pastoral, etc.).
- Évitez de republier massivement du texte sous droits sans autorisation. Le gabarit accepte tout contenu **que vous fournissez**.

## Personnalisation facile

- Réponse trop longue ? Le bot segmente automatiquement pour respecter la limite Telegram.
- Limiter les plages : modifiez `get_range(cap=15)` dans `bot.py`.
- Recherche : la FTS5 SQLite permet des requêtes comme `miséricorde AND grâce` ou des préfixes `grac*`.
- Ajoutez des commandes (ex: `/toc` sommaire) avec de nouveaux `CommandHandler`.

Bon déploiement !
