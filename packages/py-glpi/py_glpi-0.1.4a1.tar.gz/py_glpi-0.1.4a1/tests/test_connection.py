import pytest

from tests.settings import get_connection

def test_glpi_session():
    assert get_connection()

