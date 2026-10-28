<?php
/* POST { token, password }: imposta la nuova password, annulla il link e apre la sessione */
require __DIR__ . "/_lib.php";

$d = solo_post();
$token = (string)($d["token"] ?? "");
$password = (string)($d["password"] ?? "");
if (!preg_match('/^[a-f0-9]{64}$/', $token)) errore(400, "link", "Il link non è valido. Chiedi un nuovo link.");
if (mb_strlen($password) < AREA_PASSWORD_MIN || strlen($password) > 200) errore(422, "password", "La password deve avere almeno " . AREA_PASSWORD_MIN . " caratteri.");

limita("reset_nuova", ip(), 10, 60);

$q = db()->prepare("SELECT utente_id FROM area_reset WHERE token_hash = ? AND scade_il > NOW()");
$q->execute([hash("sha256", $token)]);
$id = $q->fetchColumn();
if (!$id) errore(410, "link", "Il link è scaduto o è già stato usato. Chiedi un nuovo link.");

db()->prepare("UPDATE area_utenti SET password_hash = ? WHERE id = ?")->execute([password_hash($password, PASSWORD_DEFAULT), $id]);
db()->prepare("DELETE FROM area_reset WHERE utente_id = ?")->execute([$id]);
apri_sessione((int)$id);
rispondi(200, ["ok" => true]);
