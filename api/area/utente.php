<?php
/* GET: l'utente collegato, oppure 401 */
require __DIR__ . "/_lib.php";

$u = richiedi_utente();
rispondi(200, ["ok" => true, "utente" => ["nome" => $u["nome"], "cognome" => $u["cognome"], "email" => $u["email"]]]);
