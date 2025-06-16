from pathlib import Path
import sqlite3
import csv

def export_sqlite_to_csv(db_path: Path, table: str, csv_path: Path):
    conn = sqlite3.connect(f'{db_path}.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    cols = [c[0] for c in cursor.description]
    with open(csv_path+'.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        writer.writerows(cursor.fetchall())
    conn.close()