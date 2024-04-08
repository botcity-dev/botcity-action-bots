import argparse
import json
import os.path
import pathlib
from argparse import Namespace
from distutils.util import strtobool
from mimetypes import MimeTypes

import requests
from botcity.maestro import BotMaestroSDK
from requests_toolbelt import MultipartEncoder


class Action:

    def __init__(self):
        """Class responsible for executing actions in Maestro."""
        self._maestro = None
        self._args = None
        self._filepath = None
        self._headers = None

    @property
    def maestro(self) -> BotMaestroSDK:
        """
        Get an instance maestro SDK.

        Returns:
            BotMaestroSDK: Instance maestro SDK.
        """
        return self._maestro

    @maestro.setter
    def maestro(self, maestro: BotMaestroSDK) -> None:
        """
        Set an instance maestro SDK.

        Args:
            maestro (BotMaestroSDK): The instance maestro SDK.
        """
        if not isinstance(maestro, BotMaestroSDK):
            raise ValueError("Value is not Maestro SDK.")
        self._maestro = maestro

    @property
    def headers(self) -> dict:
        """
        Get headers dict.

        Returns:
            dict: Headers dict.
        """
        return self._headers

    @headers.setter
    def headers(self, header: dict) -> None:
        """
        Set a header dict.

        Args:
            header (dict): The dict to header.
        """
        if not isinstance(header, dict):
            raise ValueError("Value is not a dict")
        self._headers = header

    @property
    def args(self) -> Namespace:
        """
        Get headers dict.

        Returns:
            dict: Headers dict.
        """
        return self._args

    @args.setter
    def args(self, args: Namespace) -> None:
        """
        Set a args.

        Args:
            args (Namespace): The namespace args to action.
        """
        if not isinstance(args, Namespace):
            raise ValueError("Value is not a Namespace")
        self._args = args

    @property
    def filepath(self) -> str:
        """
        Get filepath to upload file.

        Returns:
            str: Filepath to upload file.
        """
        return self._filepath

    @filepath.setter
    def filepath(self, filepath: str):
        """
        Set a filepath to upload Maestro.

        Args:
            filepath (str): The filepath to upload.
        """
        print(f'Filepath is {filepath}')
        if not isinstance(filepath, str):
            raise ValueError("Value is not a Namespace")

        if not os.path.exists(filepath):
            raise RuntimeError(f"{filepath} is not exists.")
        self._filepath = filepath

    def get(self) -> dict:
        """
        Get bot in Maestro.

        Returns:
            dict: Bot in Maestro.
        """
        url = f'{self.maestro.server}/api/v2/bot'

        data = {"organizationLabel": self.maestro.organization, 'botId': self.args.botId}
        params = {'botId': self.args.botId}

        with requests.get(url, json=data, params=params, headers=self.headers, timeout=5) as req:
            if req.status_code != 200:
                raise ValueError(
                    'Error during message. Server returned %d. %s' %
                    (req.status_code, req.json().get('message', ''))
                )
            response = json.loads(req.text)
            if not response or len(response) > 1:
                raise ValueError(f"{self.args.botId} not exist.")
            return response[0]

    def update(self) -> None:
        """Execute update in Maestro."""
        url = f'{self.maestro.server}/api/v2/bot/upload/{self.args.botId}/version/{self.args.version}'
        headers_to_upload = self.headers.copy()
        with open(self.filepath, 'rb') as f:
            mime = MimeTypes()
            mime_type = mime.guess_type(self.filepath)
            data = MultipartEncoder(
                fields={'file': (pathlib.Path(self.filepath).name, f, mime_type[0])}
            )
            headers_to_upload["Content-Type"] = data.content_type
            with requests.post(url, data=data, headers=headers_to_upload, timeout=5) as req:
                if not req.ok:
                    try:
                        message = 'Error during upload bot. Server returned %d. %s' % (
                            req.status_code, req.json().get('message', ''))
                    except ValueError:
                        message = 'Error during upload bot. Server returned %d. %s' % (
                            req.status_code, req.text)
                    raise ValueError(message)

    def deploy(self) -> None:
        """Execute deploy in Maestro."""
        url = f'{self.maestro.server}/api/v2/bot'
        data = {
            "organization": self.headers.get("organization"),
            "botId": self.args.botId,
            "version": self.args.version,
            "technology": self.args.technology.upper(),
            "command": None,
            "repositoryLabel": self.args.repositoryLabel,
        }
        with requests.post(url, json=data, headers=self.headers, timeout=5) as req:
            if req.status_code != 200:
                raise ValueError(
                    'Error during message. Server returned %d. %s' %
                    (req.status_code, req.json().get('message', ''))
                )

    def release(self):
        """Execute release in Maestro."""
        url = f'{self.maestro.server}/api/v2/bot/release'
        data = {
            "botId": self.args.botId,
            "version": self.args.version,
        }
        with requests.post(url, json=data, headers=self.headers, timeout=5) as req:
            if req.status_code != 200:
                raise ValueError(
                    'Error during message. Server returned %d. %s' %
                    (req.status_code, req.json().get('message', ''))
                )

    @staticmethod
    def _get_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--update", help="Will the update run", dest="update",
                            type=lambda x: bool(strtobool(x)), action="store")
        parser.add_argument("-d", "--deploy", help="Will the deploy", dest='deploy', type=lambda x: bool(strtobool(x)),
                            action="store")
        parser.add_argument("-r", "--release", help="Will the release", dest='release',
                            type=lambda x: bool(strtobool(x)), action="store")
        parser.add_argument("-v", "--version", help="New version to bot", type=str, action="store", required=True)
        parser.add_argument("-p", "--path", help="Path to github action repository", type=str, action="store")
        parser.add_argument("-bp", "--botPath", help="Path to compress bot", type=str, action="store")
        parser.add_argument("-bi", "--botId", help="Bot ID that will be modified.", type=str, action="store")
        parser.add_argument("-t", "--technology", help="technology bot.", type=str, action="store")
        parser.add_argument("-ap", "--actionPath", help="actionPath", type=str, action="store")
        parser.add_argument("-re", "--repositoryLabel", help="This is the repository used at BotCity Orchestrator",
                            type=str, action="store", required=False, default="DEFAULT")

        args = parser.parse_args()
        return args

    def _get_secrets(self):
        server = self._validate_secret(key='SERVER')
        login = self._validate_secret(key='LOGIN')
        key = self._validate_secret(key='KEY')

        secrets = {
            'server': server,
            'login': login,
            'key': key,
        }

        return secrets

    @staticmethod
    def _validate_secret(key: str):
        if not key:
            raise Exception(f"{key} is empty or none.")

        value = os.getenv(key=key.upper())

        if value:
            return value

        raise Exception(f"{key} not found in secrets")

    @staticmethod
    def _get_maestro(secrets: dict):
        maestro = BotMaestroSDK(**secrets)
        maestro.login()
        return maestro

    def _get_file_path(self) -> str:
        path = pathlib.Path(self.args.path)
        path_bot = pathlib.Path(self.args.botPath)
        file_path = f"{path}/{path_bot.as_posix()}"
        return file_path

    def run(self):
        """Execute action to Bot in Maestro."""
        self.args = self._get_args()

        secrets = self._get_secrets()

        self.maestro = self._get_maestro(secrets=secrets)

        self.headers = {
            "Content-Type": "application/json",
            "token": self.maestro.access_token,
            "organization": self.maestro.organization
        }

        self.filepath = self._get_file_path()
        bot = self._exist_bot()

        if not self.args.version:
            raise ValueError("Version is required.")

        if self.args.deploy or bot is None:
            self.deploy()
            self.update()

        if self.args.update:
            self.set_version(bot=bot)
            self.update()

        if self.args.release:
            self.release()

    def _exist_bot(self):
        try:
            bot = self.get()
            return bot
        except Exception:
            return None

    def _delete(self):
        """Delete bot in Maestro."""
        url = f"{self.maestro.server}/api/v2/bot/{self.args.botId}/version/{self.args.version}"
        with requests.delete(url, headers=self.headers, timeout=5) as req:
            if req.status_code != 200:
                raise ValueError(
                    'Error during message. Server returned %d. %s' %
                    (req.status_code, req.json().get('message', ''))
                )

    def set_version(self, bot: dict):
        """Set version to bot case not version and bot exists."""
        if not self.args.version and bot is not None:
            self.args.version = bot.get("version")
