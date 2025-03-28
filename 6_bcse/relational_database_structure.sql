-- Table for Parameters
CREATE TABLE parameters (
    id VARCHAR(255) PRIMARY KEY,
    resourceType VARCHAR(255)
);

-- Table for Parameter Values
CREATE TABLE parameter_values (
    id SERIAL PRIMARY KEY,
    parameters_id VARCHAR(255),
    name VARCHAR(255),
    valueBoolean BOOLEAN,
    valueCode VARCHAR(255),
    valueDate DATE,
    FOREIGN KEY (parameters_id) REFERENCES parameters(id)
);

-- Table for Patients
CREATE TABLE patients (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    gender VARCHAR(50),
    birthDate DATE,
    address TEXT
);

-- Table for Claims
CREATE TABLE claims (
    id VARCHAR(255) PRIMARY KEY,
    type TEXT,
    diagnosis TEXT,
    servicedDate DATE
);

-- Table for Explanation of Benefits (EOBs)
CREATE TABLE eobs (
    id VARCHAR(255) PRIMARY KEY,
    status VARCHAR(50),
    type TEXT,
    outcome VARCHAR(255)
);
