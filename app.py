from flask import Flask, render_template, request, redirect, jsonify, session
from flask_session import Session
from helpers import login_required, session_activate
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

conn = sqlite3.connect("fiftyfifty.db", check_same_thread=False)
db = conn.cursor()
# Configuración de la aplicación.
app = Flask(__name__)

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
        print (usuario)

        if usuario:
            if check_password_hash(usuario[3], password):
                # Contraseña correcta, usuario encontrado
                session["username"] = usuario[1]
                response = {"status": "success", "redirect": "/sineventos"}
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
        print(username)
        print(email)

        usuarios = db.execute("SELECT * FROM usuarios").fetchall()
        print(usuarios)
        for usuario in usuarios:
            if usuario[1] == username or usuario[2]== email:
                # response es un diccionario que se le manda al frontend indicando que si hubo
                # errores o si todo el proceso es exitoso
                response = {"status": "error", "redirect": "/register"}
                return jsonify(response)
            
        hash = generate_password_hash(respuesta['password'])
        db.execute("INSERT INTO usuarios(usuario, email, hash) VALUES(?,?,?)", (username,email, hash))
        conn.commit()
        response = {"status":"success", "redirect": "/sineventos"}
        #TODO: hashear contra, devolver respuesta al front, devolvemos estado y a donde va a redireccionar
        # creamos la sesión y almacena el nombre de usuario de la persona
        session["username"] = username
        return jsonify(response)


@app.route("/tmp")
def temporal():
    return render_template("tmp.html")

@app.route("/sineventos")
@login_required
def sineventos():
    return render_template("sineventos.html")

@app.route("/creacion_eventos")
@session_activate
def creacion_eventos():
    return render_template("creacion_eventos.html")

@app.route("/usuario")
def usuario():
    return render_template("usuario.html")
