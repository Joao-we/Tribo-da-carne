
(function () {
    var usuario = JSON.parse(localStorage.getItem("usuario") || "null");
    if (usuario && usuario.adm === 1) {
        var link = document.getElementById("linkPainel");
        if (link) link.style.display = "inline";
    }
})();
