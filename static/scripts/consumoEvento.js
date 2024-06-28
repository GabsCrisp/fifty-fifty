const idEvento = document.getElementById("id_evento").value;
const button_invitado = document.getElementById("button_invitado");
const invited = document.getElementById("invited");
const productos = document.getElementById("id_producto");
const inputPrecio = document.getElementById("id_precio");
const dataList = document.getElementById("list_product")
const inputs = document.getElementsByClassName("input");
const inp = document.getElementsByClassName("inp");
const agregar_consumo = document.getElementById("agregar_consumo");
const agregar_producto = document.getElementById("agregar_producto");
const participantes = document.getElementsByClassName("participantes");
const precio = document.getElementById("precio");
const form = document.getElementById("id_form_consumo");
const opcion_de_agregado = document.getElementById("opcion_de_agregado");
const botones_enviados = document.getElementsByClassName("botones_enviados");

for (let i = 0; i < botones_enviados.length; i++) {
    botones_enviados[i].addEventListener("click", (e) => {
        opcion_de_agregado.value = e.target.innerHTML
    })
}


//el precio no se estaba enviando correctamente
//enviamos precio en un input hidden
form.addEventListener("submit", (e) => {
    precio.value = inputPrecio.value;
})

//va contando cuantos checkbox han sido chequeado
function compartido_por() {
    let compartido = 0;
    compartido = 0;
    for (let i = 0; i < participantes.length; i++) {
        if (participantes[i].checked) {
            compartido++
        }

    }
    return compartido;
}

agregar_consumo.disabled = true;
agregar_producto.disabled = true;
let encontrado_db = false;

for (let i = 0; i < inputs.length; i++) {
    inputs[i].addEventListener("input", verificacion_inputs)
}


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
            data.forEach(item => {
                const option = document.createElement("option");
                option.value = item[0];
                option.dataset.price = item[1];
                dataList.appendChild(option);
            })
            const options = dataList.children;
            let matchFound = false;
            for (let i = 0; i < options.length; i++) {
                if (options[i].value === productos.value) {
                    inputPrecio.value = options[i].dataset.price;
                    encontrado_db = true;
                    matchFound = true;
                    verificacion_inputs();
                    break;
                }
                else {
                    console.log(productos.value);
                    encontrado_db = false;
                    verificacion_inputs()
                }
            }
            if (!matchFound) {
                inputPrecio.value = "";
            }
            inputPrecio.disabled = matchFound;

        });

})




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

function verificacion_inputs() {
    agregar_consumo.disabled = true
    agregar_producto.disabled = true
    let compartido = compartido_por();
    let contador = 0;
    for (let i = 0; i < inp.length; i++) {
        if (inp[i].value.length > 0) {
            contador++;
        }
    }
    console.log(encontrado_db);
    //para que se habilite el boton de consumo deben estar rellenados los cuatros inputs
    //debe haberse encontrado el producto en la db y debe haber por lo menos un checkbox chequeado
    if (contador == inp.length && encontrado_db && compartido > 0) {

        agregar_consumo.disabled = false;
    }
    else if (contador == inp.length && compartido > 0) {
        agregar_producto.disabled = false;
    }

}