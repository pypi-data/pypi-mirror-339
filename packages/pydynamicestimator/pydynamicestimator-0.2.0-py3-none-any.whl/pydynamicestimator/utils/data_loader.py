# Created: 2024-12-01
# Last Modified: 2025-04-05
# (c) Copyright 2024 ETH Zurich, Milos Katanic
# https://doi.org/10.5905/ethz-1007-842
#
# Licensed under the GNU General Public License v3.0;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     https://www.gnu.org/licenses/gpl-3.0.en.html
#
# This software is distributed "AS IS", WITHOUT WARRANTY OF ANY KIND,
# express or implied. See the License for specific language governing
# permissions and limitations under the License.
#


# The code is based on the publication: Katanic, M., Lygeros, J., Hug, G.: Recursive dynamic state estimation for power systems with an incomplete nonlinear DAE model.
# IET Gener. Transm. Distrib. 18, 3657–3668 (2024). https://doi.org/10.1049/gtd2.13308
# The full paper version is available at: https://arxiv.org/abs/2305.10065v2
# See full metadata at: README.md
# For inquiries, contact: mkatanic@ethz.ch


import importlib
import os
import pkgutil
import re
from pydynamicestimator import system
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def class_to_instance_name(class_name, typ):
    # Add underscores before uppercase letters and convert to lowercase
    instance_name = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower() + '_' + typ.lower()
    return instance_name


def create_device_instance(class_name, instance_name, typ):
    """
    Ensures an instance with a specific name exists in globals().
    If not, searches through all scripts in the specified subpackage to find and load the class.

    :param class_name: Name of the class as a string.
    :param instance_name: Desired instance name in snake_case.
    :param typ: Desired type 'sim' or 'est'.
    :return: The instance, or raises an ImportError if not found.
    """
    found_class = False
    for folder in ['pydynamicestimator.devices', 'pydynamicestimator.measurements']:
        package = importlib.import_module(folder)
        # Get the directory of the subpackage
        package_dir = os.path.dirname(package.__file__)

        # Iterate through all modules in the subpackage
        for _, module_name, is_pkg in pkgutil.iter_modules([package_dir]):

            full_module_name = f"{folder}.{module_name}"

            try:
                # Dynamically import the module
                module = importlib.import_module(full_module_name)

                # Check if the class exists in the module
                if hasattr(module, class_name):
                    # Get the class
                    cls = getattr(module, class_name)

                    # Create an instance and store it in globals()
                    instance = cls()
                    #globals()[instance_name] = instance
                    setattr(system, instance_name, instance)
                    logger.info(f"Created {instance_name} of class {class_name}().")
                    # Update the system's device list or measurements list
                    exec(f"system.device_list_{typ}.append(system.{instance_name})")
                    found_class = True  # Mark as found
                    break  # Stop checking further modules in this folder

            except Exception as e:
                # Log or handle individual module import errors gracefully
                logger.info(f"Error while trying to create {instance_name}: {e}")

        if found_class:
            break  # If the class was found, exit the outer loop as well


    if not found_class:
        # If the class wasn't found in any module
        raise ImportError(f"Class {class_name} not found in any script within devices or measurements.")


def read(file, typ: str):
    """Read the contents from .txt files"""
    # Define regular expressions and constants for parsing
    comment_pattern = re.compile(r'^#\s*')
    arithmetic_pattern = re.compile(r'[*/+-]')
    number_pattern = re.compile(r'[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?')
    split_pattern = re.compile(r'\s*,\s*')
    assignment_pattern = re.compile(r'\s*=\s*')

    # Process file content line by line
    while True:
        line = file.readline()
        if not line:
            break
        line = line.strip().replace('\n', '')  # Clean up the line

        if not line or comment_pattern.search(line):
            continue  # Skip empty lines or comments

        # Handle multi-line data entries (when lines end with ',' or ';')
        while line.endswith((',', ';')):
            next_line = file.readline().strip()
            if not next_line:
                break
            if not next_line or comment_pattern.search(next_line):
                continue  # Skip empty lines or comments
            line += ' ' + next_line  # Concatenate multi-line data

        parts = split_pattern.split(line)  # Split line by commas
        class_name = parts.pop(0).strip()  # The first part is the class name

        params = {}
        for part in parts:
            key, value = map(str.strip, assignment_pattern.split(part.strip()))  # Extract key-value pairs
            key = key.strip()
            value = value.strip()

            # Handle different types of values (strings, arrays, numbers, booleans)
            if value.startswith('"'):
                value = value[1:-1]  # String without quotes
            elif value.startswith('['):  # Array processing
                array_values = value[1:-1].split(';')
                if arithmetic_pattern.search(value):  # If it contains arithmetic
                    value = list(map(lambda x: eval(x), array_values))
                else:
                    value = list(map(lambda x: float(x), array_values))  # Convert strings to floats
            elif number_pattern.search(value):  # Check if it's a number (could be an arithmetic expression)
                if arithmetic_pattern.search(value):  # If it contains arithmetic
                    value = eval(value)
                else:
                    value = float(value)  # Convert to float
            elif value == 'True':
                value = True
            elif value == 'False':
                value = False
            else:
                value = int(value)  # Default to integer if no other matches

            params[key] = value  # Add parsed value to the parameters dictionary

        # Extract specific parameters
        name = params.pop('name', None)
        idx = params.pop('idx', None)

        instance_name = class_to_instance_name(class_name, typ)
        if hasattr(system, instance_name):
            try:
                # Add the instance to the system
                # exec(f"system.{instance_name}.add(idx={repr(idx)}, name={repr(name)}, **params)")
                getattr(system, instance_name).add(idx=idx, name=name, **params)

            except KeyError as e:
                logger.warning(f"Failed to add element {class_name} due to missing key: {e}")
        else:
            create_device_instance(class_name, instance_name, typ)
            try:
                # exec(f"system.{instance_name}.add(idx={repr(idx)}, name={repr(name)}, **params)")
                getattr(system, instance_name).add(idx=idx, name=name, **params)
            except KeyError as e:
                logger.warning(f"Failed to add element {class_name} due to missing key: {e}")

    return True


