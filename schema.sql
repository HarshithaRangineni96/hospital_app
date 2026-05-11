-- ============================================================
--  Hospital App - Final 3NF Schema
--  Run this file to initialize the database.
-- ============================================================

DROP TABLE IF EXISTS Admissions;
DROP TABLE IF EXISTS Doctors;
DROP TABLE IF EXISTS Patients;

CREATE TABLE Patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL UNIQUE,
    date_of_birth DATE NOT NULL
);

CREATE TABLE Doctors (
    doctor_id      INT AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL
);

CREATE TABLE Admissions (
    admission_id   INT AUTO_INCREMENT PRIMARY KEY,
    patient_id     INT  NOT NULL,
    doctor_id      INT  NOT NULL,
    admission_date DATE NOT NULL,
    discharge_date DATE,
    notes          VARCHAR(100),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id)  REFERENCES Doctors(doctor_id)
);

-- ── Seed Data ────────────────────────────────────────────────

INSERT INTO Patients (name, date_of_birth) VALUES
('John Smith',    '1985-06-15'),
('Alice Brown',   '1990-09-20'),
('Karun Bhaskar', '1978-03-10'),
('Pavan Gopal',   '2000-12-05');

INSERT INTO Doctors (name, specialization) VALUES
('Dr. Cristie', 'Cardiology'),
('Dr. Adams',   'Neurology'),
('Dr. Clark',   'Orthopedics'),
('Dr. Davis',   'Pediatrics'),
('Dr. Evans',   'General Medicine');

INSERT INTO Admissions (patient_id, doctor_id, admission_date, discharge_date, notes) VALUES
(1, 1, '2025-01-01', '2025-01-05', 'normal'),
(2, 2, '2025-02-10', '2025-02-15', 'critical'),
(3, 3, '2025-03-01', '2025-03-05', 'ongoing'),
(4, 4, '2025-03-10', '2025-03-12', 'normal');
