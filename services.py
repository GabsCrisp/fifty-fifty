

from flask import jsonify, render_template


def get_detalle_evento(db, idEvento, request, conn):
    if request.method == "POST":
        respuesta_json = request.get_json()
        tipo_usuario = respuesta_json["tipoUsuario"]
        participante = respuesta_json["participante"]
        if tipo_usuario == "invitado":
            db.execute(
                "INSERT INTO participante_evento(id_evento,nombre_participante) values(?,?)", (idEvento, participante))
            conn.commit()
        else:
            respuesta = db.execute(
                "SELECT id, usuario FROM usuarios WHERE usuario = ? OR email = ?", (
                    participante, participante)
            ).fetchone()
            if not respuesta:
                response = {"status": "error", "redirect": "/eventos/" +
                            idEvento, "message": "Usuario no encontrado"}
                return jsonify(response)
            id_usuario = respuesta[0]
            nombre_usuario = respuesta[1]
            respuesta = db.execute(
                "SELECT id_usuario FROM participante_evento WHERE id_usuario = ? AND id_evento = ?", (
                    id_usuario, idEvento)
            ).fetchone()
            # Validar si el participante ya existe
            if respuesta:
                response = {"status": "error", "redirect": "/eventos/" +
                            idEvento, "message": "Participante ya ingresado"}
                return jsonify(response)
            db.execute(
                "INSERT INTO participante_evento(id_evento,nombre_participante,id_usuario) values(?,?,?)", (idEvento, nombre_usuario, id_usuario))
            conn.commit()

        response = {"status": "success", "redirect":  "/eventos/" +
                    idEvento, "message": "¡Participante registrado!"}
        return jsonify(response)

    rows = db.execute(
        "SELECT * FROM participante_evento WHERE id_evento = ?", (idEvento,)
    ).fetchall()

    return render_template("participantes.html", rows=rows, id_evento = idEvento)
