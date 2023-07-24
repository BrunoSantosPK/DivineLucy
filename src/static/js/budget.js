function loadOptions() {
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

function renderBudgets() {
    // Recupera mês e ano
    const month = parseInt(document.getElementById("budget-month").value);
    const year = parseInt(document.getElementById("budget-year").value);

    if(month == 0 || year == 0) {
        $("#budget-area").html("");
        console.log("Mês e ano devem estar selecionadas para renderizar.");
        return;
    }

    // Estrutura de dados para render
    const demoResponse = {
        status_code: 200,
        message: "",
        data: [{
            item: "Supermercado", budget: 400, real: 439.38, id: "lambari1"
        }, {
            item: "Tecnologia", budget: 150, real: 199.99, id: "lambari2"
        }, {
            item: "Saúde", budget: 100, real: 63.8, id: "lambari3"
        }, {
            item: "Emergência", budget: 100, real: 448.96, id: "lambari4"
        }, {
            item: "Lazer", budget: 100, real: 29.9, id: "lambari5"
        }]
    };

    // Remove dados antigos e preenche os novos
    $("#budget-area").html("");
    const currency = new Intl.NumberFormat("pt-br", {style: "currency", currency: "BRL"});
    demoResponse.data.forEach(item => {
        $("#budget-area").append(`
            <div class="budget-row">
                <div class="col-4">
                    <h5>${item.item}</h5>
                </div>
                <div class="col-3">
                    <h5>${currency.format(item.budget)}</h5>
                </div>
                <div class="col-3">
                    <h5 class="${item.real > item.budget ? "warning": ""}">${currency.format(item.real)}</h5>
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

function openModal() {
    // Estrutura de dados para render
    const demoResponse = {
        status_code: 200,
        message: "",
        data: [{
            id: "item1", name: "Supermercado"
        },{
            id: "item2", name: "Tecnologia"
        }, {
            id: "item3", name: "Saúde"
        }, {
            id: "item4", name: "Emergência"
        }, {
            id: "item5", name: "Lazer"
        }]
    };
    const select = document.getElementById("budget-items");
    while(select.hasChildNodes()) { select.removeChild(select.firstChild); }
    demoResponse.data.forEach(item => {
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