import pytest
from unittest.mock import Mock, patch
from tc_http_loader_prefix import loader


@pytest.fixture
def mock_context():
    context = Mock()
    context.config.TC_HTTP_LOADER_PREFIX = "http://cdn.example.com/assets/"
    return context


def test_loader_url_is_prefixed_correctly(mock_context):
    test_url = "images/cat.jpg"
    expected_url = "http://cdn.example.com/assets/images/cat.jpg"

    with patch("tc_http_loader_prefix.loader.http_loader") as mock_http_loader:
        loader.load(mock_context, test_url)
        mock_http_loader.assert_called_once_with(mock_context, expected_url)


def test_loader_raises_if_prefix_not_set():
    context = Mock()
    context.config.TC_HTTP_LOADER_PREFIX = None

    with pytest.raises(RuntimeError, match="TC_HTTP_LOADER_PREFIX is not set in the config"):
        loader.load(context, "something.jpg")
