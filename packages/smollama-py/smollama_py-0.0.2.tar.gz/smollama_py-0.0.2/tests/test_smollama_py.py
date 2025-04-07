from smollama_py import cli
from unittest.mock import patch
import pytest


def test_create_parser():

    parser = cli.create_parser()
    result = parser.parse_args([])
    assert result.mode == "chrome"

    result = parser.parse_args(["-m", "edge"])
    assert result.mode == "edge"


@patch("eel.start")
def test_mycommand(mock_eel_start):
    class Args:
        mode = "chrome"

    cli.mycommand(Args())
    mock_eel_start.assert_called_once_with(
        "index.html", size=(800, 600), close_callback=cli.close
    )


@patch("eel.start")
def test_mycommand_keyboard_interrupt(mock_eel_start):
    class Args:
        mode = "chrome"

    mock_eel_start.side_effect = KeyboardInterrupt
    with pytest.raises(SystemExit):
        cli.mycommand(Args())
