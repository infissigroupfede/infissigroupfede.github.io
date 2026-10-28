<?php
/*
  AREA RISERVATA: funzioni comuni a tutti gli endpoint di /api/area/.
  Pensato per l'hosting condiviso Hostinger (PHP 8.1+, MySQL/MariaDB, mail() attiva).
  Configurazione in config.php (copia di config.example.php, fuori dal repo).
  Ogni endpoint risponde in JSON: { ok: true, ... } oppure { ok: false, errore: "codice", messaggio: "..." }.
*/
declare(strict_types=1);

const AREA_SESSIONE = "ig_area";
const AREA_PASSWORD_MIN = 10;

function config(): array {
  static $cfg = null;
  if ($cfg === null) {
    $file = __DIR__ . "/config.php";
    if (!is_file($file)) rispondi(503, ["ok" => false, "errore" => "non_configurato", "messaggio" => "L'area riservata non è ancora attiva."]);
    $cfg = require $file;
  }
  return $cfg;
}

function db(): PDO {
  static $pdo = null;
  if ($pdo === null) {
    $c = config()["db"];
    $pdo = new PDO("mysql:host={$c["host"]};dbname={$c["nome"]};charset=utf8mb4", $c["utente"], $c["password"], [
      PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
      PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
      PDO::ATTR_EMULATE_PREPARES => false,
    ]);
  }
  return $pdo;
}

function rispondi(int $stato, array $dati): never {
  http_response_code($stato);
  header("Content-Type: application/json; charset=utf-8");
  header("Cache-Control: no-store");
  header("X-Content-Type-Options: nosniff");
  echo json_encode($dati, JSON_UNESCAPED_UNICODE);
  exit;
}

function errore(int $stato, string $codice, string $messaggio): never {
  rispondi($stato, ["ok" => false, "errore" => $codice, "messaggio" => $messaggio]);
}

/* Sessione su cookie HttpOnly, Secure in HTTPS, SameSite=Lax */
function avvia_sessione(): void {
  if (session_status() === PHP_SESSION_ACTIVE) return;
  session_name(AREA_SESSIONE);
  session_set_cookie_params([
    "lifetime" => 0,
    "path" => "/",
    "secure" => !empty($_SERVER["HTTPS"]) && $_SERVER["HTTPS"] !== "off",
    "httponly" => true,
    "samesite" => "Lax",
  ]);
  ini_set("session.use_strict_mode", "1");
  session_start();
}

/* Le richieste POST arrivano solo dalle pagine del sito: stessa origine e intestazione aggiunta dallo script */
function solo_post(): array {
  if ($_SERVER["REQUEST_METHOD"] !== "POST") errore(405, "metodo", "Metodo non consentito.");
  if (($_SERVER["HTTP_X_REQUESTED_WITH"] ?? "") !== "fetch") errore(403, "origine", "Richiesta non valida.");
  $origine = $_SERVER["HTTP_ORIGIN"] ?? "";
  if ($origine !== "" && parse_url($origine, PHP_URL_HOST) !== ($_SERVER["HTTP_HOST"] ?? "")) errore(403, "origine", "Richiesta non valida.");
  $dati = json_decode(file_get_contents("php://input") ?: "", true);
  if (!is_array($dati)) errore(400, "dati", "Dati non validi.");
  return $dati;
}

function testo(array $d, string $k, int $max = 120): string {
  $v = trim((string)($d[$k] ?? ""));
  return mb_substr(preg_replace('/\s+/u', " ", $v), 0, $max);
}

function utente_corrente(): ?array {
  avvia_sessione();
  $id = $_SESSION["utente_id"] ?? null;
  if (!$id) return null;
  $q = db()->prepare("SELECT id, nome, cognome, email FROM area_utenti WHERE id = ?");
  $q->execute([$id]);
  return $q->fetch() ?: null;
}

function richiedi_utente(): array {
  $u = utente_corrente();
  if (!$u) errore(401, "non_autenticato", "Accedi per continuare.");
  return $u;
}

function apri_sessione(int $id): void {
  avvia_sessione();
  session_regenerate_id(true);
  $_SESSION["utente_id"] = $id;
  db()->prepare("UPDATE area_utenti SET ultimo_accesso = NOW() WHERE id = ?")->execute([$id]);
}

/* Limite tentativi: al massimo $max eventi dello stesso tipo per chiave negli ultimi $minuti */
function limita(string $tipo, string $chiave, int $max, int $minuti): void {
  $pdo = db();
  $pdo->prepare("DELETE FROM area_tentativi WHERE quando < NOW() - INTERVAL 1 DAY")->execute();
  $h = hash("sha256", $chiave);
  $q = $pdo->prepare("SELECT COUNT(*) FROM area_tentativi WHERE tipo = ? AND chiave = ? AND quando > NOW() - INTERVAL ? MINUTE");
  $q->execute([$tipo, $h, $minuti]);
  if ((int)$q->fetchColumn() >= $max) errore(429, "troppi_tentativi", "Troppi tentativi. Riprova tra qualche minuto.");
  $pdo->prepare("INSERT INTO area_tentativi (tipo, chiave, quando) VALUES (?, ?, NOW())")->execute([$tipo, $h]);
}

function ip(): string {
  return $_SERVER["REMOTE_ADDR"] ?? "";
}

function invia_mail(string $a, string $oggetto, string $corpo): bool {
  $c = config()["mail"];
  $intestazioni = [
    "From" => "{$c["nome_mittente"]} <{$c["mittente"]}>",
    "Reply-To" => $c["rispondi_a"] ?? $c["mittente"],
    "Content-Type" => "text/plain; charset=utf-8",
    "Content-Transfer-Encoding" => "8bit",
  ];
  return mail($a, "=?UTF-8?B?" . base64_encode($oggetto) . "?=", $corpo, $intestazioni, "-f" . $c["mittente"]);
}
