import json
import pandas as pd
from collections import defaultdict

def extract_resources(data):
    """
    Dynamically extracts all resource types from the NDJSON data.
    """
    resources = defaultdict(list)
    for entry in data:
        for param in entry.get("parameter", []):
            resource = param.get("resource", {})
            resource_type = resource.get("resourceType")
            if resource_type:
                resources[resource_type].append(resource)
    return resources

def flatten_resources(resources):
    """
    Flattens each resource type into a DataFrame.
    """
    flattened_dataframes = {}
    for resource_type, resource_list in resources.items():
        flattened_data = [flatten_json(resource) for resource in resource_list]
        flattened_dataframes[resource_type] = pd.DataFrame(flattened_data)
    return flattened_dataframes

def flatten_json(json_obj, parent_key='', sep='.'):
    """
    Recursively flattens a nested JSON object.
    """
    items = []
    for k, v in json_obj.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, (dict, list)):
                    items.extend(flatten_json(item, f"{new_key}[{i}]", sep=sep).items())
                else:
                    items.append((f"{new_key}[{i}]", item))
        else:
            items.append((new_key, v))
    return dict(items)

def extract_child_tables(resources):
    """
    Extracts child tables for core resources such as ExplanationOfBenefit, Claim, Encounter, etc.
    """
    child_tables = {
        "eob_diagnoses": [],
        "eob_items": [],
        "eob_adjudications": [],
        "claim_diagnoses": [],
        "claim_items": [],
        "encounter_participants": [],
        "patient_communication": []
    }

    # Extract ExplanationOfBenefit child tables
    for eob in resources.get("ExplanationOfBenefit", []):
        eob_id = eob.get("id")
        
        # Extract diagnoses
        for diagnosis in eob.get("diagnosis", []):
            child_tables["eob_diagnoses"].append({
                "EOBID": eob_id,
                "Sequence": diagnosis.get("sequence"),
                "DiagnosisCode": diagnosis.get("diagnosisCodeableConcept", {}).get("coding", [{}])[0].get("code"),
                "DiagnosisType": diagnosis.get("type", [{}])[0].get("coding", [{}])[0].get("code")
            })
        
        # Extract items
        for item in eob.get("item", []):
            child_tables["eob_items"].append({
                "EOBID": eob_id,
                "Sequence": item.get("sequence"),
                "ProductOrServiceCode": item.get("productOrService", {}).get("coding", [{}])[0].get("code"),
                "ServicedDate": item.get("servicedDate")
            })
        
        # Extract adjudications
        for item in eob.get("item", []):
            for adjudication in item.get("adjudication", []):
                child_tables["eob_adjudications"].append({
                    "EOBID": eob_id,
                    "Category": adjudication.get("category", {}).get("coding", [{}])[0].get("code"),
                    "Amount": adjudication.get("amount", {}).get("value"),
                    "Currency": adjudication.get("amount", {}).get("currency")
                })

    # Extract Claim child tables
    for claim in resources.get("Claim", []):
        claim_id = claim.get("id")
        
        # Extract diagnoses
        for diagnosis in claim.get("diagnosis", []):
            child_tables["claim_diagnoses"].append({
                "ClaimID": claim_id,
                "Sequence": diagnosis.get("sequence"),
                "DiagnosisCode": diagnosis.get("diagnosisCodeableConcept", {}).get("coding", [{}])[0].get("code"),
                "DiagnosisType": diagnosis.get("type", [{}])[0].get("coding", [{}])[0].get("code")
            })
        
        # Extract items
        for item in claim.get("item", []):
            child_tables["claim_items"].append({
                "ClaimID": claim_id,
                "Sequence": item.get("sequence"),
                "ProductOrServiceCode": item.get("productOrService", {}).get("coding", [{}])[0].get("code"),
                "ServicedDate": item.get("servicedDate")
            })

    # Extract Encounter child tables
    for encounter in resources.get("Encounter", []):
        encounter_id = encounter.get("id")
        
        # Extract participants
        for participant in encounter.get("participant", []):
            child_tables["encounter_participants"].append({
                "EncounterID": encounter_id,
                "ParticipantReference": participant.get("individual", {}).get("reference")
            })

    # Extract Patient child tables
    for patient in resources.get("Patient", []):
        patient_id = patient.get("id")
        
        # Extract communication preferences
        for communication in patient.get("communication", []):
            child_tables["patient_communication"].append({
                "PatientID": patient_id,
                "LanguageCode": communication.get("language", {}).get("coding", [{}])[0].get("code"),
                "Preferred": communication.get("preferred"),
                "PreferenceType": communication.get("_preferred", {}).get("extension", [{}])[0].get("valueCoding", {}).get("code")
            })

    return {key: pd.DataFrame(value) for key, value in child_tables.items()}

def convert_ndjson_to_relational_csv(input_file, output_dir):
    """
    Converts NDJSON data to relational CSV files for all resource types.
    """
    # Read the NDJSON file
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        data = [json.loads(line.strip()) for line in f]

    # Extract and flatten resources
    resources = extract_resources(data)
    flattened_dataframes = flatten_resources(resources)

    # Extract child tables
    child_tables = extract_child_tables(resources)

    # Save each resource type to a separate CSV file
    for resource_type, df in flattened_dataframes.items():
        output_file = f"{output_dir}/{resource_type.lower()}.csv"
        df.to_csv(output_file, index=False, encoding='utf-8', sep='|', header=True, quoting=1)
        print(f"CSV file created for resource type '{resource_type}' at: {output_file}")

    # Save child tables to separate CSV files
    for table_name, df in child_tables.items():
        output_file = f"{output_dir}/{table_name}.csv"
        df.to_csv(output_file, index=False, encoding='utf-8', sep='|', header=True, quoting=1)
        print(f"CSV file created for child table '{table_name}' at: {output_file}")

# Input and output paths
input_ndjson = r"c:\Users\BhargaviDevulapalli\Documents\SRC\LSC\211-lsc_supporting_evidence.ndjson"
output_dir = r"c:\Users\BhargaviDevulapalli\Documents\SRC\LSC\output"

# Convert NDJSON to relational CSV files
convert_ndjson_to_relational_csv(input_ndjson, output_dir)
