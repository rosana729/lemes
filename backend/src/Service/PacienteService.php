<?php

namespace App\Service;

use App\Entity\Paciente;
use Doctrine\ORM\EntityManagerInterface;

/**
 * Servicio de Pacientes
 * 
 * Maneja operaciones CRUD de pacientes
 */
class PacienteService
{
    private EntityManagerInterface $em;

    public function __construct(EntityManagerInterface $em)
    {
        $this->em = $em;
    }

    /**
     * Obtener todos los pacientes
     */
    public function listarTodos(): array
    {
        $pacientes = $this->em->getRepository(Paciente::class)->findAll();
        return array_map(fn($p) => $this->formatear($p), $pacientes);
    }

    /**
     * Obtener paciente por ID
     */
    public function obtenerPorId(int $id): ?Paciente
    {
        return $this->em->getRepository(Paciente::class)->find($id);
    }

    /**
     * Buscar paciente por documento
     */
    public function buscarPorDocumento(string $documento): ?Paciente
    {
        return $this->em->getRepository(Paciente::class)
            ->findOneBy(['documento' => $documento]);
    }

    /**
     * Crear nuevo paciente
     */
    public function crear(array $datos): Paciente
    {
        // Validar documento único
        if ($this->buscarPorDocumento($datos['documento'])) {
            throw new \Exception('Documento ya registrado', 400);
        }

        $paciente = new Paciente();
        $paciente->setNombre($datos['nombre']);
        $paciente->setApellido($datos['apellido']);
        $paciente->setDocumento($datos['documento']);
        $paciente->setTelefono($datos['telefono']);
        $paciente->setEdad($datos['edad'] ?? null);
        $paciente->setEmail($datos['email'] ?? null);
        $paciente->setAlergias($datos['alergias'] ?? null);

        $this->em->persist($paciente);
        $this->em->flush();

        return $paciente;
    }

    /**
     * Actualizar paciente
     */
    public function actualizar(int $id, array $datos): Paciente
    {
        $paciente = $this->obtenerPorId($id);
        if (!$paciente) {
            throw new \Exception('Paciente no encontrado', 404);
        }

        if (isset($datos['nombre'])) $paciente->setNombre($datos['nombre']);
        if (isset($datos['apellido'])) $paciente->setApellido($datos['apellido']);
        if (isset($datos['telefono'])) $paciente->setTelefono($datos['telefono']);
        if (isset($datos['email'])) $paciente->setEmail($datos['email']);
        if (isset($datos['edad'])) $paciente->setEdad($datos['edad']);
        if (isset($datos['alergias'])) $paciente->setAlergias($datos['alergias']);

        $this->em->flush();

        return $paciente;
    }

    /**
     * Eliminar paciente
     */
    public function eliminar(int $id): bool
    {
        $paciente = $this->obtenerPorId($id);
        if (!$paciente) {
            throw new \Exception('Paciente no encontrado', 404);
        }

        $this->em->remove($paciente);
        $this->em->flush();

        return true;
    }

    /**
     * Formatear paciente para respuesta API
     */
    public function formatear(Paciente $paciente): array
    {
        return [
            'id' => $paciente->getId(),
            'nombre' => $paciente->getNombre(),
            'apellido' => $paciente->getApellido(),
            'documento' => $paciente->getDocumento(),
            'edad' => $paciente->getEdad(),
            'telefono' => $paciente->getTelefono(),
            'email' => $paciente->getEmail(),
            'alergias' => $paciente->getAlergias()
        ];
    }
}
