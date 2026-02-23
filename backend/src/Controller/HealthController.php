<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;
use App\Util\ResponseUtil;
use Doctrine\ORM\EntityManagerInterface;
use App\Entity\Usuario;
use App\Entity\Paciente;
use App\Entity\Cita;

/**
 * Controlador de Salud y Estadísticas
 * 
 * Health checks y estadísticas de la aplicación
 */
#[Route('/api')]
class HealthController extends AbstractController
{
    private EntityManagerInterface $em;

    public function __construct(EntityManagerInterface $em)
    {
        $this->em = $em;
    }

    /**
     * GET /api/health
     * Health check del servidor
     */
    #[Route('/health', methods: ['GET'])]
    public function health(): JsonResponse
    {
        return ResponseUtil::success([
            'status' => 'ok',
            'message' => 'Clínica Pediátrica API v1.0',
            'timestamp' => date('Y-m-d H:i:s')
        ]);
    }

    /**
     * GET /api/estadisticas
     * Estadísticas para el dashboard
     */
    #[Route('/estadisticas', methods: ['GET'])]
    public function estadisticas(): JsonResponse
    {
        try {
            $totalPacientes = count($this->em->getRepository(Paciente::class)->findAll());
            $totalDoctores = count($this->em->getRepository(Usuario::class)->findBy(['rol' => 'doctor']));
            $citas = $this->em->getRepository(Cita::class)->findAll();
            $citasHoy = count(array_filter($citas, fn($c) => $c->getFecha() === date('Y-m-d')));
            $citasProgramadas = count(array_filter($citas, fn($c) => $c->getEstado() === 'programada'));

            return ResponseUtil::success([
                'pacientes' => [
                    'total' => $totalPacientes
                ],
                'doctores' => [
                    'total' => $totalDoctores
                ],
                'citas' => [
                    'total' => count($citas),
                    'hoy' => $citasHoy,
                    'programadas' => $citasProgramadas,
                    'realizadas' => count(array_filter($citas, fn($c) => $c->getEstado() === 'realizada')),
                    'canceladas' => count(array_filter($citas, fn($c) => $c->getEstado() === 'cancelada'))
                ]
            ]);
        } catch (\Exception $e) {
            return ResponseUtil::error($e->getMessage(), 400);
        }
    }
}
