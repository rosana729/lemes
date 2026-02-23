<?php

namespace App\Util;

use Firebase\JWT\JWT;
use Firebase\JWT\Key;

/**
 * Utilidad de JWT
 * 
 * Maneja codificación y decodificación de tokens JWT
 */
class JwtUtil
{
    private string $secret;
    private string $algorithm = 'HS256';

    public function __construct()
    {
        $this->secret = $_ENV['JWT_SECRET'] ?? 'change-me-in-production';
    }

    /**
     * Codificar JWT
     * 
     * @param array $datos Datos a incluir en el token
     * @param int $expiracion Segundos hasta que expire (default: 30 min)
     * @return string Token JWT
     */
    public function encode(array $datos, int $expiracion = 1800): string
    {
        $payload = array_merge($datos, [
            'iat' => time(),
            'exp' => time() + $expiracion
        ]);

        return JWT::encode($payload, $this->secret, $this->algorithm);
    }

    /**
     * Decodificar JWT
     * 
     * @param string $token Token a validar
     * @return array Datos decodificados
     * @throws \Exception
     */
    public function decode(string $token): array
    {
        try {
            $decoded = JWT::decode($token, new Key($this->secret, $this->algorithm));
            return (array) $decoded;
        } catch (\Exception $e) {
            throw new \Exception('Token inválido: ' . $e->getMessage(), 401);
        }
    }

    /**
     * Obtener token desde header Authorization
     * 
     * @param string $header Valor del header Authorization
     * @return string|null Token extraído
     */
    public function extraerDelHeader(string $header): ?string
    {
        if (preg_match('/Bearer\s+(.+)/i', $header, $matches)) {
            return $matches[1];
        }
        return null;
    }
}
