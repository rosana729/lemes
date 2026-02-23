<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;
use App\Service\CitaService;
use App\Util\ResponseUtil;

/**
 * Controlador de Citas
 * 
 * Maneja CRUD de citas médicas
 */
#[Route('/api/citas')]
class CitaController extends AbstractController
{
    private CitaService $citaService;

    public function __construct(CitaService $citaService)
    {
        $this->citaService = $citaService;
    }

    /**
     * GET /api/citas
     * Listar todas las citas
     */
    #[Route('', methods: ['GET'])]
    public function listar(): JsonResponse
    {
        try {
            $citas = $this->citaService->listarTodas();
            return ResponseUtil::success($citas);
        } catch (\Exception $e) {
            return ResponseUtil::error($e->getMessage(), 400);
        }
    }

    /**
     * GET /api/citas/{id}
     * Obtener una cita por ID
     */
    #[Route('/{id}', methods: ['GET'])]
    public function obtener(int $id): JsonResponse
    {
        try {
            $cita = $this->citaService->obtenerPorId($id);
            
            if (!$cita) {
                return ResponseUtil::error('Cita no encontrada', 404);
            }

            return ResponseUtil::success($this->citaService->formatear($cita));
        } catch (\Exception $e) {
            return ResponseUtil::error($e->getMessage(), 400);
        }
    }

    /**
     * POST /api/citas
     * Crear nueva cita
     */
    #[Route('', methods: ['POST'])]
    public function crear(Request $request): JsonResponse
    {
        try {
            $data = json_decode($request->getContent(), true) ?? [];

            $cita = $this->citaService->crear($data);

            return ResponseUtil::success(
                $this->citaService->formatear($cita),
                201
            );
        } catch (\Exception $e) {
            return ResponseUtil::error($e->getMessage(), $e->getCode() ?: 400);
        }
    }

    /**
     * PUT /api/citas/{id}
     * Actualizar cita
     */
    #[Route('/{id}', methods: ['PUT'])]
    public function actualizar(int $id, Request $request): JsonResponse
    {
        try {
            $data = json_decode($request->getContent(), true) ?? [];

            $cita = $this->citaService->actualizar($id, $data);

            return ResponseUtil::success($this->citaService->formatear($cita));
        } catch (\Exception $e) {
            return ResponseUtil::error($e->getMessage(), $e->getCode() ?: 400);
        }
    }

    /**
     * DELETE /api/citas/{id}
     * Eliminar cita
     */
    #[Route('/{id}', methods: ['DELETE'])]
    public function eliminar(int $id): JsonResponse
    {
        try {
            $this->citaService->eliminar($id);

            return ResponseUtil::success(['message' => 'Cita eliminada']);
        } catch (\Exception $e) {
            return ResponseUtil::error($e->getMessage(), $e->getCode() ?: 400);
        }
    }
}
