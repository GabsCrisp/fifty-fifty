

function descargarContenido(){
    domtoimage.toJpeg(document.querySelector('main'), { quality: 0.95 })
    .then(function (dataUrl) {
        var link = document.createElement('a');
        link.download = `factura-${document.getElementById("titulo_nombre_evento").innerHTML}.jpeg`;
        link.href = dataUrl;
        link.click();
    });
}