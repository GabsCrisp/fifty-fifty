const remove = document.getElementsByClassName("remove");
const idEvento = document.getElementById("id_evento").value;
const button_invitado = document.getElementById("button_invitado");
const invited = document.getElementById("invited");
const participants = document.getElementById("participants");
const productos = document.getElementById("id_producto");


productos.addEventListener("input", () => {
    const dataList = document.getElementById("list_product");
    dataList.innerHTML = ""
    body_producto = { "nombre_producto": productos.value };
    if (productos.value.length === 0) {
        return
    }

    fetch(
        `/${idEvento}/producto`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body_producto)
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            data.forEach(item => {
                const option = document.createElement("option");
                option.value = item[0];
                dataList.appendChild(option)
            })

        });

})

for (let i = 0; i < remove.length; i++) {
    remove[i].addEventListener("click", removeParticipants)
}

function crearParticipante(event, form) {
    event.preventDefault();

    const nombreParticipante = form.querySelector("input[name='participante']")
    const usuarioHidden = form.querySelector("input[name='tipoUsuario']")
    const info_usuario = {
        "participante": nombreParticipante.value,
        "tipoUsuario": usuarioHidden.value
    };
    fetch(
        "/eventos/" + idEvento, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(info_usuario)
    })
        .then((response) => response.json())
        .then((data) => {
            mostrarMensaje(data['status'], data['message'], data['redirect']);
        });

}

function mostrarMensaje(status, message, redirect) {
    if (status == 'success') {
        Swal.fire({
            title: message,
            text: "",
            icon: "success",
        })
            .then(function () {

                window.location = redirect;
            })
    }
    else {
        Swal.fire({
            title: "Occurió un error",
            text: message,
            icon: "error",
        })
            .then(function () {

                window.location = redirect;
            })
    }
}

function removeParticipants() {
    //parentNode permite saber el padre de un hijo en html
    //children nos retorna un arreglo de todos los hijos del padre
    const children = this.parentNode.children;
    const username = children[0].innerHTML;
    const id_participante_evento = children[1].innerHTML;

    info_borrada = { "idEvento": idEvento, "username": username, "id_participante_evento": id_participante_evento }
    fetch(
        "/remover_participantes", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(info_borrada)
    })
        .then((response) => response.json())
        .then((data) => {
            mostrarMensaje(data['status'], data['message'], data['redirect']);
        });

}