let inputs = document.getElementsByClassName("input");
let acceso = document.getElementById("acceso");
let password = document.getElementById("password")
let iniciosesion = document.getElementById("iniciosesion");
let form = document.getElementById("form");

//Diccionario que va a almacenar toda la informacion que se va a enviar al backend
let info_login = {};

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

        iniciosesion.disabled = false;
    }
    else {
        iniciosesion.disabled = true;
    }
}

iniciosesion.addEventListener("click", confirmacion);

function confirmacion() {
    
    // fetch de la información
    info_login["acceso"] = acceso.value;
    info_login["password"] = password.value;
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].value = ""
    }
    fetch("/login", {
        method: 'POST',
        headers: {
            // indica que los datos a enviar serán en formato json
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(info_login)
    })
    .then((response) => response.json())
    .then((data) => {

        if(data['status'] == 'success')
            {
                Swal.fire({
                    title: "¡Inicio de sesión exitoso!",
                    text: "",
                    icon: "success",
                })
                .then(function() {

                    window.location =data['redirect'];
                })

            }
            else 
            {
                Swal.fire({
                    title: "Usuario o contraseña no existen",
                    text: "",
                    icon: "error",
                })
                .then(function() {

                    window.location =data['redirect'];
                })
            }
        
    })
    return;
}