<?php
/*
  POST { email }: invia il link per reimpostare la password, valido un'ora.
  Risponde sempre allo stesso modo, così non rivela quali email sono registrate.
*/
require __DIR__ . "/_lib.php";

$d = solo_post();
$email = mb_strtolower(testo($d, "email", 190));
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) errore(422, "email", "Inserisci un indirizzo email valido.");

limita("reset_ip", ip(), 10, 60);
limita("reset_email", $email, 3, 60);

$q = db()->prepare("SELECT id, nome FROM area_utenti WHERE email = ?");
$q->execute([$email]);
if ($u = $q->fetch()) {
  $token = bin2hex(random_bytes(32));
  db()->prepare("DELETE FROM area_reset WHERE utente_id = ? OR scade_il < NOW()")->execute([$u["id"]]);
  db()->prepare("INSERT INTO area_reset (token_hash, utente_id, scade_il) VALUES (?, ?, NOW() + INTERVAL 1 HOUR)")
    ->execute([hash("sha256", $token), $u["id"]]);
  $link = rtrim(config()["sito"], "/") . "/area-riservata/password/?t=" . $token;
  invia_mail($email, "Reimposta la password dell'area riservata", <<<TXT
Ciao {$u["nome"]},

per scegliere una nuova password dell'area riservata di Infissi Group apri questo link entro un'ora:

$link

Se non hai chiesto tu di reimpostare la password, ignora questa email: la password attuale resta valida.

Infissi Group
TXT);
}
rispondi(200, ["ok" => true]);
