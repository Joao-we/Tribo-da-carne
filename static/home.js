let carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];
let atualizarIconeCarrinho = () => {
        let icone = document.getElementById("quantidade-carrinho");

        let total = carrinho.reduce((acumulo, item) => {
            return acumulo + item.quantidade;
        }, 0);

        icone.innerHTML = total;
    };

atualizarIconeCarrinho();



let perfil = document.getElementById("perfil")
let logout = document.getElementById("logout")

let logado = localStorage.getItem("logado")

if(logado == "true"){
    perfil.style.display = "none"

    logout.style.display = "block"
}

logout.addEventListener("click", ()=>{

    let confirmar = confirm("Você tem certeza que deseja sair da sua conta")
    if (confirmar){
        localStorage.removeItem("logado")

        location.reload()
    }
})