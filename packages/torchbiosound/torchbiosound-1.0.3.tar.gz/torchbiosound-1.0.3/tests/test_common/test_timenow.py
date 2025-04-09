import time
from datetime import datetime

import torchbiosound.common.constants
import torchbiosound.common.timenow


def test_timenow():
    before_timestamp = time.mktime(datetime.now().timetuple())
    timenow_str = torchbiosound.common.timenow.get_timenow_as_str()
    assert len(timenow_str) == len(torchbiosound.common.constants.STRFTIME_TIMESTAMP)
    timenow_str_as_timestamp = time.mktime(
        datetime.strptime(timenow_str, torchbiosound.common.constants.STRFTIME_TIMESTAMP).timetuple()
    )
    after_timestamp = time.mktime(datetime.now().timetuple())
    assert before_timestamp <= timenow_str_as_timestamp <= after_timestamp
