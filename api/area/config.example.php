<?php
/*
  AREA RISERVATA: configurazione.
  Su Hostinger copia questo file in config.php nella stessa cartella e compila i valori.
  config.php non va nel repo (è in .gitignore) e non è raggiungibile dal web (.htaccess).
*/
return [
  // hPanel > Database > MySQL: nome database, utente e password creati lì. L'host è quasi sempre localhost.
  "db" => [
    "host" => "localhost",
    "nome" => "u000000000_area",
    "utente" => "u000000000_area",
    "password" => "",
  ],

  // Casella creata in hPanel > Email: deve essere del dominio del sito, altrimenti le mail finiscono in spam
  "mail" => [
    "mittente" => "noreply@infissigroup.com",
    "nome_mittente" => "Infissi Group",
    "rispondi_a" => "info@infissigroup.com",
  ],

  // Indirizzo del sito, per i link nelle email
  "sito" => "https://infissigroup.com",

  // Cartella dei file scaricabili, FUORI da public_html: chi conosce l'indirizzo non può scaricarli senza accesso.
  // Su Hostinger public_html sta in /home/uXXXX/domains/infissigroup.com/public_html: questa è la cartella accanto.
  // Le sottocartelle diventano le sezioni della pagina (es. "Cataloghi", "Schede tecniche").
  "cartella_file" => dirname(__DIR__, 3) . "/area-riservata-file",
];
