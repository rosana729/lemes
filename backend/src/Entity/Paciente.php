<?php

namespace App\Entity;

use Doctrine\ORM\Mapping as ORM;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;

#[ORM\Entity]
#[ORM\Table(name: 'pacientes')]
class Paciente
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 100)]
    private string $nombre = '';

    #[ORM\Column(length: 100)]
    private string $apellido = '';

    #[ORM\Column(length: 20, unique: true)]
    private string $documento = '';

    #[ORM\Column(length: 10, nullable: true)]
    private ?string $fecha_nacimiento = null;

    #[ORM\Column(nullable: true)]
    private ?int $edad = null;

    #[ORM\Column(length: 10, nullable: true)]
    private ?string $genero = null;

    #[ORM\Column(length: 20)]
    private string $telefono = '';

    #[ORM\Column(length: 100, nullable: true)]
    private ?string $email = null;

    #[ORM\Column(length: 200, nullable: true)]
    private ?string $direccion = null;

    #[ORM\Column(length: 100, nullable: true)]
    private ?string $ciudad = null;

    #[ORM\Column(type: 'text', nullable: true)]
    private ?string $alergias = null;

    #[ORM\Column(type: 'text', nullable: true)]
    private ?string $antecedentes_medicos = null;

    #[ORM\Column(type: 'datetime')]
    private \DateTime $creado_en;

    #[ORM\OneToMany(mappedBy: 'paciente', targetEntity: Cita::class)]
    private Collection $citas;

    public function __construct()
    {
        $this->citas = new ArrayCollection();
        $this->creado_en = new \DateTime();
    }

    public function getId(): ?int { return $this->id; }
    public function getNombre(): string { return $this->nombre; }
    public function setNombre(string $nombre): self { $this->nombre = $nombre; return $this; }
    public function getApellido(): string { return $this->apellido; }
    public function setApellido(string $apellido): self { $this->apellido = $apellido; return $this; }
    public function getDocumento(): string { return $this->documento; }
    public function setDocumento(string $documento): self { $this->documento = $documento; return $this; }
    public function getEdad(): ?int { return $this->edad; }
    public function setEdad(?int $edad): self { $this->edad = $edad; return $this; }
    public function getTelefono(): string { return $this->telefono; }
    public function setTelefono(string $telefono): self { $this->telefono = $telefono; return $this; }
    public function getEmail(): ?string { return $this->email; }
    public function setEmail(?string $email): self { $this->email = $email; return $this; }
    public function getAlergias(): ?string { return $this->alergias; }
    public function setAlergias(?string $alergias): self { $this->alergias = $alergias; return $this; }
}
