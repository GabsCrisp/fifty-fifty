const form = document.getElementById("crear-evento");

// linea 4 y 5 hacen la misma cosa 
// form.addEventListener("submit",  (e) => { e.preventDefault(); })
if (form) {
    form.addEventListener("submit", function (e) {
        e.preventDefault(); // evita que la pagina recargue
        crearEvento();
    });
}

function crearEvento() {
    // Obtener nombre de evento
    const inputNombreEvento = document.getElementById("nombre_evento");
    // Diccionario que almacena info enviada
    const info_evento = {
        "nombre_evento": inputNombreEvento.value
    };
    fetch(
        "/eventos", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(info_evento)
    })
        .then((response) => response.json())
        .then((data) => {
            mostrarMensaje(data['status'], data['message'], data['redirect']);
        });
}

function crearParticipante(event, form) {
    event.preventDefault();

    const nombreParticipante = form.querySelector("input[name='participante']")
    const usuarioHidden = form.querySelector("input[name='tipoUsuario']")
    const idEvento = document.getElementById("id_evento").value
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


function irEvento(idEvento) {
    location.href = 'eventos/' + idEvento;
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

function eliminarParticipante(span){
    const participante = span.parentElement;
    const id = participante.getAttribute('data-id');
    participante.remove();
}