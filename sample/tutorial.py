""" tutorial.py
===============
Script supporting the tutorial at https://github.com/RISE-UNIBAS/metagrapho-tropy#tutorial. """

from metagrapho_tropy.client import Client
import os.path

DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
SAMPLE = f"{PARENT_DIR}/sample"


def process():
    Client().process_tropy(tropy_file_path=f"{SAMPLE}/sample_input.json",
                           item_type="Foto",
                           item_image_index=1)


def download():
    mapping_file_path = f"{SAMPLE}/download_input.csv"
    Client().download(mapping_file_path=mapping_file_path)


def enrich():
    tropy_file_path = f"{SAMPLE}/sample_input_updated.json"
    download_file_path = f"{SAMPLE}/download_input.json"
    Client().enrich_tropy(tropy_file_path=tropy_file_path,
                          download_file_path=download_file_path,
                          lines=True
                          # lowest_common_dir="C:/Users/hinder0000/PycharmProjects",
                          )


if __name__ == "__main__":
    print(f"Use Client to continue.")

