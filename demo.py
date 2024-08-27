from sensor.logger import logging
from sensor.Exception import apsException
import sys

try:
    a = 1 / "10"
except Exception as e:
    logging.info("hi first demo logger")
    raise apsException(e, sys) from e
