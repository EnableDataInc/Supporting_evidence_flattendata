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

-- Create the patient_communication table (child of patients)
CREATE TABLE patient_communication (
    CommunicationID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID VARCHAR(255),
    LanguageCode VARCHAR(50),
    Preferred BOOLEAN,
    PreferenceType VARCHAR(50),
    FOREIGN KEY (PatientID) REFERENCES patients(PatientID)
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

-- Create the claim_diagnoses table (child of claims)
CREATE TABLE claim_diagnoses (
    ClaimDiagnosisID INT AUTO_INCREMENT PRIMARY KEY,
    ClaimID VARCHAR(255),
    Sequence INT,
    DiagnosisCode VARCHAR(255),
    DiagnosisType VARCHAR(50),
    FOREIGN KEY (ClaimID) REFERENCES claims(ClaimID)
);

-- Create the claim_items table (child of claims)
CREATE TABLE claim_items (
    ClaimItemID INT AUTO_INCREMENT PRIMARY KEY,
    ClaimID VARCHAR(255),
    Sequence INT,
    ProductOrServiceCode VARCHAR(255),
    ServicedDate DATE,
    FOREIGN KEY (ClaimID) REFERENCES claims(ClaimID)
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

-- Create the explanation_of_benefits table
CREATE TABLE explanation_of_benefits (
    EOBID VARCHAR(255) PRIMARY KEY,
    PatientID VARCHAR(255),
    Status VARCHAR(50),
    Type TEXT,
    Created DATE,
    Provider VARCHAR(255),
    Outcome VARCHAR(50),
    FOREIGN KEY (PatientID) REFERENCES patients(PatientID)
);

-- Create the eob_diagnoses table (child of explanation_of_benefits)
CREATE TABLE eob_diagnoses (
    EOBDiagnosisID INT AUTO_INCREMENT PRIMARY KEY,
    EOBID VARCHAR(255),
    Sequence INT,
    DiagnosisCode VARCHAR(255),
    DiagnosisType VARCHAR(50),
    FOREIGN KEY (EOBID) REFERENCES explanation_of_benefits(EOBID)
);

-- Create the eob_items table (child of explanation_of_benefits)
CREATE TABLE eob_items (
    EOBItemID INT AUTO_INCREMENT PRIMARY KEY,
    EOBID VARCHAR(255),
    Sequence INT,
    ProductOrServiceCode VARCHAR(255),
    ServicedDate DATE,
    FOREIGN KEY (EOBID) REFERENCES explanation_of_benefits(EOBID)
);

-- Create the eob_adjudications table (child of explanation_of_benefits)
CREATE TABLE eob_adjudications (
    EOBAdjudicationID INT AUTO_INCREMENT PRIMARY KEY,
    EOBID VARCHAR(255),
    Category VARCHAR(255),
    Amount DECIMAL(10, 2),
    Currency VARCHAR(10),
    FOREIGN KEY (EOBID) REFERENCES explanation_of_benefits(EOBID)
);

-- Create the procedures table
CREATE TABLE procedures (
    ProcedureID VARCHAR(255) PRIMARY KEY,
    PatientID VARCHAR(255),
    Code VARCHAR(255),
    PerformedDate DATE,
    Status VARCHAR(50),
    FOREIGN KEY (PatientID) REFERENCES patients(PatientID)
);

-- Create the encounters table
CREATE TABLE encounters (
    EncounterID VARCHAR(255) PRIMARY KEY,
    PatientID VARCHAR(255),
    Type TEXT,
    StartDate DATE,
    EndDate DATE,
    Status VARCHAR(50),
    FOREIGN KEY (PatientID) REFERENCES patients(PatientID)
);

-- Create the encounter_participants table (child of encounters)
CREATE TABLE encounter_participants (
    EncounterParticipantID INT AUTO_INCREMENT PRIMARY KEY,
    EncounterID VARCHAR(255),
    ParticipantReference VARCHAR(255),
    FOREIGN KEY (EncounterID) REFERENCES encounters(EncounterID)
);
