import math
import unittest
from src.voltpy import CatenaryApparentLoad, CatenaryModel, CatenaryState, Conductor


class TestCatenaryApparentLoad(unittest.TestCase):
    def test_catenary_apparent_load_resultant(self):
        load = CatenaryApparentLoad(wind_load=3, effective_load=4)
        self.assertAlmostEqual(load.resultant, math.sqrt(3 ** 2 + 4** 2))

    def test_catenary_apparent_load_swing_angle(self):
        load = CatenaryApparentLoad(wind_load=1, effective_load=1)
        self.assertAlmostEqual(load.swing_angle, math.pi / 4)


class TestCatenaryModel(unittest.TestCase):
    def setUp(self):
        self.conductor = Conductor(
            designation="test",
            legacy_code="test",
            al_area=0,
            steel_area=0,
            total_area=100,
            al_strands=0,
            steel_strands=0,
            core_diameter=0,
            overall_diameter=0,
            mass=1000,
            rated_strength=0,
            resistance_dc=0,
            elastic_modulus=1,
            thermal_exp_factor=0,
        )
        self.model = CatenaryModel(self.conductor)

    def test_catenary_model_cos(self):
        state0 = CatenaryState(temp=0, tense=100, weight=1)
        temp1 = 0
        weight1 = 1
        span = 100
        state1 = self.model.cos(state0, temp1, weight1, span)
        self.assertIsInstance(state1, CatenaryState)
        self.assertAlmostEqual(state1.tense, state0.tense)


if __name__ == "__main__":
    unittest.main()
