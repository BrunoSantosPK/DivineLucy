class LoginState {
    constructor() {}

    toRecover() {}

    toSubscribe() {}
}

function show(box) {
    const elements = document.getElementsByClassName("login-box");
    for(let i = 0; i < elements.length; i++) {
        elements[i].classList.add("hide");
        if(elements[i].id == box) {
            elements[i].classList.remove("hide");
        }
    }
}

async function subscribe() {
    const email = document.getElementById("email-subscribe").value;
    const name = document.getElementById("name-subscribe").value;
    const password = document.getElementById("password-subscribe").value;
    const repeat_password = document.getElementById("password-subscribe2").value;

    try {
        if(email == "" | password == "" || repeat_password == "" | name == "") {
            throw new Error("Por favor, preencha os campos para cadastro.");
        }
        if(password != repeat_password) {
            throw new Error("As senhas não são iguais.");
        }

        const body = { email, password, repeat_password, name };
        const req = await fetch("/user", {method: "POST", body: JSON.stringify(body)});
        const res = await req.json();
        if(res.status_code != 200) {
            throw new Error(res.message);
        }

        alert("Parabéns, você está cadastrado! Já pode efetuar o login para utilizar o sistema.");
    } catch(error) {
        alert(error.message);
   }
}

async function login() {
    try {
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        if(email == "" | password == "") {
            throw new Error("Preencha seu e-email e senha para entrar.");
        }

        const body = {email, password};
        const req = await fetch("/login", {method: "POST", body: JSON.stringify(body)});
        const res = await req.json();
        console.log(res);
        if(res.status_code != 200) {
            throw new Error(res.message);
        }

        window.location.href = "/";
    } catch(error) {
        alert(error.message);
    }
}

async function recover() {
    try {
        const email = document.getElementById("email-recover").value;
        if(email == "") {
            throw new Error("Informe um e-mail para continuar.");
        }

        const body = {email};
        const req = await fetch("/recover", {method: "POST", body: JSON.stringify(body)});
        const res = await req.json();
        if(res.status_code != 200) {
            throw new Error(res.message);
        }

        console.log(res);
    } catch(error) {
        alert(error.message);
    }
}