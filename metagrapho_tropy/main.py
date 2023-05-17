""" main.py
=============
Main. """

from metagrapho_tropy.client import Client

import logging
import os.path

DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
TEST = f"{PARENT_DIR}/test"


def main():
    tropy_file_path = f"{TEST}/sample_input_updated.json"
    mapping_file_path = f"{TEST}/mapping_input.csv"
    logging.basicConfig(format="%(asctime)s %(levelname)s:%(name)s:%(message)s",
                        filename="main.log",
                        level=logging.DEBUG)
    logging.info(f"Started Client().enrich_tropy(tropy_file_path={tropy_file_path}, mapping_file_path={mapping_file_path})")
    Client().enrich_tropy(tropy_file_path=tropy_file_path,
                          mapping_file_path=mapping_file_path
                          # lowest_common_dir="C:/Users/hinder0000/PycharmProjects",
                          )
    logging.info("Finished")


if __name__ == "__main__":
    main()


