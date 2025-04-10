"""
This module contains the 'TokenReceiverAsync' class, which is responsible 
for performing authorization using the available login and password. 
It interacts with the VK API to obtain an access token.
"""

import os
import json
import logging
from typing import Awaitable, Callable, Union, Tuple, Optional

from httpx import AsyncClient, Response

from .client import clients
from .utils import create_logger


class TokenReceiverAsync:
    """
    A class that is responsible for performing authorization using
    the available login and password. It interacts with the VK API
    to obtain an access token.
    WARNING!!! The TokenReceiverAsync class DOESN'T provide
    methods for handling captcha, 2-factor authentication,
    and various error scenarios. You need to implement them
    yourself using the appropriate handlers.

    Attributes:
        client (Client): The client object.
        __login (str): The login.
        __password (str): The password.
        __token (str): The token.
        _logger (logging.Logger): The logger.

    Example usage:
    ```
    >>> import asyncio
    >>> from vkpymusic import TokenReceiverAsync
    >>>
    >>> receiver = TokenReceiverAsync(login="my_username", password="my_password")
    >>> if asyncio.run(receiver.auth()):
    ...     receiver.get_token()
    ...     receiver.save_to_config()
    ```
    """

    def __init__(
            self,
            login,
            password,
            client="Kate",
            logger=create_logger(__name__)
    ) -> None:
        """
        Initialize TokenReceiver.

        Args:
            login (str): Login to VK.
            password (str): Password to VK.
            client (str): Client to VK (default value = "Kate").
            logger (logging.Logger): Logger (default value = my logger).
        """
        self.__login: str = str(login)
        self.__password: str = str(password)
        if client in clients:
            self.client = clients[client]
        else:
            self.client = clients["Kate"]
        self.__token = None
        self._logger = logger

    async def request_auth(
        self, code: str = None, captcha: Tuple[str, str] = None
    ) -> Response:
        """
        Request auth from VK.

        Args:
            code (Optional[str]): Code from VK/SMS (default value = None).
            captcha (Optional[Tuple[str, str]]): Captcha (default value = None).

        Returns:
            Response: Response from VK.
        """
        query_params = [
            ("grant_type", "password"),
            ("client_id", self.client.client_id),
            ("client_secret", self.client.client_secret),
            ("username", self.__login),
            ("password", self.__password),
            ("scope", "audio,offline"),
            ("2fa_supported", 1),
            ("force_sms", 1),
            ("v", 5.131),
        ]
        if captcha:
            query_params.append(("captcha_sid", captcha[0]))
            query_params.append(("captcha_key", captcha[1]))
        if code:
            query_params.append(("code", code))
        async with AsyncClient() as session:
            session.headers.update({"User-Agent": self.client.user_agent})
            response = await session.post(
                "https://oauth.vk.com/token", params=query_params
            )
        return response

    async def request_code(self, sid: Union[str, int]) -> Response:
        """
        Request code from VK.

        Args:
            sid (Union[str, int]): Sid from VK.

        Returns:
            Response: Response from VK.
        """
        query_params = [("sid", str(sid)), ("v", "5.131")]
        async with AsyncClient() as session:
            session.headers.update({"User-Agent": self.client.user_agent})
            response = await session.post(
                "https://api.vk.com/method/auth.validatePhone",
                params=query_params,
                follow_redirects=True,
            )
        response_json = json.loads(response.content.decode("utf-8"))
        # right_response_json = {
        #     "response": {
        #         "type": "general",
        #         "sid": {str(sid)},
        #         "delay": 60,
        #         "libverify_support": False,
        #         "validation_type": "sms",
        #         "validation_resend": "sms"
        #     }
        # }
        return response_json

    async def auth(
        self,
        on_captcha: Callable[[str], Awaitable[str]],
        on_2fa: Callable[[], Awaitable[str]],
        on_invalid_client: Callable[[], Awaitable[None]],
        on_critical_error: Callable[..., Awaitable[None]],
    ) -> bool:
        """
        Performs ASYNC authorization using the available login and password.
        If necessary, interactively accepts a code from SMS or captcha.

        Args:
            on_captcha (Callable[[str], str]): ASYNC handler to captcha. Get url image. Return key.
            on_2fa (Callable[[], str]): ASYNC handler to 2-factor auth. Return captcha.
            on_invalid_client (Callable[[], None]): ASYNC handler to invalid client.
            on_critical_error (Callable[[Any], None]): ASYNC handler to crit error. Get response.

        Returns:
            bool: Boolean value indicating whether authorization was successful or not.
        """
        response_auth = await self.request_auth()
        response_auth_json = json.loads(response_auth.content.decode("utf-8"))
        while "error" in response_auth_json:
            error = response_auth_json["error"]
            error_type = response_auth_json.get("error_type", "")
            if error == "need_captcha":
                self._logger.info("Captcha is needed!")
                captcha_sid: str = response_auth_json["captcha_sid"]
                captcha_img: str = response_auth_json["captcha_img"]
                captcha_key: str = await on_captcha(captcha_img)
                response_auth = await self.request_auth(
                    captcha=(captcha_sid, captcha_key)
                )
                response_auth_json = json.loads(response_auth.content.decode("utf-8"))
            elif error == "need_validation":
                self._logger.info("2FA is needed!")
                validation_type = response_auth_json["validation_type"]
                validation_description = response_auth_json["error_description"]
                if validation_type == "2fa_app":
                    self._logger.info("Code from 2FA app is needed!")
                else:
                    self._logger.info(validation_description)
                sid = response_auth_json["validation_sid"]
                await self.request_code(sid)
                code: str = await on_2fa()
                response_auth = await self.request_auth(code=code)
                response_auth_json = json.loads(response_auth.content.decode("utf-8"))
            elif error == "invalid_request":
                self._logger.warning("Invalid code. Try again!")
                code: str = await on_2fa()
                response_auth = await self.request_auth(code=code)
                response_auth_json = json.loads(response_auth.content.decode("utf-8"))
            elif error == "invalid_client":
                self._logger.error("Login or password is invalid!")
                del self.__login
                del self.__password
                await on_invalid_client()
                return False
            elif error_type == "password_bruteforce_attempt":
                self._logger.error("Password bruteforce attempt!")
                del self.__login
                del self.__password
                return False
            else:
                del self.__login
                del self.__password
                await on_critical_error(response_auth_json)
                self.__on_error(response_auth_json)
                return False
        if "access_token" in response_auth_json:
            del self.__login
            del self.__password
            access_token = response_auth_json["access_token"]
            self._logger.info("Token was received!")
            self.__token = access_token
            return True
        del self.__login
        del self.__password
        self.__on_error(response_auth_json)
        await on_critical_error(response_auth_json)
        return False

    def get_token(self) -> Optional[str]:
        """
        Prints token in console (if authorisation was successful).
        """
        token = self.__token
        if not token:
            self._logger.warning('Please, first call the method "auth".')
            return
        self._logger.info(token)
        return token

    def save_to_config(self, file_path: str = "config_vk.ini"):
        """
        Save token and user agent data in config (if authorisation was succesful).

        Args:
            file_path (str): Filename of config (default value = "config_vk.ini").
        """
        token: str = self.__token
        if not token:
            self._logger.warning('Please, first call the method "auth"')
            return
        full_fp = self.create_path(file_path)
        if os.path.isfile(full_fp):
            print('File already exist! Enter "OK" for rewriting it')
            if input().lower() != "ok":
                return
        os.makedirs(os.path.dirname(full_fp), exist_ok=True)
        with open(full_fp, "w") as output_file:
            output_file.write("[VK]\n")
            output_file.write(f"user_agent={self.client.user_agent}\n")
            output_file.write(f"token_for_audio={token}")
            self._logger.info("Token was saved!")

    def __on_error(self, response):
        self._logger.critical(
            "Unexpected error! Please, create an issue in repository for solving this problem."
        )
        self._logger.critical(response)

    @staticmethod
    def create_path(file_path: str) -> str:
        """
        Create path before and after this for different funcs.

        Args:
            file_path (str): Relative path to file.

        Returns:
            str: Absolute path to file.
        """
        return os.path.join(os.path.dirname(__file__), file_path)
