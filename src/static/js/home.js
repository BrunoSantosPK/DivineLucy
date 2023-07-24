function loadData() {
    const demoResponse = {
        status_code: 200,
        message: "",
        data: [{
            wallet: "Crédito Nubank",
            total: 4879.69,
            in: 78965.6,
            out: 5687.6
        }, {
            wallet: "Nuconta",
            total: 4879.69,
            in: 78965.6,
            out: 5687.6
        }, {
            wallet: "PicPay",
            total: 4879.69,
            in: 78965.6,
            out: 5687.6
        }, {
            wallet: "Carteira Física",
            total: 4879.69,
            in: 78965.6,
            out: 5687.6
        }, {
            wallet: "Caixa",
            total: 4879.69,
            in: 78965.6,
            out: 5687.6
        }]
    };

    // Remove elementos existentes
    const parent = document.getElementById("wallet-area");
    while(parent.hasChildNodes()) {
        parent.removeChild(parent.firstChild);
    }

    // Estrutura o cartão para cada carteira
    const currency = new Intl.NumberFormat("pt-br", {style: "currency", currency: "BRL"});
    demoResponse.data.forEach(item => {
        $("#wallet-area").append(`
            <div class="wallet-card">
                <h4>${item.wallet}</h4>
                <div class="wallet-row sep">
                    <span class="label">Saldo</span>
                    <span class="value">${currency.format(item.total)}</span>
                </div>
                <div class="wallet-row">
                    <span class="label">Entrada</span>
                    <span class="value">${currency.format(item.in)}</span>
                </div>
                <div class="wallet-row">
                    <span class="label">Saída</span>
                    <span class="value">${currency.format(item.out)}</span>
                </div>
            </div>
        `);
    });
}

function openModal() {
    $("#new-wallet").modal("show");
}

function closeModal() {
    $("#new-wallet").modal("hide");
}