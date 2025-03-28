import json
import csv
from pathlib import Path

def process_ndjson(input_file):
    """Process NDJSON and return structured data for relational tables."""
    parameters = []
    parameter_values = []
    patients = []
    claims = []
    eobs = []

    # Open the file with utf-8-sig to handle BOM
    with open(input_file, 'r', encoding='utf-8-sig') as ndjson_file:
        for line in ndjson_file:
            record = json.loads(line.strip())
            # Main Parameters Table
            parameters.append({
                "id": record.get("id"),
                "resourceType": record.get("resourceType")
            })

            # Parameter Values Table
            for param in record.get("parameter", []):
                param_entry = {"parameters_id": record.get("id"), "name": param.get("name")}
                if "valueBoolean" in param:
                    param_entry["valueBoolean"] = param["valueBoolean"]
                if "valueCode" in param:
                    param_entry["valueCode"] = param["valueCode"]
                if "valueDate" in param:
                    param_entry["valueDate"] = param["valueDate"]
                parameter_values.append(param_entry)

                # Patient Table
                if param.get("name") == "Patient" and "resource" in param:
                    patient = param["resource"]
                    patients.append({
                        "id": patient.get("id"),
                        "name": " ".join(patient.get("name", [{}])[0].get("given", [])) + " " + patient.get("name", [{}])[0].get("family", ""),
                        "gender": patient.get("gender"),
                        "birthDate": patient.get("birthDate"),
                        "address": ", ".join(patient.get("address", [{}])[0].get("line", []))
                    })

                # Claims Table
                if param.get("name") == "Completed Encounters with diagnosis of Acute Bronchitis or Bronchiolitis during Period Claims" and "resource" in param:
                    claim = param["resource"]
                    claims.append({
                        "id": claim.get("id"),
                        "type": ", ".join([coding.get("code") for coding in claim.get("type", {}).get("coding", [])]),
                        "diagnosis": ", ".join([diag.get("diagnosisCodeableConcept", {}).get("coding", [{}])[0].get("code", "") for diag in claim.get("diagnosis", [])]),
                        "servicedDate": claim.get("item", [{}])[0].get("servicedDate")
                    })

                # ExplanationOfBenefit Table
                if param.get("name") == "Completed Encounters with diagnosis of Acute Bronchitis or Bronchiolitis during Period EOB" and "resource" in param:
                    eob = param["resource"]
                    eobs.append({
                        "id": eob.get("id"),
                        "status": eob.get("status"),
                        "type": ", ".join([coding.get("code") for coding in eob.get("type", {}).get("coding", [])]),
                        "outcome": eob.get("outcome")
                    })

    return parameters, parameter_values, patients, claims, eobs

def write_csv(data, output_file, fieldnames):
    """Write data to a pipe-delimited CSV file with double quotes around fields and no header."""
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='|', quotechar='"', quoting=csv.QUOTE_ALL)
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    input_path = Path("c:\\Users\\BhargaviDevulapalli\\Documents\\SRC\\AAB\\81510-aab_supporting_evidence.ndjson")
    output_dir = Path("c:\\Users\\BhargaviDevulapalli\\Documents\\SRC\\AAB\\tables")
    output_dir.mkdir(exist_ok=True)

    # Process NDJSON
    parameters, parameter_values, patients, claims, eobs = process_ndjson(input_path)

    # Write CSV files
    write_csv(parameters, output_dir / "parameters.csv", ["id", "resourceType"])
    write_csv(parameter_values, output_dir / "parameter_values.csv", ["parameters_id", "name", "valueBoolean", "valueCode", "valueDate"])
    write_csv(patients, output_dir / "patients.csv", ["id", "name", "gender", "birthDate", "address"])
    write_csv(claims, output_dir / "claims.csv", ["id", "type", "diagnosis", "servicedDate"])
    write_csv(eobs, output_dir / "eobs.csv", ["id", "status", "type", "outcome"])

    print(f"Pipe-delimited CSV files created in: {output_dir}")
