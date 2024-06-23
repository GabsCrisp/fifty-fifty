let inputs = document.getElementsByClassName("input");
let registro = document.getElementById("registro");
let form = document.getElementById("form");
let password = document.getElementById("password");
let confirmpassword = document.getElementById("confirmpassword");
let email = document.getElementById("email");

//validar email correctamente
const regex_email = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

//validacion password
const regex_password = /^(?=.*[!@#$%^&*(),.?":{}|<>])(?=.{9,})/;
//Diccionario que va a almacenar toda la informacion que se va a enviar al backend
let info = {};

let h6 = document.createElement("h6");
password.addEventListener("input", chequeo_password)

//previene no recargar el formulario
form.addEventListener("submit", function (e) {
    e.preventDefault();
})
registro.addEventListener("click", confirmacion);

for (let i = 0; i < inputs.length; i++) {
    inputs[i].addEventListener("input", chequeo_input);
}

// Funcion chequeo_input: Revisa si cada uno de los inputs tiene valores y habilita o desahabilita el boton
let contador = 0;
function chequeo_input() {
    contador = 0;
    for (let i = 0; i < inputs.length; i++) {
        //contador se aumenta cada que escribimos en los inputs
        if (inputs[i].value.length > 0) {
            contador++;
        }

    }
    if (contador == inputs.length && chequeo_password()) {

        registro.disabled = false;
    }
    else {
        registro.disabled = true;
    }
}
function confirmacion() {
    //regex permite validacion de inputs 
    //es una herramienta que ya es parte de js
    if (!regex_email.test(email.value)) {
        Swal.fire({
            title: "El formato del correo no es válido",
            text: "",
            icon: "error",
        });
        return;
    }
    if (password.value == confirmpassword.value) {
        //fetch
        info["username"] = document.getElementById("nombre_usuario").value;
        info["email"] = document.getElementById("email").value;
        info["password"] = password.value;
        info["confirmpassword"] = confirmpassword.value;
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

            if(data['status'] == 'success')
                {
                    Swal.fire({
                        title: "¡Registro exitoso!",
                        text: "",
                        icon: "success",
                    })
                    .then(function() {

                        window.location =data['redirect'];
                    })
                    //sessionStorage.setItem('loggedIn', 'true')

                }
                else 
                {
                    Swal.fire({
                        title: "Ya existe un usuario con ese nombre de usuario o email en la aplicacion",
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
    else {
        Swal.fire({
            title: "¡Contraseñas no coinciden!",
            text: "",
            icon: "error"
        });
        return;
    }
}

function chequeo_password() 
{
    if(!regex_password.test(password.value))
        {
            let mensaje = "La contraseña debe tener por lo menos 8 caracteres y un símbolo"
            h6.innerText = mensaje;
            password.parentNode.insertBefore(h6, password.nextSibling)
            return false
        }
        else 
        {
            h6.remove()
            return true
        }
}