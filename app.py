from flask import Flask, render_template, request, redirect, jsonify, session, flash
from flask_session import Session
from helpers import login_required, session_activate, evento_finalizado
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

from services import get_detalle_evento, get_remover_participantes

conn = sqlite3.connect("fiftyfifty.db", check_same_thread=False)
db = conn.cursor()
# Configuración de la aplicación.
app = Flask(__name__)


@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.cache_control.no_cache = True
    response.cache_control.must_revalidate = True
    response.cache_control.max_age = 0
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


# Configuracion de la sesión
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
@session_activate
def index():
    session.clear()
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
@session_activate
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # respuesta es el diccionario que el frontend devuelve al backend al llamar a fetch
        respuesta = request.get_json()
        acceso = respuesta['acceso']
        password = respuesta['password']

        # Buscar usuario por nombre de usuario o email
        usuario = db.execute(
            "SELECT * FROM usuarios WHERE usuario = ? OR email = ?", (acceso, acceso)).fetchone()
        if usuario:
            if check_password_hash(usuario[3], password):
                # Contraseña correcta, usuario encontrado
                session["username"] = usuario[1]
                session["id"] = usuario[0]
                response = {"status": "success", "redirect": "/eventos"}
            else:
                # Usuario encontrado, pero contraseña incorrecta
                response = {
                    "status": "error", "message": "Contraseña incorrecta", "redirect": "/login"}
        else:
            # Usuario no encontrado
            response = {"status": "error",
                        "message": "Usuario no encontrado", "redirect": "/login"}

        return jsonify(response)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
@session_activate
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        # respuesta es el diccionario que el frontend devuelve al backend al llamar a fetch
        respuesta = request.get_json()
        username = respuesta['username']
        email = respuesta['email']

        usuarios = db.execute("SELECT * FROM usuarios").fetchall()
        for usuario in usuarios:
            if usuario[1] == username or usuario[2] == email:
                # response es un diccionario que se le manda al frontend indicando que si hubo
                # errores o si todo el proceso es exitoso
                response = {"status": "error", "redirect": "/register"}
                return jsonify(response)

        hash = generate_password_hash(respuesta['password'])
        db.execute("INSERT INTO usuarios(usuario, email, hash) VALUES(?,?,?)",
                   (username, email, hash))
        conn.commit()
        user_id = db.execute(
            "SELECT * FROM usuarios WHERE usuario = ?", (username,)).fetchone()
        response = {"status": "success", "redirect": "/eventos"}
        # TODO: hashear contra, devolver respuesta al front, devolvemos estado y a donde va a redireccionar
        # creamos la sesión y almacena el nombre de usuario de la persona
        user_id = db.execute(
            "SELECT id FROM usuarios WHERE usuario =?", (username,)).fetchone()[0]
        session["username"] = username
        session["id"] = user_id
        return jsonify(response)


@app.route("/eventos/<idEvento>/consumo_evento")
@login_required
@evento_finalizado
def consumo_evento(idEvento):
    rows = db.execute(
        "SELECT * FROM participante_evento WHERE id_evento = ?", (idEvento,)
    ).fetchall()
    nombre_evento = db.execute(
        "SELECT nombre_evento FROM eventos WHERE id_evento = ?", (idEvento,)).fetchone()[0]
    lista_categoria = db.execute("SELECT * FROM categorias").fetchall()
    # obtenemos el la suma del total del consumo por cada participante del evento
    consumo_cadaparticipante = db.execute("""SELECT round(sum(subtotal_participante),2),nombre_participante from participante_evento JOIN consumo_cadaparticipante on
                participante_evento.id_participante_evento = consumo_cadaparticipante.id_participante
                where participante_evento.id_evento = ? group by participante_evento.id_participante_evento""", (idEvento,)).fetchall()

    print(consumo_cadaparticipante)
    id_consumo = db.execute(
        "select id_consumo, id_participante from consumo_cadaparticipante where id_evento = ?", (idEvento,)).fetchall()
    consumo = {}
    for i in id_consumo:
        # si ya hay consumo existente agrega el id del consumidor
        if (i[0] in consumo):
            consumidores.append(i[1])
            consumo[i[0]] = consumidores
        # si no crea una lista vacia y agrega el primer consumidor
        else:
            consumidores = []
            consumidores.append(i[1])
            consumo[i[0]] = consumidores

    consumo_general = db.execute(
        """select * from consumo_general join productos on consumo_general.id_producto = productos.id_producto where consumo_general.id_evento = ?""", (idEvento,)).fetchall()
    consumo_final = []
    for i in consumo_general:
        consumo_info = {}
        for j in consumo:
            if (i[0] == j):
                # crea una lista de ? que se pondran dentro del IN
                ids_str = ','.join('?'for _ in consumo[j])
                # agarramos nombre participante que participaron en el consumo
                participantes = db.execute(
                    "SELECT nombre_participante, id_participante_evento from participante_evento where id_evento = ?", (idEvento,)).fetchall()
                p = {}
                for participante in participantes:
                    for id_consumidor in consumo[j]:
                        if (id_consumidor == participante[1]):
                            p[id_consumidor] = participante[0]
                # diccionario que almacena producto y nombre participantes que comparten este producto
                consumo_info["consumidores"] = p
                consumo_info["producto"] = i[8]
                consumo_info["precio"] = i[9]
                consumo_info["cantidad"] = i[2]
                consumo_info["precio_total"] = i[4]
                consumo_final.append(consumo_info)

    # print(consumo_final)
    return render_template("consumo_evento.html", rows=rows, id_evento=idEvento, nombre_evento=nombre_evento, lista_categoria=lista_categoria, consumo_cadaparticipante=consumo_cadaparticipante, consumo_final=consumo_final)


