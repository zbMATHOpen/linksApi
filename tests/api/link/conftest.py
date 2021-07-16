import os
import time

import pytest
from unittest import mock

from zb_links.app import create_app

if os.getenv("PYCHARM_HOSTED"):
    # wait for database migrations to complete
    time.sleep(5)
os.environ["ZBMATH_API_KEY"] = "PyTestKey"
app = create_app()
app.config['TESTING'] = True


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def mock_title():
    with mock.patch(
            "zb_links.api.link.helpers.dlmf_source_helpers.get_title"
        ) as title_mock:

        title_mock.return_value = "Asymptotic Approximation"
        yield title_mock
