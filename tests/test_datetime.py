import pytest
from datetime import datetime, timezone
from multiprocessing.sharedctypes import Value
from utils.datetime import get_next_deadline, Daliy, WeekDays, Weekly, Monthly, Yearly


class TestNextDeadline:

    def test_Daliy(self):
        a = datetime(2020, 1, 1, 1)
        b = datetime(2020, 1, 2, 1)
        task = {
            'interval': 1,
            'intervalType': Daliy,
            'type': '',
            'weekdays': [],
        }
        assert get_next_deadline(a, task) == b

        a = datetime(2020, 1, 31, 1)
        b = datetime(2020, 2, 1, 1)
        assert get_next_deadline(a, task) == b

    def test_WeekDays(self):
        a = datetime(2020, 1, 1, 1)
        b = datetime(2020, 1, 2, 1)
        task = {
            'interval': 1,
            'intervalType': WeekDays,
            'type': '',
            'weekdays': [],
        }
        assert get_next_deadline(a, task) == b

        a = datetime(2020, 1, 2, 1)
        b = datetime(2020, 1, 3, 1)
        assert get_next_deadline(a, task) == b

        a = datetime(2020, 1, 3, 1)
        b = datetime(2020, 1, 6, 1)
        assert get_next_deadline(a, task) == b

        a = datetime(2020, 1, 4, 1)
        b = datetime(2020, 1, 6, 1)
        assert get_next_deadline(a, task) == b

        a = datetime(2020, 1, 5, 1)
        b = datetime(2020, 1, 6, 1)
        assert get_next_deadline(a, task) == b

    def test_Weekly(self):
        a = datetime(2020, 1, 1, 1)
        b = datetime(2020, 1, 8, 1)
        task = {
            'interval': 1,
            'intervalType': Weekly,
            'type': '',
            'weekdays': [],
        }
        assert get_next_deadline(a, task) == b

        a = datetime(2020, 1, 31, 1)
        b = datetime(2020, 2, 7, 1)
        assert get_next_deadline(a, task) == b

        a = datetime(2020, 2, 22, 1)
        b = datetime(2020, 2, 29, 1)
        assert get_next_deadline(a, task) == b

        a = datetime(2020, 2, 29, 1)
        b = datetime(2020, 3, 7, 1)
        assert get_next_deadline(a, task) == b

    def test_Monthly(self):
        task = {
            'interval': 1,
            'intervalType': Monthly,
            'type': '',
            'weekdays': [],
        }
        a = datetime(2020, 1, 1, 1)
        b = datetime(2020, 2, 1, 1)
        assert get_next_deadline(a, task) == b

        a = datetime(2020, 1, 31, 1)
        b = datetime(2020, 2, 29, 1)
        assert get_next_deadline(a, task) == b

        a = datetime(2020, 1, 30, 1)
        b = datetime(2020, 2, 29, 1)
        assert get_next_deadline(a, task) == b

        a = datetime(2020, 1, 29, 1)
        b = datetime(2020, 2, 29, 1)
        assert get_next_deadline(a, task) == b

    def test_Yearly(self):
        task = {
            'interval': 1,
            'intervalType': Yearly,
            'type': '',
            'weekdays': [],
        }
        a = datetime(2020, 1, 1, 1)
        b = datetime(2021, 1, 1, 1)
        assert get_next_deadline(a, task) == b

        a = datetime(2020, 2, 29, 1)
        b = datetime(2021, 2, 28, 1)
        assert get_next_deadline(a, task) == b

        a = datetime(2020, 2, 28, 1)
        b = datetime(2021, 2, 28, 1)
        assert get_next_deadline(a, task) == b

    def test_other(self):
        a = datetime(2020, 1, 1, 1)
        b = datetime(2021, 1, 1, 1)
        with pytest.raises(KeyError):
            get_next_deadline(a, {})
