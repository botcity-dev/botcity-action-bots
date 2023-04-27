import argparse
import os
from typing import Tuple
from unittest.mock import patch

import pytest
import requests_mock

from botcity.maestro import BotMaestroSDK

from src.action import Action


def test_get_maestro(action: Action):
    secrets = action._get_secrets()
    maestro = action._get_maestro(secrets=secrets)

    assert isinstance(maestro, BotMaestroSDK)
    assert maestro.access_token


def test_set_maestro_error(action: Action):
    with pytest.raises(ValueError):
        action.maestro = 123


def test_set_maestro(action: Action):
    secrets = action._get_secrets()
    maestro = action._get_maestro(secrets=secrets)
    action.maestro = maestro
    assert isinstance(action.maestro, BotMaestroSDK)


def test_action_class():
    action = Action()
    assert action.maestro is None
    assert action.filepath is None
    assert action.args is None
    assert action.headers is None


@pytest.mark.parametrize(
    'headers',
    [1, '1', None, []]
)
def test_set_headers_error(action: Action, headers):
    with pytest.raises(ValueError):
        action.headers = headers


def test_set_headers(action: Action):
    headers = {
        "Content-Type": "application/json",
        "token": '123',
        "organization": '123'
    }

    action.headers = headers
    assert action.headers == headers


@pytest.mark.parametrize(
    'args',
    [1, '1', None, []]
)
def test_set_args_error(action: Action, args):
    with pytest.raises(ValueError):
        action.args = args


def test_set_args(action: Action):
    args = argparse.Namespace()
    args.testing = 1
    action.args = args
    assert action.args == args


@pytest.mark.parametrize(
    'filepath',
    [1, {}, None, [], '/test/123']
)
def test_set_filepath_error(action: Action, filepath):
    with pytest.raises(tuple([ValueError, RuntimeError])):
        action.filepath = filepath


def test_set_filepath(action: Action):
    filepath = './conftest.py'
    action.filepath = filepath


def test_get(action_logged_mocked: Action, args: argparse.Namespace):
    bot = action_logged_mocked.get()
    assert bot.get("botId") == args.botId


def test_get_error(action_logged_mocked: Action, args: argparse.Namespace):
    with pytest.raises(ValueError):
        with requests_mock.Mocker() as mock_request:
            mock_request.get(f'{action_logged_mocked.maestro.server}/api/v2/bot?botId={args.botId}', json={'message': 'testing error'}, status_code=400)
            action_logged_mocked.get()


def test_get_error_bot_exists(action_logged_mocked: Action, args: argparse.Namespace):
    with pytest.raises(ValueError):
        with requests_mock.Mocker() as mock_request:
            mock_request.get(f'{action_logged_mocked.maestro.server}/api/v2/bot?botId={args.botId}', json=[], status_code=200)
            action_logged_mocked.get()


def test_update(action_logged_mocked: Action, args: argparse.Namespace):
    action_logged_mocked.update()


def test_update_error(action_logged_mocked: Action, args: argparse.Namespace):
    with pytest.raises(ValueError):
        with requests_mock.Mocker() as mock_request:
            mock_request.post(f'{action_logged_mocked.maestro.server}/api/v2/bot/upload/{args.botId}/version/{args.version}', status_code=400)
            action_logged_mocked.update()


def test_deploy(action_logged_mocked: Action, args: argparse.Namespace):
    action_logged_mocked.deploy()


def test_deploy_error(action_logged_mocked: Action, args: argparse.Namespace):
    with pytest.raises(ValueError):
        with requests_mock.Mocker() as mock_request:
            mock_request.post(f'{action_logged_mocked.maestro.server}/api/v2/bot', status_code=400)
            action_logged_mocked.deploy()


def test_release(action_logged_mocked: Action, args: argparse.Namespace):
    action_logged_mocked.release()


def test_release_error(action_logged_mocked: Action, args: argparse.Namespace):
    with pytest.raises(ValueError):
        with requests_mock.Mocker() as mock_request:
            mock_request.post(f'{action_logged_mocked.maestro.server}/api/v2/bot/release', status_code=400)
            action_logged_mocked.release()


def test_get_args(action_logged_mocked: Action):
    args_mocked = [
        "main",
        "--update",
        'true',
        "--deploy",
        'true',
        "--release",
        'true',
        "--version",
        '1.0',
        "--path",
        'testing',
        "--botPath",
        'testing',
        "--botId",
        'testing',
        "--technology",
        'python',
        "--actionPath",
        'testing'
    ]
    with patch("sys.argv", args_mocked):
        args_mocked = action_logged_mocked._get_args()
        assert args_mocked.update
        assert args_mocked.release
        assert args_mocked.deploy
        assert args_mocked.version == '1.0'
        assert args_mocked.path == 'testing'
        assert args_mocked.botPath == 'testing'
        assert args_mocked.botId == 'testing'
        assert args_mocked.technology == 'python'
        assert args_mocked.actionPath == 'testing'


def test_validate_secret_error_none(action_logged_mocked):
    with pytest.raises(Exception):
        action_logged_mocked._validate_secret(None)


def test_validate_secret_error_not_value(action_logged_mocked):
    with pytest.raises(Exception):
        action_logged_mocked._validate_secret('a')


def test_run(action_logged_mocked, args_mocked):
    with patch("sys.argv", args_mocked):
        os.environ['SERVER'] = 'https://testing.com'
        os.environ['LOGIN'] = '123'
        os.environ['KEY'] = '123'
        action_logged_mocked.run()


def test_exist_bot(action_logged_mocked: Action, args: argparse.Namespace):
    exist_bot = action_logged_mocked._exist_bot()
    assert exist_bot


def test_exist_bot_error(action_logged_mocked: Action, args: argparse.Namespace):
    with requests_mock.Mocker() as mock_request:
        mock_request.get(f'{action_logged_mocked.maestro.server}/api/v2/bot?botId={args.botId}',
                         json={'message': 'testing error'}, status_code=400)
        exist_bot = action_logged_mocked._exist_bot()
        assert not exist_bot


def test_delete(action_logged_mocked: Action, args: argparse.Namespace):
    action_logged_mocked._delete()


def test_delete_error(action_logged_mocked: Action, args: argparse.Namespace):
    with pytest.raises(ValueError):
        with requests_mock.Mocker() as mock_request:
            mock_request.delete(f'{action_logged_mocked.maestro.server}/api/v2/bot/{args.botId}/version/{args.version}',
                             json={'message': 'testing error'}, status_code=400)
            action_logged_mocked._delete()


def test_set_version(action_logged_mocked: Action):
    action_logged_mocked.args.version = ''
    action_logged_mocked.set_version(bot={'version': '1.0'})
    assert action_logged_mocked.args.version == '1.0'

