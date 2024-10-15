from unittest import TestCase
from unittest.mock import call, mock_open, patch
from typer.testing import CliRunner
from datetime import datetime, date

from app import HugoWriter

class TestHugoWriter(TestCase):

    def setUp(self) -> None:
        self.runner = CliRunner()
        self._open = patch("builtins.open").start()
        today = patch("app.date", wraps=date).start()
        today.today.return_value = datetime.strptime(
            "2024-01-01", "%Y-%m-%d"
        )
    

    def tearDown(self) -> None:
        patch.stopall()


    def test_process_settings(self):
        # given
        m = mock_open()
        with patch("app.open", m):
            # when 
            HugoWriter()
        for _call in ("./settings.yml", "./template.md"):
            # then
            self.assertTrue(call(_call) in m.mock_calls)


    def test_get_file_with_path(self) -> None:
        # given
        patch("app.HugoWriter._process_settings").start().return_value = {"posts": "/path/to/settings/"}
        patch("app.HugoWriter._load_template").start()
        hugo_writer = HugoWriter()
        # when
        result = hugo_writer.get_file_with_path()
        # then
        self.assertEqual("/path/to/settings/2024-01-01.md", result)
