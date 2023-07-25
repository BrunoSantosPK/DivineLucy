class TransactionState {
    constructor() {
        this.resTransactions = {
            status_code: 200,
            message: "",
            data: [{
                id: "transaction1",
                date: "2023-07-25",
                description: "Transferência para investimento",
                value: 100000,
                targetWallet: "lambari1",
                originWallet: "lambari2",
                classificationTag: "lambari3",
                details: [{
                    id: "lambari1",
                    text: "Investimento A",
                    value: 50000
                }, {
                    id: "lambari2",
                    text: "Investimento B",
                    value: 20000
                }, {
                    id: "lambari3",
                    text: "Investimento C",
                    value: 30000
                }]
            }, {
                id: "transaction2",
                date: "2023-07-24",
                description: "Supermercado",
                value: 132.69,
                targetWallet: "lambari2",
                originWallet: null,
                classificationTag: "lambari1",
                details: [{
                    id: "lambari1",
                    text: "Produto A",
                    value: 100
                }, {
                    id: "lambari2",
                    text: "Produto B",
                    value: 32.69
                }]
            
            }, {
                id: "transaction3",
                date: "2023-07-20",
                description: "Compra colchão",
                value: 599.90,
                targetWallet: "lambari3",
                originWallet: null,
                classificationTag: "lambari4",
                details: []
            }]
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

    getTransactions() {
        return this.resTransactions.data;
    }
    
    getWallets() {
        return this.resWallets.data;
    }

    getClassificationItems() {
        return this.resItems.data;
    }

    getTransaction(id) {
        return this.resTransactions.data.find(e => e.id == id);
    }

    formatDate(date) {
        const split = date.split("-");
        return `${split[2]}/${split[1]}/${split[0]}`;
    }
}

const state = new TransactionState();

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

function renderOptionsModal() {
    $("#transaction-target-wallet").html("");
    state.getWallets().forEach(item => {
        $("#transaction-target-wallet").append(`
            <option value="${item.id}">${item.name}</option>
        `);
    });

    $("#transaction-origin-wallet").html("");
    state.getWallets().forEach(item => {
        $("#transaction-origin-wallet").append(`
            <option value="${item.id}">${item.name}</option>
        `);
    });

    $("#transaction-tag").html("");
    state.getClassificationItems().forEach(item => {
        $("#transaction-tag").append(`
            <option value="${item.id}">${item.name}</option>
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

function newTransaction() {
    document.getElementById("modal-title").textContent = "Nova Movimentação";
    document.getElementById("transaction-date").value = null;
    document.getElementById("transactin-description").value = "";
    document.getElementById("transaction-target-wallet").value = null;
    document.getElementById("transaction-origin-wallet").value = null;
    document.getElementById("transaction-tag").value = null;
    $("#transaction-details-area").html("");
    
    openModal();
}

function openModal() {
    $("#transaction-form").modal("show");
}

function closeModal() {
    $("#transaction-form").modal("hide");
}