__version__ = '0.0.1'

# Set default logging handler to avoid "No handler found" warnings.
import logging
logging.getLogger('atlass3hook').addHandler(logging.NullHandler())