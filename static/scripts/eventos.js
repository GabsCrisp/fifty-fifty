const form = document.getElementById("crear-evento");
// linea 4 y 5 hacen la misma cosa 
// form.addEventListener("submit",  (e) => { e.preventDefault(); })
if (form) {
    form.addEventListener("submit", function (e) {
        e.preventDefault(); // evita que la pagina recargue
        crearEvento();
    });
}

// funciones
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


function irEvento(idEvento, estado) {
    if (estado == "FINALIZADO") {
        location.href = idEvento + '/cuenta_final';
    } else {
        location.href = 'eventos/' + idEvento;
    }
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