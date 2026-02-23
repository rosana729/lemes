<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;
use App\Service\PacienteService;
use App\Util\ResponseUtil;

/**
 * Controlador de Pacientes
 * 
 * Maneja CRUD de pacientes
 */
#[Route('/api/pacientes')]
class PacienteController extends AbstractController
{
    private PacienteService $pacienteService;

    public function __construct(PacienteService $pacienteService)
    {
        $this->pacienteService = $pacienteService;
    }

    /**
     * GET /api/pacientes
     * Listar todos los pacientes
     */
    #[Route('', methods: ['GET'])]
    public function listar(): JsonResponse
    {
        try {
            $pacientes = $this->pacienteService->listarTodos();
            return ResponseUtil::success($pacientes);
        } catch (\Exception $e) {
            return ResponseUtil::error($e->getMessage(), 400);
        }
    }

    /**
     * GET /api/pacientes/{id}
     * Obtener un paciente por ID
     */
    #[Route('/{id}', methods: ['GET'])]
    public function obtener(int $id): JsonResponse
    {
        try {
            $paciente = $this->pacienteService->obtenerPorId($id);
            
            if (!$paciente) {
                return ResponseUtil::error('Paciente no encontrado', 404);
            }

            return ResponseUtil::success($this->pacienteService->formatear($paciente));
        } catch (\Exception $e) {
            return ResponseUtil::error($e->getMessage(), 400);
        }
    }

    /**
     * POST /api/pacientes
     * Crear nuevo paciente
     */
    #[Route('', methods: ['POST'])]
    public function crear(Request $request): JsonResponse
    {
        try {
            $data = json_decode($request->getContent(), true) ?? [];

            $paciente = $this->pacienteService->crear($data);

            return ResponseUtil::success(
                $this->pacienteService->formatear($paciente),
                201
            );
        } catch (\Exception $e) {
            return ResponseUtil::error($e->getMessage(), 400);
        }
    }

    /**
     * PUT /api/pacientes/{id}
     * Actualizar paciente
     */
    #[Route('/{id}', methods: ['PUT'])]
    public function actualizar(int $id, Request $request): JsonResponse
    {
        try {
            $data = json_decode($request->getContent(), true) ?? [];

            $paciente = $this->pacienteService->actualizar($id, $data);

            return ResponseUtil::success($this->pacienteService->formatear($paciente));
        } catch (\Exception $e) {
            return ResponseUtil::error($e->getMessage(), $e->getCode() ?: 400);
        }
    }

    /**
     * DELETE /api/pacientes/{id}
     * Eliminar paciente
     */
    #[Route('/{id}', methods: ['DELETE'])]
    public function eliminar(int $id): JsonResponse
    {
        try {
            $this->pacienteService->eliminar($id);

            return ResponseUtil::success(['message' => 'Paciente eliminado']);
        } catch (\Exception $e) {
            return ResponseUtil::error($e->getMessage(), $e->getCode() ?: 400);
        }
    }
}
