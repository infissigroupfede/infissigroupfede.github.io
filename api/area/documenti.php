<?php
/*
  GET: elenco dei file scaricabili, solo per utenti collegati.
  I file in cima alla cartella vanno nella sezione "Documenti", ogni sottocartella è una sezione col suo nome.
  Il titolo mostrato è il nome del file senza estensione, con trattini e trattini bassi al posto degli spazi.
*/
require __DIR__ . "/_lib.php";

richiedi_utente();
$base = realpath(config()["cartella_file"]);
if ($base === false || !is_dir($base)) rispondi(200, ["ok" => true, "sezioni" => []]);

function elenca(string $cartella, string $base): array {
  $out = [];
  foreach (scandir($cartella) as $nome) {
    $percorso = "$cartella/$nome";
    if ($nome[0] === "." || !is_file($percorso)) continue;
    $out[] = [
      "titolo" => str_replace(["-", "_"], " ", pathinfo($nome, PATHINFO_FILENAME)),
      "file" => ltrim(substr($percorso, strlen($base)), "/"),
      "tipo" => strtoupper(pathinfo($nome, PATHINFO_EXTENSION)),
      "byte" => filesize($percorso),
      "data" => date("Y-m-d", filemtime($percorso)),
    ];
  }
  usort($out, fn($a, $b) => strnatcasecmp($a["titolo"], $b["titolo"]));
  return $out;
}

$sezioni = [];
$radice = elenca($base, $base);
if ($radice) $sezioni[] = ["titolo" => "Documenti", "file" => $radice];
$cartelle = array_filter(scandir($base), fn($n) => $n[0] !== "." && is_dir("$base/$n"));
natcasesort($cartelle);
foreach ($cartelle as $c) {
  $file = elenca("$base/$c", $base);
  if ($file) $sezioni[] = ["titolo" => $c, "file" => $file];
}
rispondi(200, ["ok" => true, "sezioni" => $sezioni]);