@app.route("/eventos", methods=["GET", "POST"])
@login_required
def eventos():
    if request.method == "GET":
        if(session.get('evento')):
            session.pop('evento')
        rows = db.execute(
            """
            SELECT 
                e.nombre_evento, 
                e.id_evento, 
                e.estado, 
                u.usuario 
            FROM 
                eventos e
            INNER JOIN 
                usuarios u ON u.id = e.id_usuario
            LEFT JOIN 
                participante_evento pe ON pe.id_evento = e.id_evento AND pe.id_usuario = ?
            WHERE 
                e.id_usuario = ? OR pe.id_usuario IS NOT NULL
            ORDER BY e.f_creacion DESC

            """, (session["id"],session["id"])).fetchall()
        return render_template("eventos.html", rows=rows)
    else:
        respuesta = request.get_json()
        nombre_evento = respuesta['nombre_evento']
        db.execute("INSERT INTO eventos (nombre_evento, id_usuario) values (?,?)",
                   (nombre_evento, session["id"]))
        conn.commit()
        response = {"status": "success", "redirect": "/eventos",
                    "message": "¡Evento registrado!"}
        #insertamos por defecto al usuario creador del evento
        idEvento= db.lastrowid
        print(session)
        db.execute("INSERT INTO participante_evento(id_evento,nombre_participante,id_usuario) values(?,?,?)", (idEvento, session['username'], session['id']))
        return jsonify(response)


@app.route("/participantes")
@login_required
def participantes():
    return render_template("participantes.html")


@app.route("/usuario", methods=["GET", "POST"])
@login_required
def usuario():
    if request.method == "GET":
        return render_template("usuario.html")
    else:
        # respuesta es el diccionario que el frontend devuelve al backend al llamar a fetch
        respuesta = request.get_json()
        password_actual = respuesta['password_actual']
        password_nueva = respuesta['password_nueva']

        # Buscar usuario por
        usuario = db.execute(
            "SELECT * FROM usuarios WHERE id = ?", (session["id"],)).fetchone()

        if (check_password_hash(usuario[3], password_actual)):
            response = {"status": "success", "redirect": "/usuario",
                        "message": "Cambio de contraseña exitoso"}
            db.execute("UPDATE usuarios SET hash= ? WHERE id = ?",
                       (generate_password_hash(password_nueva), session["id"]))
            conn.commit()
        else:
            response = {"status": "error", "redirect": "/usuario",
                        "message": "La contraseña actual es incorrecta"}

        return jsonify(response)


@app.route("/eventos/<idEvento>", methods=["GET", "POST"])
@login_required
def detalle_evento(idEvento):
    return get_detalle_evento(db, idEvento, request, conn, session)


@app.route("/remover_participantes", methods=["POST"])
@login_required
def remover_participantes():
    return get_remover_participantes(db, request, conn, redirect)


@app.route("/buscar_user", methods=["POST"])
@login_required
def buscar_user():
    user = request.get_json()
    u = db.execute("SELECT usuario from usuarios WHERE usuario LIKE ? LIMIT 6",
                   (user["username"] + "%",)).fetchall()
    usuarios = []
    for user in u:
        usuarios.append(user[0])
    return jsonify(usuarios)


@app.route("/<idEvento>/producto", methods=["POST"])
@login_required
def buscar_producto(idEvento):
    body = request.get_json()
    producto = db.execute("SELECT nombre_producto, precio_producto from productos WHERE id_evento = ? AND nombre_producto LIKE ?",
                          (idEvento, "%" + body["nombre_producto"] + "%")).fetchall()
    return jsonify(producto)


