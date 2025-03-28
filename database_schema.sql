-- Create patients table
CREATE TABLE patients (
    id TEXT PRIMARY KEY,
    lastUpdated TEXT,
    gender TEXT,
    birthDate TEXT,
    address_line1 TEXT,
    address_line2 TEXT,
    city TEXT,
    state TEXT,
    postalCode TEXT,
    telecom_system TEXT,
    telecom_value TEXT,
    name_family TEXT,
    name_given TEXT,
    identifier_system TEXT,
    identifier_value TEXT,
    communication_language TEXT,
    communication_preferred BOOLEAN
);

-- Create claims table
CREATE TABLE claims (
    id TEXT PRIMARY KEY,
    patient_id TEXT,
    status TEXT,
    type_system TEXT,
    type_code TEXT,
    created TEXT,
    provider TEXT,
    diagnosis_code TEXT,
    item_code TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients (id)
);

-- Create observations table
CREATE TABLE observations (
    id TEXT PRIMARY KEY,
    patient_id TEXT,
    status TEXT,
    code_system TEXT,
    code_value TEXT,
    effective_start TEXT,
    effective_end TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients (id)
);

-- Create explanation_of_benefits table
CREATE TABLE explanation_of_benefits (
    id TEXT PRIMARY KEY,
    patient_id TEXT,
    status TEXT,
    type_system TEXT,
    type_code TEXT,
    created TEXT,
    diagnosis_code TEXT,
    item_code TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients (id)
);

-- Create procedures table
CREATE TABLE procedures (
    id TEXT PRIMARY KEY,
    patient_id TEXT,
    status TEXT,
    code_system TEXT,
    code_value TEXT,
    performed_start TEXT,
    performed_end TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients (id)
);
