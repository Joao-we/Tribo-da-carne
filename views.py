from app import app
import time
import os
import hashlib
from flask import render_template, jsonify, request
import sqlite3
from datetime import datetime
import ml_vendas
 
# ROTAS DAS TELAS
@app.route("/")
def inicio():
    return render_template("index.html")
    
@app.route("/bovino.html")
def bovino():
    return render_template("bovino.html")
 
@app.route("/frango.html")
def frango():
    return render_template("frango.html")
 
@app.route("/suino.html")
def suino():
    return render_template("suino.html")
 
@app.route("/empanados.html")
def empanados():
    return render_template("empanados.html")
 
@app.route("/variados.html")
def variados():
    return render_template("variados.html")
 
@app.route("/Carrinho.html")
def carrinho():
    return render_template("Carrinho.html")
 
@app.route("/login.html")
def login():
    return render_template("login.html")
 
@app.route("/pagamento.html")
def pagamento():
    return render_template("pagamento.html")
 
@app.route("/meusPedidos.html")
def meus_pedidos():
    return render_template("meusPedidos.html")
 
@app.route("/cadastro.html")
def cadastro():
    return render_template("cadastro.html")

@app.route("/vendas.html")
def vendas():
    return render_template("vendas.html")
 
# FINAL DAS ROTAS DAS TELAS
 
# COMEÇO ROTAS DA API
 
# GET - lista produtos
@app.route("/api/produtos")
def api_produtos():
    conexao = sqlite3.connect("produtos.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos")
    dados = cursor.fetchall()
    conexao.close()
    listaNova = []
    for produto in dados:
        listaNova.append({
            "id": produto[0],
            "nome": produto[1],
            "preco": produto[2],
            "img": produto[3],
            "det": produto[4],
            "categoria": produto[5],
            "disponivel": produto[6]
        })
    return jsonify(listaNova)
 
# POST - criar produto (só ADM)
@app.route("/api/produtos/criar", methods=["POST"])
def criar_produto():
    email_adm = request.form.get("email_adm", "").strip().lower()
 
    conexao = sqlite3.connect("produtos.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT adm FROM usuarios WHERE email = ?", (email_adm,))
    usuario = cursor.fetchone()
    conexao.close()
 
    if not usuario or usuario[0] != 1:
        return jsonify({"success": False, "erro": "Sem permissão"}), 403
 
    nome = request.form.get("nome", "").strip()
    preco = request.form.get("preco", "").strip()
    descricao = request.form.get("descricao", "").strip()
    categoria = request.form.get("categoria", "").strip()
    imagem = request.files.get("imagem")
 
    if not nome or not preco or not imagem or not categoria:
        return jsonify({"success": False, "erro": "Campos obrigatórios"}), 400
 
    nome_arquivo = f"{int(time.time())}_{imagem.filename}"
    pasta_uploads = os.path.join("static", "uploads")
    os.makedirs(pasta_uploads, exist_ok=True)
    imagem.save(os.path.join(pasta_uploads, nome_arquivo))
    caminho = f"/static/uploads/{nome_arquivo}"
 
    conexao = sqlite3.connect("produtos.db")
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO produtos (nome, preco, img, det, categoria, disponivel)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, float(preco), caminho, descricao, categoria, 1))
    conexao.commit()
    conexao.close()
 
    return jsonify({"success": True})
 
# API de cadastro
@app.route("/api/cadastro", methods=["POST"])
def api_cadastro():
    dados = request.get_json()
 
    nome = dados.get("nome", "").strip()
    endereco = dados.get("endereco", "").strip()
    email = dados.get("email", "").strip().lower()
    senha = dados.get("senha", "")
 
    if not nome or not email or not senha or not endereco:
        return jsonify({"sucesso": False, "mensagem": "Preencha todos os campos"}), 400
 
    if len(senha) < 6:
        return jsonify({"sucesso": False, "mensagem": "A senha deve ter pelo menos 6 caracteres"}), 400
 
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
 
    try:
        conexao = sqlite3.connect("produtos.db")
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, endereco, email, senha) VALUES(?, ?, ?, ?)",
            (nome, endereco, email, senha_hash)
        )
        conexao.commit()
        conexao.close()
        return jsonify({"sucesso": True, "mensagem": "Cadastro realizado com sucesso!"}), 201
 
    except sqlite3.IntegrityError:
        return jsonify({"sucesso": False, "mensagem": "Este e-mail já está cadastrado!"}), 409
    except Exception:
        return jsonify({"sucesso": False, "mensagem": "Erro interno do servidor"}), 500
 
