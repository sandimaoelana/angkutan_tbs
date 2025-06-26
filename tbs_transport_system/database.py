import sqlite3

DATABASE_FILE = "data/tbs_data.db"

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Tabel Pengguna
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL -- 'admin', 'pengawas', 'supir'
        )
    ''')

    # Tabel Data Angkutan TBS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transport_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT NOT NULL,
            jam TEXT NOT NULL,
            km_awal REAL NOT NULL,
            km_akhir REAL NOT NULL,
            dari TEXT NOT NULL,
            ke TEXT NOT NULL,
            jenis_muatan TEXT NOT NULL,
            volume REAL NOT NULL,
            satuan TEXT NOT NULL,
            bbm REAL NOT NULL,
            biaya REAL NOT NULL,
            supir TEXT NOT NULL,
            keterangan TEXT,
            status TEXT DEFAULT 'pending' -- 'pending', 'verified', 'rejected'
        )
    ''')

    # Tambahkan user default jika belum ada (hanya untuk testing awal)
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                   ("admin", "admin123", "admin"))
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                   ("pengawas", "pengawas123", "pengawas"))
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                   ("budi", "supir123", "supir"))

    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
    user_data = cursor.fetchone()
    conn.close()
    return user_data[0] if user_data else None

def insert_transport_data(data):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transport_records (tanggal, jam, km_awal, km_akhir, dari, ke, jenis_muatan, volume, satuan, bbm, biaya, supir, keterangan)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['tanggal'], data['jam'], data['km_awal'], data['km_akhir'], data['dari'], data['ke'],
          data['jenis_muatan'], data['volume'], data['satuan'], data['bbm'], data['biaya'],
          data['supir'], data['keterangan']))
    conn.commit()
    conn.close()

def get_transport_data(filters=None):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    query = "SELECT * FROM transport_records"
    params = []
    
    if filters:
        conditions = []
        if 'tanggal' in filters and filters['tanggal']:
            conditions.append("tanggal = ?")
            params.append(filters['tanggal'])
        if 'supir' in filters and filters['supir']:
            conditions.append("supir = ?")
            params.append(filters['supir'])
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    # Mendapatkan nama kolom
    cols = [description[0] for description in cursor.description]
    
    conn.close()
    return [dict(zip(cols, row)) for row in rows] # Mengembalikan list of dictionaries

def update_record_status(record_id, status):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE transport_records SET status = ? WHERE id = ?", (status, record_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    import os
    if not os.path.exists('data'):
        os.makedirs('data')
    init_db()
    print("Database initialized with default users.")