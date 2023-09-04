async function recover() {
    try {
        const password = document.getElementById("password").value;
        const repeat_password = document.getElementById("password-repeat").value;
        const recover_id = document.getElementById("recover-page").getAttribute("recover-id");

        if(repeat_password == "" | password == "") {
            throw new Error("Preencha o campo de senha para redefinir.");
        }

        if(repeat_password != password) {
            throw new Error("As senhas não são iguais.");
        }

        const body = {password, repeat_password, recover_id};
        const req = await fetch("/recover", {method: "PUT", body: JSON.stringify(body)});
        const res = await req.json();

        if(req.status != 200) {
            throw new Error(res.message);
        }

        alert("Sua senha foi redefinida, você já pode acessar o sistema com a nova senha!")
    } catch(error) {
        alert(error.message);
    }
}