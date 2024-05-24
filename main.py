import os
import pandas as pd
import json
import uuid
from parsers.edifact_parser import parse_edifact
from parsers.xml_parser import parse_xml
from parsers.edisimplex_parser import parse_edisimplex
from utils.logger import logger

def read_input_file(file_path):
    """Reads the input CSV file and returns a DataFrame."""
    df = pd.read_csv(file_path)
    return df

def dataclass_to_dict(obj):
    """Recursively converts dataclass instances to dictionaries."""
    if isinstance(obj, list):
        return [dataclass_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: dataclass_to_dict(value) for key, value in obj.items()}
    elif hasattr(obj, "__dataclass_fields__"):
        return {key: dataclass_to_dict(getattr(obj, key)) for key in obj.__dataclass_fields__}
    else:
        return obj

def save_to_json(parsed_data, output_dir):
    """Saves the parsed data to a JSON file in the specified output directory."""
    os.makedirs(output_dir, exist_ok=True)
    unique_id = uuid.uuid4()
    output_path = os.path.join(output_dir, f"{unique_id}.json")
    try:
        with open(output_path, 'w') as f:
            json.dump(dataclass_to_dict(parsed_data), f, indent=4)
        logger.info(f"Saved parsed data to {output_path}")
    except Exception as e:
        logger.error(f"Failed to save JSON to {output_path}: {e}")
    return output_path

def process_messages(df, output_dir):
    """Processes each message in the DataFrame and saves the parsed data to JSON."""
    for index, row in df.iterrows():
        format_type = row['FORMAT']
        content = row['CONTENIDO']
        
        logger.debug(f"Processing message {index} of format {format_type}")
        
        if format_type == 'EDIFACT':
            parsed_data = parse_edifact(content)
        elif format_type == 'EDIXML':
            parsed_data = parse_xml(content)
        elif format_type == 'EDISIMPLEX':
            parsed_data = parse_edisimplex(content)
        else:
            logger.warning(f"Unsupported format {format_type} for message {index}")
            continue

        output_path = save_to_json(parsed_data, output_dir)
        print(f"Saved parsed data to {output_path}")

def find_csv_file(directory):
    """Finds the first CSV file in the given directory."""
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            return os.path.join(directory, file)
    return None

if __name__ == "__main__":
    input_dir = 'data'
    output_dir = 'output'

    # Find the first CSV file in the input directory
    input_file = find_csv_file(input_dir)
    if input_file:
        df = read_input_file(input_file)
        process_messages(df, output_dir)
    else:
        logger.error(f"No CSV file found in the directory {input_dir}")
        print(f"No CSV file found in the directory {input_dir}")