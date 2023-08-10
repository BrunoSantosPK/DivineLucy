class BudgetState {
    constructor(userID) {
        this.userID = userID;
        this.resBudget = {status_code: 400, message: "", data: []};
        this.resItems = {status_code: 400, message: "", data: []};
    }

    getUserID() {
        return this.userID;
    }

    getBudgets() {
        return this.resBudget.data;
    }

    getItems() {
        return this.resItems.data;
    }

    async updateBudgets(month, year) {
        try {
            const req = await fetch(`/budget/${this.userID}?month=${month}&year=${year}`, {method: "GET"});
            const res = await req.json();
            if(res.status_code != 200) {
                throw Error(res.message);
            }
            this.resBudget = res;
        } catch(error) {
            alert(error.message);
        }
    }

    async updateItems() {
        try {
            const req = await fetch(`/item/${this.userID}`, {method: "GET"});
            const res = await req.json();
            if(res.status_code != 200) {
                throw Error(res.message);
            }
            this.resItems = res;
        } catch(error) {
            alert(error.message);
        }
    }
}

const userID = "49fe6c42-b940-4122-906b-e95c7316e349";
const budgetState = new BudgetState(userID);

async function loadOptions() {
    // Carrega itens
    await budgetState.updateItems();

    // Os meses são sempre fixos
    const mData = [
        { number: 0, name: "Selecione o mês" },
        { number: 1, name: "Janeiro" },
        { number: 2, name: "Fevereiro" },
        { number: 3, name: "Março" },
        { number: 4, name: "Abril" },
        { number: 5, name: "Maio" },
        { number: 6, name: "Junho" },
        { number: 7, name: "Julho" },
        { number: 8, name: "Agosto" },
        { number: 9, name: "Setembro" },
        { number: 10, name: "Outubro" },
        { number: 11, name: "Novembro" },
        { number: 12, name: "Dezembro" },
    ]

    // Os anos disponíveis são desde 2023 até 10 anos após o ano atual
    const mYear = [{number: 0, name: "Selecione o ano"}];
    const start = 2023, finish = (new Date()).getFullYear() + 10;
    for(let i = start; i <= finish; i++) {
        mYear.push({number: i, name: i});
    }

    // Limpa dados anteriores
    const month = document.getElementById("budget-month");
    const year = document.getElementById("budget-year");
    while(month.hasChildNodes()) { month.removeChild(month.firstChild); }
    while(year.hasChildNodes()) { year.removeChild(year.firstChild); }

    // Preenche informações
    mData.forEach(item => {
        let opt = document.createElement("option");
        opt.value = item.number;
        opt.textContent = item.name;
        month.appendChild(opt);
    });

    mYear.forEach(item => {
        let opt = document.createElement("option");
        opt.value = item.number;
        opt.textContent = item.name;
        year.appendChild(opt);
    });
}

async function renderBudgets() {
    // Recupera mês e ano
    const month = parseInt(document.getElementById("budget-month").value);
    const year = parseInt(document.getElementById("budget-year").value);

    if(month == 0 || year == 0) {
        $("#budget-area").html("");
        console.log("Mês e ano devem estar selecionadas para renderizar.");
        return;
    }

    // Atualiza dados de metas
    await budgetState.updateBudgets(month, year);
    const items = budgetState.getItems();

    // Remove dados antigos e preenche os novos
    $("#budget-area").html("");
    const currency = new Intl.NumberFormat("pt-br", {style: "currency", currency: "BRL"});
    budgetState.getBudgets().forEach(item => {
        $("#budget-area").append(`
            <div class="budget-row">
                <div class="col-4">
                    <h5>${items.find(e => e.id == item.item_id).name}</h5>
                </div>
                <div class="col-3">
                    <h5>${currency.format(item.value)}</h5>
                </div>
                <div class="col-3">
                    <h5 class="${item.real > item.value ? "warning": ""}">${currency.format(item.real)}</h5>
                </div>
                <div class="col-2">
                    <div class="actions">
                        <span class="material-symbols-outlined" onclick="editBudget('${item.id}')">edit</span>
                        <span class="material-symbols-outlined" onclick="deleteBudget('${item.id}')">delete</span>
                    </div>
                </div>
            </div>
        `);
    });
}

async function saveBudget() {
    try {
        // Recupera dados e valida seleções
        const month = parseInt(document.getElementById("budget-month").value);
        const year = parseInt(document.getElementById("budget-year").value);
        let itemID = document.getElementById("budget-items").value;
        const itemName = document.getElementById("new-item").value;
        const value = parseFloat(document.getElementById("budget-value").value);

        if(itemID == "" && itemName.length < 5) {
            throw new Error("Para cadastrar um novo item, informe um nome com ao menos 5 caracteres.");
        }
        if(isNaN(value) || value <= 0) {
            throw new Error("Informe um valor positivo para a meta.");
        }
        if(month == 0 || year == 0) {
            throw new Error("Selecione mês e ano para cadastrar a meta.");
        }

        // Cadatras um novo item, caso necessário
        if(itemID == "") {
            let req = await fetch("/item", {
                method: "POST",
                body: JSON.stringify({user_id: budgetState.getUserID(), name: itemName})
            });
            let res = await req.json();
            if(res.status_code != 200) {
                throw Error(res.message);
            }
            itemID = res.data.item_id;

            // Atualiza registro de itens interno
            await budgetState.updateItems();
        }

        // Cadastra a meta
        const body = {user_id: budgetState.getUserID(), year, month, item_id: itemID, value};
        req = await fetch("/budget", {method: "POST", body: JSON.stringify(body)});
        res = await req.json();
        if(res.status_code != 200) {
            throw Error(res.message);
        }

        // Exibe feedback e chama o render
        alert("Meta cadastrada com sucesso.");
        renderBudgets();
        closeModal();

    } catch(error) {
        alert(error.message);
    }
}

function deleteBudget(id) {
    console.log("Apagando meta " + id);
}

function editBudget(id) {
    console.log("Editando meta " + id);
    document.getElementById("modal-title").textContent = "Editar meta";
    openModal();
}

function newBudget() {
    document.getElementById("modal-title").textContent = "Nova Meta";
    openModal();
}

async function openModal() {
    // Estrutura de dados para render
    const select = document.getElementById("budget-items");
    while(select.hasChildNodes()) {
        select.removeChild(select.firstChild);
    }
    budgetState.getItems().forEach(item => {
        let opt = document.createElement("option");
        opt.value = item.id;
        opt.textContent = item.name;
        select.appendChild(opt);
    });
    $("#budget-items").append("<option value=''>Novo item</option>");
    newItem();

    $("#form-budget").modal("show");
}

function closeModal() {
    $("#form-budget").modal("hide");
}

function newItem() {
    const select = document.getElementById("budget-items").value;
    const input = document.getElementById("new-item");
    if(select == "") {
        input.value = "";
        input.classList.remove("hide");
    } else {
        input.classList.add("hide");
    }
}