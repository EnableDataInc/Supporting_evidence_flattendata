import json
import pandas as pd
from pandas import json_normalize
import os

def extract_and_export_tables(input_file, output_folder):
    # Read the NDJSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Parse each line into a JSON object
    data = [json.loads(line) for line in lines]

    # Create lists to hold data for each table
    patients = []
    claims = []
    observations = []
    explanation_of_benefits = []
    procedures = []

    # Extract data for each table
    for record in data:
        parameters = record.get('parameter', [])
        for param in parameters:
            if param['name'] == 'Patient':
                patient = param['resource']
                patients.append({
                    'id': patient['id'],
                    'lastUpdated': patient['meta']['lastUpdated'],
                    'gender': patient['gender'],
                    'birthDate': patient['birthDate'],
                    'address': json.dumps(patient.get('address', [])),
                    'telecom': json.dumps(patient.get('telecom', [])),
                    'name': json.dumps(patient.get('name', [])),
                    'identifier': json.dumps(patient.get('identifier', [])),
                    'communication': json.dumps(patient.get('communication', []))
                })
            elif param['name'].startswith('Claim'):
                claim = param['resource']
                claims.append({
                    'id': claim['id'],
                    'patient_id': claim['patient']['reference'].split('/')[-1],
                    'status': claim['status'],
                    'type': json.dumps(claim['type']),
                    'created': claim['created'],
                    'provider': claim['provider']['reference'],
                    'diagnosis': json.dumps(claim.get('diagnosis', [])),
                    'item': json.dumps(claim.get('item', []))
                })
            elif param['name'].startswith('Observation'):
                observation = param['resource']
                observations.append({
                    'id': observation['id'],
                    'patient_id': observation['subject']['reference'].split('/')[-1],
                    'status': observation['status'],
                    'code': json.dumps(observation['code']),
                    'effective': json.dumps(observation.get('effectivePeriod', observation.get('effectiveDateTime')))
                })
            elif param['name'].startswith('EOB'):
                eob = param['resource']
                explanation_of_benefits.append({
                    'id': eob['id'],
                    'patient_id': eob['patient']['reference'].split('/')[-1],
                    'status': eob['status'],
                    'type': json.dumps(eob['type']),
                    'created': eob['created'],
                    'diagnosis': json.dumps(eob.get('diagnosis', [])),
                    'item': json.dumps(eob.get('item', []))
                })
            elif param['name'].startswith('Procedures'):
                procedure = param['resource']
                procedures.append({
                    'id': procedure['id'],
                    'patient_id': procedure['subject']['reference'].split('/')[-1],
                    'status': procedure['status'],
                    'code': json.dumps(procedure['code']),
                    'performed': json.dumps(procedure.get('performedPeriod', {}))
                })

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Export each table to a pipe-delimited CSV file with double quotes around fields and no header
    pd.DataFrame(patients).to_csv(
        os.path.join(output_folder, 'patients.csv'), 
        index=False, sep='|', encoding='utf-8', header=False, quoting=1
    )
    pd.DataFrame(claims).to_csv(
        os.path.join(output_folder, 'claims.csv'), 
        index=False, sep='|', encoding='utf-8', header=False, quoting=1
    )
    pd.DataFrame(observations).to_csv(
        os.path.join(output_folder, 'observations.csv'), 
        index=False, sep='|', encoding='utf-8', header=False, quoting=1
    )
    pd.DataFrame(explanation_of_benefits).to_csv(
        os.path.join(output_folder, 'explanation_of_benefits.csv'), 
        index=False, sep='|', encoding='utf-8', header=False, quoting=1
    )
    pd.DataFrame(procedures).to_csv(
        os.path.join(output_folder, 'procedures.csv'), 
        index=False, sep='|', encoding='utf-8', header=False, quoting=1
    )

# Input and output paths
input_ndjson = r"c:\Users\BhargaviDevulapalli\Documents\SRC\LSC\211-lsc_supporting_evidence.ndjson"
output_folder = r"c:\Users\BhargaviDevulapalli\Documents\SRC\LSC\output_tables"

# Extract and export tables
extract_and_export_tables(input_ndjson, output_folder)
