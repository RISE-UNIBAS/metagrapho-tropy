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
    logging.basicConfig(format="%(asctime)s %(levelname)s:%(name)s:%(message)s",
                        filename="main.log",
                        level=logging.DEBUG)
    logging.info('Started')
    Client().enrich(tropy_file_path=f"{TEST}/sample_input.json",
                    item_image_index=1,
                    lowest_common_dir="C:/Users/hinder0000/PycharmProjects")
    logging.info('Finished')


if __name__ == "__main__":
    main()


