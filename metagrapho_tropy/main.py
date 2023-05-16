""" main.py
=============
Main. """

from metagrapho_tropy.client import Client

import os.path

DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
TEST = f"{PARENT_DIR}/test"

Client().enrich(tropy_file_path=f"{TEST}/sample_input.json",
                item_image_index=1,
                lowest_common_dir="C:/Users/hinder0000/PycharmProjects")
