import sqlite3
import hashlib

DB_NAME = "usuarios.db"

def criar_tabela():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def cadastrar_usuario(usuario, senha):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO usuarios (usuario, senha_hash) VALUES (?, ?)", (usuario, hash_senha(senha)))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def verificar_login(usuario, senha):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT senha_hash FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = c.fetchone()
    conn.close()
    if resultado and resultado[0] == hash_senha(senha):
        return True
    return False
