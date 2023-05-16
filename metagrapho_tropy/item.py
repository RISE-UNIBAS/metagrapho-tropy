""" items.py
=============
Item classes. """

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Dict


@dataclass
class Item:
    """ A representation of a Tropy item.

    Parameter naming prioritizes Tropy naming conventions for fields over PEP.

    :param template: http://purl.org/dc/elements/1.1/type
    :param title: http://purl.org/dc/elements/1.1/title
    :param LocationShown: http://iptc.org/std/Iptc4xmpExt/2008-02-29/LocationShown
    :param LocationCreated: http://iptc.org/std/Iptc4xmpExt/2008-02-29/LocationCreated
    :param PersonInImage: http://iptc.org/std/Iptc4xmpExt/2008-02-29/PersonInImage
    :param PersonInImageWDetails: http://iptc.org/std/Iptc4xmpExt/2008-02-29/PersonInImageWDetails
    :param creator: http://purl.org/dc/elements/1.1/creator
    :param dcterms_creator: http://purl.org/dc/terms/creator
    :param date: http://purl.org/dc/elements/1.1/date
    :param dcterms_date: http://purl.org/dc/terms/date
    :param type: http://purl.org/dc/elements/1.1/type
    :param source: http://purl.org/dc/elements/1.1/source
    :param collection: https://tropy.org/v1/tropy#collection
    :param box: https://tropy.org/v1/tropy#box
    :param folder: https://tropy.org/v1/tropy#folder
    :param object: http://www.europeana.eu/schemas/edm/object
    :param identifier: http://purl.org/dc/elements/1.1/identifier
    :param rights: http://purl.org/dc/elements/1.1/rights
    :param hasPart: http://purl.org/dc/terms/hasPart
    :param isPartOf: http://purl.org/dc/terms/isPartOf
    :param isRelatedTo: http://www.europeana.eu/schemas/edm/isRelatedTo
    :param photo: https://tropy.org/v1/tropy#photo
    :param list: Tropy list
    :param tag: Tropy tag
    :param note: Tropy note
    """

    template: str = "https://tropy.org/v1/templates/id#iTbU0YBP"
    LocationShown: str = None
    LocationCreated: str = None
    PersonInImage: str = None
    PersonInImageWDetails: str = None
    title: str = None
    creator: str = None
    dcterms_creator: str = None
    date: str = None
    dcterms_date: str = None
    type: str = None
    source: str = None
    collection: str = None
    box: str = None
    folder: str = None
    object: str = None
    identifier: str = None
    rights: str = None
    hasPart: str = None
    isPartOf: str = None
    isRelatedTo: str = None
    photo: List[Dict] = None
    list: List[str] = None
    tag: list = None
    note: list = None

    @staticmethod
    def get_normalized_tropy_field_names() -> dict:
        """ Get normalized keys. """

        normalized_keys = {"dcterms:creator": "dcterms_creator",
                           "dcterms:date": "dcterms_date"}

        return normalized_keys

    @staticmethod
    def get_inscribed_map() -> dict:
        """ Get mapping of field to inscribed field. """

        inscribed_map = {"creator": "dcterms_creator",
                         "date": "dcterms_date",
                         "LocationShown": "LocationCreated",
                         "PersonInImage": "PersonInImageWDetails"}

        return inscribed_map

    def serialize(self) -> dict:
        """ Serialize item as dictionary. """

        serialized = {"@item": "item"}
        serialized.update(asdict(self))

        return serialized

    def copy_metadata_from_dict(self, dictionary: dict) -> None:
        """ Copy metadata from dictionary. """

        try:
            for key in dictionary.keys():
                try:
                    normalized_key = self.get_normalized_tropy_field_names()[key]
                    self.__setattr__(normalized_key, dictionary[key])
                except KeyError:
                    pass
                self.__setattr__(key, dictionary[key])
        except Exception:
            raise

    def copy_metadata_from_item(self,
                                item: Item,
                                *args):
        """ Copy metadata from item.

        :param item: the item from which metadata is copied
        :param args: deselected attributes (values not copied)
        """

        for key in item.serialize().keys():
            try:
                if key in args:
                    continue
                else:
                    self.__setattr__(key, item.serialize()[key])
            except Exception:
                raise
