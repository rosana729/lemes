<?php

namespace App\Entity;

use Doctrine\ORM\Mapping as ORM;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;

#[ORM\Entity]
#[ORM\Table(name: 'usuarios')]
class Usuario
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 100)]
    private string $nombre = '';

    #[ORM\Column(length: 100, unique: true)]
    private string $email = '';

    #[ORM\Column(length: 255)]
    private string $contraseña = '';

    #[ORM\Column(length: 20)]
    private string $rol = 'doctor'; // doctor, secretaria, admin

    #[ORM\Column(length: 100, nullable: true)]
    private ?string $especialidad = null;

    #[ORM\Column(length: 20, nullable: true)]
    private ?string $telefono = null;

    #[ORM\Column]
    private bool $activo = true;

    #[ORM\Column(type: 'datetime')]
    private \DateTime $creado_en;

    #[ORM\OneToMany(mappedBy: 'doctor', targetEntity: Cita::class)]
    private Collection $citas;

    public function __construct()
    {
        $this->citas = new ArrayCollection();
        $this->creado_en = new \DateTime();
    }

    public function getId(): ?int { return $this->id; }
    public function getNombre(): string { return $this->nombre; }
    public function setNombre(string $nombre): self { $this->nombre = $nombre; return $this; }
    public function getEmail(): string { return $this->email; }
    public function setEmail(string $email): self { $this->email = $email; return $this; }
    public function getContraseña(): string { return $this->contraseña; }
    public function setContraseña(string $contraseña): self { $this->contraseña = $contraseña; return $this; }
    public function getRol(): string { return $this->rol; }
    public function setRol(string $rol): self { $this->rol = $rol; return $this; }
    public function getEspecialidad(): ?string { return $this->especialidad; }
    public function setEspecialidad(?string $especialidad): self { $this->especialidad = $especialidad; return $this; }
    public function getTelefono(): ?string { return $this->telefono; }
    public function setTelefono(?string $telefono): self { $this->telefono = $telefono; return $this; }
    public function isActivo(): bool { return $this->activo; }
    public function setActivo(bool $activo): self { $this->activo = $activo; return $this; }
    public function getCitasAs(): Collection { return $this->citas; }
}
