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
    Client().get_response(4996065)
    exit()
    logging.basicConfig(format="%(asctime)s %(levelname)s:%(name)s:%(message)s",
                        filename="main.log",
                        level=logging.DEBUG)
    logging.info('Started')
    Client().process_tropy(tropy_file_path=f"{TEST}/sample_input.json",
                           item_type="Foto",
                           item_image_index=1,
                           # lowest_common_dir="C:/Users/hinder0000/PycharmProjects",
                           )
    logging.info('Finished')


if __name__ == "__main__":
    main()


