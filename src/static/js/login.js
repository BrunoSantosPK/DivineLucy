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