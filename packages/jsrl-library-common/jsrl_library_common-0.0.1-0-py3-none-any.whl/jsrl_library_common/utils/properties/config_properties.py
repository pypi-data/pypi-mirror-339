import os
import configparser
from itertools import chain
from jsrl_library_common.constants.properties.config_properties_constants import PropertiesSections
from jsrl_library_common.constants.properties.config_properties_constants import CONFIG_PATH
from jsrl_library_common.exceptions.properties.config_properties_exceptions import EnvironmentParameterException

def get_env(env_name, default_value=None):
    """Get value from environment variable

    Args:
        - env_name (str): the environment variable name
        - default_value (str, optional): the default value if the variable does not exist. Defaults to None.

    Raises:
        - EnvironmentParameterException: the environment variable doesn not exist

    Returns:
        - str: the environment variable value
    """
    if default_value is not None:
        return os.environ.get(env_name, default_value)
    
    if os.environ.get(env_name) is None:
        raise EnvironmentParameterException(f"environment parameter not found: {env_name}")
    
    return os.environ[env_name]


def get_property(property_name, section=PropertiesSections.DEFAULT_SECTION.value):
    """Get the property from config file

    Args:
        - property_name (str): the property to extract from config file
        - section (str, optional): the section where property is stored. Defaults to PropertiesSections.DEFAULT_SECTION.value.

    Returns:
        - str: the property value
    """
    _config_file = _create_config_file()
    result = _config_file.get(section, property_name)
    return result



def get_env_or_property(env_name,
                        property_name,
                        section=PropertiesSections.DEFAULT_SECTION.value):
    """Get value from environment variable or a config file property

    Args:
        env_name (str): the environment variable name
        property_name (str): the property to extract from config file
        section (_type_, optional): the section where property is stored. Defaults to PropertiesSections.DEFAULT_SECTION.value.

    Returns:
        str: the environment or property value
    """
    response = get_env(env_name, '')
    if not response:
        return get_property(property_name, section)
    return response


def get_properties(section=PropertiesSections.DEFAULT_SECTION.value, nested_section=True):
    """Get all properties of specific section

    Args:
        section (str, optional): the section to request. Defaults to PropertiesSections.DEFAULT_SECTION.value.
        nested_section (bool, optional): is it a nested section?. Defaults to True.

    Returns:
        dict: the section properties
    """
    properties = []
    _config_file = _create_config_file()

    if (nested_section):
        _sections = _get_existing_nested_sections(_config_file, section) 
        properties = dict(chain(*[_config_file.items(section) for section in _sections]))
    else:
        properties = dict(_config_file.items(section))
    
    return properties


def _create_config_file():
    """Create a config file reader

    Returns:
        ConfigParser: object to can read the config file content
    """
    config_file_path = CONFIG_PATH
    _config_file = configparser.ConfigParser()
    _config_file.read(config_file_path)
    return _config_file


def _get_existing_nested_sections(config_file, section):
    """Get the sub section of specific section

    Args:
        config_file (ConfigParser): the config file reader
        section (str): the source section

    Returns:
        list: the subsections
    """
    
    sections = []
    _nested_sections = section.split('.')
    section = ''

    for subsection in _nested_sections:
        section += subsection if (not section)\
                              else f'.{subsection}'
        
        if (config_file.has_section(section)):
            sections.append(section)
    
    return sections