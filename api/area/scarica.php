<?php
/* GET ?f=percorso/relativo.pdf: invia il file solo a utenti collegati e solo se sta dentro la cartella dei file */
require __DIR__ . "/_lib.php";

if (!utente_corrente()) {
  header("Location: /area-riservata/?torna=" . rawurlencode("/area-riservata/documenti/"), true, 303);
  exit;
}
$base = realpath(config()["cartella_file"]);
$file = $base ? realpath($base . "/" . (string)($_GET["f"] ?? "")) : false;
if ($file === false || !is_file($file) || !str_starts_with($file, $base . DIRECTORY_SEPARATOR) || basename($file)[0] === ".") {
  http_response_code(404);
  exit("File non trovato.");
}

$nome = basename($file);
$tipo = (new finfo(FILEINFO_MIME_TYPE))->file($file) ?: "application/octet-stream";
header("Content-Type: $tipo");
header("Content-Length: " . filesize($file));
header("Content-Disposition: attachment; filename=\"" . preg_replace('/[^\x20-\x7E]|"/', "_", $nome) . "\"; filename*=UTF-8''" . rawurlencode($nome));
header("Cache-Control: private, no-store");
header("X-Content-Type-Options: nosniff");
readfile($file);
