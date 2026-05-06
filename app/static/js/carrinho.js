let carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];

function adicionarItem(id, nome, preco) {
    let existente = carrinho.find(i => i.id === id);
    if (existente) {
        existente.quantidade += 1;
    } else {
        carrinho.push({ id, nome, preco, quantidade: 1 });
    }
    localStorage.setItem("carrinho", JSON.stringify(carrinho));
    atualizarCarrinho();
}
function atualizarCarrinho() {
    let total = carrinho.reduce((soma, item) => soma + (item.preco * item.quantidade), 0);
    let quantidadeTotal = carrinho.reduce((soma, item) => soma + item.quantidade, 0);
    document.getElementById("total").innerText = "Total: R$ " + total.toFixed(2);
    document.getElementById("quantidade").innerText = "Quantidade: " + quantidadeTotal;
}

function finalizarPedidoPainel(unidade_id) {
    const select = document.getElementById("cliente_id");
    const cliente_id = select ? select.value : null;

    fetch("/pedidos/criar_com_itens", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            itens: carrinho,
            unidade_id: unidade_id,
            cliente_id: cliente_id
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.erro) {
            alert("Erro: " + data.erro);
            return;
        }

        alert("Pedido criado com sucesso!");
        localStorage.removeItem("carrinho");
        window.location.href = "/pedidos";
    });
}

function finalizarPedido(unidade_id) {
    fetch("/pedido_publico", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            itens: carrinho,
            unidade_id: unidade_id
        })
    })
    .then(res => res.json())
    .then(data => {
    alert("Pedido realizado com sucesso!");
    window.location.reload();});
}
document.addEventListener("DOMContentLoaded", function () {
    localStorage.removeItem("carrinho");
    carrinho = [];
    atualizarCarrinho();
});
