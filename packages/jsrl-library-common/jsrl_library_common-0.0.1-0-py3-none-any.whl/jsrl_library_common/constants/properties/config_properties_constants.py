import os
from enum import Enum

class PropertiesSections(Enum):
    DEFAULT_SECTION = 'general'


DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
CONFIG_PATH = os.environ.get("JSRL_CONFIG_PATH", DEFAULT_CONFIG_PATH)
