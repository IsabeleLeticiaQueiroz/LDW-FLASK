import sqlite3
import os
from typing import List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), 'gallery.sqlite3')


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(app=None):
    # create tables if they don't exist
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS families (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            species TEXT,
            image TEXT,
            members INTEGER
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            family TEXT,
            age INTEGER,
            occupation TEXT,
            characteristic TEXT,
            image TEXT
        )
    ''')
    # perform safe migrations: ensure required columns exist and remove legacy 'year' if present
    cur.execute("PRAGMA table_info(families)")
    cols = [r[1] for r in cur.fetchall()]
    # ensure image and members exist
    if 'image' not in cols:
        cur.execute('ALTER TABLE families ADD COLUMN image TEXT')
    if 'members' not in cols:
        cur.execute('ALTER TABLE families ADD COLUMN members INTEGER')
    # If a legacy 'year' column exists, recreate the table without it (SQLite doesn't support DROP COLUMN)
    if 'year' in cols:
        # create temporary table without 'year'
        cur.execute('''
            CREATE TABLE IF NOT EXISTS families_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                species TEXT,
                image TEXT,
                members INTEGER
            )
        ''')
        # copy data from old table (ignore year)
        cur.execute('INSERT OR IGNORE INTO families_new (id, name, species, image, members) SELECT id, name, species, image, members FROM families')
        # drop old table and rename
        cur.execute('DROP TABLE families')
        cur.execute('ALTER TABLE families_new RENAME TO families')

    cur.execute("PRAGMA table_info(characters)")
    cols_c = [r[1] for r in cur.fetchall()]
    if 'age' not in cols_c:
        cur.execute('ALTER TABLE characters ADD COLUMN age INTEGER')
    if 'occupation' not in cols_c:
        cur.execute('ALTER TABLE characters ADD COLUMN occupation TEXT')
    if 'characteristic' not in cols_c:
        cur.execute('ALTER TABLE characters ADD COLUMN characteristic TEXT')
    if 'image' not in cols_c:
        cur.execute('ALTER TABLE characters ADD COLUMN image TEXT')
    conn.commit()
    conn.close()


def get_families() -> List[Dict[str, Any]]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, name, species, members, image FROM families')
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_family(fid: int) -> Dict[str, Any] | None:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, name, species, members, image FROM families WHERE id = ?', (fid,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def update_family(fid: int, data: Dict[str, Any]) -> None:
    conn = _get_conn()
    cur = conn.cursor()
    # normalize numeric fields
    members = data.get('members')
    try:
        members = int(members) if members not in (None, '') else None
    except Exception:
        members = None

    cur.execute('''
        UPDATE families SET name = ?, species = ?, image = ?, members = ? WHERE id = ?
    ''', (data.get('name'), data.get('species'), data.get('image'), members, fid))
    conn.commit()
    conn.close()


def delete_family(fid: int) -> None:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM families WHERE id = ?', (fid,))
    conn.commit()
    conn.close()


def add_family(data: Dict[str, Any]) -> int:
    conn = _get_conn()
    cur = conn.cursor()
    # normalize numeric fields
    members = data.get('members')
    try:
        members = int(members) if members not in (None, '') else None
    except Exception:
        members = None
    cur.execute('INSERT INTO families (name, species, image, members) VALUES (?, ?, ?, ?)',
                (data.get('name'), data.get('species'), data.get('image'), members))
    conn.commit()
    fid = cur.lastrowid
    conn.close()
    return fid


def get_characters() -> List[Dict[str, Any]]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, name, family, age, occupation, characteristic, image FROM characters')
    rows = cur.fetchall()
    conn.close()
    out = []
    for r in rows:
        d = dict(r)
        # normalize age to int if possible
        try:
            d['age'] = int(d['age']) if d.get('age') not in (None, '') else None
        except Exception:
            # keep as-is if not convertible
            pass
        out.append(d)
    return out


def add_character(data: Dict[str, Any]) -> int:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO characters (name, family, age, occupation, characteristic, image)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data.get('name'), data.get('family'), data.get('age'), data.get('occupation'), data.get('characteristic'), data.get('image')))
    conn.commit()
    cid = cur.lastrowid
    conn.close()
    return cid


def get_character(cid: int) -> Dict[str, Any] | None:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, name, family, age, occupation, characteristic, image FROM characters WHERE id = ?', (cid,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    try:
        d['age'] = int(d['age']) if d.get('age') not in (None, '') else None
    except Exception:
        pass
    return d


def update_character(cid: int, data: Dict[str, Any]) -> None:
    conn = _get_conn()
    cur = conn.cursor()
    # normalize age
    age = data.get('age')
    try:
        age = int(age) if age not in (None, '') else None
    except Exception:
        age = None
    cur.execute('''
        UPDATE characters SET name = ?, family = ?, age = ?, occupation = ?, characteristic = ?, image = ? WHERE id = ?
    ''', (data.get('name'), data.get('family'), age, data.get('occupation'), data.get('characteristic'), data.get('image'), cid))
    conn.commit()
    conn.close()


def delete_character(cid: int) -> None:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM characters WHERE id = ?', (cid,))
    conn.commit()
    conn.close()

