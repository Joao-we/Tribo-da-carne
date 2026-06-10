let btn = document.getElementById("enviar")

btn.addEventListener("click", async (event) => {
    event.preventDefault()

    const email = document.getElementById("email").value.trim()
    const senha = document.getElementById("senha").value

    if (!email || !senha) {
        alert("Por favor, preencha e-mail e senha.")
        return
    }
    btn.disabled = true
    btn.textContent = "Entrando..."
    try {
        const resposta = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, senha })
        })
        const dados = await resposta.json()
        if (dados.sucesso) {
            localStorage.setItem("usuario", JSON.stringify(dados.usuario))
            alert("Bem-vindo, " + dados.usuario.nome + "!")
            window.location.href = "/"
        } else {
            alert(dados.mensagem)
            btn.disabled = false
            btn.textContent = "Entrar"
        }
        if (dados.sucesso) {
            localStorage.setItem("usuario", JSON.stringify(dados.usuario))
            localStorage.setItem("logado", "true")
            alert("Bem-vindo, " + dados.usuario.nome + "!")
            window.location.href = "/"
        } else {
            alert(dados.mensagem)
            btn.disabled = false
            btn.textContent = "Entrar"
        }
    } catch (erro) {
        alert("Erro ao conectar com o servidor. Tente novamente.")
        btn.disabled = false
        btn.textContent = "Entrar"
    }
})