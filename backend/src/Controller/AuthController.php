<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;
use App\Service\AuthService;
use App\Util\ResponseUtil;

/**
 * Controlador de Autenticación
 * 
 * Maneja login y validación de tokens
 */
#[Route('/api/auth')]
class AuthController extends AbstractController
{
    private AuthService $authService;

    public function __construct(AuthService $authService)
    {
        $this->authService = $authService;
    }

    /**
     * POST /api/auth/login
     * Login del usuario
     */
    #[Route('/login', methods: ['POST'])]
    public function login(Request $request): JsonResponse
    {
        try {
            $data = json_decode($request->getContent(), true) ?? [];

            $resultado = $this->authService->login(
                $data['email'] ?? '',
                $data['contraseña'] ?? ''
            );

            return ResponseUtil::success($resultado);
        } catch (\Exception $e) {
            return ResponseUtil::error($e->getMessage(), $e->getCode() ?: 400);
        }
    }

    /**
     * GET /api/auth/me
     * Obtener datos del usuario actual
     */
    #[Route('/me', methods: ['GET'])]
    public function me(Request $request): JsonResponse
    {
        try {
            $token = $request->headers->get('Authorization');
            
            if (!$token) {
                return ResponseUtil::error('Token requerido', 401);
            }

            // Aquí iría la lógica de validación del token
            return ResponseUtil::success(['message' => 'Usuario autenticado']);
        } catch (\Exception $e) {
            return ResponseUtil::error($e->getMessage(), 401);
        }
    }
}
