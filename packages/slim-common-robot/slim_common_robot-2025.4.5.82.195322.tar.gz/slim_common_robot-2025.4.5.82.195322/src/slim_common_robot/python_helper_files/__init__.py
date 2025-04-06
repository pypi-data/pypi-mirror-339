"""
Python Helper Files for Robot Framework.

This package provides Python modules with helper functions decorated with @keyword
for use in Robot Framework test suites.

These keywords can be used directly when importing the main library:
    *** Settings ***
    Library    slim_common_robot
"""

# Import all keyword functions from the modules
from slim_common_robot.python_helper_files.account_helper import (
    walk_and_render_templates,
    retrieve_asset_id,
    load_env_variables
)

from slim_common_robot.python_helper_files.file_helper import (
    to_file_path_pair,
    is_unique,
    all_same_url,
    flatten_and_clean_list
)

# Define __all__ to specify what gets imported with "from slim_common_robot.python_helper_files import *"
__all__ = [
    # Modules
    'account_helper',
    'file_helper',
    
    # Functions from account_helper
    'walk_and_render_templates',
    'retrieve_asset_id',
    'load_env_variables',
    
    # Functions from file_helper
    'to_file_path_pair',
    'is_unique',
    'all_same_url',
    'flatten_and_clean_list'
]

# Dictionary mapping keyword names to functions for easier access
KEYWORDS = {
    'Render Env Variables for JSON File': walk_and_render_templates,
    'Retrieve Asset Id': retrieve_asset_id,
    'Load Env Variables': load_env_variables,
    'Get Files In Dir': to_file_path_pair,
    'Check For Uniqueness': is_unique,
    'Check For Constant Values For All Snaps': all_same_url,
    'Flatten_and_clean_list': flatten_and_clean_list
}