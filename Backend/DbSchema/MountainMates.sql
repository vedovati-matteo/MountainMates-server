CREATE TABLE "Escursione_template" (
  "id_escursione_template" int,
  "nome" varchar(50),
  "provincia" varchar(2),
  "partenza" varchar(30),
  "mapLink" varchar(2000),
  "dislivello" int,
  "distanza" float,
  "tempo_stimato" varchar(20),
  "altezza_min" int,
  "altezza_max" int,
  "difficulty" int,
  "strumenti_richiesti" varchar(500),
  "descrizione_percorso" varchar(2000),
  "numero_max" int,
  "img" varchar(500),
  PRIMARY KEY ("id_escursione_template")
);

CREATE TABLE "Escursione" (
  "id_escursione" int,
  "nome" varchar(50),
  "id_organizzatore" varchar(50),
  "data" date,
  "provincia" varchar(2),
  "partenza" varchar(30),
  "mapLink" varchar(2000),
  "dislivello" int,
  "distanza" float,
  "tempo_stimato" varchar(20),
  "altezza_min" int,
  "altezza_max" int,
  "difficulty" int,
  "strumenti_richiesti" varchar(500),
  "descrizione_percorso" varchar(2000),
  "numero_max" int,
  "img" varchar(500),
  PRIMARY KEY ("id_escursione")
);

CREATE TABLE "Utente" (
  "id_firebase" varchar(50),
  "nome" varchar(50),
  "cognome" varchar(50),
  "nickname" varchar(50),
  "flag_organizzatore" bool,
  "bio" varchar(50),
  "data_di_nascita" date,
  "numero_amici" int,
  "livello_di_camminatore" int,
  "img" varchar,
  PRIMARY KEY ("id_firebase")
);

CREATE TABLE "Utente_Escursione" (
  "Utente_id_firebase" varchar(50),
  "Escursione_id_escursione" int,
  PRIMARY KEY ("Utente_id_firebase", "Escursione_id_escursione")
);

ALTER TABLE "Utente_Escursione" ADD FOREIGN KEY ("Utente_id_firebase") REFERENCES "Utente" ("id_firebase");

ALTER TABLE "Utente_Escursione" ADD FOREIGN KEY ("Escursione_id_escursione") REFERENCES "Escursione" ("id_escursione");

