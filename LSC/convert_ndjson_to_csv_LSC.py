import json
import pandas as pd
from pandas import json_normalize

def flatten_ndjson_to_csv(input_file, output_file):
    # Read the NDJSON file
    with open(input_file, 'r', encoding='utf-8-Sig') as f:
        lines = f.readlines()

    # Parse each line into a JSON object
    data = [json.loads(line) for line in lines]

    # Flatten the JSON structure
    flattened_data = []
    for record in data:
        # Use json_normalize to flatten nested structures
        flat_record = json_normalize(record, sep='.')
        flattened_data.append(flat_record)

    # Concatenate all flattened records into a single DataFrame
    df = pd.concat(flattened_data, ignore_index=True)

    # Export the DataFrame to a CSV file
    df.to_csv(output_file, index=False, encoding='utf-8')

# Input and output file paths
input_ndjson = r"c:\Users\BhargaviDevulapalli\Documents\SRC\LSC\211-lsc_supporting_evidence.ndjson"
output_csv = r"c:\Users\BhargaviDevulapalli\Documents\SRC\LSC\211-lsc_supporting_evidence.csv"

# Convert NDJSON to CSV
flatten_ndjson_to_csv(input_ndjson, output_csv)
