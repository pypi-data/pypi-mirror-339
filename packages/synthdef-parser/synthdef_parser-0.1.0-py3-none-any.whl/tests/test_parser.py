import unittest
import os
from synthdef_parser.parser import parse_synthdef_file


class TestSynthDefParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_files_dir = os.path.join(
            os.path.dirname(__file__), "test_files")

    def test_parse_basic_sine(self):
        """Test parsing a simple sine SynthDef."""
        result = parse_synthdef_file(os.path.join(
            self.test_files_dir, "testSine.scsyndef"))
        synth = result["synths"]["testSine"]

        self.assertEqual(len(synth["ugens"]), 4)

        ugen_names = [u["name"] for u in synth["ugens"]]
        self.assertIn("Control", ugen_names)
        self.assertIn("SinOsc", ugen_names)
        self.assertIn("BinaryOpUGen", ugen_names)
        self.assertIn("Out", ugen_names)

    def test_parse_buffer_ugens(self):
        """Test buffer references (e.g., PlayBuf)."""
        result = parse_synthdef_file(os.path.join(
            self.test_files_dir, "testPlayBuf.scsyndef"))
        synth = result["synths"]["testPlayBuf"]

        playbuf = next(u for u in synth["ugens"] if u["name"] == "PlayBuf")
        self.assertEqual(playbuf["buffer"], 0)

    def test_parse_variants(self):
        """Test SynthDef variants (presets)."""
        result = parse_synthdef_file(os.path.join(
            self.test_files_dir, "testWithVariants.scsyndef"))
        synth = result["synths"]["testWithVariants"]

        self.assertIn("testWithVariants.high", synth["variants"])
        self.assertAlmostEqual(
            synth["variants"]["testWithVariants.high"][1], 880.0)


if __name__ == '__main__':
    unittest.main()
