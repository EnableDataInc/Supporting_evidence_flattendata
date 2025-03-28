import json
import pandas as pd
from pandas import json_normalize

def flatten_ndjson_to_csv(input_file, output_file):
    """
    Converts an NDJSON file to a flat CSV file.
    
    Args:
        input_file (str): Path to the input NDJSON file.
        output_file (str): Path to the output CSV file.
    """
    # Read the NDJSON file line by line with utf-8-sig encoding to handle BOM
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        data = [json.loads(line) for line in f]

    # Flatten each JSON object
    flattened_data = []
    for record in data:
        # Use json_normalize to flatten nested structures
        flat_record = json_normalize(record, sep='.')
        flattened_data.append(flat_record)

    # Concatenate all flattened records into a single DataFrame
    df = pd.concat(flattened_data, ignore_index=True)

    # Write the DataFrame to a CSV file
    df.to_csv(output_file, index=False, encoding='utf-8')

# Input and output file paths
input_ndjson = r"c:\Users\BhargaviDevulapalli\Documents\SRC\AAB\81510-aab_supporting_evidence.ndjson"
output_csv = r"c:\Users\BhargaviDevulapalli\Documents\SRC\AAB\81510-aab_supporting_evidence.csv"

# Convert the NDJSON to CSV
flatten_ndjson_to_csv(input_ndjson, output_csv)

print(f"NDJSON file has been successfully converted to CSV: {output_csv}")