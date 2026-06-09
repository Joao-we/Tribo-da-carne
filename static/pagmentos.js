let carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];
let listaProdutos = document.getElementById("listaProdutos");
let totalCompra = document.getElementById("totalCompra");
let produtos = []
fetch("/api/produtos")
    .then(response => response.json())
    .then(dados => {
        produtos = dados;
        gerarPagamento();
    });
let gerarPagamento = () => {
    let total = 0;
    listaProdutos.innerHTML = carrinho.map((item) => {
        let produto = produtos.find((produto) => produto.id === Number(item.id));
        if (!produto) return "";
        let subtotal = produto.preco * item.quantidade;
        total += subtotal;
        return `
            <article class="produto">
                <span>${produto.nome}</span>
                <span>${item.quantidade}x</span>
                <span>R$${subtotal.toFixed(2)}</span>
            </article>
        `;
    }).join("");
    totalCompra.innerHTML = `
        Total: R$${total.toFixed(2)}
    `;
};


document.getElementById("formPagamento")
    .addEventListener("submit", (e) => {
        e.preventDefault();
        alert("Pagamento realizado com sucesso!");
        localStorage.removeItem("carrinho");
        window.location.href = "meusPedidos.html";
    });

function finalizarCompra(){
    fetch("/aprovar-pagamento", {
        method:"POST"
    })
    .then(response => response.json())
    .then(data => {
        alert(data.mensagem)
    })
    window.location.href = "meusPedidos.html";
}