@app.route("/<idEvento>/crear_consumo", methods=["POST"])
@login_required
def crear_consumo(idEvento):
    categoria = request.form.get("categoria")
    id_producto = request.form.get("id_producto")
    id_precio = request.form.get("precio")
    id_cantidad = request.form.get("id_cantidad")
    participantes = request.form.getlist("participantes")
    cantidad_individual = request.form.getlist("cantidad_individual")
    productodb = db.execute(
        "SELECT id_producto,nombre_producto,precio_producto FROM productos WHERE id_evento = ? AND nombre_producto = ?", (idEvento, id_producto)).fetchone()
    if not productodb:
        # insertar
        db.execute(" INSERT INTO productos (id_categoria, nombre_producto, precio_producto,id_evento) values(?,?,?,?)",
                   (categoria, id_producto, id_precio, idEvento))
        conn.commit()
        productodb = db.execute(
            "SELECT id_producto,nombre_producto,precio_producto FROM productos WHERE id_evento = ? AND nombre_producto = ?", (idEvento, id_producto)).fetchone()
    # subtotal = int(id_precio) * int(id_cantidad) / len(participantes)
    # obtener el subtotal por participante
    # bucle para insertar consumo
    total_consumo = float(id_precio) * float(id_cantidad)
    db.execute("INSERT INTO consumo_general (id_producto, cantidad_consumida, precio_uniproducto, total_consumo, id_evento) values(?,?,?,?, ?)",
               (productodb[0], id_cantidad, productodb[2], total_consumo, idEvento))
    conn.commit()
    id_consumo = db.lastrowid
    # insertamos consumo por cada participantes
    print(participantes)
    for index, item in enumerate(participantes):
        print(item)
        if (len(cantidad_individual) == 0):
            subtotal_participante = float(productodb[2])/len(participantes)
            db.execute("INSERT INTO consumo_cadaparticipante(id_consumo, id_participante, cantidad_individual, subtotal_participante, id_evento) VALUES(?, ?, ?, ?, ?)",
                       (id_consumo, item, 1, subtotal_participante, idEvento))
            conn.commit()
        else:
            subtotal_participante = float(
                productodb[2])*float(cantidad_individual[index])
            db.execute("INSERT INTO consumo_cadaparticipante(id_consumo, id_participante, cantidad_individual, subtotal_participante, id_evento) VALUES(?, ?, ?, ?, ?)",
                       (id_consumo, item, float(cantidad_individual[index]), subtotal_participante, idEvento))
            conn.commit()
    return redirect('/eventos/' + idEvento + '/consumo_evento')


@app.route("/<idEvento>/finalizar", methods=["POST"])
@login_required
def finalizar_evento(idEvento):
    impuesto = float(request.form.get("impuesto"))/100
    propina = float(request.form.get("propina"))/100

    db.execute(
        "UPDATE consumo_cadaparticipante SET propina = subtotal_participante * ?, impuesto = subtotal_participante * ? WHERE id_evento = ?",(propina,impuesto,idEvento)
    )
    db.execute(
        "UPDATE eventos SET estado = 'FINALIZADO' WHERE id_evento = ?", (idEvento,))
    conn.commit()
    session['evento'] = 'FINALIZADO'
    print(session)
    return redirect('/' + idEvento + '/cuenta_final')


@app.route("/<idEvento>/cuenta_final")
@login_required
def cuenta_final(idEvento):
    print(session)
    nombre_evento = db.execute(
        "SELECT nombre_evento FROM eventos WHERE id_evento = ?", (idEvento,)).fetchone()[0]
    rows = db.execute(
        "SELECT id_participante_evento, nombre_participante FROM participante_evento WHERE id_evento = ?", (idEvento,)).fetchall()

    data = []

    for row in rows:
        to_add = {
            "id_participante_evento": row[0], "nombre_participante": row[1]}
        consumo_rows = db.execute("""
        SELECT p.nombre_producto, ccg.precio_uniproducto, SUM(ccp.cantidad_individual), SUM(ccp.subtotal_participante), SUM(ccp.propina), Sum(ccp.impuesto) FROM consumo_cadaparticipante ccp 
              INNER JOIN consumo_general ccg ON ccg.id_consumo = ccp.id_consumo
            INNER JOIN productos p ON ccg.id_producto = p.id_producto
            WHERE ccp.id_evento = ? AND ccp.id_participante = ?            
                                  GROUP BY p.nombre_producto, ccg.precio_uniproducto 

        """, (idEvento, row[0])).fetchall()
        to_add["consumos"] = consumo_rows
        subtotal_participante = 0.0
        total_propina = 0.0
        total_impuesto = 0.0
        for record in consumo_rows:
            subtotal_participante = subtotal_participante + float(record[3])
            total_propina = total_propina + float(record[4])
            total_impuesto = total_impuesto + float(record[5])

        to_add["subtotal"] = subtotal_participante
        to_add["total_propina"] = total_propina
        to_add["total_impuesto"] = total_impuesto
        to_add["total"] = subtotal_participante + total_impuesto + total_propina
        data.append(to_add)

    return render_template("cuenta_final.html", data=data, nombre_evento=nombre_evento)
