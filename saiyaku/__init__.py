__all__ = ["retry", "retry_call"]

import logging
from logging import NullHandler

from .api import retry, retry_call

# Set default logging handler to avoid "No handler found" warnings.
log = logging.getLogger(__name__)
log.addHandler(NullHandler())
