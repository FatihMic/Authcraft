import sqlite3
from core.security import SecurityManager

class SQLiteStorage:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    email TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS vault_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    category TEXT NOT NULL,
                    title TEXT NOT NULL,
                    account_name TEXT,
                    secret_val TEXT NOT NULL,
                    url TEXT,
                    FOREIGN KEY(username) REFERENCES users(username)
                )
            ''')

    def save_user(self, username, password, email, role="user"):
        salt = SecurityManager.generate_salt()
        hashed = SecurityManager.hash_password(password, salt)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?)', (username, hashed, salt, email, role))

    def get_user(self, username):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT username, password, salt, email, role FROM users WHERE username = ?', (username,))
            return cursor.fetchone()

    # Kasa Verilerini AES-256 İle Şifreleyerek Kaydetme
    def add_vault_item(self, username, master_pass, salt, category, title, account_name, secret_val, url=""):
        encrypted_secret = SecurityManager.encrypt_data(secret_val, master_pass, salt)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO vault_items (username, category, title, account_name, secret_val, url) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, category, title, account_name, encrypted_secret, url))

    # Verileri Okurken AES-256 İle Çözme
    def get_vault_items(self, username, master_pass, salt, search_query=""):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if search_query:
                query = '''
                    SELECT id, category, title, account_name, secret_val, url 
                    FROM vault_items 
                    WHERE username = ? AND (title LIKE ? OR account_name LIKE ?)
                '''
                cursor.execute(query, (username, f"%{search_query}%", f"%{search_query}%"))
            else:
                cursor.execute('SELECT id, category, title, account_name, secret_val, url FROM vault_items WHERE username = ?', (username,))
            
            raw_items = cursor.fetchall()
            decrypted_items = []
            for item_id, cat, title, acc, enc_secret, url in raw_items:
                dec_secret = SecurityManager.decrypt_data(enc_secret, master_pass, salt)
                decrypted_items.append((item_id, cat, title, acc, dec_secret, url))
            return decrypted_items

    def delete_vault_item(self, item_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('DELETE FROM vault_items WHERE id = ?', (item_id,))