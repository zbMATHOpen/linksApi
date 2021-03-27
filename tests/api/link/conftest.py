import os
import time

import pytest

from zb_links.app import create_app


@pytest.fixture
def client():
    if os.getenv("PYCHARM_HOSTED"):
        # wait for database migrations to complete
        time.sleep(5)

    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client
