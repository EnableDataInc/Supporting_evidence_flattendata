-- FHIR to Relational Database Schema
-- Generated on 2025-04-04 16:01:09

CREATE TABLE parameters (
    id INTEGER PRIMARY KEY,
    resourceType TEXT
);

CREATE TABLE patients (
    id INTEGER PRIMARY KEY,
    parameters_id TEXT -- Foreign key to parameters(id),
    gender TEXT,
    birthDate TEXT,
    race_code TEXT,
    race_system TEXT,
    ethnicity_code TEXT,
    ethnicity_system TEXT
);

CREATE TABLE patient_identifiers (
    id INTEGER PRIMARY KEY,
    patient_id TEXT -- Foreign key to patient(id),
    system TEXT,
    value TEXT,
    use TEXT
);

CREATE TABLE patient_names (
    id INTEGER PRIMARY KEY,
    patient_id TEXT -- Foreign key to patient(id),
    family TEXT,
    given TEXT
);

CREATE TABLE patient_telecom (
    id INTEGER PRIMARY KEY,
    patient_id TEXT -- Foreign key to patient(id),
    system TEXT,
    value TEXT
);

CREATE TABLE patient_addresses (
    id INTEGER PRIMARY KEY,
    patient_id TEXT -- Foreign key to patient(id),
    line TEXT,
    city TEXT,
    state TEXT,
    postalCode TEXT
);

CREATE TABLE claims (
    id INTEGER PRIMARY KEY,
    parameters_id TEXT -- Foreign key to parameters(id),
    type TEXT,
    patient_id TEXT -- Foreign key to patient(id),
    servicedDate TEXT
);

CREATE TABLE claim_diagnoses (
    id INTEGER PRIMARY KEY,
    claim_id TEXT -- Foreign key to claim(id),
    sequence TEXT,
    code TEXT,
    system TEXT
);

CREATE TABLE claim_items (
    id INTEGER PRIMARY KEY,
    claim_id TEXT -- Foreign key to claim(id),
    sequence TEXT,
    productOrService_code TEXT,
    productOrService_system TEXT,
    servicedDate TEXT
);

CREATE TABLE explanation_of_benefits (
    id INTEGER PRIMARY KEY,
    parameters_id TEXT -- Foreign key to parameters(id),
    status TEXT,
    type TEXT,
    patient_id TEXT -- Foreign key to patient(id),
    outcome TEXT
);

CREATE TABLE eob_diagnoses (
    id INTEGER PRIMARY KEY,
    eob_id TEXT -- Foreign key to eob(id),
    sequence TEXT,
    code TEXT,
    system TEXT
);

CREATE TABLE eob_items (
    id INTEGER PRIMARY KEY,
    eob_id TEXT -- Foreign key to eob(id),
    sequence TEXT,
    productOrService_code TEXT,
    productOrService_system TEXT,
    servicedDate TEXT
);

CREATE TABLE eob_adjudications (
    id INTEGER PRIMARY KEY,
    eob_item_id TEXT -- Foreign key to eob_item(id),
    category_code TEXT,
    category_system TEXT,
    amount_value TEXT,
    amount_currency TEXT
);

CREATE TABLE parameter_values (
    id INTEGER PRIMARY KEY,
    parameters_id TEXT -- Foreign key to parameters(id),
    name TEXT,
    value_type TEXT,
    value TEXT
);

