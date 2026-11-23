import unittest
import tempfile
import json
from pathlib import Path
from demo import run

class ExperimentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.output=Path(cls.temp.name)/'results.json'
        cls.r=run(cls.output)
    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()
    def test_output_matches_returned_result(self):
        self.assertEqual(json.loads(self.output.read_text()),self.r)
    def test_score_ranges(self):
        self.assertTrue(all(0<=self.r[k]<=1 for k in ['precision','recall','f1','average_precision','false_positive_rate']))
    def test_counts(self):
        self.assertEqual(sum(map(sum,self.r['confusion_matrix'])),560)
    def test_training_normal_only(self):
        self.assertEqual(self.r['train_normal_rows'],800)

if __name__ == "__main__":
    unittest.main()
