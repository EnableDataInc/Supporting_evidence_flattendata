-- Create the patients table
CREATE TABLE patients (
    PatientID VARCHAR(255) PRIMARY KEY,
    LastName VARCHAR(255),
    FirstName VARCHAR(255),
    Gender VARCHAR(50),
    BirthDate DATE,
    Address TEXT,
    City VARCHAR(255),
    State VARCHAR(50),
    PostalCode VARCHAR(20),
    Phone VARCHAR(50)
);

-- Create the claims table
CREATE TABLE claims (
    ClaimID VARCHAR(255) PRIMARY KEY,
    PatientID VARCHAR(255),
    Status VARCHAR(50),
    Type TEXT,
    Created DATE,
    Provider VARCHAR(255),
    FOREIGN KEY (PatientID) REFERENCES patients(PatientID)
);

-- Create the observations table
CREATE TABLE observations (
    ObservationID VARCHAR(255) PRIMARY KEY,
    PatientID VARCHAR(255),
    Code VARCHAR(255),
    EffectiveDate DATE,
    Status VARCHAR(50),
    FOREIGN KEY (PatientID) REFERENCES patients(PatientID)
);
