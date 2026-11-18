import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from triage import load_log, triage_log  # noqa: E402


def test_load_log(tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text("Test log content")
    assert load_log(str(log_file)) == "Test log content"


def test_load_log_missing_file():
    with pytest.raises(FileNotFoundError):
        load_log("/nonexistent/path/file.log")


def test_triage_log_calls_gemini():
    with patch("triage.genai") as mock_genai:
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = "Severity: Warning"
        mock_genai.GenerativeModel.return_value = mock_model

        result = triage_log("some log content", "fake-api-key")

        mock_genai.configure.assert_called_once_with(api_key="fake-api-key")
        assert "Severity" in result
