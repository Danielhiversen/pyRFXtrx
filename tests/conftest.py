from datetime import timedelta
import pytest
from freezegun import freeze_time
from unittest import mock


@pytest.fixture(name="frozen_sleep", autouse=True)
def fixture_frozen_sleep():
    with mock.patch('RFXtrx.sleep') as mock_sleep:
        with freeze_time() as frozen_time:
            mock_sleep.side_effect = lambda seconds: frozen_time.tick(timedelta(seconds=seconds))
            yield frozen_time