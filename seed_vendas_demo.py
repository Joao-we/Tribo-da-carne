# seed_vendas_demo.py
# ---------------------------------------------------------
# Este script gera VENDAS DE DEMONSTRACAO (fake) dos ultimos 90 dias
# e salva no banco com origem = "demo".
#
# Por que isso existe?
#   O modelo de Machine Learning so consegue aprender e prever se
#   tiver historico de vendas. Como o site e novo e ainda nao tem
#   pedidos reais suficientes, este script cria um historico
#   simulado (com tendencia de crescimento + variacao por dia da
#   semana + ruido aleatorio) so para você conseguir DEMONSTRAR o
#   funcionamento da ML para o professor.
#
# IMPORTANTE (seja transparente na apresentacao):
#   - Esses dados sao sinteticos/fake, marcados com origem = "demo".
#   - Quando o site comecar a receber vendas reais (origem = "real",
#     que e o que a rota /api/pedidos/criar grava automaticamente),
#     voce pode rodar "remover_demo()" para apagar os dados ficticios
#     e deixar so o historico real.
#
# Como usar:
#   python seed_vendas_demo.py
# ---------------------------------------------------------

import sqlite3
import random
from datetime import datetime, timedelta

CAMINHO_BANCO = "produtos.db"
DIAS_DE_HISTORICO = 90


def remover_demo():
    """Remove apenas os dados marcados como demo, mantendo vendas reais."""
    conexao = sqlite3.connect(CAMINHO_BANCO)
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM pedidos WHERE origem = 'demo'")
    ids = [linha[0] for linha in cursor.fetchall()]
    for pedido_id in ids:
        cursor.execute("DELETE FROM itens_pedido WHERE pedido_id = ?", (pedido_id,))
    cursor.execute("DELETE FROM pedidos WHERE origem = 'demo'")
    conexao.commit()
    conexao.close()
    print(f"{len(ids)} pedido(s) de demonstracao removido(s).")


def gerar_demo():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    cursor = conexao.cursor()

    cursor.execute("SELECT id, nome, preco, categoria FROM produtos WHERE disponivel > 0")
    produtos = cursor.fetchall()

    if not produtos:
        print("Nenhum produto disponivel encontrado. Rode banco.py primeiro.")
        conexao.close()
        return

    # Evita duplicar dados demo se o script for rodado mais de uma vez
    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE origem = 'demo'")
    if cursor.fetchone()[0] > 0:
        print("Ja existem dados de demonstracao no banco. Rode remover_demo() antes de gerar de novo.")
        conexao.close()
        return

    hoje = datetime.now()
    total_pedidos_criados = 0

    for i in range(DIAS_DE_HISTORICO, 0, -1):
        dia = hoje - timedelta(days=i)

        # Tendencia: a loja vai vendendo um pouco mais com o tempo
        fator_tendencia = 1 + (DIAS_DE_HISTORICO - i) * 0.01

        # Sazonalidade semanal: fins de semana (5=sab, 6=dom) vendem mais
        fator_fim_de_semana = 1.6 if dia.weekday() in (5, 6) else 1.0

        # Quantidade de pedidos (vendas) naquele dia
        pedidos_no_dia = max(1, round(random.gauss(4, 1.5) * fator_tendencia * fator_fim_de_semana))

        for _ in range(pedidos_no_dia):
            qtd_itens_no_pedido = random.randint(1, 4)
            itens_escolhidos = random.sample(produtos, min(qtd_itens_no_pedido, len(produtos)))

            total_pedido = 0
            itens_para_inserir = []
            for produto_id, nome, preco, categoria in itens_escolhidos:
                quantidade = random.randint(1, 3)
                subtotal = round(preco * quantidade, 2)
                total_pedido += subtotal
                itens_para_inserir.append((produto_id, nome, categoria, quantidade, preco, subtotal))

            data_pedido = dia.replace(
                hour=random.randint(8, 21),
                minute=random.randint(0, 59),
                second=0
            ).strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                "INSERT INTO pedidos (email_usuario, data, total, origem) VALUES (?, ?, ?, ?)",
                ("demo@exemplo.com", data_pedido, round(total_pedido, 2), "demo")
            )
            pedido_id = cursor.lastrowid

            for produto_id, nome, categoria, quantidade, preco, subtotal in itens_para_inserir:
                cursor.execute(
                    """INSERT INTO itens_pedido
                       (pedido_id, produto_id, nome_produto, categoria, quantidade, preco_unitario, subtotal)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (pedido_id, produto_id, nome, categoria, quantidade, preco, subtotal)
                )
            total_pedidos_criados += 1

    conexao.commit()
    conexao.close()
    print(f"{total_pedidos_criados} pedidos de demonstracao criados ao longo de {DIAS_DE_HISTORICO} dias.")
    print("Esses dados estao marcados com origem='demo' e podem ser removidos com remover_demo().")


if __name__ == "__main__":
    gerar_demo()
