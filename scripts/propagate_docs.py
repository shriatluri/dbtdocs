import yaml
import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def load_yaml(filepath):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

def save_yaml(filepath, data):
    with open(filepath, 'w') as file:
        yaml.dump(data, file, sort_keys=False, width=100)

def propagate_descriptions(source_path, target_path):
    """
    Main function to copy column descriptions from source YAML to target YAML.
    """
    logging.info(f"Loading source YAML: {source_path}")
    source_yaml = load_yaml(source_path)

    logging.info(f"Loading target YAML: {target_path}")
    target_yaml = load_yaml(target_path)

    # Extract columns + descriptions from source model
    source_columns = {}
    for model in source_yaml.get('models', []):
        for column in model.get('columns', []):
            source_columns[column['name']] = column.get('description', '')

    # Check for matching columns in target and propagate descriptions
    matched_columns = 0
    for model in target_yaml.get('models', []):
        for column in model.get('columns', []):
            col_name = column['name']
            if col_name in source_columns:
                column['description'] = source_columns[col_name]
                matched_columns += 1

    # Save updated target YAML
    save_yaml(target_path, target_yaml)

    logging.info(f"Propagated {matched_columns} descriptions from {os.path.basename(source_path)} to {os.path.basename(target_path)}")

    # Optional: Check for columns missing from target
    source_column_names = set(source_columns.keys())
    target_column_names = set(col['name'] for model in target_yaml.get('models', []) for col in model.get('columns', []))

    missing_columns = source_column_names - target_column_names
    if missing_columns:
        logging.warning(f"Warning: These columns exist in source but not in target: {', '.join(missing_columns)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/propagate_docs.py <source_yaml> <target_yaml>")
        sys.exit(1)

    source_yaml = os.path.abspath(sys.argv[1])
    target_yaml = os.path.abspath(sys.argv[2])

    propagate_descriptions(source_yaml, target_yaml)
    logging.info("Documentation propagation complete!")
