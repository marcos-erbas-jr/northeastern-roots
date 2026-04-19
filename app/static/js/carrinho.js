let carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];

function adicionarItem(nome, preco) {
    carrinho.push({nome, preco});
    localStorage.setItem("carrinho", JSON.stringify(carrinho));
    atualizarCarrinho();
}
function atualizarCarrinho() {
    let total = carrinho.reduce((soma, item) => soma+item.preco, 0);
    document.getElementById("total").innerText = "- Total: R$ " + total.toFixed(2);
    document.getElementById("quantidade").innerText = "Quantidade: " + carrinho.length;
}

function finalizarPedido() {
    if (carrinho.length === 0) {
        return;
    }
    localStorage.removeItem("carrinho");
    carrinho = [];
    atualizarCarrinho();
    //window.location.href = "/";
}