let açougue = document.getElementById("grid-produtos");
const categoria = document.body.dataset.categoria;
let dados = []
 
fetch("/api/produtos")
    .then(response => response.json())
    .then(produtos => {
        dados = produtos;
        gerarAçougue();
    })
 
let carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];
 
// Lê o usuário salvo pelo login.js (formato: { id, nome, email, adm })
const usuarioSalvo = JSON.parse(localStorage.getItem("usuario")) || null;
const isAdmin = usuarioSalvo && usuarioSalvo.adm === 1;
 
let gerarAçougue = () => {
 
    const filtro = dados.filter(p => p.categoria === categoria);
 
    let html = "";
 
    // Botão de cadastrar produto — só aparece para ADM
    if (isAdmin) {
        html += `
        <article class="admin-card" id="abrir-popup">
            <div class="admin-content">
                <h2>+</h2>
                <p>Cadastrar Produto</p>
            </div>
        </article>
        `;
    }
 
    html += filtro.map((produto) => {
        let { id, nome, preco, img, det } = produto;
        return `
        <article class="card" id="produto${id}">
            <img src="${img}">
            <p>${nome}</p>
            <p style="color: rgb(190, 0, 0);">R$${preco}</p>
            <button class="btn" onclick="adicionar('${id}')">
                Adicionar ao carrinho
            </button>
            <a class="btn2" href="${det}">
                Ver mais detalhes
            </a>
        </article>
        `;
    }).join("");
 
    açougue.innerHTML = html;
};
 
let adicionar = (id) => {
    id = Number(id);
    let itemNoCarrinho = carrinho.find((item) => item.id === id);
    let limite = dados.find((produto) => produto.id === id);
    if (!itemNoCarrinho) {
        carrinho.push({ id: id, quantidade: 1 });
    } else {
        if (itemNoCarrinho.quantidade >= limite.disponivel) {
            alert("Você atingiu o limite máximo");
        } else {
            itemNoCarrinho.quantidade += 1;
        }
    }
    atualizarIconeCarrinho();
    localStorage.setItem("carrinho", JSON.stringify(carrinho));
};
 
let atualizarIconeCarrinho = () => {
    let icone = document.getElementById("quantidade-carrinho");
    let total = carrinho.reduce((acumulo, item) => acumulo + item.quantidade, 0);
    icone.innerHTML = total;
};
 
atualizarIconeCarrinho();
 
document.addEventListener("click", (e) => {
    if (e.target.closest("#abrir-popup")) {
        document.querySelector("#popup").style.display = "flex";
    }
    if (e.target.id === "fechar-popup" || e.target.id === "cancelar-popup") {
        document.querySelector("#popup").style.display = "none";
    }
});
 
document.querySelector("#salvar-produto")?.addEventListener("click", async () => {
    const nome = document.querySelector("#nome").value;
    const preco = document.querySelector("#preco").value;
    const imagem = document.querySelector("#imagem").files[0];
    const categoria = document.querySelector("#categoria").value;
    const descricao = document.querySelector("#descricao").value;
 
    if (!nome || !preco || !imagem || !categoria) {
        alert("Preencha nome, preço e imagem.");
        return;
    }
 
    const formData = new FormData();
    formData.append("nome", nome);
    formData.append("preco", preco);
    formData.append("imagem", imagem);
    formData.append("descricao", descricao);
    formData.append("categoria", categoria);
    formData.append("email_adm", usuarioSalvo ? usuarioSalvo.email : "");
 
    const resposta = await fetch("/api/produtos/criar", {
        method: "POST",
        body: formData
    });
 
    const resultado = await resposta.json();
 
    if (resultado.success) {
        alert("Produto criado!");
        location.reload();
    } else {
        alert(resultado.erro || "Erro ao criar produto!");
    }
});