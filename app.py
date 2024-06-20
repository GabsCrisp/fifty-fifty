from flask import Flask, render_template, request, redirect, jsonify, session
from flask_session import Session
from helpers import login_required, session_activate
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

from services import get_detalle_evento

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
#Configuracion de la sesión
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
        usuario = db.execute("SELECT * FROM usuarios WHERE usuario = ? OR email = ?", (acceso, acceso)).fetchone()
        if usuario:
            if check_password_hash(usuario[3], password):
                # Contraseña correcta, usuario encontrado
                session["username"] = usuario[1]
                session["id"] = usuario[0]
                response = {"status": "success", "redirect": "/eventos"}
            else:
                # Usuario encontrado, pero contraseña incorrecta
                response = {"status": "error", "message": "Contraseña incorrecta", "redirect": "/login"}
        else:
            # Usuario no encontrado
            response = {"status": "error", "message": "Usuario no encontrado", "redirect": "/login"}
        
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
        #respuesta es el diccionario que el frontend devuelve al backend al llamar a fetch
        respuesta = request.get_json()
        username = respuesta['username']
        email = respuesta['email']

        usuarios = db.execute("SELECT * FROM usuarios").fetchall()
        for usuario in usuarios:
            if usuario[1] == username or usuario[2]== email:
                # response es un diccionario que se le manda al frontend indicando que si hubo
                # errores o si todo el proceso es exitoso
                response = {"status": "error", "redirect": "/register"}
                return jsonify(response)
            
        hash = generate_password_hash(respuesta['password'])
        db.execute("INSERT INTO usuarios(usuario, email, hash) VALUES(?,?,?)", (username,email, hash))
        conn.commit()
        user_id = db.execute("SELECT * FROM usuarios WHERE usuario = ?", (username,)).fetchone()
        response = {"status":"success", "redirect": "/eventos"}
        #TODO: hashear contra, devolver respuesta al front, devolvemos estado y a donde va a redireccionar
        # creamos la sesión y almacena el nombre de usuario de la persona
        user_id = db.execute("SELECT id FROM usuarios WHERE usuario =?",(username,)).fetchone()[0]
        session["username"] = username
        session["id"] = user_id
        return jsonify(response)


@app.route("/tmp")
def temporal():
    return render_template("tmp.html")

@app.route("/eventos", methods=["GET", "POST"])
@login_required
def eventos():
    if request.method =="GET":
        rows = db.execute("SELECT nombre_evento FROM eventos WHERE id_usuario = ?", (session["id"],)).fetchall()
        return render_template("eventos.html", rows= rows)
    else:
        respuesta = request.get_json()
        nombre_evento= respuesta['nombre_evento']
        db.execute("INSERT INTO eventos (nombre_evento, id_usuario) values (?,?)", (nombre_evento,session["id"]))
        conn.commit()
        response = {"status": "success", "redirect": "/eventos", "message": "¡Evento registrado!"}
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
        usuario = db.execute("SELECT * FROM usuarios WHERE id = ?", (session["id"],)).fetchone()

        if (check_password_hash(usuario[3], password_actual)):
            response = {"status": "success", "redirect": "/usuario", "message": "Cambio de contraseña exitoso"}
            db.execute("UPDATE usuarios SET hash= ? WHERE id = ?", (generate_password_hash(password_nueva), session["id"]))
            conn.commit()
        else:
            response = {"status": "error", "redirect": "/usuario", "message": "La contraseña actual es incorrecta"}

        return jsonify(response)
        

@app.route("/eventos/<idEvento>", methods=["GET", "POST"])
@login_required
def detalle_evento(idEvento):
    return get_detalle_evento(idEvento, request)
