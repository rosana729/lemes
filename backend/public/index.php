<?php

use Symfony\Component\Dotenv\Dotenv;
use Symfony\Component\HttpFoundation\Request;

require dirname(__DIR__).'/vendor/autoload.php';

// Cargar variables de entorno
if (file_exists(dirname(__DIR__).'/.env')) {
    (new Dotenv())->loadEnv(dirname(__DIR__).'/.env');
}

// Crear kernel
$kernel = new App\Kernel($_ENV['APP_ENV'] ?? 'dev', ($_ENV['APP_DEBUG'] ?? 0) == 1);

// Manejar request
$request = Request::createFromGlobals();
$response = $kernel->handle($request);

// Enviar respuesta
$response->send();

// Terminar
$kernel->terminate($request, $response);
