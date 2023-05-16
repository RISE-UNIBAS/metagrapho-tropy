""" client.py
=============
Client class. """
from __future__ import annotations

import base64
import json
import logging
import os.path
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
                logging.critical(f"File 'credentials.py' not found or not valid!")
                raise

    @staticmethod
    def _repath(image_path: str,
                lowest_common_dir: str) -> str:
        """ Refactor a Tropy image path from machine X to be used on machine Y given the lowest common directory of X
        and Y.

         :param image_path: the Tropy image path
         :param lowest_common_dir: the lowest common directory
         """

        image_dir = lowest_common_dir.split("\\")[-1]
        image_path_split = image_path.split("\\")
        index = image_path_split.index(image_dir)

        return "\\".join(lowest_common_dir.split("\\") + image_path_split[index + 1:])

    @staticmethod
    def _validate(tropy_file_path: str,
                  item_type: str = None,
                  item_tag: str = None,
                  item_image_index: int = None,
                  line_model_id: int = None,
                  atr_model_id: int = None,
                  lowest_common_dir: str = None,
                  ) -> Tropy:
        """ Validate and initialize user input.

        :param tropy_file_path: complete path to Tropy export file including filename and extension
        :param item_type: the item type, defaults to None
        :param item_tag: the item tag, defaults to None
        :param item_image_index: the selected item's index, defaults to None
        :param line_model_id: the Transkribus line model ID, defaults to None
        :param atr_model_id: the Transkribus ATR model ID, defaults to None
        :param lowest_common_dir: lowest common directory, defaults to None
        """

        try:
            tropy = Tropy(json_export=Utility.load_json(file_path=tropy_file_path))
        except FileNotFoundError:
            logging.critical(f"Invalid 'tropy_file_path' parameter: file '{tropy_file_path}' not found!")
            raise
        except json.JSONDecodeError:
            logging.critical(
                f"Invalid 'tropy_file_path' parameter: file '{tropy_file_path}' is not a valid Tropy export "
                f"file!")
            raise
        if item_type is not None:
            try:
                assert item_type in tropy.get_types()
            except AssertionError:
                logging.critical(f"Item type '{item_type}' is a type not found in file '{tropy_file_path}'!")
        if item_tag is not None:
            pass
            # TODO: add validation for item_tag
        if item_image_index is not None:
            pass
            # TODO: add validation for item_image_index
        if line_model_id is not None:
            pass
            # TODO: add validation for line_model_id
        if atr_model_id is not None:
            pass
            # TODO: add validation for atr_model_id
        if lowest_common_dir is not None:
            try:
                assert os.path.isdir(lowest_common_dir)
            except AssertionError:
                logging.critical(
                    f"Invalid 'lowest_common_dir' parameter: directory '{lowest_common_dir}' does not exist!")
                raise

        return tropy

    def _process_image(self,
                       item: Item,
                       item_image_index: int,
                       lowest_common_dir: str,
                       data: list,
                       api: TranskribusProcessingAPI,
                       line_model_id: int = None,
                       atr_model_id: int = None,
                       ) -> None:
        """ Process a single image.

        :param item: a Tropy item
        :param item_image_index: the selected item's index
        :param lowest_common_dir: lowest common directory
        :param data:
        :param api:
        :param line_model_id: the Transkribus line model ID, defaults to None
        :param atr_model_id: the Transkribus ATR model ID, defaults to None
        """

        try:
            image_path = self._repath(image_path=os.path.normpath(item.photo[item_image_index]["path"]),
                                      lowest_common_dir=os.path.normpath(lowest_common_dir))
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read())

            process_id = api.post_processes(line_model_id=line_model_id,
                                            atr_model_id=atr_model_id,
                                            image=encoded_image.decode("utf-8"))
            data.append([item.identifier, process_id])
            logging.info(f"Item {item.identifier} has process ID {process_id}.")
        except IndexError:
            logging.warning(f"Item {item.identifier} has no image with index {item_image_index}!")
        except TypeError:
            logging.warning(f"Item {item.identifier} has no image!")
        except:
            logging.exception("Unexpected exception.")
            raise

    def enrich(self,
               tropy_file_path: str,
               item_type: str = None,
               item_tag: str = None,
               item_image_index: int = None,
               line_model_id: int = None,
               atr_model_id: int = None,
               lowest_common_dir: str = None,
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
        :param lowest_common_dir: lowest common directory, defaults to None
        """

        tropy = self._validate(tropy_file_path=tropy_file_path,
                               item_type=item_type,
                               item_tag=item_tag,
                               item_image_index=item_image_index,
                               line_model_id=line_model_id,
                               atr_model_id=atr_model_id,
                               lowest_common_dir=lowest_common_dir)

        api = TranskribusProcessingAPI(user=self.email,
                                       password=self.password)

        header = ["identifier", "process_id"]
        data = []

        for item in tropy.graph:
            parsed_item = Item()
            parsed_item.copy_metadata_from_dict(item)

            if "processed" in item.tag:
                # TODO: perhaps better via metadata field w/ process ID? requires schema to be adapted...
                logging.info(f"Item {item.identifier} skipped (already processed).")
                continue

            if item_image_index is None:
                for image in parsed_item.photo:
                    pass
                    # TODO: add self._enrich_image
            else:
                self._process_image(item=parsed_item,
                                    item_image_index=item_image_index,
                                    lowest_common_dir=lowest_common_dir,
                                    data=data,
                                    api=api,
                                    line_model_id=line_model_id,
                                    atr_model_id=atr_model_id)

            # TODO: add "processed" tag to item

        # TODO: update and save JSON LD

        Utility.save_csv(header=header,
                         data=data,
                         file_path="item_id2process_id.csv", )


        """get_response = api.get_result(process_id=4982858)
        print(get_response.json())"""
