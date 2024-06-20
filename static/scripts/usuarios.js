let inputs = document.getElementsByClassName("input");
let password_actual = document.getElementById("password_actual");
let password_nueva = document.getElementById("password_nueva")
let password_confirm = document.getElementById("password_confirm");
let boton_cambiarcontrasena = document.getElementById("contrasena");
let form = document.getElementById("form");


//Diccionario que va a almacenar toda la informacion que se va a enviar al backend
let info_contrasena = {};

//previene no recargar el formulario
form.addEventListener("submit", function (e) {
    e.preventDefault();
})

for (let i = 0; i < inputs.length; i++) {
    inputs[i].addEventListener("input", chequeo_input);
}

// Funcion chequeo_input: Revisa si cada uno de los inputs tiene valores y habilita o desahabilita el boton

function chequeo_input() {
    let contador = 0;
    for (let i = 0; i < inputs.length; i++) {
        //contador se aumenta cada que escribimos en los inputs
        if (inputs[i].value.length > 0) {
            contador++;
        }

    }
    if (contador == inputs.length) {

        boton_cambiarcontrasena.disabled = false;
    }
    else {
        boton_cambiarcontrasena.disabled = true;
    }
}

iniciosesion.addEventListener("click", confirmacion);

function confirmacion() {

    if (password_nueva.value == password_confirm.value) {
        //fetch
        info_contrasena["password_actual"] = password_actual.value;
        info_contrasena["password_nueva"] = password_nueva.value;
        info_contrasena["password_confirm"] = password_confirm.value;

        for (let i = 0; i < inputs.length; i++) {
            inputs[i].value = ""
        }
        fetch("/register", {
            method: 'POST',
            headers: {
                // indica que los datos a enviar serán en formato json
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(info)
        })
            .then((response) => response.json())
            .then((data) => {

                if (data['status'] == 'success') {
                    Swal.fire({
                        title: "¡Cambio de contraseña exitoso!",
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
                        title: "La contraseña actual ingresada no es válida",
                        text: "",
                        icon: "error",
                    })
                        .then(function () {

                            window.location = data['redirect'];
                        })
                }

            })
        return;
    }
    else {
        Swal.fire({
            title: "¡Contraseñas nuevas no coinciden!",
            text: "",
            icon: "error"
        });
        return;
    }
}