let ultimoPedido = localStorage.getItem("ultimoPedido");

if (!ultimoPedido) {
    ultimoPedido = 1000;
} else {
    ultimoPedido = Number(ultimoPedido);
}
ultimoPedido++;

localStorage.setItem("ultimoPedido", ultimoPedido);

document.getElementById("numeroPedido").innerHTML = `#${ultimoPedido}`;
