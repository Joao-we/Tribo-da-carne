import sqlite3
import hashlib
 
print("=== Criar ADM ===")
nome     = input("Nome: ").strip()
endereco = input("Endereço: ").strip()
email    = input("E-mail: ").strip().lower()
adm      = int(input("ADM? (1=sim, 0=não): "))
senha    = input("Senha (mín. 6 caracteres): ")
 
if len(senha) < 6:
    print("Erro: senha muito curta.")
    exit()
 
senha_hash = hashlib.sha256(senha.encode()).hexdigest()
 
try:
    conexao = sqlite3.connect("produtos.db")
    cursor  = conexao.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, endereco, email, senha, adm) VALUES (?, ?, ?, ?, ?)",
        (nome, endereco, email, senha_hash, adm)
    )
    conexao.commit()
    conexao.close()
    print(f"\nADM '{nome}' criado com sucesso! Faça login com: {email}")
 
except sqlite3.IntegrityError:
    conexao = sqlite3.connect("produtos.db")
    cursor  = conexao.cursor()
    cursor.execute("UPDATE usuarios SET adm = 1 WHERE email = ?", (email,))
    conexao.commit()
    conexao.close()
    print(f"\nUsuário '{email}' já existia — promovido para ADM!")