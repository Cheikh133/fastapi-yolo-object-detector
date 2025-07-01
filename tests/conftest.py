from pathlib import Path
import pytest

@pytest.fixture
def fixtures_dir():
    """
    Returns the path to the fixtures directory.
    """
    return Path(__file__).parent / "fixtures"