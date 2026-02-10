import json
import numpy as np
import os


class NumpyEncoder(json.JSONEncoder):
    """ Converts NumPy numbers to Python numbers for JSON saving """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)


def save_to_json(filename, new_data, mode='overwrite'):
    """
    Saves data to a JSON file.
    mode='overwrite': Replaces the file completely.
    mode='append': Adds/Updates the existing file with new keys.
    """
    final_data = {}

    # If appending, try to load existing data first
    if mode == 'append' and os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                final_data = json.load(f)
            print(f"Loaded existing data from {filename}...")
        except json.JSONDecodeError:
            print("File found but empty or corrupted. Starting fresh.")

    # Merge new_data into final_data
    # (This adds new keys or updates existing ones)
    final_data.update(new_data)

    # Save everything back to the file
    with open(filename, 'w') as f:
        json.dump(final_data, f, cls=NumpyEncoder, indent=4)

    print(f"Data successfully saved to {filename}")


def load_from_json(filename):
    """ Reads data back from JSON """
    if not os.path.exists(filename):
        print(f"Error: {filename} does not exist.")
        return None

    with open(filename, 'r') as f:
        data = json.load(f)
    return data