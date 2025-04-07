import json
import os
import csv
from pathlib import Path
from datetime import datetime

class FHIRToQuotedPipeDelimitedNoHeader:
    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize tables with their columns
        self.tables = {
            'parameters': ['id', 'resourceType'],
            'patients': ['id', 'parameters_id', 'gender', 'birthDate', 'race_code', 'race_system', 'ethnicity_code', 'ethnicity_system'],
            'patient_identifiers': ['id', 'patient_id', 'system', 'value', 'use'],
            'patient_names': ['id', 'patient_id', 'family', 'given'],
            'patient_telecom': ['id', 'patient_id', 'system', 'value'],
            'patient_addresses': ['id', 'patient_id', 'line', 'city', 'state', 'postalCode'],
            'claims': ['id', 'parameters_id', 'type', 'patient_id', 'servicedDate'],
            'claim_diagnoses': ['id', 'claim_id', 'sequence', 'code', 'system'],
            'claim_items': ['id', 'claim_id', 'sequence', 'productOrService_code', 'productOrService_system', 'servicedDate'],
            'explanation_of_benefits': ['id', 'parameters_id', 'status', 'type', 'patient_id', 'outcome'],
            'eob_diagnoses': ['id', 'eob_id', 'sequence', 'code', 'system'],
            'eob_items': ['id', 'eob_id', 'sequence', 'productOrService_code', 'productOrService_system', 'servicedDate'],
            'eob_adjudications': ['id', 'eob_item_id', 'category_code', 'category_system', 'amount_value', 'amount_currency'],
            'parameter_values': ['id', 'parameters_id', 'name', 'value_type', 'value']
        }
        
        # Initialize data dictionaries
        self.data = {table: [] for table in self.tables}
        
        # Counter for generating IDs
        self.counter = {table: 1 for table in self.tables}
    
    def process_file(self):
        """Process the input NDJSON file"""
        with open(self.input_file, 'r') as f:
            for line_number, line in enumerate(f, start=1):
                if line.strip():  # Skip empty lines
                    try:
                        record = json.loads(line)
                        self.process_record(record)
                    except json.JSONDecodeError as e:
                        print(f"Skipping invalid JSON at line {line_number}: {e}")
    
    def process_record(self, record):
        """Process a single FHIR record"""
        if record['resourceType'] == 'Parameters':
            parameters_id = record['id']
            
            # Add to parameters table
            self.data['parameters'].append({
                'id': parameters_id,
                'resourceType': record['resourceType']
            })
            
            # Process parameters
            for param in record['parameter']:
                self.process_parameter(param, parameters_id)
    
    def process_parameter(self, param, parameters_id):
        """Process a single parameter from the FHIR record"""
        name = param['name']
        
        # Check if this parameter contains a resource
        if 'resource' in param:
            resource = param['resource']
            resource_type = resource['resourceType']
            
            if resource_type == 'Patient':
                self.process_patient(resource, parameters_id)
            elif resource_type == 'Claim':
                self.process_claim(resource, parameters_id)
            elif resource_type == 'ExplanationOfBenefit':
                self.process_eob(resource, parameters_id)
        else:
            # This is a simple parameter with a value
            value_entry = {'id': self.counter['parameter_values'], 
                          'parameters_id': parameters_id,
                          'name': name,
                          'value_type': None,
                          'value': None}
            
            # Find the value field (valueBoolean, valueString, etc.)
            for key, value in param.items():
                if key.startswith('value'):
                    value_type = key[5:]  # Remove 'value' prefix
                    if value_type == '':
                        value_type = 'String'
                    
                    value_entry['value_type'] = value_type
                    
                    # Convert value to string for CSV storage
                    if isinstance(value, (bool, int, float)):
                        value_entry['value'] = str(value)
                    elif isinstance(value, dict) and 'code' in value:
                        value_entry['value'] = value['code']
                    else:
                        value_entry['value'] = value
                    
                    break
            
            self.data['parameter_values'].append(value_entry)
            self.counter['parameter_values'] += 1
    
    def process_patient(self, patient, parameters_id):
        """Process a Patient resource"""
        patient_id = patient['id']
        
        # Basic patient info
        patient_data = {
            'id': patient_id,
            'parameters_id': parameters_id,
            'gender': patient.get('gender', ''),
            'birthDate': patient.get('birthDate', ''),
            'race_code': '',
            'race_system': '',
            'ethnicity_code': '',
            'ethnicity_system': ''
        }
        
        # Extract race and ethnicity from extensions
        if 'extension' in patient:
            for ext in patient['extension']:
                if 'url' in ext and ext['url'].endswith('us-core-race'):
                    for race_ext in ext.get('extension', []):
                        if race_ext.get('url') in ['ombCategory', 'detailed'] and 'valueCoding' in race_ext:
                            patient_data['race_code'] = race_ext['valueCoding'].get('code', '')
                            patient_data['race_system'] = race_ext['valueCoding'].get('system', '')
                
                if 'url' in ext and ext['url'].endswith('us-core-ethnicity'):
                    for eth_ext in ext.get('extension', []):
                        if eth_ext.get('url') == 'ombCategory' and 'valueCoding' in eth_ext:
                            patient_data['ethnicity_code'] = eth_ext['valueCoding'].get('code', '')
                            patient_data['ethnicity_system'] = eth_ext['valueCoding'].get('system', '')
        
        self.data['patients'].append(patient_data)
        
        # Process identifiers
        if 'identifier' in patient:
            for identifier in patient['identifier']:
                self.data['patient_identifiers'].append({
                    'id': self.counter['patient_identifiers'],
                    'patient_id': patient_id,
                    'system': identifier.get('system', ''),
                    'value': identifier.get('value', ''),
                    'use': identifier.get('use', '')
                })
                self.counter['patient_identifiers'] += 1
        
        # Process names
        if 'name' in patient:
            for name in patient['name']:
                self.data['patient_names'].append({
                    'id': self.counter['patient_names'],
                    'patient_id': patient_id,
                    'family': name.get('family', ''),
                    'given': ' '.join(name.get('given', []))
                })
                self.counter['patient_names'] += 1
        
        # Process telecom
        if 'telecom' in patient:
            for telecom in patient['telecom']:
                self.data['patient_telecom'].append({
                    'id': self.counter['patient_telecom'],
                    'patient_id': patient_id,
                    'system': telecom.get('system', ''),
                    'value': telecom.get('value', '')
                })
                self.counter['patient_telecom'] += 1
        
        # Process addresses
        if 'address' in patient:
            for address in patient['address']:
                self.data['patient_addresses'].append({
                    'id': self.counter['patient_addresses'],
                    'patient_id': patient_id,
                    'line': ' '.join(address.get('line', [])),
                    'city': address.get('city', ''),
                    'state': address.get('state', ''),
                    'postalCode': address.get('postalCode', '')
                })
                self.counter['patient_addresses'] += 1
    
    def process_claim(self, claim, parameters_id):
        """Process a Claim resource"""
        claim_id = claim['id']
        
        # Get patient reference
        patient_ref = claim.get('patient', {}).get('reference', '')
        patient_id = patient_ref.split('/')[-1] if '/' in patient_ref else patient_ref
        
        # Get claim type
        claim_type = ''
        if 'type' in claim and 'coding' in claim['type']:
            coding = claim['type']['coding'][0] if claim['type']['coding'] else None
            claim_type = coding.get('code', '') if coding else ''
        
        # Basic claim info
        self.data['claims'].append({
            'id': claim_id,
            'parameters_id': parameters_id,
            'type': claim_type,
            'patient_id': patient_id,
            'servicedDate': ''  # Will get from items
        })
        
        # Process diagnoses
        if 'diagnosis' in claim:
            for diag in claim['diagnosis']:
                sequence = diag.get('sequence', '')
                code = ''
                system = ''
                
                if 'diagnosisCodeableConcept' in diag and 'coding' in diag['diagnosisCodeableConcept']:
                    coding = diag['diagnosisCodeableConcept']['coding'][0] if diag['diagnosisCodeableConcept']['coding'] else None
                    if coding:
                        code = coding.get('code', '')
                        system = coding.get('system', '')
                
                self.data['claim_diagnoses'].append({
                    'id': self.counter['claim_diagnoses'],
                    'claim_id': claim_id,
                    'sequence': sequence,
                    'code': code,
                    'system': system
                })
                self.counter['claim_diagnoses'] += 1
        
        # Process items
        if 'item' in claim:
            for item in claim['item']:
                sequence = item.get('sequence', '')
                code = ''
                system = ''
                serviced_date = item.get('servicedDate', '')
                
                # Update claim with first item's service date if available
                if serviced_date and not self.data['claims'][-1]['servicedDate']:
                    self.data['claims'][-1]['servicedDate'] = serviced_date
                
                if 'productOrService' in item and 'coding' in item['productOrService']:
                    coding = item['productOrService']['coding'][0] if item['productOrService']['coding'] else None
                    if coding:
                        code = coding.get('code', '')
                        system = coding.get('system', '')
                
                self.data['claim_items'].append({
                    'id': self.counter['claim_items'],
                    'claim_id': claim_id,
                    'sequence': sequence,
                    'productOrService_code': code,
                    'productOrService_system': system,
                    'servicedDate': serviced_date
                })
                self.counter['claim_items'] += 1
    
    def process_eob(self, eob, parameters_id):
        """Process an ExplanationOfBenefit resource"""
        eob_id = eob['id']
        
        # Get patient reference
        patient_ref = eob.get('patient', {}).get('reference', '')
        patient_id = patient_ref.split('/')[-1] if '/' in patient_ref else patient_ref
        
        # Get EOB type
        eob_type = ''
        if 'type' in eob and 'coding' in eob['type']:
            coding = eob['type']['coding'][0] if eob['type']['coding'] else None
            eob_type = coding.get('code', '') if coding else ''
        
        # Basic EOB info
        self.data['explanation_of_benefits'].append({
            'id': eob_id,
            'parameters_id': parameters_id,
            'status': eob.get('status', ''),
            'type': eob_type,
            'patient_id': patient_id,
            'outcome': eob.get('outcome', '')
        })
        
        # Process diagnoses
        if 'diagnosis' in eob:
            for diag in eob['diagnosis']:
                sequence = diag.get('sequence', '')
                code = ''
                system = ''
                
                if 'diagnosisCodeableConcept' in diag and 'coding' in diag['diagnosisCodeableConcept']:
                    coding = diag['diagnosisCodeableConcept']['coding'][0] if diag['diagnosisCodeableConcept']['coding'] else None
                    if coding:
                        code = coding.get('code', '')
                        system = coding.get('system', '')
                
                self.data['eob_diagnoses'].append({
                    'id': self.counter['eob_diagnoses'],
                    'eob_id': eob_id,
                    'sequence': sequence,
                    'code': code,
                    'system': system
                })
                self.counter['eob_diagnoses'] += 1
        
        # Process items
        if 'item' in eob:
            for item in eob['item']:
                sequence = item.get('sequence', '')
                code = ''
                system = ''
                serviced_date = item.get('servicedDate', '')
                
                if 'productOrService' in item and 'coding' in item['productOrService']:
                    coding = item['productOrService']['coding'][0] if item['productOrService']['coding'] else None
                    if coding:
                        code = coding.get('code', '')
                        system = coding.get('system', '')
                
                item_id = self.counter['eob_items']
                self.data['eob_items'].append({
                    'id': item_id,
                    'eob_id': eob_id,
                    'sequence': sequence,
                    'productOrService_code': code,
                    'productOrService_system': system,
                    'servicedDate': serviced_date
                })
                self.counter['eob_items'] += 1
                
                # Process adjudications
                if 'adjudication' in item:
                    for adj in item['adjudication']:
                        category_code = ''
                        category_system = ''
                        amount_value = ''
                        amount_currency = ''
                        
                        if 'category' in adj and 'coding' in adj['category']:
                            coding = adj['category']['coding'][0] if adj['category']['coding'] else None
                            if coding:
                                category_code = coding.get('code', '')
                                category_system = coding.get('system', '')
                        
                        if 'amount' in adj:
                            amount_value = str(adj['amount'].get('value', ''))
                            amount_currency = adj['amount'].get('currency', '')
                        
                        self.data['eob_adjudications'].append({
                            'id': self.counter['eob_adjudications'],
                            'eob_item_id': item_id,
                            'category_code': category_code,
                            'category_system': category_system,
                            'amount_value': amount_value,
                            'amount_currency': amount_currency
                        })
                        self.counter['eob_adjudications'] += 1
    
    def export_to_quoted_pipe_delimited_no_header(self):
        """Export all tables to pipe-delimited CSV files with quoted fields but no headers"""
        for table, columns in self.tables.items():
            if not self.data[table]:  # Skip empty tables
                continue
                
            file_path = os.path.join(self.output_dir, f"{table}.csv")
            
            with open(file_path, 'w', newline='') as csvfile:
                # Create a writer that will not write a header but will quote all fields
                writer = csv.writer(
                    csvfile,
                    delimiter='|',
                    quotechar='"',
                    quoting=csv.QUOTE_ALL
                )
                
                # For each row, extract values in the same order as columns
                for row in self.data[table]:
                    # Extract values in the correct order
                    values = []
                    for col in columns:
                        value = row.get(col, '')
                        # Escape double quotes by doubling them
                        if isinstance(value, str) and '"' in value:
                            value = value.replace('"', '""')
                        values.append(value)
                    
                    writer.writerow(values)
            
            print(f"Exported {len(self.data[table])} rows to {file_path}")
    
    def generate_schema_sql(self):
        """Generate SQL schema for the database tables"""
        sql_path = os.path.join(self.output_dir, "schema.sql")
        
        with open(sql_path, 'w') as f:
            f.write("-- FHIR to Relational Database Schema\n")
            f.write(f"-- Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Generate CREATE TABLE statements
            for table, columns in self.tables.items():
                f.write(f"CREATE TABLE {table} (\n")
                
                col_defs = []
                for col in columns:
                    data_type = "INTEGER PRIMARY KEY" if col == 'id' else "TEXT"
                    
                    # Add foreign key hints in comments
                    fk_comment = ""
                    if col.endswith('_id') and col != 'id':
                        referenced_table = col[:-3]
                        fk_comment = f" -- Foreign key to {referenced_table}(id)"
                    
                    col_defs.append(f"    {col} {data_type}{fk_comment}")
                
                f.write(",\n".join(col_defs))
                f.write("\n);\n\n")
            
            print(f"Generated SQL schema at {sql_path}")
    
    def generate_microsoft_access_sql(self):
        """Generate SQL schema specifically for Microsoft Access"""
        access_sql_path = os.path.join(self.output_dir, "ms_access_schema.sql")
        
        with open(access_sql_path, 'w') as f:
            f.write("/* FHIR to Relational Database Schema for Microsoft Access\n")
            f.write(f"   Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} */\n\n")
            
            # Generate CREATE TABLE statements for Access
            for table, columns in self.tables.items():
                f.write(f"CREATE TABLE {table} (\n")
                
                col_defs = []
                for col in columns:
                    # Use Access-specific data types
                    if col == 'id' and 'patient' not in table and 'parameters' not in table:
                        data_type = "COUNTER PRIMARY KEY"
                    elif col == 'id':
                        data_type = "TEXT(50) PRIMARY KEY"
                    elif col.endswith('_id'):
                        data_type = "TEXT(50)"
                    elif col in ['line', 'value']:
                        data_type = "MEMO"
                    else:
                        data_type = "TEXT(255)"
                    
                    # Escape reserved words
                    if col in ['type', 'use']:
                        col = f"[{col}]"
                    
                    col_defs.append(f"    {col} {data_type}")
                
                f.write(",\n".join(col_defs))
                f.write("\n);\n\n")
            
            print(f"Generated Microsoft Access SQL schema at {access_sql_path}")
    
    def generate_field_maps(self):
        """Generate field mapping files for each table"""
        field_maps_dir = os.path.join(self.output_dir, "field_maps")
        os.makedirs(field_maps_dir, exist_ok=True)
        
        for table, columns in self.tables.items():
            file_path = os.path.join(field_maps_dir, f"{table}_fields.txt")
            
            with open(file_path, 'w') as f:
                f.write(f"Field map for table: {table}\n")
                f.write("---------------------------\n")
                f.write("Position | Field Name\n")
                f.write("---------------------------\n")
                
                for i, col in enumerate(columns):
                    f.write(f"{i+1:8} | {col}\n")
            
            print(f"Generated field map at {file_path}")

def main():
    input_file = '81779-amr_supporting_evidence.ndjson'
    output_dir = 'fhir_relational_quoted_pipe_no_header'
    
    converter = FHIRToQuotedPipeDelimitedNoHeader(input_file, output_dir)
    converter.process_file()
    converter.export_to_quoted_pipe_delimited_no_header()
    converter.generate_schema_sql()
    converter.generate_microsoft_access_sql()
    converter.generate_field_maps()
    
    print(f"\nConversion completed successfully!")
    print(f"Quoted pipe-delimited CSV files without headers created in: {output_dir}")
    print(f"SQL schemas and field maps are included for reference.")
    
    # Print table statistics
    print("\nTable statistics:")
    for table, data in converter.data.items():
        if data:  # Only show non-empty tables
            print(f"- {table}: {len(data)} rows")
    
    print("\nNOTE: Since header rows were omitted, field maps have been generated")
    print("in the 'field_maps' subdirectory to help identify column positions.")

if __name__ == "__main__":
    main()