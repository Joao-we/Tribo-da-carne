let tel = document.getElementById("numero")
let cartao = document.getElementById("cartao")

if(tel){
numero.addEventListener("input", () =>{
    let macaraTelefone = tel.value
    macaraTelefone = macaraTelefone.replace(/[^0-9]/g, "")
    macaraTelefone = macaraTelefone.slice(0, 11)
    let parte1 = macaraTelefone.slice(0, 2)
    let parte2 = macaraTelefone.slice(2, 7)
    let parte3 = macaraTelefone.slice(7, 11)
    let numero = macaraTelefone
    if (macaraTelefone.length > 2){
        numero = `(${parte1}) ${parte2}`
    }
    if (macaraTelefone.length > 7){
        numero = `(${parte1}) ${parte2}-${parte3}`
    }
    tel.value = numero
})}

if(cartao){
cartao.addEventListener("input" , () =>{
    let mascaraCartao = cartao.value
    mascaraCartao = mascaraCartao.replace(/[^0-9]/g, "")
    mascaraCartao = mascaraCartao.slice(0, 16)
    let parte1 = mascaraCartao.slice(0, 4)
    let parte2 = mascaraCartao.slice(4, 8)
    let parte3 = mascaraCartao.slice(8, 12)
    let parte4 = mascaraCartao.slice(12, 16)
    let numero = mascaraCartao
    if (mascaraCartao.length > 4){
        numero = `${parte1} ${parte2}`
    }
    if (mascaraCartao.length > 8){
        numero = `${parte1} ${parte2} ${parte3}`
    }
    if (mascaraCartao.length > 12){
        numero = `${parte1} ${parte2} ${parte3} ${parte4}`
    }
    cartao.value = numero
})}