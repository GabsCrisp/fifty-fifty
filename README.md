# FIFTY FIFTY
#### Video Demo: 
#### Description:
Bienvenidos a Fifty/Fifty, la solución perfecta para dividir cuentas entre amigos, familiares y compañeros de trabajo. Nuestra página web permite ingresar a las personas y sus consumos, y en segundos obtienes una división justa y precisa. Olvídate de las discusiones y los cálculos complicados con nuestra plataforma rápida, intuitiva y accesible desde cualquier dispositivo. Perfecta para cenas, viajes o cualquier evento compartido. ¡Prueba Fifty/Fifty y disfruta de la armonía en cada encuentro!

#### Estructura del archivo

- Carpeta static/scripts: 
Contiene todos los achivos javascript que se usan para comunicarse con el backend de manera asincrónica así como validaciones de formularios en tiempo real. Adicionalmente tiene una librería que permite descargar imágenes a partir de html.

- Carpeta static/fonts:
Contiene las fuentes de text que se utilizan en el proyecto.

- Archivos CSS dentro de static:
Contiene los estilos que ayudan a la responsividad del sistema así como colores, bordes, sombreados, espaciado, etc.

- Carpeta templates:
Contiene todo lo que el usuario va a ver, ayudado por las hojas de estilo y scripts.
    - consumo_evento.html
    Es el ciclo más importante de la aplicación donde el usuario podrá insertar qué consume cada participante.
    - cuenta_final.html
    Muesta el consumo agrupado por cada participante en formato de tabla. Asimismo, presenta un botón que permite descargarlo en imagen.
    - eventos.html
    Lista los eventos que el usuario ha creado y los que ha participado. También el usuario puede crear un evento.
    - index.html
    Contiene la información de qué es el proyecto y las personas que lo constuyeron
    - layout.html
    Es el html base para las plantillas
    - login
    Contiene la pantalla de inicio de sesión
    - participantes.html
    Sección donde el usuario puede agregar participantes ya sea registrados o no que participarán en el evento creado
    - register.html:
    Contiene pantalla donde se crea el usuario en el sistema
    - usuario.html:
    Sección que permite al usuario cambiar contraseña

- Archivo .env: archivo donde se guardan las variables de entorno del proyecto

- Archivo .gitignore: lista de archivos/ carpetas que no se suben al repositorio git

- app.py:
Es el cerebro de la aplicación en donde se procesan todas las solicitudes del cliente. Permite a los usuarios registrarse, iniciar sesión, crear y gestionar eventos, añadir participantes, registrar consumos, y calcular una división justa de los gastos al finalizar un evento. Cada evento puede incluir múltiples participantes y cada consumo registrado se puede dividir entre ellos, incluyendo cálculos de impuestos y propinas.