# API login
@app.route("/api/login", methods=["POST"])
def api_login():
    dados = request.get_json()
 
    email = dados.get("email", "").strip().lower()
    senha = dados.get("senha", "")
 
    if not email or not senha:
        return jsonify({"sucesso": False, "mensagem": "Preencha todos os campos"}), 400
 
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
 
    conexao = sqlite3.connect("produtos.db")
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome, email, adm FROM usuarios WHERE email = ? AND senha = ?",
        (email, senha_hash)
    )
    usuario = cursor.fetchone()
    conexao.close()
 
    if usuario:
        return jsonify({
            "sucesso": True,
            "mensagem": "Login realizado com sucesso!",
            "usuario": {
                "id": usuario[0],
                "nome": usuario[1],
                "email": usuario[2],
                "adm": usuario[3]
            }
        }), 200
    else:
        return jsonify({"sucesso": False, "mensagem": "E-mail ou senha incorretos."}), 401
 
@app.route("/aprovar-pagamento", methods=["POST"])
def aprovar_pagamento():
    return jsonify({
        "status": "Aprovado",
        "mensagem": "Pagamento aprovado com sucesso!"
    })

# CRIAR PEDIDO (grava a venda no banco - e o que alimenta o relatorio e a ML)
@app.route("/api/pedidos/criar", methods=["POST"])
def criar_pedido():
    dados = request.get_json()
    email = (dados.get("email") or "visitante").strip().lower()
    itens = dados.get("itens", [])

    if not itens:
        return jsonify({"sucesso": False, "mensagem": "Carrinho vazio"}), 400

    conexao = sqlite3.connect("produtos.db")
    cursor = conexao.cursor()

    total_pedido = 0
    itens_validados = []

    for item in itens:
        produto_id = item.get("id")
        quantidade = int(item.get("quantidade", 0))
        if quantidade <= 0:
            continue
        cursor.execute("SELECT nome, preco, categoria FROM produtos WHERE id = ?", (produto_id,))
        produto = cursor.fetchone()
        if not produto:
            continue
        nome, preco, categoria = produto
        subtotal = round(preco * quantidade, 2)
        total_pedido += subtotal
        itens_validados.append((produto_id, nome, categoria, quantidade, preco, subtotal))

    if not itens_validados:
        conexao.close()
        return jsonify({"sucesso": False, "mensagem": "Nenhum item valido no carrinho"}), 400

    data_pedido = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO pedidos (email_usuario, data, total, origem) VALUES (?, ?, ?, 'real')",
        (email, data_pedido, round(total_pedido, 2))
    )
    pedido_id = cursor.lastrowid

    for produto_id, nome, categoria, quantidade, preco, subtotal in itens_validados:
        cursor.execute(
            """INSERT INTO itens_pedido
               (pedido_id, produto_id, nome_produto, categoria, quantidade, preco_unitario, subtotal)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (pedido_id, produto_id, nome, categoria, quantidade, preco, subtotal)
        )

    conexao.commit()
    conexao.close()

    return jsonify({
        "sucesso": True,
        "mensagem": "Pedido registrado com sucesso!",
        "pedido_id": pedido_id,
        "total": round(total_pedido, 2)
    }), 201

# RESUMO DE VENDAS (calculo direto - quanto ja foi vendido)
@app.route("/api/vendas/resumo")
def api_vendas_resumo():
    email_adm = request.args.get("email_adm", "").strip().lower()

    conexao = sqlite3.connect("produtos.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT adm FROM usuarios WHERE email = ?", (email_adm,))
    usuario = cursor.fetchone()
    conexao.close()

    if not usuario or usuario[0] != 1:
        return jsonify({"sucesso": False, "erro": "Sem permissao"}), 403

    resumo_geral = ml_vendas.calcular_total_vendido()
    resumo_real = ml_vendas.calcular_total_vendido(origem="real")
    resumo_demo = ml_vendas.calcular_total_vendido(origem="demo")
    por_categoria = ml_vendas.vendas_por_categoria()

    return jsonify({
        "sucesso": True,
        "geral": resumo_geral,
        "real": resumo_real,
        "demo": resumo_demo,
        "por_categoria": por_categoria
    })

# PREVISAO DE VENDAS (Machine Learning - Regressao Linear)
@app.route("/api/vendas/previsao")
def api_vendas_previsao():
    email_adm = request.args.get("email_adm", "").strip().lower()
    dias = int(request.args.get("dias", 7))

    conexao = sqlite3.connect("produtos.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT adm FROM usuarios WHERE email = ?", (email_adm,))
    usuario = cursor.fetchone()
    conexao.close()

    if not usuario or usuario[0] != 1:
        return jsonify({"sucesso": False, "erro": "Sem permissao"}), 403

    resultado = ml_vendas.prever_vendas(dias_futuros=dias)
    resultado["sucesso"] = True
    return jsonify(resultado)