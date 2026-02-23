<?php

namespace App\Service;

use App\Entity\Usuario;
use App\Util\JwtUtil;
use Doctrine\ORM\EntityManagerInterface;

/**
 * Servicio de Autenticación
 * 
 * Maneja login, validación de tokens y autenticación de usuarios
 */
class AuthService
{
    private EntityManagerInterface $em;
    private JwtUtil $jwtUtil;

    public function __construct(EntityManagerInterface $em, JwtUtil $jwtUtil)
    {
        $this->em = $em;
        $this->jwtUtil = $jwtUtil;
    }

    /**
     * Autenticar usuario y generar JWT
     * 
     * @param string $email Email del usuario
     * @param string $contraseña Contraseña (sin hash)
     * @return array Token y datos usuario
     * @throws \Exception
     */
    public function login(string $email, string $contraseña): array
    {
        // Validar inputs
        if (empty($email) || empty($contraseña)) {
            throw new \Exception('Email y contraseña requeridos', 400);
        }

        // Buscar usuario
        $usuario = $this->em->getRepository(Usuario::class)
            ->findOneBy(['email' => $email]);

        if (!$usuario) {
            throw new \Exception('Usuario no encontrado', 401);
        }

        // Verificar contraseña
        if (!$this->verificarContraseña($contraseña, $usuario->getContraseña())) {
            throw new \Exception('Contraseña incorrecta', 401);
        }

        if (!$usuario->isActivo()) {
            throw new \Exception('Usuario inactivo', 403);
        }

        // Generar JWT
        $token = $this->jwtUtil->encode([
            'id' => $usuario->getId(),
            'email' => $usuario->getEmail(),
            'rol' => $usuario->getRol()
        ]);

        return [
            'access_token' => $token,
            'token_type' => 'bearer',
            'usuario' => $this->formatearUsuario($usuario)
        ];
    }

    /**
     * Verificar si token es válido
     * 
     * @param string $token JWT token
     * @return array Datos decodificados
     * @throws \Exception
     */
    public function verificarToken(string $token): array
    {
        return $this->jwtUtil->decode($token);
    }

    /**
     * Verificar contraseña (soporta texto plano y hash)
     */
    private function verificarContraseña(string $plana, string $almacenada): bool
    {
        // Para demo: texto plano
        if ($plana === $almacenada) {
            return true;
        }

        // Para producción: hash password_verify
        return password_verify($plana, $almacenada);
    }

    /**
     * Formatear datos del usuario para respuesta
     */
    private function formatearUsuario(Usuario $usuario): array
    {
        return [
            'id' => $usuario->getId(),
            'email' => $usuario->getEmail(),
            'nombre' => $usuario->getNombre(),
            'rol' => $usuario->getRol(),
            'especialidad' => $usuario->getEspecialidad()
        ];
    }
}
