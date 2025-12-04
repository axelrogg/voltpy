import math
import unittest
from src.voltpy import CatenaryState, CatenaryApparentLoad, Conductor, MechAnalysis, MechAnalysisZone, SagTensionAnalyzer, MechAnalysisHypothesis


class TestMechAnalysis(unittest.TestCase):
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
            overall_diameter=100,
            mass=1000,
            rated_strength=1000,
            resistance_dc=0,
            elastic_modulus=1,
            thermal_exp_factor=0,
        )
        self.mech_a = MechAnalysis(self.conductor, MechAnalysisZone.A)
        self.mech_b = MechAnalysis(self.conductor, MechAnalysisZone.B)
        self.mech_c = MechAnalysis(self.conductor, MechAnalysisZone.C)

    def test_ice_weight(self):
        with self.assertRaises(ValueError):
            self.mech_a.ice_weight
        self.assertAlmostEqual(self.mech_b.ice_weight, 0.18 * math.sqrt(self.conductor.overall_diameter))
        self.assertAlmostEqual(self.mech_c.ice_weight, 0.36 * math.sqrt(self.conductor.overall_diameter))

    def test_eds(self):
        eds_no_dampers = self.mech_a.eds()
        self.assertIsInstance(eds_no_dampers, CatenaryState)
        self.assertAlmostEqual(eds_no_dampers.tense, 0.15 * self.conductor.rated_strength)

        eds_with_dampers = self.mech_a.eds(with_dampers=True)
        self.assertIsInstance(eds_with_dampers, CatenaryState)
        self.assertAlmostEqual(eds_with_dampers.tense, 0.22 * self.conductor.rated_strength)

    def test_chs(self):
        chs_state = self.mech_a.chs(temp=-5, rts_factor=0.2)
        self.assertIsInstance(chs_state, CatenaryState)
        self.assertAlmostEqual(chs_state.tense, 0.2 * self.conductor.rated_strength)
        self.assertEqual(chs_state.temp, -5)

    def test_overload(self):
        overload_no_wind_no_ice = self.mech_a.overload()
        self.assertIsInstance(overload_no_wind_no_ice, CatenaryApparentLoad)
        self.assertAlmostEqual(overload_no_wind_no_ice.wind_load, 0)
        self.assertAlmostEqual(overload_no_wind_no_ice.effective_load, self.conductor.unit_weight)

    def test_overload_factor(self):
        apparent_load = CatenaryApparentLoad(wind_load=3, effective_load=4)
        overload_factor = self.mech_a.overload_factor(apparent_load)
        self.assertAlmostEqual(overload_factor, 5 / self.conductor.unit_weight)

    def test_ruling_span(self):
        spans = [100, 200, 300]
        ruling_span = self.mech_a.ruling_span(spans)
        self.assertAlmostEqual(ruling_span, math.sqrt((100**3 + 200**3 + 300**3) / (100 + 200 + 300)))


class TestSagTensionAnalyzer(unittest.TestCase):
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
            overall_diameter=100,
            mass=1000,
            rated_strength=1000,
            resistance_dc=0,
            elastic_modulus=1,
            thermal_exp_factor=0,
        )
        self.mech = MechAnalysis(self.conductor, MechAnalysisZone.A)
        self.hypotheses = [
            MechAnalysisHypothesis(temp=15, rts_factor=0.15),
            MechAnalysisHypothesis(temp=-5, rts_factor=0.25),
        ]
        self.analyzer = SagTensionAnalyzer(self.mech, self.hypotheses)

    def test_find_controlling_state(self):
        controller = self.analyzer.find_controlling_state(span=100)
        self.assertIsInstance(controller, MechAnalysisHypothesis)

    def test_tbl(self):
        tbl = self.analyzer.tbl(spans=[100, 200])
        self.assertIsInstance(tbl, list)
        self.assertEqual(len(tbl), 2)
        self.assertIn("span", tbl[0])
        self.assertIn("results", tbl[0])
        self.assertEqual(len(tbl[0]["results"]), 2)


if __name__ == "__main__":
    unittest.main()
