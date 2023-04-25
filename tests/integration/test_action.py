from unittest.mock import patch


def test_run(action, args_mocked):
    with patch("sys.argv", args_mocked):
        action.run()
        action._delete()
