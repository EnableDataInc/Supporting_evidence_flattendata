-- Patients Table
CREATE TABLE patients (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    gender VARCHAR,
    birthDate DATE,
    address VARCHAR,
    city VARCHAR,
    state VARCHAR,
    postalCode VARCHAR,
    telecom VARCHAR
);

-- Claims Table
CREATE TABLE claims (
    id VARCHAR PRIMARY KEY,
    patient_id VARCHAR,
    status VARCHAR,
    type VARCHAR,
    created DATE,
    provider VARCHAR,
    diagnosis VARCHAR,
    servicedDate DATE,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

-- MedicationDispenses Table
CREATE TABLE medication_dispenses (
    id VARCHAR PRIMARY KEY,
    patient_id VARCHAR,
    status VARCHAR,
    medication VARCHAR,
    quantity FLOAT,
    daysSupply INT,
    whenHandedOver DATE,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);