let inputs = document.getElementsByClassName("input");
let password_actual = document.getElementById("password_actual");
let password_nueva = document.getElementById("password_nueva")
let password_confirm = document.getElementById("password_confirm");
let boton_cambiarcontrasena = document.getElementById("contrasena");
let form = document.getElementById("form");


//Diccionario que va a almacenar toda la informacion que se va a enviar al backend
let info_contrasena = {};

//validacion password
const regex_password = /^(?=.*[!@#$%^&*(),.?":{}|<>])(?=.{9,})/;

password_nueva.addEventListener("input", chequeo_password)

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
    if (contador == inputs.length && chequeo_password()) {

        boton_cambiarcontrasena.disabled = false;
    }
    else {
        boton_cambiarcontrasena.disabled = true;
    }
}

boton_cambiarcontrasena.addEventListener("click", confirmacion);

function confirmacion() {

    if (password_nueva.value == password_confirm.value) 
        {
            if (password_actual.value == password_confirm.value)
                {
                    Swal.fire({
                        title: "¡Su nueva contraseña no puede ser igual a la actual!",
                        text: "",
                        icon: "error",
                    });
                    return;   
                }
        //fetch
        info_contrasena["password_actual"] = password_actual.value;
        info_contrasena["password_nueva"] = password_nueva.value;
        info_contrasena["password_confirm"] = password_confirm.value;
        for (let i = 0; i < inputs.length; i++) {
            console.log("a");
            inputs[i].value = ""
        }
        fetch("/usuario", {
            method: 'POST',
            headers: {
                // indica que los datos a enviar serán en formato json
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(info_contrasena)
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

                }
                else {
                    Swal.fire({
                        title: data['message'],
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
let h6 = document.createElement("h6")
h6.id = "chequeo_password"
function chequeo_password() 
{

    if(!regex_password.test(password_nueva.value))
        {
            let mensaje = "La contraseña debe tener por lo menos 8 caracteres y un símbolo"
            h6.innerText = mensaje;
            password_nueva.parentNode.insertBefore(h6, password_nueva.nextSibling)
            return false
        }
        else 
        {
            h6.remove()
            return true
        }
}