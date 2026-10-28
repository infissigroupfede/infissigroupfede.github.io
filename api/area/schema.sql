-- AREA RISERVATA: tabelle MySQL/MariaDB.
-- Su Hostinger: hPanel > Database > phpMyAdmin, seleziona il database e importa questo file.

CREATE TABLE IF NOT EXISTS area_utenti (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  nome VARCHAR(80) NOT NULL,
  cognome VARCHAR(80) NOT NULL,
  email VARCHAR(190) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  marketing TINYINT(1) NOT NULL DEFAULT 0,
  privacy_il DATETIME NOT NULL,
  creato_il DATETIME NOT NULL,
  ultimo_accesso DATETIME NULL,
  PRIMARY KEY (id),
  UNIQUE KEY email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Link per reimpostare la password: si salva solo l'hash del token, valido un'ora e una volta sola
CREATE TABLE IF NOT EXISTS area_reset (
  token_hash CHAR(64) NOT NULL,
  utente_id INT UNSIGNED NOT NULL,
  scade_il DATETIME NOT NULL,
  PRIMARY KEY (token_hash),
  KEY utente_id (utente_id),
  CONSTRAINT area_reset_utente FOREIGN KEY (utente_id) REFERENCES area_utenti (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tentativi di accesso, registrazione e recupero, per frenare gli attacchi a forza bruta (si cancellano dopo un giorno)
CREATE TABLE IF NOT EXISTS area_tentativi (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  tipo VARCHAR(20) NOT NULL,
  chiave CHAR(64) NOT NULL,
  quando DATETIME NOT NULL,
  PRIMARY KEY (id),
  KEY tipo_chiave (tipo, chiave, quando)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
