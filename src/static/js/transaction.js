class RecordState {
    constructor() {
        this.userID = null;
        this.recordID = null;
        this.recordData = [];
        this.walletData = [];
        this.itemData = [];
        this.formDetais = [];

        this.resTransactions = {
            status_code: 200,
            message: "",
            data: []
        };
        this.resWallets = {
            status_code: 200,
            message: "",
            data: [{
                id: "lambari1",
                name: "Nuconta"
            }, {
                id: "lambari2",
                name: "Caixa"
            }, {
                id: "lambari3",
                name: "PicPay"
            }]
        };
        this.resItems = {
            status_code: 200,
            message: "",
            data: [{
                id: "lambari1",
                name: "Supermercado"
            }, {
                id: "lambari2",
                name: "Lazer"
            }, {
                id: "lambari3",
                name: "Investimento"
            }, {
                id: "lambari4",
                name: "Casa"
            }]
        }
    }

    async render() {
        // Recupera informação do usuário
        const cookies = document.cookie.split(";");
        for(let i = 0; i < cookies.length; i++) {
            let [key, value] = cookies[i].split("=");
            if(key.trim() == "user_id") {
                this.userID = value;
                break
            }
        }

        // Atualiza dados
        await this.renderListRecords();
        await this.getWallets();
        await this.getItems();

        // Renderiza inputs
        $("#transaction-target-wallet").html("");
        $("#transaction-origin-wallet").html("");
        this.walletData.forEach(item => {
            $("#transaction-target-wallet").append(`<option value="${item.id}">${item.name}</option>`);
            $("#transaction-origin-wallet").append(`<option value="${item.id}">${item.name}</option>`);
        });

        $("#transaction-tag").html("");
        this.itemData.forEach(item => {
            $("#transaction-tag").append(`
                <option value="${item.id}">${item.name}</option>
            `);
        });
    }

    async getWallets() {
        try {
            const req = await fetch(`/wallets/${this.userID}`, {method: "GET"});
            const res = await req.json();
            if(res.status_code != 200) {
                throw new Error(res.message);
            }
            this.walletData = res.data;
        } catch(error) {
            console.log(error.message);
        }
    }

    async getItems() {
        try {
            const req = await fetch(`/item/${this.userID}`, {method: "GET"});
            const res = await req.json();
            if(res.status_code != 200) {
                throw new Error(res.message);
            }
            this.itemData = res.data;
        } catch(error) {
            console.log(error.message);
        }
    }

    async renderListRecords() {
        try {
            // Acessa a API
            const req = await fetch(`/record/${this.userID}`, {method: "GET"});
            const res = await req.json();
            if(res.status_code != 200) {
                throw new Error(res.message);
            }
            this.recordData = res.data;

            // Modifica a DOM
            $("#transaction-area").html("");
            const currency = new Intl.NumberFormat("pt-br", {style: "currency", currency: "BRL"});
            this.recordData.forEach(item => {
                $("#transaction-area").append(`
                    <div class="transaction-row">
                        <div class="col-2">
                            <p>${this.formatDate(item.moviment_date)}</p>
                        </div>
                        <div class="col-6">
                            <p>${item.description}</p>
                        </div>
                        <div class="col-2">
                            <p>${currency.format(item.value)}</p>
                        </div>
                        <div class="col-2">
                            <div class="buttons">
                                <span class="material-symbols-outlined" onclick="editTransaction('${item.id}')">edit</span>
                                <span class="material-symbols-outlined" onclick="deleteTransaction('${item.id}')">delete</span>
                            </div>
                        </div>
                    </div>
                `);
            });
        } catch(error) {
            console.log(error.message);
        }
    }

    async save() {
        try {
            // Recupera dados de acesso
            const item_id = document.getElementById("transaction-tag").value;
            const target_id = document.getElementById("transaction-target-wallet").value;
            const moviment_date = document.getElementById("transaction-date").value;
            const description = document.getElementById("transaction-description").value;
            const value = parseFloat(document.getElementById("transaction-value").value);

            // Verifica inserções
            if(item_id == "" || target_id == "" || moviment_date == "" || description.length < 5 || isNaN(value)) {
                throw new Error("Todos os campos obrigatórios devem estar preenchidos.");
            }

            // Trabalha com campos opcionais
            let origin_id = document.getElementById("transaction-origin-wallet").value;
            const details = [];
            if(origin_id == "") {
                origin_id = null;
            }
            for(let i = 0; i < this.details.length; i++) {
                // Verifica se algum campo está vazio e atualiza registro enviado
                let id = this.details[i];
                let detail_description = document.getElementById(`description-${id}`).value;
                let detail_value = parseFloat(document.getElementById(`value-${id}`).value);
                if(detail_description == "" || isNaN(detail_value)) {
                    throw new Error("Os detalhes não podem estar em branco.");
                }
                details.push({description: detail_description, value: detail_value});
            }

            // Envia requisição
            const body = {user_id: this.userID, record_id: this.recordID, item_id, target_id, moviment_date, description, value, details, origin_id};
            const method = this.recordID ? "PUT" : "POST";
            const req = await fetch("/record", {method: method, body: JSON.stringify(body)});
            const res = await req.json();
            if(res.status_code != 200) {
                throw new Error(res.message);
            }

            // Feedback de sucesso
            alert("Registro salvo com sucesso!");
            this.renderListRecords();
            this.closeModal();
        } catch(error) {
            alert(error.message);
        }
    }

    async delete(id) {
        try {
            const next = confirm("Deseja realmente remover o registro?");
            if(next) {
                const body = {record_id: id, user_id: this.userID};
                const req = await fetch("/record", {method: "DELETE", body: JSON.stringify(body)});
                const res = await req.json();
                if(res.status_code != 200) {
                    throw new Error(res.message);
                }

                alert("Registro removido com sucesso.");
                this.renderListRecords();
            }
        } catch(error) {
            alert(error.message);
        }
    }

    openModalCreate() {
        document.getElementById("modal-title").textContent = "Nova Movimentação";
        document.getElementById("transaction-date").value = "";
        document.getElementById("transaction-description").value = "";
        document.getElementById("transaction-value").value = "";
        document.getElementById("transaction-target-wallet").value = "";
        document.getElementById("transaction-origin-wallet").value = "";
        document.getElementById("transaction-tag").value = "";
        document.getElementById("is-transfer").value = "0";
        $("#transaction-details-area").html("");
        this.details = [];
        this.recordID == null;
        this.showTransferWallet();
        this.openModal();
    }

    modalEdit() {}

    openModal() {
        $("#transaction-form").modal("show");
    }

    closeModal() {
        $("#transaction-form").modal("hide");
    }

    formatDate(date) {
        const split = date.split("-");
        return `${split[2]}/${split[1]}/${split[0]}`;
    }

    showTransferWallet() {
        const show = parseInt(document.getElementById("is-transfer").value);
        const select = document.getElementById("transaction-origin-wallet");
        if(show == 1) {
            select.classList.remove("hide");
        } else {
            select.classList.add("hide");
        }
    }

    createRowDetails() {
        const id = this.createID();
        let defaultValue = "", defaultDescription = "";
        if(arguments.length == 2) {
            defaultDescription = arguments[0];
            defaultValue = arguments[1];
        }
        $("#transaction-details-area").append(`
            <div class="modal-form-details" id="${id}">
                <input value="${defaultDescription}" placeholder="Descrição" id="description-${id}">
                <input type="number" value="${defaultValue}" placeholder="Valor (R$)" id="value-${id}">
                <span class="material-symbols-outlined" onclick="deleteItemDetais('${id}')">delete</span>
            </div>
        `);
        this.details.push(id);
    }

    removeRowDetails(id) {
        const div = document.getElementById("transaction-details-area");
        div.childNodes.forEach(child => {
            if(child.id == id) {
                div.removeChild(child);
            }
        });
    }

    openModalEdit(id) {
        const item = this.recordData.find(e => e.id == id);
        this.recordID = id;
        document.getElementById("modal-title").textContent = "Editar Movimentação";
        document.getElementById("transaction-date").value = item.moviment_date;
        document.getElementById("transaction-value").value = item.value;
        document.getElementById("transaction-description").value = item.description;
        document.getElementById("transaction-target-wallet").value = item.target_wallet;
        document.getElementById("transaction-origin-wallet").value = item.origin_wallet ?? "";
        document.getElementById("transaction-tag").value = item.item_id;
        document.getElementById("is-transfer").value = item.origin_wallet ? "1" : "0";

        $("#transaction-details-area").html("");
        this.details = [];
        item.details.forEach(detail => {
            this.createRowDetails(detail.description, detail.value);
        });

        this.showTransferWallet();
        this.openModal()
    }

    createID() {
        const time = (new Date()).getTime();
        const random = parseInt(Math.random() * 1001);
        return time + random
    }
}