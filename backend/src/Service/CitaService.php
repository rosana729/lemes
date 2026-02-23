<?php

namespace App\Service;

use App\Entity\Cita;
use App\Entity\Paciente;
use App\Entity\Usuario;
use Doctrine\ORM\EntityManagerInterface;

/**
 * Servicio de Citas
 * 
 * Maneja operaciones CRUD de citas médicas
 */
class CitaService
{
    private EntityManagerInterface $em;

    public function __construct(EntityManagerInterface $em)
    {
        $this->em = $em;
    }

    /**
     * Obtener todas las citas
     */
    public function listarTodas(): array
    {
        $citas = $this->em->getRepository(Cita::class)->findAll();
        return array_map(fn($c) => $this->formatear($c), $citas);
    }

    /**
     * Obtener cita por ID
     */
    public function obtenerPorId(int $id): ?Cita
    {
        return $this->em->getRepository(Cita::class)->find($id);
    }

    /**
     * Listar citas deun paciente
     */
    public function listarPorPaciente(int $pacienteId): array
    {
        $citas = $this->em->getRepository(Cita::class)
            ->findBy(['paciente' => $pacienteId]);
        return array_map(fn($c) => $this->formatear($c), $citas);
    }

    /**
     * Listar citas de un doctor
     */
    public function listarPorDoctor(int $doctorId): array
    {
        $citas = $this->em->getRepository(Cita::class)
            ->findBy(['doctor' => $doctorId]);
        return array_map(fn($c) => $this->formatear($c), $citas);
    }

    /**
     * Crear nueva cita
     */
    public function crear(array $datos): Cita
    {
        // Validar referencias
        $paciente = $this->em->getRepository(Paciente::class)->find($datos['paciente_id']);
        $doctor = $this->em->getRepository(Usuario::class)->find($datos['doctor_id']);

        if (!$paciente || !$doctor) {
            throw new \Exception('Paciente o doctor no encontrado', 404);
        }

        $cita = new Cita();
        $cita->setPaciente($paciente);
        $cita->setDoctor($doctor);
        $cita->setFecha($datos['fecha']);
        $cita->setHora($datos['hora']);
        $cita->setEspecialidad($datos['especialidad']);
        $cita->setMotivo($datos['motivo'] ?? null);
        $cita->setEstado($datos['estado'] ?? 'programada');

        $this->em->persist($cita);
        $this->em->flush();

        return $cita;
    }

    /**
     * Actualizar cita
     */
    public function actualizar(int $id, array $datos): Cita
    {
        $cita = $this->obtenerPorId($id);
        if (!$cita) {
            throw new \Exception('Cita no encontrada', 404);
        }

        if (isset($datos['fecha'])) $cita->setFecha($datos['fecha']);
        if (isset($datos['hora'])) $cita->setHora($datos['hora']);
        if (isset($datos['estado'])) $cita->setEstado($datos['estado']);
        if (isset($datos['motivo'])) $cita->setMotivo($datos['motivo']);
        if (isset($datos['notas'])) $cita->setNotas($datos['notas']);

        $this->em->flush();

        return $cita;
    }

    /**
     * Eliminar cita
     */
    public function eliminar(int $id): bool
    {
        $cita = $this->obtenerPorId($id);
        if (!$cita) {
            throw new \Exception('Cita no encontrada', 404);
        }

        $this->em->remove($cita);
        $this->em->flush();

        return true;
    }

    /**
     * Formatear cita para respuesta API
     */
    public function formatear(Cita $cita): array
    {
        return [
            'id' => $cita->getId(),
            'paciente' => [
                'id' => $cita->getPaciente()->getId(),
                'nombre' => $cita->getPaciente()->getNombre(),
                'apellido' => $cita->getPaciente()->getApellido()
            ],
            'doctor' => [
                'id' => $cita->getDoctor()->getId(),
                'nombre' => $cita->getDoctor()->getNombre()
            ],
            'fecha' => $cita->getFecha(),
            'hora' => $cita->getHora(),
            'especialidad' => $cita->getEspecialidad(),
            'estado' => $cita->getEstado(),
            'motivo' => $cita->getMotivo()
        ];
    }
}
