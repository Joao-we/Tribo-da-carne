let btn = document.getElementById("enviar")
 
btn.addEventListener("click", async (event) => {
    event.preventDefault()
 
    const nome     = document.getElementById("nome").value.trim()
    const endereco = document.getElementById("endereco").value.trim()
    const email    = document.getElementById("email").value.trim()
    const senha    = document.getElementById("senha").value
 
    // Validação no front antes de enviar
    if (!nome || !endereco || !email || !senha) {
        alert("Por favor, preencha todos os campos.")
        return
    }
 
    if (senha.length < 6) {
        alert("A senha deve ter pelo menos 6 caracteres.")
        return
    }
 
    btn.disabled = true
    btn.textContent = "Cadastrando..."
 
    try {
        const resposta = await fetch("/api/cadastro", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nome, endereco, email, senha })
        })
 
        const dados = await resposta.json()
 
        if (dados.sucesso) {
            alert(dados.mensagem)
            // Redireciona para o login após cadastro bem-sucedido
            window.location.href = "/login.html"
        } else {
            alert(dados.mensagem)
            btn.disabled = false
            btn.textContent = "Cadastrar"
        }
 
    } catch (erro) {
        alert("Erro ao conectar com o servidor. Tente novamente.")
        btn.disabled = false
        btn.textContent = "Cadastrar"
    }
})