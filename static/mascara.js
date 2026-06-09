let tel = document.getElementById("numero")
let cartao = document.getElementById("cartao")


if(cep){
cep.addEventListener("input", () => {
    let texto = cep.value
    texto = texto.replace(/[^0-9]/g, "")
    texto = texto.slice(0, 8)
    let parte1 = texto.slice(0, 5)
    let parte2 = texto.slice(5, 8)
    if (texto.length > 5) {
        texto = `${parte1}-${parte2}`
    }
    cep.value = texto
})
}

if (cpf){cpf.addEventListener("input", () => {
    let texto = cpf.value
    texto = texto.replace(/[^0-9]/g, "")
    texto = texto.slice(0, 11)
    let parte1 = texto.slice(0, 3)
    let parte2 = texto.slice(3, 6)
    let parte3 = texto.slice(6, 9)
    let parte4 = texto.slice(9, 11)
    let numero = texto
    if (texto.length > 3) {
        numero = `${parte1}.${parte2}`
    }
    if (texto.length > 6) {
        numero = `${parte1}.${parte2}.${parte3}`
    }
    if (texto.length > 9) {
        numero = `${parte1}.${parte2}.${parte3}-${parte4}`
    }
    cpf.value = numero
})}

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
cartao.addEventListener("input", () =>{
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