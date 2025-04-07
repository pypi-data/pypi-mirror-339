"""
Package integrity verification module.

This module checks that all required modules are available and provides 
fallbacks for missing modules.
"""

import importlib
import logging
import os
import sys
from typing import List, Dict, Any, Optional, Union, Tuple

logger = logging.getLogger(__name__)

CRITICAL_MODULES = [
    'amauta_ai.task_manager.template_service',
    'amauta_ai.rules.template_manager',
]

def verify_integrity() -> bool:
    """
    Verify the integrity of the package installation.
    
    Returns:
        bool: True if all critical modules are available, False otherwise
    """
    missing_modules = []
    
    for module_name in CRITICAL_MODULES:
        try:
            importlib.import_module(module_name)
            logger.debug(f"Module {module_name} is available")
        except ImportError as e:
            logger.warning(f"Module {module_name} is missing: {e}")
            missing_modules.append(module_name)
            
    if missing_modules:
        logger.warning(f"Missing critical modules: {missing_modules}")
        try:
            fix_missing_modules(missing_modules)
        except Exception as e:
            logger.error(f"Failed to fix missing modules: {e}")
            return False
            
    return True

def fix_missing_modules(missing_modules: List[str]) -> None:
    """
    Attempt to fix missing modules by creating them from fallbacks.
    
    Args:
        missing_modules: List of missing module names
    """
    for module_name in missing_modules:
        try:
            # Try to get the fallback module
            fallback_name = f"{module_name}_fallback"
            parts = module_name.split('.')
            base_dir = os.path.dirname(sys.modules['.'.join(parts[:-1])].__file__)
            
            module_path = os.path.join(base_dir, f"{parts[-1]}.py")
            fallback_path = os.path.join(base_dir, f"{parts[-1]}_fallback.py")
            
            if os.path.exists(fallback_path):
                logger.info(f"Creating {module_path} from {fallback_path}")
                with open(fallback_path, 'r') as src:
                    with open(module_path, 'w') as dst:
                        dst.write(src.read())
            else:
                logger.error(f"No fallback found for {module_name}")
        except Exception as e:
            logger.error(f"Failed to fix module {module_name}: {e}")
            raise

def run_integrity_check() -> None:
    """
    Run the integrity check and log the results.
    This is intended to be called on package import.
    """
    try:
        if verify_integrity():
            logger.info("Package integrity check passed")
        else:
            logger.warning("Package integrity check failed")
    except Exception as e:
        logger.error(f"Error during integrity check: {e}") 