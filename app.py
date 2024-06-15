from flask import Flask, render_template, request # type: ignore
# Configure application
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


@app.route("/tmp")
def temporal():
    return render_template("tmp.html")

@app.route("/sineventos")
def sineventos():
    return render_template("sineventos.html")

@app.route("/usuario")
def usuario():
    return render_template("usuario.html")


