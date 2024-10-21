"""
PyTest Fixtures.
"""

import pytest

import figfind.filesystem  # noqa: F401


@pytest.fixture(scope="function")
def mock_os(mocker):
    """Mock builtin os calls in figfind.file_system."""
    mock_os = mocker.patch("figfind.filesystem.os")
    yield mock_os
