from flask import Flask, render_template
# Configure application
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/tmp")
def temporal():
    return render_template("tmp.html")

@app.route("/sineventos")
def sineventos():
    return render_template("sineventos.html")


