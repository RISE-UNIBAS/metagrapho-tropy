""" tropy.py
=============
 Tropy class. """

from __future__ import annotations
from metagrapho_tropy.utility import Utility
from metagrapho_tropy.item import Item


class Tropy:
    """ A representation of a Tropy export.

    :param json_export: loaded Tropy JSON export file
    """

    def __init__(self,
                 json_export: dict) -> None:
        self.json_export = json_export
        self.graph = self.json_export["@graph"]

    def save(self,
             file_path) -> None:
        """ Save Tropy export to file path.

        :param file_path: complete path to file including filename and extension
        """

        Utility.save_json(data=self.json_export,
                          file_path=file_path)

    def get_types(self) -> set:
        """ Get deduplicated values of the items' type fields. """

        types = set()
        for item in self.graph:
            parsed_item = Item()
            parsed_item.copy_metadata_from_dict(item)
            types.add(parsed_item.type)

        return types
