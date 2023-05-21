""" processing_api.py
=============
TranskribusProcessingAPI class.
"""

import logging
import requests


class TranskribusProcessingAPI:
    """ Wrapper class of the Transkribus Processing API (Transkribus metagrapho API).

    Swagger documentation of the API at https://transkribus.eu/processing/swagger/.

    :param user: Transkribus username
    :param password: Transkribus password
    """

    def __init__(self,
                 user: str,
                 password: str) -> None:
        self.user = user
        self.password = password
        self.base_url = "https://transkribus.eu/processing/v1"
        self.refresh_token = None
        self.setup()

    def setup(self):
        try:
            response = self.authenticate(user=self.user,
                                         password=self.password)
            if response.status_code != 200:
                print(f"{response.json()}")
                raise ConnectionError
            self.refresh_token = response.json()["access_token"]
            logging.info(f"{self.user} authorized successfully with {self.base_url}.")
        except ImportError:
            logging.exception(f"Could not authorize {self.user} with {self.base_url}!")
            raise

    @staticmethod
    def authenticate(user: str,
                     password: str) -> requests.Response:
        """ Wrapper of oAuth2AuthCode.

        :param user: the username
        :param password: the password
        """

        data = {
            "grant_type": "password",
            "username": user,
            "password": password,
            "client_id": "processing-api-client",
        }

        response = requests.post("https://account.readcoop.eu/auth/realms/readcoop/protocol/openid-connect/token",
                                 data=data)

        return response

    def post_processes(self,
                       line_model_id: int,
                       atr_model_id: int,
                       image: str
                       ) -> requests.Response:
        """ Wrapper of https://transkribus.eu/processing/swagger/#/Submit%20data%20for%20processing.

        :param line_model_id: the Transkribus layout detection model ID
        :param atr_model_id: the Transkribus ATR model ID
        :param image: an image encoded to Base64
        """

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.refresh_token}",
            "Content-Type": "application/json",
        }

        data = {
            "config": {
                "lineDetection": {
                    "modelId": line_model_id,
                },
                "textRecognition": {
                    "htrId": atr_model_id,
                },
            },
            "image": {
                "base64": image,
            },

        }

        response = requests.post(f"{self.base_url}/processes",
                                 headers=headers,
                                 json=data)

        return response

    def get_result(self,
                   process_id: int):
        """ Wrapper of https://transkribus.eu/processing/swagger/#/Retrieve%20processing%20status%20and%20result.

        :param process_id: the Transkribus Processing API "processId" parameter
        """

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.refresh_token}",
        }

        response = requests.get(f"{self.base_url}/processes/{process_id}",
                                headers=headers)

        return response

    def get_user(self) -> requests.Response:
        """ Wrapper of https://transkribus.eu/processing/swagger/#/User%20Account/getUserInfo. """

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.refresh_token}",
        }

        response = requests.get(f"{self.base_url}/user",
                                headers=headers)

        return response
