""" utility.py
=============
Utility class. """

from __future__ import annotations
import csv
from json import load, dump
from typing import List, Dict, Union


class Utility:
    """ A collection of utility functions. """

    @staticmethod
    def load_json(file_path: str) -> dict:
        """ Load a JSON object from file.

        :param file_path: complete path to file including filename and extension
        """

        with open(file_path, encoding="utf-8") as file:
            loaded = load(file)

            return loaded

    @staticmethod
    def save_json(data: Union[List, Dict],
                  file_path: str) -> None:
        """ Save data as JSON file.

        :param data: the data to be saved
        :param file_path: complete path to file including filename and extension
        """

        with open(file_path, "w") as file:
            dump(data, file, indent=4)

    @staticmethod
    def load_csv(file_path: str) -> list:
        """ Load CSV from file as list.

        :param file_path: complete path to file including filename and extension
        """

        with open(file_path, "r") as file:
            return [line for line in csv.reader(file)]

    @staticmethod
    def save_csv(header: List,
                 data: List,
                 file_path: str) -> None:
        """ Save data as CSV file.

        :param header: the header
        :param data: the data to be saved
        :param file_path: complete path to file including filename and extension
        """

        with open(file_path, 'w', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(data)