import sqlite3
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

CAMINHO_BANCO = "produtos.db"
MINIMO_DIAS_PARA_TREINAR = 5  


def _conectar():
    return sqlite3.connect(CAMINHO_BANCO)


def calcular_total_vendido(origem=None):
    """
    Soma simples (sem ML) do quanto ja foi vendido ate agora.
    'origem' pode ser None (tudo), 'real' ou 'demo'.
    """
    conexao = _conectar()
    cursor = conexao.cursor()
    if origem:
        cursor.execute("SELECT COALESCE(SUM(total), 0), COUNT(*) FROM pedidos WHERE origem = ?", (origem,))
    else:
        cursor.execute("SELECT COALESCE(SUM(total), 0), COUNT(*) FROM pedidos")
    total, quantidade_pedidos = cursor.fetchone()
    conexao.close()
    return {"total_vendido": round(total or 0, 2), "quantidade_pedidos": quantidade_pedidos or 0}


def vendas_por_categoria():
    """Soma simples (sem ML) do total vendido por categoria de produto."""
    conexao = _conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT categoria, SUM(subtotal) as total, SUM(quantidade) as quantidade
        FROM itens_pedido
        GROUP BY categoria
        ORDER BY total DESC
    """)
    linhas = cursor.fetchall()
    conexao.close()
    return [
        {"categoria": categoria, "total": round(total or 0, 2), "quantidade": quantidade or 0}
        for categoria, total, quantidade in linhas
    ]


def _vendas_diarias():
    """
    Retorna a lista (data, total_do_dia) ordenada cronologicamente.
    E a partir dela que o modelo de ML aprende.
    """
    conexao = _conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT date(data) as dia, SUM(total) as total
        FROM pedidos
        GROUP BY dia
        ORDER BY dia ASC
    """)
    linhas = cursor.fetchall()
    conexao.close()
    return linhas 


def prever_vendas(dias_futuros=7):
    """
    Treina a Regressao Linear com o historico diario de vendas e
    retorna a previsao para os proximos "dias_futuros" dias.

    Retorno (dict):
        - status: "ok" ou "dados_insuficientes"
        - dias_usados_no_treino: quantos dias de historico existem
        - historico: [{"data": ..., "total": ...}, ...]
        - previsao: [{"data": ..., "total_previsto": ...}, ...]
        - total_previsto_periodo: soma da previsao do periodo
        - tendencia_dia: quanto a venda cresce (ou cai) por dia, em R$
        - confiabilidade_r2: o quao bem o modelo explica os dados (0 a 1)
    """
    linhas = _vendas_diarias()

    if len(linhas) < MINIMO_DIAS_PARA_TREINAR:
        return {
            "status": "dados_insuficientes",
            "mensagem": (
                f"Ha apenas {len(linhas)} dia(s) com vendas registradas. "
                f"Sao necessarios pelo menos {MINIMO_DIAS_PARA_TREINAR} dias "
                "de historico para treinar o modelo com um minimo de confianca."
            ),
            "dias_usados_no_treino": len(linhas),
        }

    datas_str = [linha[0] for linha in linhas]
    totais = np.array([linha[1] for linha in linhas], dtype=float)

    # Transforma cada data em um numero sequencial (0, 1, 2, 3...)
    # para servir de variavel de entrada (X) do modelo.
    primeira_data = datetime.strptime(datas_str[0], "%Y-%m-%d")
    X = np.array([
        (datetime.strptime(d, "%Y-%m-%d") - primeira_data).days
        for d in datas_str
    ]).reshape(-1, 1)
    y = totais

    modelo = LinearRegression()
    modelo.fit(X, y)

    y_previsto_historico = modelo.predict(X)
    confiabilidade = round(float(r2_score(y, y_previsto_historico)), 3) if len(set(totais)) > 1 else 0.0

    ultimo_dia_indice = X[-1][0]
    ultima_data = datetime.strptime(datas_str[-1], "%Y-%m-%d")

    previsao = []
    for i in range(1, dias_futuros + 1):
        indice_futuro = ultimo_dia_indice + i
        data_futura = ultima_data + timedelta(days=i)
        valor_previsto = float(modelo.predict([[indice_futuro]])[0])
        valor_previsto = max(0.0, valor_previsto)  # vendas nao podem ser negativas
        previsao.append({
            "data": data_futura.strftime("%Y-%m-%d"),
            "total_previsto": round(valor_previsto, 2)
        })

    return {
        "status": "ok",
        "dias_usados_no_treino": len(linhas),
        "historico": [{"data": d, "total": round(float(t), 2)} for d, t in zip(datas_str, totais)],
        "previsao": previsao,
        "total_previsto_periodo": round(sum(p["total_previsto"] for p in previsao), 2),
        "tendencia_dia": round(float(modelo.coef_[0]), 2),
        "confiabilidade_r2": confiabilidade,
    }


if __name__ == "__main__":
    print("Total vendido:", calcular_total_vendido())
    print("Por categoria:", vendas_por_categoria())
    resultado = prever_vendas()
    print("Previsao:", resultado)
