"""
Module `conductor`

Provides classes and utilities for modeling electrical conductors 
and accessing conductor data from a SQLite database.

This module includes:

- `Conductor`: A dataclass representing an overhead line conductor, 
  with mechanical, geometric, and electrical properties. Includes 
  a computed `unit_weight` property with optional override.

- `ConductorRepository`: A repository class to retrieve conductor 
  information from a SQLite database by designation or legacy code.

Constants:
    GRAVITY (float): Acceleration due to gravity, used for weight 
                     calculations (m/s²).
"""


import sqlite3
from dataclasses import dataclass


GRAVITY = 9.80665


@dataclass
class Conductor:
    """Represents an electrical conductor with mechanical and geometric properties.

    Attributes:
        designation (str): Official designation of the conductor.
        legacy_code (str | None): Legacy or older code for the conductor.
        al_area (float): Aluminum cross-sectional area (mm²).
        steel_area (float): Steel cross-sectional area (mm²).
        total_area (float): Total cross-sectional area (mm²).
        al_strands (int): Number of aluminum strands.
        steel_strands (int): Number of steel strands.
        core_diameter (float): Diameter of the core (mm).
        overall_diameter (float): Overall conductor diameter (mm).
        mass (float): Mass of the conductor per km (kg/km).
        rated_strength (float): Rated tensile strength (daN).
        resistance_dc (float): DC resistance of the conductor (ohm/km).
        elastic_modulus (float): Young's modulus of the conductor material (kN/mm²).
        thermal_exp_factor (float): Thermal expansion coefficient (1/°C).
        _unit_weight_override (float | None): Optional override for the conductor unit weight (daN/m).
    """

    designation: str
    legacy_code: str | None

    al_area: float
    steel_area: float
    total_area: float

    al_strands: int
    steel_strands: int

    core_diameter: float
    overall_diameter: float

    mass: float
    rated_strength: float
    resistance_dc: float

    elastic_modulus: float
    thermal_exp_factor: float

    # This is only so the user can overwrite the conductor's weight
    _unit_weight_override: float | None = None
    
    @property
    def unit_weight(self) -> float:
        """Compute or return the conductor's unit weight (daN/m).

        Returns:
            float: Unit weight of the conductor including any override.
        """
        if self._unit_weight_override:
            return self._unit_weight_override
        return self.mass * GRAVITY * 1e-4  # Turn mass (kg/km) into weight (daN/m)

    @unit_weight.setter
    def unit_weight(self, value: float | None) -> None:
        """Optionally override the conductor unit weight.

        Args:
            value (float | None): New unit weight in daN/m or None to reset.
        """
        self._unit_weight_override = value


class ConductorRepository:
    """Repository for retrieving conductor data from a SQLite database."""

    def __init__(self, db_path: str = "src/voltpy/conductor_db") -> None:
        """Initialize the repository with a SQLite database path.

        Args:
            db_path (str): Path to the conductor database.
        """
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.table = "conductors"

    def get(self, designation: str | None = None, legacy_code: str | None = None) -> Conductor:
        """Retrieve a conductor by designation or legacy code.

        Args:
            designation (str | None): Official designation of the conductor.
            legacy_code (str | None): Legacy or older code of the conductor.

        Raises:
            ValueError: If neither designation nor legacy_code is provided,
                        or if no conductor matches the query.

        Returns:
            Conductor: The conductor object matching the query.
        """

        if not (designation or legacy_code):
            raise ValueError("Need designation or legacy_code to find conductor")
        
        query = f"select * from {self.table} where designation = ? or legacy_code = ? limit 1"

        cur = self.conn.execute(query, (designation, legacy_code))
        row = cur.fetchone()

        if not row:
            raise ValueError(f"Conductor not found for designation={designation} legacy_code={legacy_code}")

        c = Conductor(
            designation=row["designation"],
            legacy_code=row["legacy_code"],
            al_area=row["al_area"],
            steel_area=row["steel_area"],
            total_area=row["total_area"],
            al_strands=row["al_strands"],
            steel_strands=row["steel_strands"],
            core_diameter=row["core_diameter"],
            overall_diameter=row["overall_diameter"],
            mass=row["mass"],
            rated_strength=row["rated_strength"] * 100,  # N to daN
            resistance_dc=row["resistance_dc"],
            elastic_modulus=row["elastic_modulus"],
            thermal_exp_factor=row["thermal_exp_factor"],
        )

        return c
