# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from loggers.models import DebugData


class HandlerDB(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
      full_debug = ':'.join((str(record.created), record.levelname,
                              record.filename, str(record.lineno),
                              record.msg))
      debug_data = DebugData(msg_level=record.levelname,
                             msg=record.msg,
                             full_debug=full_debug)
      debug_data.save()
#datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
