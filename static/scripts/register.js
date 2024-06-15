let input = document.querySelectorAll('.input');
let boton = document.getElementById('registro');
let form = document.getElementById('form');
let contador = 0;
form.addEventListener("submit", function(e){
    e.preventDefault();
})

let ids = {}

boton.disabled = true;
for (let i = 0; i < input.length; i++)
{
    input[i].addEventListener("input", habilitacion_boton);
    ids[input[i].id] = 0;
}

function habilitacion_boton(e)
{
    contador = 0;
    if (e.target.value.length > 1)
    {
        ids[e.target.id] = e.target.value.length;
    }

    for (let key in ids)
    {
        if (ids[key] > 0)
        {
            contador += 1;
        }

    }
    console.log(contador);
}