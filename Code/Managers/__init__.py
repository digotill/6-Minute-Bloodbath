import os
import importlib

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize an empty list to store all module names
__all__ = []

# Iterate through all .py files in the current directory
for filename in os.listdir(current_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = filename[:-3]  # Remove the .py extension

        # Import the module
        module = importlib.import_module(f'.{module_name}', package=__package__)

        # Add all classes from the module to __all__
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if isinstance(attribute, type):  # Check if it's a class
                globals()[attribute_name] = attribute
                __all__.append(attribute_name)

# Remove empty string if it exists in __all__
if '' in __all__:
    __all__.remove('')
