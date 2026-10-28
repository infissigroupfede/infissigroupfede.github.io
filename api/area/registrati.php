<?php
/* POST { nome, cognome, email, password, privacy, marketing, website }: crea l'account e apre la sessione */
require __DIR__ . "/_lib.php";

$d = solo_post();
if (testo($d, "website") !== "") rispondi(200, ["ok" => true]); // campo trappola compilato: è un bot

$nome = testo($d, "nome", 80);
$cognome = testo($d, "cognome", 80);
$email = mb_strtolower(testo($d, "email", 190));
$password = (string)($d["password"] ?? "");

if ($nome === "" || $cognome === "") errore(422, "nome", "Inserisci nome e cognome.");
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) errore(422, "email", "Inserisci un indirizzo email valido.");
if (mb_strlen($password) < AREA_PASSWORD_MIN || strlen($password) > 200) errore(422, "password", "La password deve avere almeno " . AREA_PASSWORD_MIN . " caratteri.");
if (($d["privacy"] ?? false) !== true) errore(422, "privacy", "Per registrarti accetta l'informativa privacy.");

limita("registrazione", ip(), 5, 60);

try {
  db()->prepare("INSERT INTO area_utenti (nome, cognome, email, password_hash, marketing, privacy_il, creato_il) VALUES (?, ?, ?, ?, ?, NOW(), NOW())")
    ->execute([$nome, $cognome, $email, password_hash($password, PASSWORD_DEFAULT), ($d["marketing"] ?? false) === true ? 1 : 0]);
} catch (PDOException $e) {
  if ($e->errorInfo[1] === 1062) errore(409, "email_esistente", "Questa email è già registrata. Accedi oppure reimposta la password.");
  throw $e;
}

apri_sessione((int)db()->lastInsertId());
rispondi(201, ["ok" => true, "utente" => ["nome" => $nome, "cognome" => $cognome, "email" => $email]]);
