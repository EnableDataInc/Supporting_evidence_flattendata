/* FHIR to Relational Database Schema for Microsoft Access
   Generated on 2025-04-07 14:08:02 */

CREATE TABLE parameters (
    id TEXT(50) PRIMARY KEY,
    resourceType TEXT(255)
);

CREATE TABLE patients (
    id TEXT(50) PRIMARY KEY,
    parameters_id TEXT(50),
    gender TEXT(255),
    birthDate TEXT(255),
    race_code TEXT(255),
    race_system TEXT(255),
    ethnicity_code TEXT(255),
    ethnicity_system TEXT(255)
);

CREATE TABLE patient_identifiers (
    id TEXT(50) PRIMARY KEY,
    patient_id TEXT(50),
    system TEXT(255),
    value MEMO,
    [use] TEXT(255)
);

CREATE TABLE patient_names (
    id TEXT(50) PRIMARY KEY,
    patient_id TEXT(50),
    family TEXT(255),
    given TEXT(255)
);

CREATE TABLE patient_telecom (
    id TEXT(50) PRIMARY KEY,
    patient_id TEXT(50),
    system TEXT(255),
    value MEMO
);

CREATE TABLE patient_addresses (
    id TEXT(50) PRIMARY KEY,
    patient_id TEXT(50),
    line MEMO,
    city TEXT(255),
    state TEXT(255),
    postalCode TEXT(255)
);

CREATE TABLE claims (
    id COUNTER PRIMARY KEY,
    parameters_id TEXT(50),
    [type] TEXT(255),
    patient_id TEXT(50),
    servicedDate TEXT(255)
);

CREATE TABLE claim_diagnoses (
    id COUNTER PRIMARY KEY,
    claim_id TEXT(50),
    sequence TEXT(255),
    code TEXT(255),
    system TEXT(255)
);

CREATE TABLE claim_items (
    id COUNTER PRIMARY KEY,
    claim_id TEXT(50),
    sequence TEXT(255),
    productOrService_code TEXT(255),
    productOrService_system TEXT(255),
    servicedDate TEXT(255)
);

CREATE TABLE explanation_of_benefits (
    id COUNTER PRIMARY KEY,
    parameters_id TEXT(50),
    status TEXT(255),
    [type] TEXT(255),
    patient_id TEXT(50),
    outcome TEXT(255)
);

CREATE TABLE eob_diagnoses (
    id COUNTER PRIMARY KEY,
    eob_id TEXT(50),
    sequence TEXT(255),
    code TEXT(255),
    system TEXT(255)
);

CREATE TABLE eob_items (
    id COUNTER PRIMARY KEY,
    eob_id TEXT(50),
    sequence TEXT(255),
    productOrService_code TEXT(255),
    productOrService_system TEXT(255),
    servicedDate TEXT(255)
);

CREATE TABLE eob_adjudications (
    id COUNTER PRIMARY KEY,
    eob_item_id TEXT(50),
    category_code TEXT(255),
    category_system TEXT(255),
    amount_value TEXT(255),
    amount_currency TEXT(255)
);

CREATE TABLE parameter_values (
    id COUNTER PRIMARY KEY,
    parameters_id TEXT(50),
    name TEXT(255),
    value_type TEXT(255),
    value MEMO
);

