--Instrucciones para el nuevo cambio en la base de datos:

--Instalar SQLite, SQLTools y SQLViewer: (si ya se tiene, omitir paso)

--crear una tabla que muestre el consumo general de cada vez que se introducen productos en el evento

--CREATE TABLE 'consumo_general' ('id_consumo' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
--id_producto INTEGER NOT NULL,
--cantidad_consumida INTEGER,
--precio_uniproducto NUMERIC,
--total_consumo NUMERIC,
--FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
--FOREIGN KEY (precio_uniproducto) REFERENCES productos(precio_producto)
--);

--crear una tabla que muestre el consumo de cada participante (muestra como se divide ese consumo general o cantidad de productos en consumo general)

--CREATE TABLE 'consumo_cadaparticipante' ('id_consumo_individual' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
--id_consumo INTEGER NOT NULL,
--id_participante INTEGER NOT NULL,
--cantidad_individual INTEGER,
--subtotal_participante NUMERIC,
--id_evento INTEGER NOT NULL,
--propina NUMERIC,
--impuesto NUMERIC,
--FOREIGN KEY (id_participante) REFERENCES participante_evento(id_participante_evento)
--FOREIGN KEY (id_consumo) REFERENCES consumo_general(id_consumo)
--);


--Todavía no hay drop de consumo_participante hasta que se sepa que está correcto lo que se pensó
--Acá está el comando si:
--DROP TABLE consumo_cadaparticipante
