<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasher;
use Doctrine\ORM\EntityManagerInterface;
use App\Entity\Usuario;
use App\Entity\Paciente;
use App\Entity\Cita;
use Firebase\JWT\JWT;

#[Route('/api', format: 'json')]
class ApiController extends AbstractController
{
    private EntityManagerInterface $em;
    private string $jwtSecret;

    public function __construct(EntityManagerInterface $em)
    {
        $this->em = $em;
        $this->jwtSecret = $_ENV['JWT_SECRET'] ?? 'tu-clave-jwt';
    }

    /**
     * POST /api/login
     * Login endpoint - Retorna JWT token
     */
    #[Route('/login', methods: ['POST'])]
    public function login(Request $request): JsonResponse
    {
        $data = json_decode($request->getContent(), true);
        
        $email = $data['email'] ?? null;
        $contraseña = $data['contraseña'] ?? null;

        if (!$email || !$contraseña) {
            return new JsonResponse(
                ['error' => 'Email y contraseña requeridos'],
                400
            );
        }

        // Buscar usuario
        $usuario = $this->em->getRepository(Usuario::class)
            ->findOneBy(['email' => $email]);

        if (!$usuario) {
            return new JsonResponse(
                ['error' => 'Usuario no encontrado'],
                401
            );
        }

        // Verificar contraseña (en demofunciona texto plano)
        if ($usuario->getContraseña() !== $contraseña && !password_verify($contraseña, $usuario->getContraseña())) {
            return new JsonResponse(
                ['error' => 'Contraseña incorrecta'],
                401
            );
        }

        if (!$usuario->isActivo()) {
            return new JsonResponse(
                ['error' => 'Usuario inactivo'],
                403
            );
        }

        // Generar JWT
        $payload = [
            'iat' => time(),
            'exp' => time() + (30 * 60),
            'id' => $usuario->getId(),
            'email' => $usuario->getEmail(),
            'rol' => $usuario->getRol()
        ];

        $token = JWT::encode($payload, $this->jwtSecret, 'HS256');

        return new JsonResponse([
            'success' => true,
            'access_token' => $token,
            'token_type' => 'bearer',
            'usuario' => [
                'id' => $usuario->getId(),
                'email' => $usuario->getEmail(),
                'nombre' => $usuario->getNombre(),
                'rol' => $usuario->getRol()
            ]
        ]);
    }

    /**
     * GET /api/pacientes
     * Listar todos los pacientes
     */
    #[Route('/pacientes', methods: ['GET'])]
    public function getPacientes(): JsonResponse
    {
        $pacientes = $this->em->getRepository(Paciente::class)->findAll();
        
        $data = array_map(fn($p) => [
            'id' => $p->getId(),
            'nombre' => $p->getNombre(),
            'apellido' => $p->getApellido(),
            'documento' => $p->getDocumento(),
            'email' => $p->getEmail(),
            'telefono' => $p->getTelefono(),
            'edad' => $p->getEdad()
        ], $pacientes);

        return new JsonResponse($data);
    }

    /**
     * GET /api/citas
     * Listar todas las citas
     */
    #[Route('/citas', methods: ['GET'])]
    public function getCitas(): JsonResponse
    {
        $citas = $this->em->getRepository(Cita::class)->findAll();
        
        $data = array_map(fn($c) => [
            'id' => $c->getId(),
            'paciente' => $c->getPaciente()->getNombre(),
            'doctor' => $c->getDoctor()->getNombre(),
            'fecha' => $c->getFecha(),
            'hora' => $c->getHora(),
            'estado' => $c->getEstado()
        ], $citas);

        return new JsonResponse($data);
    }

    /**
     * GET /api/estadisticas
     * Endpoint para dashboard
     */
    #[Route('/estadisticas', methods: ['GET'])]
    public function getEstadisticas(): JsonResponse
    {
        $totalPacientes = count($this->em->getRepository(Paciente::class)->findAll());
        $citas = $this->em->getRepository(Cita::class)->findAll();
        $citasHoy = count(array_filter($citas, fn($c) => $c->getFecha() === date('Y-m-d')));

        return new JsonResponse([
            'total_pacientes' => $totalPacientes,
            'consultas_hoy' => $citasHoy,
            'ingresos_mes' => 0,
            'gastos_mes' => 0
        ]);
    }

    /**
     * GET /api/health
     * Health check
     */
    #[Route('/health', methods: ['GET'])]
    public function health(): JsonResponse
    {
        return new JsonResponse([
            'status' => 'ok',
            'message' => 'Clínica Pediátrica API v1.0'
        ]);
    }
}
