import unittest
import spaCy

class spacyTest(unittest.TestCase):
    def test_correct_output(self):
        self.assertEqual(spaCy.extract_entities("hvor er Obama født?"), ['Obama'])  # add assertion here
        self.assertEqual(spaCy.extract_entities("Aalborg er i Danmark"), ['Aalborg', 'Danmark'])  # add assertion here
        self.assertEqual(spaCy.extract_entities("Hvordan åbner man en flaske vin?"), [])  # add assertion here
        self.assertEqual(spaCy.extract_entities("Jeg bor i New York"), ['New York'])
        self.assertEqual(spaCy.extract_entities("Hvem er Elon Musk"), ['Elon Musk'])

if __name__ == '__main__':
    unittest.main()
