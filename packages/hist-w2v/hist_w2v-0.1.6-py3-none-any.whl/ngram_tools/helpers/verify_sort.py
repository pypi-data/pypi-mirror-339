import argparse
import sys

import lz4.frame
import orjson
from tqdm import tqdm

from ngram_tools.helpers.file_handler import FileHandler


def is_file_sorted(file_handler, field, sort_order):
    """
    Check if a file is sorted based on the specified field and order.

    Args:
        file_handler (FileHandler): An instance of the FileHandler class.
        field (str): The JSON field to verify sorting on ('ngram' or 'freq_tot').
        sort_order (str): The order to check ('ascending' or 'descending').

    Returns:
        bool: True if the file is sorted, False otherwise.
    """
    previous_value = None

    with file_handler.open() as infile, tqdm(
        unit='line', desc="Lines", dynamic_ncols=True, file=sys.stdout
    ) as pbar:
        for line_number, line in enumerate(infile, start=1):
            # Deserialize the line using FileHandler
            entry = file_handler.deserialize(line.strip())
            current_value = entry.get(field)

            if current_value is None:
                print(f"Line {line_number}: Missing '{field}' field.")
                return False

            # Compare values based on sort order
            if previous_value is not None:
                if sort_order == 'ascending' and current_value < previous_value:
                    print(
                        f"Line {line_number}: File is not sorted. "
                        f"'{current_value}' appears after '{previous_value}'."
                    )
                    return False
                elif sort_order == 'descending' and current_value > previous_value:
                    print(
                        f"Line {line_number}: File is not sorted. "
                        f"'{current_value}' appears before '{previous_value}'."
                    )
                    return False

            # Update previous value for the next comparison
            previous_value = current_value
            pbar.update(1)

    return True


def check_file_sorted(input_file, field, sort_order):
    """
    High-level function to verify if a JSONL file is sorted. This function
    can be called programmatically, and it uses FileHandler internally.

    Args:
        input_file (str): Path to the file to be checked.
        field (str): Field name to verify sorting on ('ngram' or 'freq_tot').
        sort_order (str): 'ascending' or 'descending'.
    """
    # Create a FileHandler instance for the input file
    file_handler = FileHandler(path=input_file, is_output=False)
    # Reuse the is_file_sorted function to perform the actual check
    if is_file_sorted(file_handler, field, sort_order):
        print("\nThe file is sorted.")
    else:
        print("\nThe file is not sorted.")