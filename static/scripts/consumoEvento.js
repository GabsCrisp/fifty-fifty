const idEvento = document.getElementById("id_evento").value;
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
const cantidad_individual = document.getElementsByClassName("cantidad_individual")
const id_cantidad = document.getElementById("id_cantidad");

agregar_consumo.disabled = true;
agregar_producto.disabled = true;
let encontrado_db = false;
id_cantidad.addEventListener("input", () => {
    const nuevoValor = id_cantidad.value;
    if (nuevoValor == "") {
        for (let i = 0; i < participantes.length; i++) {
            participantes[i].disabled = true
            participantes[i].checked = false
        }

    }
    else {
        for (let i = 0; i < participantes.length; i++) {
            participantes[i].disabled = false
        }
    }

    if (nuevoValor == 1) {
        const cantidad_individual_array = Array.from(cantidad_individual);

        // Iteramos sobre el array y eliminamos los elementos
        cantidad_individual_array.forEach(element => {
            element.remove();
        });

    
    } else {
        for (let i = 0; i < participantes.length;i++){
            habilitar_input_cantidad_base(participantes[i])
        }
    }



    for (let i = 0; i < cantidad_individual.length; i++) {
        cantidad_individual[i].value = "";
    }
})
for (let i = 0; i < participantes.length; i++) {

    participantes[i].addEventListener("change", habilitar_input_cantidad);
}

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

//habilita el boton correcto dependiendo de los inputs que tengamos
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
    limitar_cantidad_individual(id_cantidad.value)
    //habilitar_input_cantidad()

}
//se encarga de limitar el tamaño maximo de los inputs numericos de los checkbox
function limitar_cantidad_individual(valor) {
    for (let i = 0; i < cantidad_individual.length; i++) {
        cantidad_individual[i].setAttribute("max", valor);
    }
}
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
//crea dinamicamente cada uno de tus inputs numericos
function habilitar_input_cantidad(e) {
   habilitar_input_cantidad_base(e.target);
}
function habilitar_input_cantidad_base(input_afectado) {

    let input;
    //habilita los inputs
    if (id_cantidad.value > 1) {
        if (input_afectado.checked) {
            // Verifica si ya existe un input con la clase "cantidad_individual" en el contenedor padre
            const existingInput = input_afectado.parentNode.querySelector(".cantidad_individual");
            if (!existingInput) {
                // Crea dinámicamente cada uno de los inputs
                input = document.createElement("input");
                input.type = "number";
                input.name = "cantidad_individual";
                input.setAttribute("form", "id_form_consumo");
                input.classList.add("cantidad_individual");
                // Agrega el elemento al div
                input_afectado.parentNode.appendChild(input);
                input.setAttribute("min", 1);
                input.setAttribute("max", id_cantidad.value);
            }
        } else if (!input_afectado.checked) {
            input_afectado.parentNode.querySelector(".cantidad_individual").remove();
        }
    } else {
        const cantidad_individual = document.getElementsByClassName("cantidad_individual");
        for (let i = 0; i < cantidad_individual.length; i++) {
            cantidad_individual[i].value = "";
        }
    }
}

function validateForm() {
    let confirmation = false;
    let totalCantIndividual = 0
    for (let i = 0; i < cantidad_individual.length; i++) {
        totalCantIndividual += parseInt(cantidad_individual[i].value);
    }

    console.log(id_cantidad.value, totalCantIndividual);
    if( id_cantidad.value != totalCantIndividual && id_cantidad.value>1 ){
        Swal.fire({
            title: "Occurió un error",
            text: "Cantidad de cada participante no coincide con cantidad total",
            icon: "error",
        });
        return false;
    }
    else{
        return true;
    }
     
}