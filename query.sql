--Instrucciones para contener problema en la base de datos

--Instalar SQLite, SQLTools y SQLViewer:

--CREATE TABLE 'participante_evento' ('id_participante_evento' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
--id_evento INTEGER NOT NULL,
--id_usuario INTEGER,
--nombre_participante TEXT,
--monto_a_pagar NUMERIC,
--FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
--FOREIGN KEY (id_evento) REFERENCES eventos(id_evento)
--);

--Generar un drop de participantes_evento

--DROP TABLE participantes_evento

--Luego cambiar todos los participantes_evento en services.py