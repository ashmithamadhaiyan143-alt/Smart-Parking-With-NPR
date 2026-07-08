import sqlite3

conn = sqlite3.connect("data/parking.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS parking(
id INTEGER PRIMARY KEY AUTOINCREMENT,
vehicle TEXT,
slot INTEGER,
entry TEXT,
exit TEXT,
status TEXT
)
""")

conn.commit()
conn.close()

print("✅ Database Created Successfully")