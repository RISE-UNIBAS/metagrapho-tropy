""" client.py
=============
Client class. """

from __future__ import annotations
from dataclasses import dataclass
from metagrapho_tropy.item import Item
from metagrapho_tropy.api import TranskribusProcessingAPI
from metagrapho_tropy.tropy import Tropy
from metagrapho_tropy.utility import Utility
import base64
import json
import logging
import os.path
import time


@dataclass
class Client:
    """ Standalone client.

     :param user: User's Transkribus email, defaults to None
     :param password: User's Transkribus password, defaults to None
     :param api: Transkribus metagrapho API wrapper instance, defaults to None
     :param processing_data: map of item IDs to Transkribus metagrapho API processing IDs, defaults to None
     """

    user: str = None
    password: str = None
    api: TranskribusProcessingAPI = None
    processing_data: list = None

    def __post_init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s %(levelname)s:%(name)s:%(message)s",
                            handlers=[logging.FileHandler(f"metagrapho_tropy_{time.strftime('%Y%m%d-%H%M%S')}.log"),
                                      logging.StreamHandler(),
                                      ]
                            )
        logging.info(
            f"Started Client.")
        if self.user is None or self.password is None:
            try:
                from metagrapho_tropy.credentials import TRANSKRIBUS_USER, TRANSKRIBUS_PASSWORD
                self.user = TRANSKRIBUS_USER
                self.password = TRANSKRIBUS_PASSWORD
                self.api = TranskribusProcessingAPI(user=self.user,
                                                    password=self.password)
            except (ModuleNotFoundError, ImportError):
                logging.critical(f"File 'credentials.py' not found or not valid!")
                raise
        self.processing_data = []

    @staticmethod
    def _repath(image_path: str,
                lowest_common_dir: str
                ) -> str:
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
                  tropy_save_path: str = None,
                  mapping_file_path: str = None,
                  mapping_save_path: str = None,
                  item_type: str = None,
                  item_tag: str = None,
                  item_image_index: int = None,
                  line_model_id: int = None,
                  atr_model_id: int = None,
                  lowest_common_dir: str = None,
                  ) -> Tropy:
        """ Validate user input and initialize Tropy instance.

        :param tropy_file_path: complete path to Tropy export file including file extension
        :param tropy_save_path: complete path to updated Tropy save file including file extension, defaults to None
        :param mapping_save_path: complete path to CSV mapping save file including file extension, defaults to None
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
        if tropy_save_path is not None:
            pass
            # TODO: add validation for tropy_save_path
        if mapping_file_path is not None:
            pass
            # TODO: add validation for download_file_path
        if mapping_save_path is not None:
            pass
            # TODO: add validation for mapping_save_path
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

    @staticmethod
    def _load_mapping(mapping_file_path: str) -> dict:
        """ Load mapping as dictionary with Tropy item ID as key and list of image index, processing ID as value. """

        list_map = Utility.load_csv(file_path=mapping_file_path)
        dict_map = dict()
        for row in list_map[1:]:
            dict_map[row[0]] = [row[1], row[2]]

        return dict_map

    def _process_image(self,
                       item: Item,
                       item_image_index: int,
                       line_model_id: int = None,
                       atr_model_id: int = None,
                       lowest_common_dir: str = None
                       ) -> None:
        """ Process a single image.

        :param item: a Tropy item
        :param item_image_index: the selected item's index
        :param line_model_id: the Transkribus line model ID, defaults to None
        :param atr_model_id: the Transkribus ATR model ID, defaults to None
        :param lowest_common_dir: lowest common directory, defaults to None
        """

        try:
            image_path = os.path.normpath(item.photo[item_image_index]["path"])
            if lowest_common_dir is not None:
                image_path = self._repath(image_path=image_path,
                                          lowest_common_dir=os.path.normpath(lowest_common_dir))
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read())
            post_response = self.api.post_processes(line_model_id=line_model_id,
                                                    atr_model_id=atr_model_id,
                                                    image=encoded_image.decode("utf-8"))
            process_id = post_response.json()["processId"]
            self.processing_data.append([item.identifier, item_image_index, process_id])
            logging.info(f"Item {item.identifier} image {item_image_index} has process ID {process_id}.")
        except IndexError:
            logging.warning(f"Item {item.identifier} has no image with index {item_image_index}!")
        except TypeError:
            logging.warning(f"Item {item.identifier} has no image!")
        except:
            logging.exception(f"Unexpected exception with item {item.identifier}.")
            raise

    def process_tropy(self,
                      tropy_file_path: str,
                      tropy_save_path: str = None,
                      mapping_save_path: str = None,
                      item_type: str = None,
                      item_tag: str = None,
                      item_image_index: int = None,
                      line_model_id: int = 49272,
                      atr_model_id: int = 39995,
                      lowest_common_dir: str = None,
                      ) -> None:
        """ Process selected Tropy items to yield image to text transcriptions.

        Provide a Tropy export JSON-LD file. Items are selected via type and tag (optional and conjunctive). If no
        selection is made, all items are enriched. Images are selected via their index. If no specific image is
        selected, image to text is applied to all images. Processed items get the tag "atr_processed" and are saved
        to an updated JSON-LD file; in addition, there is a CSV file mapping items to processing IDs. The Transkribus
        Processing API generates the transcription based on a layout detection model and an ATR model,
        both customizable via their IDs. If the Tropy image paths do not correspond to the image paths on the machine
        running this module, provide the losest common directory shared by both paths. Use the Client.download method
        to download the transcription from the Transkribus Processing API (do this within at most 24 hours).

        :param tropy_file_path: complete path to Tropy export file including file extension
        :param tropy_save_path: complete path to updated Tropy save file including file extension, defaults to None
        :param mapping_save_path: complete path to CSV mapping save file including file extension, defaults to None
        :param item_type: the item type, defaults to None
        :param item_tag: the item tag, defaults to None
        :param item_image_index: the selected item's index, defaults to None
        :param line_model_id: the Transkribus line model ID, defaults to 49272 (= Mixed Text Line Orientation)
        :param atr_model_id: the Transkribus ATR model ID, defaults to 39995 (= Transkribus Print M1)
        :param lowest_common_dir: the lowest common directory, defaults to None
        """

        logging.info(
            f"Started Client().process_tropy(tropy_file_path={tropy_file_path}, "
            f"tropy_save_path={tropy_save_path}), "
            f"mapping_save_path={mapping_save_path}), "
            f"item_type={item_type}), "
            f"item_tag={item_tag}), "
            f"line_model_id={line_model_id}), "
            f"atr_model_id={atr_model_id}), "
            f"lowest_common_dir={lowest_common_dir}).")

        tropy = self._validate(tropy_file_path=tropy_file_path,
                               tropy_save_path=tropy_save_path,
                               mapping_save_path=mapping_save_path,
                               item_type=item_type,
                               item_tag=item_tag,
                               item_image_index=item_image_index,
                               line_model_id=line_model_id,
                               atr_model_id=atr_model_id,
                               lowest_common_dir=lowest_common_dir)

        for item in tropy.graph:
            parsed_item = Item()
            parsed_item.copy_metadata_from_dict(item)

            # check exclusion criteria:
            if item_type is not None:
                if parsed_item.type != item_type:
                    continue
            if item_tag is not None:
                try:
                    if item_tag not in parsed_item.tag:
                        continue
                except TypeError:
                    continue
            try:
                if "atr_processed" in parsed_item.tag:  # TODO: perhaps better via metadata field w/ process ID?
                    logging.info(f"Item {parsed_item.identifier} skipped (already processed).")
                    continue
            except TypeError:
                pass

            # process item:
            if item_image_index is None:
                i = 0
                while i < len(parsed_item.photo):
                    self._process_image(item=parsed_item,
                                        item_image_index=i,
                                        lowest_common_dir=lowest_common_dir)
                    i += 1
            else:
                self._process_image(item=parsed_item,
                                    item_image_index=item_image_index,
                                    line_model_id=line_model_id,
                                    atr_model_id=atr_model_id,
                                    lowest_common_dir=lowest_common_dir)

            try:
                item["tag"].append("atr_processed")
            except KeyError:
                item["tag"] = ["atr_processed"]
            logging.info(f"Item {parsed_item.identifier} processed.")

        if mapping_save_path is None:
            mapping_save_path = f"mapping_{time.strftime('%Y%m%d-%H%M%S')}.csv"
        Utility.save_csv(header=["item_id", "photo_index", "process_id"],
                         data=self.processing_data,
                         file_path=mapping_save_path)
        logging.info(
            f"Map of map of item IDs to Transkribus metagrapho API processing IDs saved to {mapping_save_path}.")

        if tropy_save_path is None:
            tropy_save_path = "".join(
                tropy_file_path.split(".")[:-1] + [f"_updated_{time.strftime('%Y%m%d-%H%M%S')}.json"])
        Utility.save_json(data=tropy.json_export,
                          file_path=tropy_save_path)
        logging.info(f"Updated Tropy export JSON-LD file saved to {tropy_save_path}.")

        logging.info(f"Finished Client.process_tropy.")

    def download(self,
                 mapping_file_path: str,
                 download_save_path: str = None,
                 ) -> None:

        """ Download image to text transcriptions for Tropy items from the Transkribus Processing API initialized with
        the Client.process_tropy method.

        :param mapping_file_path: complete path to CSV mapping file including file extension
        :param download_save_path: complete path to download JSON save file including file extension, defaults to None
        """

        logging.info(
            f"Started Client().download(download_file_path={mapping_file_path}, "
            f"download_save_path={download_save_path}).")

        mapping = self._load_mapping(mapping_file_path=mapping_file_path)

        for key in mapping.keys():
            try:
                processing_id = mapping[key][1]
                result = self.api.get_result(processing_id)
                mapping[key].append(result.json())
            except:
                logging.exception(f"Unexpected exception in Client.download for {key}.")
                raise

        if download_save_path is None:
            download_save_path = f"download_{time.strftime('%Y%m%d-%H%M%S')}.json"
        Utility.save_json(data=mapping,
                          file_path=download_save_path)
        logging.info(f"Download JSON file saved to {download_save_path}.")

        logging.info(f"Finished Client.download.")

    def enrich_tropy(self,
                     tropy_file_path: str,
                     download_file_path: str,
                     tropy_save_path: str = None,
                     lines: bool = False,
                     ) -> None:
        """ Enrich items in a Tropy export JSON-LD with transcriptions.

        The transcriptions must be provided in a separate file generated by running Client.process_tropy and
        Client.download first.

        :param tropy_file_path: complete path to Tropy export file including file extension
        :param download_file_path: complete path to JSON download file including file extension
        :param tropy_save_path: complete path to enriched Tropy save file including file extension, defaults to None
        :param lines: toggle line by line transcription as selection elements, defaults to False
        """

        logging.info(
            f"Started Client().enrich_tropy(tropy_file_path={tropy_file_path}, "
            f"download_file_path={download_file_path}),"
            f"tropy_save_path={tropy_save_path},"
            f"lines={lines}.")

        tropy = self._validate(tropy_file_path=tropy_file_path,
                               mapping_file_path=download_file_path,
                               tropy_save_path=tropy_save_path)

        download = Utility.load_json(file_path=download_file_path)

        for item in tropy.graph:
            parsed_item = Item()
            parsed_item.copy_metadata_from_dict(item)

            try:
                if "atr_processed" not in parsed_item.tag:
                    continue
            except TypeError:
                continue

            try:
                image_index = int(download[parsed_item.identifier][0])
                text = download[parsed_item.identifier][2]["content"]["text"]  # TODO: add metadata for transcription
                if text == "":
                    logging.info(f"Item {parsed_item.identifier} not enriched, empty transcription.")
                    continue
                regions = download[parsed_item.identifier][2]["content"]["regions"]
                parsed_item.add_note_element(text=text,
                                             photo_index=image_index)
                if lines is True:
                    for region in regions:
                        for line in region["lines"]:
                            parsed_item.add_selection_element(text=line["text"],
                                                              photo_index=image_index,
                                                              coords=line["coords"]["points"])
                item = parsed_item.serialize()
                logging.info(f"Successfully enriched item {parsed_item.identifier}.")
            except KeyError:
                logging.exception(f"Item {parsed_item.identifier} has no result, previous processing or download failed.")
                pass
            except:
                logging.exception(f"Unexpected exception in Client.enrich_tropy for {parsed_item.identifier}.")
                raise

        if tropy_save_path is None:
            tropy_save_path = "".join(tropy_file_path.split(".")[:-1] + [f"_enriched_{time.strftime('%Y%m%d-%H%M%S')}.json"])
        Utility.save_json(data=tropy.json_export,
                          file_path=tropy_save_path)
        logging.info(f"Enriched Tropy export JSON-LD file saved to {tropy_save_path}.")

        logging.info(f"Finished Client.enrich_tropy.")
