let inputs = document.getElementsByClassName("input");

for (let i = 0; i < inputs.length; i++) {
    inputs[i].addEventListener("input", chequeo_input);
}
let habilitar = false;
//revisa si cada uno de los inputs tiene valores y habilita o deshabilta el boton
function chequeo_input()
{
    for (let i = 0; i < inputs.length; i++) {
        if(inputs[i].value < 1)
            {
                habilitar = false;
            }
            else 
            {
                habilitar = true;
            }
    }
    console.log(habilitar);
}