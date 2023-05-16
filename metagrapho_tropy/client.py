""" client.py
=============
Client class. """
import json
from dataclasses import dataclass
from metagrapho_tropy.item import Item
from metagrapho_tropy.api import TranskribusProcessingAPI
from metagrapho_tropy.tropy import Tropy
from metagrapho_tropy.utility import Utility


@dataclass
class Client:
    """ Standalone client.

     :param email: User's Transkribus email
     :param password: User's Transkribus password
     """

    email: str = None
    password: str = None

    def __post_init__(self):
        if self.email is None or self.password is None:
            try:
                from metagrapho_tropy.credentials import TRANSKRIBUS_EMAIL, TRANSKRIBUS_PASSWORD
                self.email = TRANSKRIBUS_EMAIL
                self.password = TRANSKRIBUS_PASSWORD
            except (ModuleNotFoundError, ImportError):
                raise

    @staticmethod
    def validate(tropy_file_path: str,
                 item_type: str = None,
                 item_tag: str = None,
                 item_image_index: int = None,
                 line_model_id: int = None,
                 atr_model_id: int = None,
                 ) -> Tropy:
        """ Validate and initialize user input. """

        try:
            tropy = Tropy(json_export=Utility.load_json(file_path=tropy_file_path))
        except FileNotFoundError:
            f"Error: {tropy_file_path} not found!"
            raise
        except json.JSONDecodeError:
            print(f"Error: {tropy_file_path} is not a valid Tropy export file!")
            raise
        if item_type is not None:
            try:
                assert item_type in tropy.get_types()
            except AssertionError:
                print(f"Error: {item_type} is a type not found in {tropy_file_path}!")

        # TODO: add validation for line_model_id, atr_model_id

        return tropy

    def enrich(self,
               tropy_file_path: str,
               item_type: str = None,
               item_tag: str = None,
               item_image_index: int = None,
               line_model_id: int = None,
               atr_model_id: int = None,
               ) -> None:
        """ Enrich selected Tropy items with image to text transcriptions generated by the Transkribus metagrapho API.

        Items are selected via type and tag (optional and conjunctive). If no selection is made, all items are
        enriched. Images are selected via their ordering. If no specific image is selected, to text is applied to all
        images.


        :param tropy_file_path: complete path to Tropy export file including filename and extension
        :param item_type: the item type, defaults to None
        :param item_tag: the item tag, defaults to None
        :param item_image_index: the selected item's index, defaults to None
        :param line_model_id: the Transkribus line model ID, defaults to None
        :param atr_model_id: the Transkribus ATR model ID, defaults to None
        """

        tropy = self.validate(tropy_file_path=tropy_file_path,
                              item_type=item_type,
                              item_tag=item_tag,
                              item_image_index=item_image_index,
                              line_model_id=line_model_id,
                              atr_model_id=atr_model_id)

        for item in tropy.graph:
            parsed_item = Item()
            parsed_item.copy_metadata_from_dict(item)

            if item_image_index is None:
                for image in parsed_item.photo:
                    pass
            else:
                # put this into function:
                try:
                    print(parsed_item.photo[item_image_index])

                except IndexError:
                    print(f"Error: {parsed_item.identifier} has no image with index {item_image_index}!")
                except TypeError:
                    print(f"Error: {parsed_item.identifier} has no image!")

        # TODO: log with item id and metagrapho process id