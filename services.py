

from flask import jsonify, render_template


def get_detalle_evento(db, idEvento, request, conn, session):
    if request.method == "POST":
        respuesta_json = request.get_json()
        tipo_usuario = respuesta_json["tipoUsuario"]
        participante = respuesta_json["participante"]
        validacion_invitado = db.execute("SELECT nombre_participante FROM participante_evento WHERE nombre_participante = ? AND id_evento = ?",(participante,idEvento)).fetchone()
        validacion_invitado2 = db.execute("SELECT usuario FROM usuarios WHERE usuario = ?",(participante,)).fetchone()
        
        if tipo_usuario == "invitado":
            if validacion_invitado2:
                response = {"status": "error", "redirect": "/eventos/" +
                idEvento, "message": "Ya existe un invitado con este nombre"}
                return jsonify(response)

        if validacion_invitado:
            response = {"status": "error", "redirect": "/eventos/" +
            idEvento, "message": "El usuario ya participa en el evento"}
            return jsonify(response)
        
            
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
    #get
    rows = db.execute(
        "SELECT * FROM participante_evento WHERE id_evento = ?", (idEvento,)
    ).fetchall()
    nombre_evento = db.execute("SELECT nombre_evento FROM eventos WHERE id_evento = ?", (idEvento,)).fetchone()[0]
    return render_template("participantes.html", rows=rows, id_evento = idEvento, nombre_evento = nombre_evento)

def get_remover_participantes(db, request, conn, redirect):
    respuesta_json = request.get_json()
    participanteid = respuesta_json["id_participante_evento"]
    evento = respuesta_json["idEvento"]
    username = respuesta_json["username"]

    # Validar si ya realizó consumo
    respuesta = db.execute ("SELECT id_participante FROM consumo_cadaparticipante WHERE id_participante = ? AND id_evento = ?",(participanteid,evento)).fetchone()
    if respuesta:
        response = {"status": "error", "redirect": "/eventos/" +
                    evento, "message": "Participante tiene consumo. No se puede eliminar"}
        return jsonify(response)
    db.execute("DELETE FROM participante_evento WHERE id_participante_evento = ? AND id_evento = ?", (participanteid,evento))
    conn.commit()
    response = {"status": "success","message": username + " ha sido eliminado/a del evento", "redirect":  "/eventos/" + evento}
    return jsonify(response)
    
