const form = document.getElementById("crear-evento");

// linea 4 y 5 hacen la misma cosa 
// form.addEventListener("submit",  (e) => { e.preventDefault(); })
form.addEventListener("submit", function (e) {
    e.preventDefault();
    crearEvento();
});

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
            if (data['status'] == 'success') {
                Swal.fire({
                    title: data['message'],
                    text: "",
                    icon: "success",
                })
                    .then(function () {

                        window.location = data['redirect'];
                    })
                //sessionStorage.setItem('loggedIn', 'true')

            }
            else {
                Swal.fire({
                    title: "toy dormida",
                    text: "",
                    icon: "error",
                })
                    .then(function () {

                        window.location = data['redirect'];
                    })
            }
        })


}

