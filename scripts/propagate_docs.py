import yaml

def load_yaml(filepath):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)
    
def save_yaml(filepath, data):
    with open(filepath, 'w') as file:
        yaml.dump(data, file, sort_keys = False, width = 100)

def copy_descriptions(source_path, target_path):
    # load the files
    source_yaml = load_yaml(source_path)
    target_yaml = load_yaml(target_path)

    # extract and columns and descriptions from the source model
    source_columns = {}
    for model in source_yaml.get('models', []):
        for column in model.get('columns', []):
            source_columns[column['name']] = column.get('description', '')


    # update the target columns with descriptions if they exist
    for model in target_yaml.get('models', []):
        for column in model.get('columns', []):
            # if the name is there, copy the description
            if column['name'] in source_columns:
                column['description'] = source_columns[column['name']]
    

    # save the updated target YAML
    save_yaml(target_path, target_yaml)

# testing with an upstream source and downstream target
copy_descriptions('models/staging/stg_orders.yml', 'models/intermediate/int_orders.yml')
