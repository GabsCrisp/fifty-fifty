const idEvento = document.getElementById("id_evento").value;
const button_invitado = document.getElementById("button_invitado");
const invited = document.getElementById("invited");
const productos = document.getElementById("id_producto");
const inputPrecio = document.getElementById("id_precio");
const dataList = document.getElementById("list_product")

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
            console.log(data)
            data.forEach(item => {
                const option = document.createElement("option");
                option.value = item[0];
                option.dataset.price = item[1];
                dataList.appendChild(option);
            })

        });

})

productos.addEventListener("change", () => {
    const options = dataList.options;
    let matchFound = false;
    for (let i = 0; i < options.length; i++) {
        if (options[i].value === productos.value) {
            inputPrecio.value = options[i].dataset.price;
            matchFound = true;
            break;
        }
    }
    if (!matchFound) {
        inputPrecio.value = "";
    }
    inputPrecio.disabled = matchFound;
});


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
