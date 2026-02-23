<?php

namespace App\Entity;

use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity]
#[ORM\Table(name: 'citas')]
class Cita
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\ManyToOne(targetEntity: Paciente::class, inversedBy: 'citas')]
    #[ORM\JoinColumn(nullable: false)]
    private Paciente $paciente;

    #[ORM\ManyToOne(targetEntity: Usuario::class, inversedBy: 'citas')]
    #[ORM\JoinColumn(nullable: false)]
    private Usuario $doctor;

    #[ORM\Column(length: 10)]
    private string $fecha = '';

    #[ORM\Column(length: 5)]
    private string $hora = '';

    #[ORM\Column(length: 100)]
    private string $especialidad = '';

    #[ORM\Column(type: 'text', nullable: true)]
    private ?string $motivo = null;

    #[ORM\Column(length: 20)]
    private string $estado = 'programada'; // programada, realizada, cancelada

    #[ORM\Column(type: 'text', nullable: true)]
    private ?string $notas = null;

    #[ORM\Column(type: 'datetime')]
    private \DateTime $creado_en;

    public function __construct()
    {
        $this->creado_en = new \DateTime();
    }

    public function getId(): ?int { return $this->id; }
    public function getPaciente(): Paciente { return $this->paciente; }
    public function setPaciente(Paciente $paciente): self { $this->paciente = $paciente; return $this; }
    public function getDoctor(): Usuario { return $this->doctor; }
    public function setDoctor(Usuario $doctor): self { $this->doctor = $doctor; return $this; }
    public function getFecha(): string { return $this->fecha; }
    public function setFecha(string $fecha): self { $this->fecha = $fecha; return $this; }
    public function getHora(): string { return $this->hora; }
    public function setHora(string $hora): self { $this->hora = $hora; return $this; }
    public function getEspecialidad(): string { return $this->especialidad; }
    public function setEspecialidad(string $especialidad): self { $this->especialidad = $especialidad; return $this; }
    public function getMotivo(): ?string { return $this->motivo; }
    public function setMotivo(?string $motivo): self { $this->motivo = $motivo; return $this; }
    public function getEstado(): string { return $this->estado; }
    public function setEstado(string $estado): self { $this->estado = $estado; return $this; }
    public function getNotas(): ?string { return $this->notas; }
    public function setNotas(?string $notas): self { $this->notas = $notas; return $this; }
}
