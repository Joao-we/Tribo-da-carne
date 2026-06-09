import sqlite3
conexao = sqlite3.connect("produtos.db")
from produtos import produtos
cursor = conexao.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS produtos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        preco REAL,
        img TEXT,
        det TEXT,
        categoria TEXT,
        disponivel INTEGER
    )
    """
)

# CORRIGIDO: adicionada vírgula que faltava antes de "adm INTEGER"
cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        endereco TEXT,
        email TEXT UNIQUE,
        senha TEXT,
        adm INTEGER DEFAULT 0
        )
    """)

cursor.execute("DELETE FROM sqlite_sequence WHERE name='produtos'")
cursor.execute("DELETE FROM produtos")

for produto in produtos:
    cursor.execute(
       """ INSERT OR IGNORE INTO produtos (nome, preco, img, det, categoria, disponivel) VALUES (?, ?, ?, ?, ?, ?)""", (
           produto["nome"],
           produto["preco"],
           produto["img"],
           produto["det"],
           produto["categoria"],
           produto["disponivel"]
           ))
conexao.commit()
conexao.close()
print("Banco de dados inicializado com sucesso!")
