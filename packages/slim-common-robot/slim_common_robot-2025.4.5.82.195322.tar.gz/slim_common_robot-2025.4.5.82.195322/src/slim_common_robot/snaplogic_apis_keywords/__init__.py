"""
Common APIs Keywords for Robot Framework.

This package provides Robot Framework resource files with keywords for API testing
and platform operations.

The resource files can be imported in Robot Framework tests using:
    *** Settings ***
    Resource    slim_common_robot/snaplogic_apis_keywords/platform_apis.resource
    Resource    slim_common_robot/snaplogic_apis_keywords/platform_keywords.resource
"""

import os
import pkg_resources

# Define __all__ to specify what gets imported with "from slim_common_robot.snaplogic_apis_keywords import *"
__all__ = [
    # The resource files are not directly importable in Python,
    # but we list them here for documentation purposes
    'platform_apis.resource',
    'platform_keywords.resource',
    'get_resource_path'
]

def get_resource_path(resource_name):
    """
    Get the full path to a resource file in this package.
    
    This is useful for programmatically locating resource files
    when they're installed as part of a Python package.
    
    Args:
        resource_name: Name of the resource file (e.g., 'platform_apis.resource')
        
    Returns:
        Full path to the resource file
    """
    return pkg_resources.resource_filename('slim_common_robot.snaplogic_apis_keywords', resource_name)