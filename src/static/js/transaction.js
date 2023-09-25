class RecordState {
    constructor() {
        this.userID = null;
        this.recordData = [];
        this.walletData = [];
        this.itemData = [];

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
            const req = await fetch(`/record/${this.userID}`, {method: "GET"});
            const res = await req.json();
            if(res.status_code != 200) {
                throw new Error(res.message);
            }

            this.recordData = res.data;
        } catch(error) {
            console.log(error.message);
        }
    }

    async create() {
        try {
            // Recupera dados de acesso
            const item_id = document.getElementById("transaction-tag").value;

            // Envia requisição
            const body = {user_id: this.userID, item_id, target_id, moviment_date, description, value, details, origin_id};

            required_fields = [("user_id", str), ("item_id", str), ("target_id", str), ("moviment_date", str), ("description", str), ("value", float)]
            optional_fields = [("details", list, []), ("origin_id", str, None)]

            // Feedback de sucesso
            this.closeModal();
        } catch(error) {
            alert(error.message);
        }
    }

    selectAction() {
        this.modalCreate();
    }

    modalCreate() {
        document.getElementById("modal-title").textContent = "Nova Movimentação";
        document.getElementById("transaction-date").value = null;
        document.getElementById("transactin-description").value = "";
        document.getElementById("transaction-target-wallet").value = null;
        document.getElementById("transaction-origin-wallet").value = null;
        document.getElementById("transaction-tag").value = null;
        $("#transaction-details-area").html("");
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
}



function renderTransactions() {
    $("#transaction-area").html("");
    const currency = new Intl.NumberFormat("pt-br", {style: "currency", currency: "BRL"});

    state.getTransactions().forEach(item => {
        $("#transaction-area").append(`
            <div class="transaction-row">
                <div class="col-2">
                    <p>${state.formatDate(item.date)}</p>
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
}

function editTransaction(id) {
    const transaction = state.getTransaction(id);
    document.getElementById("modal-title").textContent = "Editar Movimentação";
    document.getElementById("transaction-date").value = transaction.date;
    document.getElementById("transactin-description").value = transaction.description;
    document.getElementById("transaction-target-wallet").value = transaction.targetWallet;
    document.getElementById("transaction-origin-wallet").value = transaction.originWallet;
    document.getElementById("transaction-tag").value = transaction.classificationTag;

    $("#transaction-details-area").html("");
    transaction.details.forEach(item => {
        $("#transaction-details-area").append(`
            <div class="modal-form-details" id="${item.id}">
                <input value="${item.text}">
                <input type="number" value="${item.value}">
                <span class="material-symbols-outlined" onclick="deleteItemDetais('${item.id}')">delete</span>
            </div>
        `);
    });

    openModal();
}

function deleteTransaction(id) {
    console.log(`Deletando a movimentação ${id}`);
}

function showTransferWallet() {
    const show = parseInt(document.getElementById("is-transfer").value);
    const select = document.getElementById("transaction-origin-wallet");
    if(show == 1) {
        select.classList.remove("hide");
    } else {
        select.classList.add("hide");
    }
}

function addItemDetails() {
    const id = (new Date()).getTime()
    $("#transaction-details-area").append(`
        <div class="modal-form-details" id="${id}">
            <input value="">
            <input type="number" value="">
            <span class="material-symbols-outlined" onclick="deleteItemDetais('${id}')">delete</span>
        </div>
    `);
}

function deleteItemDetais(id) {
    const element = document.getElementById(id);
    const parent = document.getElementById("transaction-details-area");
    parent.removeChild(element);
}