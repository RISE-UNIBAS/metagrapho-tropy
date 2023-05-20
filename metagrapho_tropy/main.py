""" main.py
=============
Main. """

from metagrapho_tropy.client import Client

import logging
import os.path

DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
TEST = f"{PARENT_DIR}/test"


def main_process():
    Client().process_tropy(tropy_file_path=f"{TEST}/sample_input.json", item_type="Foto", item_image_index=1)


def main_download():
    mapping_file_path = f"{TEST}/mapping_input.csv"
    Client().download(mapping_file_path=mapping_file_path)


def main_enrich():
    tropy_file_path = f"{TEST}/sample_input_updated.json"
    download_file_path = f"{TEST}/download_input.json"
    Client().enrich_tropy(tropy_file_path=tropy_file_path,
                          download_file_path=download_file_path
                          # lowest_common_dir="C:/Users/hinder0000/PycharmProjects",
                          )



if __name__ == "__main__":
    main_enrich()
