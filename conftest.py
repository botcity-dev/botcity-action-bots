import argparse
import os
import pathlib
import shutil
import tempfile
from uuid import uuid4

import pytest
import requests_mock

from src.action import Action

SERVER = os.getenv("SERVER")
LOGIN = os.getenv("LOGIN")
KEY = os.getenv("KEY")


@pytest.fixture
def tmp_folder():
    folder = tempfile.mkdtemp()
    yield folder
    shutil.rmtree(folder)


@pytest.fixture()
def action():
    action = Action()
    yield action


@pytest.fixture(scope="session")
def action_logged_mocked(args):
    with requests_mock.Mocker() as mock_request:
        action = Action()
        action.args = args
        secrets = {
            'server': 'https://testing.com',
            'login': '123',
            'key': '123',
        }
        mock_request.get(f'{secrets["server"]}/api/v2/maestro/version', json={'version': '2.0'})
        mock_request.post(f'{secrets["server"]}/api/v2/workspace/login', json={'accessToken': '123'})
        mock_request.get(f'{secrets["server"]}/api/v2/bot?botId={args.botId}', json=[{'botId': args.botId}])
        mock_request.post(f'{secrets["server"]}/api/v2/bot/upload/{args.botId}/version/{args.version}', json={})
        mock_request.post(f'{secrets["server"]}/api/v2/bot', json={})
        mock_request.post(f'{secrets["server"]}/api/v2/bot/release', json={})
        mock_request.delete(f'{secrets["server"]}/api/v2/bot/{args.botId}/version/{args.version}', json={})
        action.maestro = action._get_maestro(secrets=secrets)
        action.headers = {
            "Content-Type": "application/json",
            "token": action.maestro.access_token,
            "organization": action.maestro.organization
        }
        action.filepath = action._get_file_path()
        yield action


@pytest.fixture(scope="session")
def bot_id():
    return f'Test-Action-{uuid4()}'


@pytest.fixture(scope="session")
def args(bot_id):
    print(bot_id)
    args = argparse.Namespace()
    args.update = False
    args.deploy = False
    args.release = False
    args.version = '1.0'
    args.path = pathlib.Path().absolute()
    args.botId = bot_id
    args.technology = "python"
    args.actionPath = pathlib.Path().absolute()
    args.botPath = './bot.zip'
    return args


@pytest.fixture()
def args_mocked(args):
    args_mocked = [
        "main",
        "--update",
        'true',
        "--deploy",
        'true',
        "--release",
        'true',
        "--version",
        args.version,
        "--path",
        str(pathlib.Path().absolute()),
        "--botPath",
        './bot.zip',
        "--botId",
        args.botId,
        "--technology",
        'python',
        "--actionPath",
        str(pathlib.Path().absolute()),
    ]
    return args_mocked
