import csv, sqlite3, sys, pathlib

def main(csv_path: str, out_db: str):
    p = pathlib.Path(csv_path)
    if not p.exists():
        print(f"CSV introuvable: {p}")
        sys.exit(1)
    conn = sqlite3.connect(out_db)
    conn.executescript("""    PRAGMA journal_mode=WAL;
    PRAGMA synchronous=NORMAL;
    CREATE TABLE IF NOT EXISTS ccc (
        id INTEGER PRIMARY KEY,
        text TEXT NOT NULL,
        topics TEXT
    );
    CREATE VIRTUAL TABLE IF NOT EXISTS ccc_fts USING fts5(
        text,
        topics,
        content='ccc',
        content_rowid='id',
        tokenize='unicode61'
    );
    """ )
    conn.execute("DELETE FROM ccc;")
    conn.execute("DELETE FROM ccc_fts;")

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [(int(r['id']), r['text'], r.get('topics', '')) for r in reader]
    conn.executemany("INSERT INTO ccc(id,text,topics) VALUES (?,?,?)", rows)
    # populate FTS
    conn.execute("INSERT INTO ccc_fts(rowid, text, topics) SELECT id, text, topics FROM ccc;")
    conn.commit()
    print(f"Base construite: {out_db} (paragraphes: {len(rows)})")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python scripts/build_db.py data/ccc.csv data/ccc.db")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
