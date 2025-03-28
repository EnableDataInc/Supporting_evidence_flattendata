import json
import pandas as pd
from pandas import json_normalize
import os

def extract_and_export_tables(input_file, output_folder):
    # Read the NDJSON file
    with open(input_file, 'r', encoding='utf-8-sig') as f:
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
                address = patient.get('address', [{}])[0]
                telecom = patient.get('telecom', [{}])[0]
                name = patient.get('name', [{}])[0]
                identifier = patient.get('identifier', [{}])[0]
                communication = patient.get('communication', [{}])[0]

                patients.append({
                    'id': patient['id'],
                    'lastUpdated': patient['meta']['lastUpdated'],
                    'gender': patient['gender'],
                    'birthDate': patient['birthDate'],
                    'address_line1': address.get('line', [''])[0],
                    'address_line2': address.get('line', [''])[1] if len(address.get('line', [])) > 1 else '',
                    'city': address.get('city', ''),
                    'state': address.get('state', ''),
                    'postalCode': address.get('postalCode', ''),
                    'telecom_system': telecom.get('system', ''),
                    'telecom_value': telecom.get('value', ''),
                    'name_family': name.get('family', ''),
                    'name_given': ' '.join(name.get('given', [])),
                    'identifier_system': identifier.get('system', ''),
                    'identifier_value': identifier.get('value', ''),
                    'communication_language': communication.get('language', {}).get('coding', [{}])[0].get('code', ''),
                    'communication_preferred': communication.get('preferred', False)
                })
            elif param['name'].startswith('Claim'):
                claim = param['resource']
                diagnosis = claim.get('diagnosis', [{}])
                items = claim.get('item', [{}])

                claims.append({
                    'id': claim['id'],
                    'patient_id': claim['patient']['reference'].split('/')[-1],
                    'status': claim['status'],
                    'type_system': claim['type']['coding'][0]['system'] if 'coding' in claim['type'] else '',
                    'type_code': claim['type']['coding'][0]['code'] if 'coding' in claim['type'] else '',
                    'created': claim['created'],
                    'provider': claim['provider']['reference'],
                    'diagnosis_code': diagnosis[0].get('diagnosisCodeableConcept', {}).get('coding', [{}])[0].get('code', ''),
                    'item_code': items[0].get('productOrService', {}).get('coding', [{}])[0].get('code', '')
                })
            elif param['name'].startswith('Observation'):
                observation = param['resource']
                observations.append({
                    'id': observation['id'],
                    'patient_id': observation['subject']['reference'].split('/')[-1],
                    'status': observation['status'],
                    'code_system': observation['code']['coding'][0]['system'] if 'coding' in observation['code'] else '',
                    'code_value': observation['code']['coding'][0]['code'] if 'coding' in observation['code'] else '',
                    'effective_start': observation.get('effectivePeriod', {}).get('start', ''),
                    'effective_end': observation.get('effectivePeriod', {}).get('end', '')
                })
            elif param['name'].startswith('EOB'):
                eob = param['resource']
                diagnosis = eob.get('diagnosis', [{}])
                items = eob.get('item', [{}])

                explanation_of_benefits.append({
                    'id': eob['id'],
                    'patient_id': eob['patient']['reference'].split('/')[-1],
                    'status': eob['status'],
                    'type_system': eob['type']['coding'][0]['system'] if 'coding' in eob['type'] else '',
                    'type_code': eob['type']['coding'][0]['code'] if 'coding' in eob['type'] else '',
                    'created': eob['created'],
                    'diagnosis_code': diagnosis[0].get('diagnosisCodeableConcept', {}).get('coding', [{}])[0].get('code', ''),
                    'item_code': items[0].get('productOrService', {}).get('coding', [{}])[0].get('code', '')
                })
            elif param['name'].startswith('Procedures'):
                procedure = param['resource']
                procedures.append({
                    'id': procedure['id'],
                    'patient_id': procedure['subject']['reference'].split('/')[-1],
                    'status': procedure['status'],
                    'code_system': procedure['code']['coding'][0]['system'] if 'coding' in procedure['code'] else '',
                    'code_value': procedure['code']['coding'][0]['code'] if 'coding' in procedure['code'] else '',
                    'performed_start': procedure.get('performedPeriod', {}).get('start', ''),
                    'performed_end': procedure.get('performedPeriod', {}).get('end', '')
                })

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Export each table to a pipe-delimited CSV file with double quotes around fields and exclude header
    pd.DataFrame(patients).to_csv(
        os.path.join(output_folder, 'patients.csv'), 
        index=False, sep='|', encoding='utf-8-sig', header=False, quoting=1
    )
    pd.DataFrame(claims).to_csv(
        os.path.join(output_folder, 'claims.csv'), 
        index=False, sep='|', encoding='utf-8-sig', header=False, quoting=1
    )
    pd.DataFrame(observations).to_csv(
        os.path.join(output_folder, 'observations.csv'), 
        index=False, sep='|', encoding='utf-8-sig', header=False, quoting=1
    )
    pd.DataFrame(explanation_of_benefits).to_csv(
        os.path.join(output_folder, 'explanation_of_benefits.csv'), 
        index=False, sep='|', encoding='utf-8-sig', header=False, quoting=1
    )
    pd.DataFrame(procedures).to_csv(
        os.path.join(output_folder, 'procedures.csv'), 
        index=False, sep='|', encoding='utf-8-sig', header=False, quoting=1
    )

# Input and output paths
input_ndjson = r"c:\Users\BhargaviDevulapalli\Documents\SRC\LSC\211-lsc_supporting_evidence.ndjson"
output_folder = r"c:\Users\BhargaviDevulapalli\Documents\SRC\LSC\output_tables"

# Extract and export tables
extract_and_export_tables(input_ndjson, output_folder)
