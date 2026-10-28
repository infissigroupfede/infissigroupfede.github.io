<?php
/* POST {}: chiude la sessione */
require __DIR__ . "/_lib.php";

solo_post();
avvia_sessione();
$_SESSION = [];
$p = session_get_cookie_params();
setcookie(session_name(), "", ["expires" => time() - 3600, "path" => $p["path"], "secure" => $p["secure"], "httponly" => true, "samesite" => "Lax"]);
session_destroy();
rispondi(200, ["ok" => true]);
