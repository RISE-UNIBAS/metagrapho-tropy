"""" test.py
=============
Unittest. """

import os.path
import unittest
from metagrapho_tropy.client import Client

DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
SAMPLE = f"{PARENT_DIR}/sample"


class TestClient(unittest.TestCase):
    """ Test Client class. """

    def setUp(self) -> None:
        self.client = Client()
        self.export = f"{DIR}/input/export.json"
        self.enrich_gold_standard = f"{DIR}/gold_standard/enrich.json"

    def test_enrich_tropy(self) -> None:
        """ Test Client.enrich_tropy. """

        self.client.enrich_tropy(tropy_file_path=self.export,
                                 download_file_path=f"{SAMPLE}/download_input.json",
                                 tropy_save_path=f"{DIR}/output.json",
                                 lines=True)

        with open(self.enrich_gold_standard, mode="r", encoding="utf-8") as file:
            enrich_gold_standard = file.read()
        with open(f"{DIR}/output.json", mode="r", encoding="utf-8") as file:
            output = file.read()

        self.assertEqual(enrich_gold_standard, output)


if __name__ == '__main__':
    unittest.main()
