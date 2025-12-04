import unittest
import sqlite3
from src.voltpy import Conductor, ConductorRepository
from src.voltpy.conductor import GRAVITY


class TestConductorRepository(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.conn.execute(
            """
            CREATE TABLE conductors (
                designation TEXT,
                legacy_code TEXT,
                al_area REAL,
                steel_area REAL,
                total_area REAL,
                al_strands INTEGER,
                steel_strands INTEGER,
                core_diameter REAL,
                overall_diameter REAL,
                mass REAL,
                rated_strength REAL,
                resistance_dc REAL,
                elastic_modulus REAL,
                thermal_exp_factor REAL
            )
            """
        )
        self.conn.execute(
            """
            INSERT INTO conductors VALUES (
                '337-AL1/44-ST1A:LA 380',
                'LA 380',
                337.3,
                43.7,
                381.0,
                54,
                7,
                8.46,
                25.38,
                932,
                107.18,
                0.0857,
                6.9e3,
                1.93e-5
            )
            """
        )
        self.repo = ConductorRepository(db_path=":memory:")
        self.repo.conn = self.conn

    def tearDown(self):
        self.conn.close()

    def test_get_conductor_by_designation(self):
        conductor = self.repo.get(designation="337-AL1/44-ST1A:LA 380")
        self.assertIsInstance(conductor, Conductor)
        self.assertEqual(conductor.designation, "337-AL1/44-ST1A:LA 380")

    def test_get_conductor_by_legacy_code(self):
        conductor = self.repo.get(legacy_code="LA 380")
        self.assertIsInstance(conductor, Conductor)
        self.assertEqual(conductor.legacy_code, "LA 380")

    def test_get_conductor_not_found(self):
        with self.assertRaises(ValueError):
            self.repo.get(designation="non-existent")

    def test_get_conductor_no_identifier(self):
        with self.assertRaises(ValueError):
            self.repo.get()


class TestConductor(unittest.TestCase):
    def setUp(self):
        self.conductor = Conductor(
            designation="test",
            legacy_code="test",
            al_area=0,
            steel_area=0,
            total_area=0,
            al_strands=0,
            steel_strands=0,
            core_diameter=0,
            overall_diameter=0,
            mass=1000,
            rated_strength=0,
            resistance_dc=0,
            elastic_modulus=0,
            thermal_exp_factor=0,
        )

    def test_conductor_unit_weight(self):
        self.assertAlmostEqual(
            self.conductor.unit_weight, self.conductor.mass * GRAVITY * 1e-4
        )

    def test_conductor_unit_weight_override(self):
        self.conductor.unit_weight = 1.0
        self.assertEqual(self.conductor.unit_weight, 1.0)


if __name__ == "__main__":
    unittest.main()
