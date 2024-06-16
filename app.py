from flask import Flask, render_template, request, redirect, jsonify
from werkzeug.security import generate_password_hash
import sqlite3

conn = sqlite3.connect("fiftyfifty.db", check_same_thread=False)
db = conn.cursor()
# Configure application.
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
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
        print(hash)
        db.execute("INSERT INTO usuarios(usuario, email, hash) VALUES(?,?,?)", (username,email, hash))
        conn.commit()
        response = {"status":"success", "redirect": "/sineventos"}
        #TODO: hashear contra, devolver respuesta al front, devolvemos estado y a donde va a redireccionar
        return jsonify(response)


@app.route("/tmp")
def temporal():
    return render_template("tmp.html")

@app.route("/sineventos")
def sineventos():
    return render_template("sineventos.html")

@app.route("/usuario")
def usuario():
    return render_template("usuario.html")


