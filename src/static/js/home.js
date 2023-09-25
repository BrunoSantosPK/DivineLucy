class HomeState {
    constructor() {
        this.userID = null;
        this.resWallets = {
            status_code: 400,
            message: "",
            data: []
        };
    }

    async updateWallets() {
        try {
            const req = await fetch(`/wallets/${this.userID}`, {method: "GET"});
            const res = await req.json();
            if(res.status_code != 200) {
                throw Error(res.message);
            }
            this.resWallets = res;
        } catch(error) {
            alert(error.message);
        }
    }

    getWallets() {
        return this.resWallets.data;
    }

    render() {
        // Recupera informação do usuário
        const cookies = document.cookie.split(";");
        for(let i = 0; i < cookies.length; i++) {
            let [key, value] = cookies[i].split("=");
            if(key.trim() == "user_id") {
                this.userID = value;
                break
            }
        }

        // Faz a carga inicial de carteiras existentes
        this.renderWallets();
    }

    async renderWallets() {
        // Atualiza informações via API
        await this.updateWallets();

        // Remove elementos existentes
        const parent = document.getElementById("wallet-area");
        while(parent.hasChildNodes()) {
            parent.removeChild(parent.firstChild);
        }

        // Estrutura o cartão para cada carteira
        const currency = new Intl.NumberFormat("pt-br", {style: "currency", currency: "BRL"});
        this.getWallets().forEach(item => {
            $("#wallet-area").append(`
                <div class="wallet-card">
                    <h4>${item.name}</h4>
                    <div class="wallet-row sep">
                        <span class="label">Saldo</span>
                        <span class="value">${currency.format(item.current_value)}</span>
                    </div>
                    <div class="wallet-row">
                        <span class="label">Entrada</span>
                        <span class="value">${currency.format(item.total_income)}</span>
                    </div>
                    <div class="wallet-row">
                        <span class="label">Saída</span>
                        <span class="value">${currency.format(item.total_outcome)}</span>
                    </div>
                </div>
            `);
        });
    }

    async createWallet() {
        try {
            // Recupera dados do formulário e valida entradas
            const name = document.getElementById("new-wallet-name").value;
            if(name.length < 5) {
                throw Error("Infome um nome para a carteira com ao menos 5 caracteres.");
            }
    
            // Envia requisição para o servidor
            const body = {name: name, user_id: this.userID};
            const req = await fetch("/wallets", {
                method: "POST",
                body: JSON.stringify(body)
            });
            const res = await req.json();
            
            if(res.status_code != 200) {
                throw Error(res.message);
            }
    
            // Envia feedback de sucesso
            alert("Nova carteira cadastrada com sucesso.");
            this.renderWallets();
            closeModal();
        } catch(error) {
            alert(error.message);
        }
    }
}

function openModal() {
    $("#new-wallet").modal("show");
}

function closeModal() {
    $("#new-wallet").modal("hide");
}