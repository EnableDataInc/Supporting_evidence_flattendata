import json
import csv
from pathlib import Path

def flatten_patient(patient):
    """Flatten patient data."""
    return {
        "id": patient.get("id"),
        "name": " ".join(patient.get("name", [{}])[0].get("given", [])) + " " + patient.get("name", [{}])[0].get("family", ""),
        "gender": patient.get("gender"),
        "birthDate": patient.get("birthDate"),
        "address": ", ".join(patient.get("address", [{}])[0].get("line", [])),
        "city": patient.get("address", [{}])[0].get("city"),
        "state": patient.get("address", [{}])[0].get("state"),
        "postalCode": patient.get("address", [{}])[0].get("postalCode"),
        "telecom": patient.get("telecom", [{}])[0].get("value"),
    }

def flatten_claim(claim):
    """Flatten claim data."""
    return {
        "id": claim.get("id"),
        "patient_id": claim.get("patient", {}).get("reference", "").split("/")[-1],
        "status": claim.get("status"),
        "type": ", ".join([coding.get("code") for coding in claim.get("type", {}).get("coding", [])]),
        "created": claim.get("created"),
        "provider": claim.get("provider", {}).get("reference", "").split("/")[-1],
        "diagnosis": ", ".join([diag.get("diagnosisCodeableConcept", {}).get("coding", [{}])[0].get("code", "") for diag in claim.get("diagnosis", [])]),
        "servicedDate": claim.get("item", [{}])[0].get("servicedDate"),
    }

def flatten_medication_dispense(med_dispense):
    """Flatten medication dispense data."""
    return {
        "id": med_dispense.get("id"),
        "patient_id": med_dispense.get("subject", {}).get("reference", "").split("/")[-1],
        "status": med_dispense.get("status"),
        "medication": med_dispense.get("medicationCodeableConcept", {}).get("coding", [{}])[0].get("display"),
        "quantity": med_dispense.get("quantity", {}).get("value"),
        "daysSupply": med_dispense.get("daysSupply", {}).get("value"),
        "whenHandedOver": med_dispense.get("whenHandedOver"),
    }

def process_ndjson(input_file):
    """Process NDJSON and extract data for relational tables."""
    patients = []
    claims = []
    medication_dispenses = []

    # Use utf-8-sig to handle BOM
    with open(input_file, 'r', encoding='utf-8-sig') as ndjson_file:
        for line in ndjson_file:
            record = json.loads(line.strip())
            for param in record.get("parameter", []):
                if param.get("name") == "Patient" and "resource" in param:
                    patients.append(flatten_patient(param["resource"]))
                if param.get("name").startswith("Claims") and "resource" in param:
                    claims.append(flatten_claim(param["resource"]))
                if param.get("name").startswith("Dispenses") and "resource" in param:
                    medication_dispenses.append(flatten_medication_dispense(param["resource"]))

    return patients, claims, medication_dispenses

def write_pipe_delimited_csv(data, output_file, fieldnames):
    """Write data to a pipe-delimited CSV file with double quotes around fields and no header."""
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter='|', quoting=csv.QUOTE_ALL)
        for row in data:
            writer.writerow([row[field] for field in fieldnames])

if __name__ == "__main__":
    input_path = Path("c:\\Users\\BhargaviDevulapalli\\Documents\\SRC\\AMR\\81779-amr_supporting_evidence.ndjson")
    output_dir = Path("c:\\Users\\BhargaviDevulapalli\\Documents\\SRC\\AMR\\tables")
    output_dir.mkdir(exist_ok=True)

    # Process NDJSON
    patients, claims, medication_dispenses = process_ndjson(input_path)

    # Write pipe-delimited CSV files without headers
    write_pipe_delimited_csv(patients, output_dir / "patients.csv", ["id", "name", "gender", "birthDate", "address", "city", "state", "postalCode", "telecom"])
    write_pipe_delimited_csv(claims, output_dir / "claims.csv", ["id", "patient_id", "status", "type", "created", "provider", "diagnosis", "servicedDate"])
    write_pipe_delimited_csv(medication_dispenses, output_dir / "medication_dispenses.csv", ["id", "patient_id", "status", "medication", "quantity", "daysSupply", "whenHandedOver"])

    print(f"Pipe-delimited CSV files created in: {output_dir}")
