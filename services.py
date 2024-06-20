

from flask import render_template


def get_detalle_evento(db, idEvento, request,conn):
    if request.method =="POST":
        tipo_usuario = request.form.get("tipoUsuario")
        participante = request.form.get("participante")
        if tipo_usuario == "invitado":
            db.execute("INSERT INTO participantes_evento(id_evento,nombre_participante) values(?,?)",(idEvento,participante))
            conn.commit()
        print(request.form.get("tipoUsuario"))

    return render_template("participantes.html")