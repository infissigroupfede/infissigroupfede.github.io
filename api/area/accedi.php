<?php
/* POST { email, password }: apre la sessione. Lo stesso messaggio per email sconosciuta e password errata. */
require __DIR__ . "/_lib.php";

$d = solo_post();
$email = mb_strtolower(testo($d, "email", 190));
$password = (string)($d["password"] ?? "");
if ($email === "" || $password === "") errore(422, "dati", "Inserisci email e password.");

limita("accesso_ip", ip(), 20, 15);
limita("accesso_email", $email, 8, 15);

$q = db()->prepare("SELECT id, nome, cognome, email, password_hash FROM area_utenti WHERE email = ?");
$q->execute([$email]);
$u = $q->fetch();
if (!$u || !password_verify($password, $u["password_hash"])) errore(401, "credenziali", "Email o password non corrette.");

if (password_needs_rehash($u["password_hash"], PASSWORD_DEFAULT)) {
  db()->prepare("UPDATE area_utenti SET password_hash = ? WHERE id = ?")->execute([password_hash($password, PASSWORD_DEFAULT), $u["id"]]);
}
apri_sessione((int)$u["id"]);
rispondi(200, ["ok" => true, "utente" => ["nome" => $u["nome"], "cognome" => $u["cognome"], "email" => $u["email"]]]);
