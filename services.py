

from flask import jsonify, render_template


def get_detalle_evento(db, idEvento, request, conn):
    if request.method == "POST":
        tipo_usuario = request.form.get("tipoUsuario")
        participante = request.form.get("participante")
        if tipo_usuario == "invitado":
            db.execute(
                "INSERT INTO participantes_evento(id_evento,nombre_participante) values(?,?)", (idEvento, participante))
            conn.commit()
        else:
            respuesta = db.execute(
                "SELECT id FROM usuarios WHERE usuario = ? OR email = ?", (
                    participante, participante)
            ).fetchone()
            if not respuesta:
                response = {"status": "error", "redirect": "/eventos/" +
                            idEvento, "message": "Usuario no encontrado"}
                return jsonify(response)
            id_usuario = respuesta[0]
            respuesta = db.execute(
                "SELECT id_usuario FROM participantes_evento WHERE id_usuario = ? AND id_evento = ?", (
                    id_usuario, idEvento)
            ).fetchone()
            if respuesta:
                response = {"status": "error", "redirect": "/eventos/" +
                            idEvento, "message": "Participante ya ingresado"}
                return jsonify(response)
            db.execute(
                "INSERT INTO participantes_evento(id_evento,nombre_participante,id_usuario) values(?,?,?)", (idEvento, participante, id_usuario))
            conn.commit()

        response = {"status": "success", "redirect":  "/eventos/" +
                    idEvento, "message": "¡Participante registrado!"}
        return jsonify(response)

    rows = db.execute(
        "SELECT * FROM participantes_evento WHERE id_evento = ?", (idEvento,)
    ).fetchall()

    return render_template("participantes.html", rows=rows)
