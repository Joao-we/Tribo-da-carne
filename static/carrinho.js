const carrinhoCompra = document.getElementById("cards")
let totalCompra = document.getElementById("precos")
let compras = document.getElementById("total-compras")
const vazio = document.getElementById("carrinhoVazio")
let carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];
let dados = []
fetch("/api/produtos")
    .then(response => response.json())
    .then(produtos => {
        dados = produtos
        gerarItensCarrinho();;
    })

let atualizarIconeCarrinho = () => {
    let icone = document.getElementById("quantidade-carrinho");

    if (!icone) return;

    let total = carrinho.reduce((acumulo, item) => {
        return acumulo + item.quantidade;
    }, 0);

    icone.innerHTML = total;
};

let gerarItensCarrinho = () => {
    if (carrinho.length !== 0) {
        carrinhoCompra.innerHTML = carrinho.map((item) => {
            let { id, quantidade } = item;
            let produto = dados.find((produto) => produto.id === Number(id)) || {};
            let { preco, img, nome, disponivel } = produto;
            return `
                <fieldset id="card">
                    <legend>${nome}</legend>
                    <article class="card-item">
                        <img src="${img}" alt="" class="produto">
                        <p>Temos ${disponivel} desse item disponivel</p>
                        <fieldset class="btns">
                            <button class="botao" id="mais" onclick="aumentar('${id}')">+</button>
                            <p class="quantidade" id="${id}">${quantidade}</p>
                            <button class="botao" id="menos" onclick="diminuir('${id}')">-</button>
                            <span id="valor">R$${(preco * quantidade).toFixed(2)}</span>
                            <button class="remover" onclick="removerItem('${id}')">Remover</button>
                        </fieldset>
                    </article>
                </fieldset>
                `
        }).join("");
        let total = carrinho.reduce((totalAtual, item) => {
            let produto = dados.find(
                (produto) => produto.id === Number(item.id)
            ) || {};
            if (!produto.preco) return totalAtual;
            return totalAtual + (produto.preco * item.quantidade);
        }, 0);
        totalCompra.innerHTML = `   
    ${carrinho.map((item) => {
            let { id, quantidade } = item;
            let produto = dados.find((produto) => produto.id === Number(item.id)) || {};

            let { preco, nome } = produto;
            if (!produto.preco) return totalAtual;
            return `
            <span>${nome}</span> 
            <span>${(preco * quantidade).toFixed(2)}</span> 
            <span>${quantidade}</span>
        `;

        }).join("")}
        
        <h2 class:"text">Total:</h2>
        <h2>R$${total.toFixed(2)}</h2>
`;
        `<section><h2>Valor Total R$${(total).toFixed(2)}</h2></section>`
    } else {
        carrinhoCompra.innerHTML = "";
        vazio.innerHTML = `
            <h1>Carrinho vazio</h1>
            <a href="bovino.html">Adicionar itens ao carrinho</a>
            `
        compras.classList.remove("total-compras")
        compras.classList.add("deletar")
    };

}
atualizarIconeCarrinho()
gerarItensCarrinho()

function diminuir(id) {
    id = Number(id)
    let itemNoCarrinho = carrinho.find((item) => item.id === id);
    if (!itemNoCarrinho) return;
    itemNoCarrinho.quantidade -= 1;
    if (itemNoCarrinho.quantidade === 0) {
        carrinho = carrinho.filter((item) => item.id !== id);
    };

    localStorage.setItem("carrinho", JSON.stringify(carrinho));

    atualizarIconeCarrinho()
    gerarItensCarrinho()
}

function aumentar(id) {
    id = Number(id)
    let itemNoCarrinho = carrinho.find((item) => Number(item.id) === id);
    let limite = dados.find((produto) => produto.id === Number(id));
    if (!itemNoCarrinho) return;
    if (itemNoCarrinho.quantidade >= limite.disponivel) {
        alert("Você atigiu o limite máximo")
    } else {
        itemNoCarrinho.quantidade += 1;
    }
    localStorage.setItem("carrinho", JSON.stringify(carrinho));

    atualizarIconeCarrinho()
    gerarItensCarrinho()
}

function removerItem(id) {
    id = Number(id)
    carrinho = carrinho.filter((item) => item.id !== id);
    localStorage.setItem("carrinho", JSON.stringify(carrinho));
    atualizarIconeCarrinho()
    gerarItensCarrinho()
}