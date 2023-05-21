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
                                *args) -> None:
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

    @staticmethod
    def transform_coordinates(coordinates: str) -> list[int]:
        """ Transform Transkribus coordinates points to Tropy coordinates.

        Sample Transkribus coordinates points: '192,458 192,514 332,514 332,458'. Read the tuple '192,
        458' as 'x, y' where '0, 0' is the top left corner of an image. Note that the y-axis is inverted (going down
        is positive).

        :param coordinates: value of Transkribus 'coords' key
        """

        x_coordinates = [int(c.split(",")[0]) for c in coordinates.split(" ")]
        y_coordinates = [int(c.split(",")[1]) for c in coordinates.split(" ")]

        tropy_x = min(x_coordinates)
        tropy_y = min(y_coordinates)
        tropy_width = max(x_coordinates) - tropy_x
        tropy_height = max(y_coordinates) - tropy_y

        return [tropy_x, tropy_y, tropy_width, tropy_height]

    def add_note_element(self,
                         text: str,
                         photo_index: int,
                         language: str = "de"
                         ) -> None:
        """ Add a note element to a photo.

        :param text: the note element's text
        :param photo_index: the photo to which the note will attach
        :param language: the note's language, defaults to 'de'
        """

        note_element = {
            "@type": "Note",
            "text": {
                "@value": text,
                "@language": language
            },
            "html": {
                "@value": f"<p>{text}</p>",
                "@language": language
            }
        }
        try:
            self.photo[photo_index]["note"].append(note_element)
        except KeyError:
            self.photo[photo_index]["note"] = [note_element]

    def add_selection_element(self,
                              text: str,
                              photo_index: int,
                              coords: str,
                              language: str = "de",
                              ):
        """ Add a selection element with a line transcription to a photo.

        :param text: the note element's text
        :param photo_index: the photo to which the note will attach
        :param coords: Transkribus coordinates
        :param language: the note's language, defaults to 'de'
        """

        note_element = {
            "@type": "Note",
            "text": {
                "@value": text,
                "@language": language
            },
            "html": {
                "@value": f"<p>{text}</p>",
                "@language": language
            }
        }
        line_coordinates = self.transform_coordinates(coords)
        selection_element = {
            "@type": "Selection",
            "template": "https://tropy.org/v1/templates/selection",
            "x": line_coordinates[0],
            "y": line_coordinates[1],
            "angle": 0,
            "brightness": 0,
            "contrast": 0,
            "height": line_coordinates[3],
            "hue": 0,
            "mirror": False,
            "negative": False,
            "saturation": 0,
            "sharpen": 0,
            "width": line_coordinates[2],
            "title": {
                "@type": "text",
                "@value": text},
            "note": [note_element]
        }
        try:
            self.photo[photo_index]["selection"].append(selection_element)
        except KeyError:
            self.photo[photo_index]["selection"] = [selection_element]