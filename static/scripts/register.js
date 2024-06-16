let inputs = document.getElementsByClassName("input");
let registro = document.getElementById("registro");
let form = document.getElementById("form");
let password = document.getElementById("password");
let confirmpassword = document.getElementById("confirmpassword");
let email = document.getElementById("email");
let info = {};
//previene no recargar el formulario
form.addEventListener("submit", function(e){
    e.preventDefault();
})
registro.addEventListener("click", confirmacion);

for (let i = 0; i < inputs.length; i++) {
    inputs[i].addEventListener("input", chequeo_input);
}

// Funcion chequeo_input: Revisa si cada uno de los inputs tiene valores y habilita o desahabilita el boton

let deshabilitado = true;
let contador = 0;
function chequeo_input() {
    contador = 0;
    for (let i = 0; i < inputs.length; i++) {
        //contador se aumenta cada que escribimos en los inputs
        if (inputs[i].value.length > 0) {
            contador++;
        }

    }
    if (contador == inputs.length) {

        registro.disabled = false;
    }
    else {
        registro.disabled = true;
    }
}
function confirmacion() {
    if(!(email.value.includes("@")))
        {
            Swal.fire({
                title: "El formato del correo no es válido",
                text: "",
                icon: "error",
              });
              return;
        }
    if (password.value == confirmpassword.value)
        {
            Swal.fire({
                title: "¡Registro exitoso!",
                text: "",
                icon: "success",
              });
              
              return;
              //fetch
              //verificar nombre de usuarios e email en la db
              //hashear contra
              //insertar
        }
    else
    {
        Swal.fire({
            title: "¡Contraseñas no coinciden!",
            text: "",
            icon: "error"
          });
          return;
    }
}