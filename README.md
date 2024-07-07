# FIFTY FIFTY
#### Video Demo: 
#### Description:
Bienvenidos a Fifty/Fifty, la solución perfecta para dividir cuentas entre amigos, familiares y compañeros de trabajo. Nuestra página web permite ingresar a las personas y sus consumos, y en segundos obtienes una división justa y precisa. Olvídate de las discusiones y los cálculos complicados con nuestra plataforma rápida, intuitiva y accesible desde cualquier dispositivo. Perfecta para cenas, viajes o cualquier evento compartido. ¡Prueba Fifty/Fifty y disfruta de la armonía en cada encuentro!

#### Estructura del archivo

- Carpeta static/scripts: 
Contiene todos los achivos javascript que se usan para comunicarse con el backend de manera asincrónica así como validaciones de formularios en tiempo real. Adicionalmente tiene una librería que permite descargar imágenes a partir de html.
    - login.js: 
    Se encarga de permitir que el usuario pueda iniciar sesión a través de su cuenta previamente creada. Para esto se utilizan variables que nos permiten hacer que el usuario pueda almacenar su información. Al código se le brinda una función que nos permite activar o desactivar el botón de “submit” dependiendo si los valores ingresados por el usuario son aquellos que consideramos válidos (como por ejemplo su dirección de correo electrónico; esta función recibe el nombre de chequeo_input()).
    - register.js: 
    Es el encargado de la creación de una cuenta para aquellos nuevos usuarios. Este a su vez requiere de algunos datos básicos para la creación de una nueva cuenta como lo son: el correo electrónico, Nombre de usuario o apodo, contraseña creada por el usuario.
    Una vez el usuario creó una contraseña y esta a su vez haya sido confirmada, el código también solicita un nombre de usuario correo al cual vincular la cuenta; y es redireccionada a un archivo, Json.
    - usuarios.js:
    Permite manipular la información de nuestras cuentas ya creadas, la función de “cambiar mi contraseña” es realizada por este código. A través de un botón de “cambiar_contraseña”, el usuario puede solicitar al programa un cambio de su contraseña; los input proporcionados por el mismo siempre son verificados si coinciden con los formatos que se requieren. También una vez que el usuario decide confirmar que esta será su nueva contraseña se le pide una confirmación, si la contraseña propuesta y la confirmación no coinciden entonces no se realiza el cambio. 

- Carpeta static/fonts:
Contiene las fuentes de text que se utilizan en el proyecto.

- Archivos CSS dentro de static:
Contiene los estilos que ayudan a la responsividad del sistema así como colores, bordes, sombreados, espaciado, etc.

- Carpeta templates:
Contiene todo lo que el usuario va a ver, ayudado por las hojas de estilo y scripts.
    - consumo_evento.html:
    Es el ciclo más importante de la aplicación donde el usuario podrá insertar qué consume cada participante.
    - cuenta_final.html:
    Muesta el consumo agrupado por cada participante en formato de tabla. Asimismo, presenta un botón que permite descargarlo en imagen.
    - eventos.html:
    se encarga de establecer la apariencia de la página de creación de nuevos eventos, con todas las características que este necesita. Y mostrar todos datos que son importantes acerca del evento, como sus miembros o creador.
    - index.html:
    Contiene la información de qué es el proyecto y las personas que lo constuyeron
    - layout.html:
    Es el html base para las plantillas
    - login:
    Se encarga de establecer la apariencia de la página de creación de nuevos eventos, con todas las características que este necesita. Y mostrar todos datos que son importantes acerca del evento, como sus miembros o creador.
    - participantes.html
    Sección donde el usuario puede agregar participantes ya sea registrados o no que participarán en el evento creado
    - register.html:
    Contiene pantalla donde se crea el usuario en el sistema
    - usuario.html:
    Sección que permite al usuario cambiar contraseña

- Archivo .env: archivo donde se guardan las variables de entorno del proyecto

- Archivo .gitignore: lista de archivos/ carpetas que no se suben al repositorio git

- Archvio app.py:
Es el cerebro de la aplicación en donde se procesan todas las solicitudes del cliente. Permite a los usuarios registrarse, iniciar sesión, crear y gestionar eventos, añadir participantes, registrar consumos, y calcular una división justa de los gastos al finalizar un evento. Cada evento puede incluir múltiples participantes y cada consumo registrado se puede dividir entre ellos, incluyendo cálculos de impuestos y propinas.

- Archivo cambio_base_datos.sql:
Cuando el proyecto iba en un 60% notamos una necesidad de cambiar el diseño de la base de datos, por lo que respaldó en este archivo la consulta sql

- Base de datos fiftyfifty.db:
Utilizando SQLite creamos una base de datos para almacenar datos de usuarios, eventos, participantes y consumos.

- Archivo helpers.py:
En este archivo se declaran decoradores que facilitan el manejo de usuarios en la aplicación

- Archivo requirements.txt:
Contiene la lista de las dependencias del proyecto

- Archivo services.py:
Contiene dos funcionalidades importantes "agregar participante" y "remover participante"  que por complejidad en su momento se decidió trabajar en una archivo separado del app.py.