let usuario = JSON.parse(localStorage.getItem("usuario")) || null;

function formatarReal(valor) {
    return "R$" + Number(valor).toFixed(2).replace(".", ",");
}

if (!usuario || usuario.adm !== 1) {
    document.getElementById("bloqueado").style.display = "block";
} else {
    document.getElementById("painel").style.display = "block";
    carregarResumo();
    carregarPrevisao();
}

function carregarResumo() {
    fetch(`/api/vendas/resumo?email_adm=${encodeURIComponent(usuario.email)}`)
        .then(resposta => resposta.json())
        .then(dados => {
            if (!dados.sucesso) return;

            document.getElementById("totalVendido").innerText = formatarReal(dados.geral.total_vendido);
            document.getElementById("qtdPedidos").innerText = `${dados.geral.quantidade_pedidos} pedidos`;

            document.getElementById("origemDados").innerText =
                `${dados.real.quantidade_pedidos} pedido(s) real(is) registrados pelo site `
                + `e ${dados.demo.quantidade_pedidos} pedido(s) de demonstração (gerados pelo `
                + `script seed_vendas_demo.py) usados para a Machine Learning ter histórico suficiente.`;

            desenharGraficoCategoria(dados.por_categoria);
        });
}

function carregarPrevisao() {
    fetch(`/api/vendas/previsao?email_adm=${encodeURIComponent(usuario.email)}&dias=7`)
        .then(resposta => resposta.json())
        .then(dados => {
            if (dados.status === "dados_insuficientes") {
                document.getElementById("avisoML").innerText = dados.mensagem;
                document.getElementById("totalPrevisto").innerText = "--";
                return;
            }

            document.getElementById("totalPrevisto").innerText = formatarReal(dados.total_previsto_periodo);
            document.getElementById("confiabilidade").innerText = dados.confiabilidade_r2;

            let tendenciaTexto = dados.tendencia_dia >= 0
                ? `crescendo ${formatarReal(dados.tendencia_dia)}/dia`
                : `caindo ${formatarReal(Math.abs(dados.tendencia_dia))}/dia`;
            document.getElementById("tendencia").innerText = `tendência: ${tendenciaTexto}`;

            document.getElementById("avisoML").innerText =
                `Modelo treinado com ${dados.dias_usados_no_treino} dias de histórico (Regressão Linear).`;

            desenharGraficoPrevisao(dados.historico, dados.previsao);
        });
}

function desenharGraficoPrevisao(historico, previsao) {
    let labels = [...historico.map(h => h.data), ...previsao.map(p => p.data)];
    let dadosHistorico = [...historico.map(h => h.total), ...previsao.map(() => null)];
    let dadosPrevisao = [...historico.map(() => null), ...previsao.map(p => p.total_previsto)];

    // conecta o último ponto real com o primeiro previsto
    if (historico.length > 0) {
        dadosPrevisao[historico.length - 1] = historico[historico.length - 1].total;
    }

    new Chart(document.getElementById("graficoPrevisao"), {
        type: "line",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Vendas reais (R$/dia)",
                    data: dadosHistorico,
                    borderColor: "#010014",
                    backgroundColor: "transparent",
                    tension: 0.2,
                    pointRadius: 2
                },
                {
                    label: "Previsão (Machine Learning)",
                    data: dadosPrevisao,
                    borderColor: "rgb(190, 0, 0)",
                    backgroundColor: "transparent",
                    borderDash: [6, 4],
                    tension: 0.2,
                    pointRadius: 3
                }
            ]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true } }
        }
    });
}

function desenharGraficoCategoria(porCategoria) {
    new Chart(document.getElementById("graficoCategoria"), {
        type: "bar",
        data: {
            labels: porCategoria.map(c => c.categoria),
            datasets: [{
                label: "Total vendido (R$)",
                data: porCategoria.map(c => c.total),
                backgroundColor: "rgb(190, 0, 0)"
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true } }
        }
    });
}