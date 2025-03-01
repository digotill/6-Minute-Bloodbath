import os
import importlib
import inspect

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize an empty list to store all class names
__all__ = []

# Iterate through all .py files in the current directory
for filename in os.listdir(current_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = filename[:-3]  # Remove the .py extension

        # Import the module dynamically
        try:
            module = importlib.import_module(f'.{module_name}', package=__package__)
        except ImportError as e:
            print(f"Warning: Failed to import {module_name}: {e}")
            continue

        # Get all classes defined in the module
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Only include classes defined in this module (not imported)
            if obj.__module__ == module.__name__:
                __all__.append(name)

# Remove duplicates and sort for consistency
__all__ = sorted(set(__all__))

# Optional: Function to dynamically access a class by name
def get_class_by_name(class_name):
    """Retrieve a class by its name from any module in the current directory."""
    for filename in os.listdir(current_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            module = importlib.import_module(f'.{module_name}', package=__package__)
            if hasattr(module, class_name) and inspect.isclass(getattr(module, class_name)):
                return getattr(module, class_name)
    raise AttributeError(f"Class '{class_name}' not found in any module.")
