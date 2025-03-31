import yaml
import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def load_yaml(filepath):
    if not os.path.exists(filepath):
        logging.error(f"Error: File not found: {filepath}")
        sys.exit(1)
    with open(filepath, 'r') as file:
        try:
            return yaml.safe_load(file) or {}
        except yaml.YAMLError as e:
            logging.error(f"YAML parsing error in {filepath}: {e}")
            sys.exit(1)

def save_yaml(filepath, data):
    with open(filepath, 'w') as file:
        yaml.dump(data, file, sort_keys=False, width=100)

def propagate_descriptions(source_path, target_path):
    logging.info(f"Loading source YAML: {source_path}")
    source_yaml = load_yaml(source_path)

    logging.info(f"Loading target YAML: {target_path}")
    target_yaml = load_yaml(target_path)

    # Extract column descriptions from ALL models (keep first occurrence)
    source_columns = {}
    for model in source_yaml.get('models', []):
        for column in model.get('columns', []):
            col_name = column['name']
            if col_name not in source_columns:
                source_columns[col_name] = column.get('description', '')

    if not source_columns:
        logging.warning("Warning: No column descriptions found in the source YAML.")

    matched_columns = 0
    apply_all = None

    for model in target_yaml.get('models', []):
        for column in model.get('columns', []):
            col_name = column['name']
            target_desc = column.get("description", "")
            source_desc = source_columns.get(col_name)

            if col_name in source_columns:
                if apply_all == 'yes':
                    column["description"] = source_desc
                    matched_columns += 1
                    continue
                elif apply_all == 'no':
                    logging.info(f"[l] Skipped: {col_name}")
                    continue

                print(f"\nColumn: {col_name}")
                print(f"Current (target): {target_desc if target_desc else '[empty]'}")
                print(f"Source (new):     {source_desc}")
                user_input = input("Overwrite with source description? [y]es / [n]o / yes to all [k] / no to all [l]: ").strip().lower()

                while user_input not in ["yes", "y", "no", "n", "yes to all", "k", "no to all", "l"]:
                    user_input = input("Please enter [y], [n], [k] (yes to all), or [l] (no to all): ").strip().lower()

                if user_input in ["yes", "y"]:
                    column["description"] = source_desc
                    matched_columns += 1
                    logging.info(f"[y] Updated: {col_name}")
                elif user_input in ["no", "n"]:
                    logging.info(f"[n] Skipped: {col_name}")
                elif user_input in ["yes to all", "k"]:
                    column["description"] = source_desc
                    matched_columns += 1
                    apply_all = "yes"
                    logging.info(f"[k] Updated: {col_name} (yes to all)")
                elif user_input in ["no to all", "l"]:
                    logging.info(f"[l] Skipped: {col_name} (no to all)")
                    apply_all = "no"

    save_yaml(target_path, target_yaml)

    logging.info(f"\nSuccessfully propagated {matched_columns} descriptions from {os.path.basename(source_path)} to {os.path.basename(target_path)}.")

    source_column_names = set(source_columns.keys())
    target_column_names = set(col['name'] for model in target_yaml.get('models', []) for col in model.get('columns', []))
    missing_columns = source_column_names - target_column_names
    if missing_columns:
        logging.warning(f"\nWarning: These columns exist in source but not in target: {', '.join(missing_columns)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        logging.error("Usage: python scripts/propagate_docs.py <source_yaml> <target_yaml>")
        sys.exit(1)

    source_yaml = os.path.abspath(sys.argv[1])
    target_yaml = os.path.abspath(sys.argv[2])

    propagate_descriptions(source_yaml, target_yaml)
    logging.info("Documentation propagation complete.")
