-- database.sql - Schema configuration for Smart Healthcare Management System (SHMS)

CREATE DATABASE IF NOT EXISTS HealthcareDB;
USE HealthcareDB;

-- Drop tables in reverse order of dependencies to avoid FK violation errors
DROP TABLE IF EXISTS settings;
DROP TABLE IF EXISTS login_history;
DROP TABLE IF EXISTS audit_logs;
DROP TABLE IF EXISTS activity_logs;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS insurance;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS bills;
DROP TABLE IF EXISTS beds;
DROP TABLE IF EXISTS wards;
DROP TABLE IF EXISTS admissions;
DROP TABLE IF EXISTS laboratory_results;
DROP TABLE IF EXISTS laboratory_tests;
DROP TABLE IF EXISTS pharmacy_inventory;
DROP TABLE IF EXISTS medicines;
DROP TABLE IF EXISTS prescriptions;
DROP TABLE IF EXISTS vitals;
DROP TABLE IF EXISTS ehr_records;
DROP TABLE IF EXISTS clinical_pathways;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS nurses;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS user_roles;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS permissions;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS departments;

-- 1. DEPARTMENTS
CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

-- 2. ROLES
CREATE TABLE roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- 3. PERMISSIONS
CREATE TABLE permissions (
    permission_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

-- 4. USERS
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT,
    status VARCHAR(20) DEFAULT 'Active' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE SET NULL
);

-- 5. USER ROLES (Join Table for Many-to-Many support)
CREATE TABLE user_roles (
    user_id INT,
    role_id INT,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE
);

-- 6. PATIENTS
CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    gender VARCHAR(10),
    dob DATE,
    blood_group VARCHAR(10),
    emergency_contact VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- 7. DOCTORS
CREATE TABLE doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    department_id INT,
    specialization VARCHAR(100),
    license_number VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE SET NULL
);

-- 8. NURSES
CREATE TABLE nurses (
    nurse_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    department_id INT,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE SET NULL
);

-- 9. APPOINTMENTS
CREATE TABLE appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATETIME NOT NULL,
    status VARCHAR(20) DEFAULT 'Scheduled' NOT NULL,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
);

-- 10. CLINICAL PATHWAYS
CREATE TABLE clinical_pathways (
    pathway_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    assigned_doctor_id INT,
    current_stage VARCHAR(50) DEFAULT 'Registration' NOT NULL, -- Registration, Triage, Diagnosis, Lab, Treatment, Pharmacy, Billing, Discharge
    symptoms TEXT,
    diagnosis TEXT,
    treatment_plan TEXT,
    status VARCHAR(20) DEFAULT 'Active' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_doctor_id) REFERENCES doctors(doctor_id) ON DELETE SET NULL
);

-- 11. EHR RECORDS
CREATE TABLE ehr_records (
    ehr_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    recorded_by_user_id INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (recorded_by_user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- 12. VITALS
CREATE TABLE vitals (
    vital_id INT AUTO_INCREMENT PRIMARY KEY,
    ehr_id INT,
    patient_id INT,
    blood_pressure VARCHAR(20),
    pulse_rate INT,
    temperature DECIMAL(4,1),
    weight_kg DECIMAL(5,2),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ehr_id) REFERENCES ehr_records(ehr_id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

-- 13. PRESCRIPTIONS
CREATE TABLE prescriptions (
    prescription_id INT AUTO_INCREMENT PRIMARY KEY,
    pathway_id INT,
    doctor_id INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pathway_id) REFERENCES clinical_pathways(pathway_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE SET NULL
);

-- 14. MEDICINES
CREATE TABLE medicines (
    medicine_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- 15. PHARMACY INVENTORY
CREATE TABLE pharmacy_inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    medicine_id INT,
    quantity INT DEFAULT 0 NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    expiry_date DATE,
    FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id) ON DELETE CASCADE
);

-- 16. LABORATORY TESTS
CREATE TABLE laboratory_tests (
    test_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    cost DECIMAL(10,2) NOT NULL
);

-- 17. LABORATORY RESULTS
CREATE TABLE laboratory_results (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    pathway_id INT,
    test_id INT,
    technician_id INT,
    result_value TEXT,
    status VARCHAR(20) DEFAULT 'Pending' NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pathway_id) REFERENCES clinical_pathways(pathway_id) ON DELETE CASCADE,
    FOREIGN KEY (test_id) REFERENCES laboratory_tests(test_id) ON DELETE CASCADE,
    FOREIGN KEY (technician_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- 18. ADMISSIONS
CREATE TABLE admissions (
    admission_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    admitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    discharged_at TIMESTAMP NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

-- 19. WARDS
CREATE TABLE wards (
    ward_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL,
    capacity INT NOT NULL
);

-- 20. BEDS
CREATE TABLE beds (
    bed_id INT AUTO_INCREMENT PRIMARY KEY,
    ward_id INT,
    bed_number VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'Available' NOT NULL,
    FOREIGN KEY (ward_id) REFERENCES wards(ward_id) ON DELETE CASCADE
);

-- 21. BILLS
CREATE TABLE bills (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    pathway_id INT,
    total_amount DECIMAL(10,2) DEFAULT 0.00 NOT NULL,
    discount DECIMAL(10,2) DEFAULT 0.00 NOT NULL,
    insurance_claimed DECIMAL(10,2) DEFAULT 0.00 NOT NULL,
    status VARCHAR(20) DEFAULT 'Unpaid' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pathway_id) REFERENCES clinical_pathways(pathway_id) ON DELETE CASCADE
);

-- 22. PAYMENTS
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    bill_id INT,
    amount DECIMAL(10,2) NOT NULL,
    method VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'Success' NOT NULL,
    paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bill_id) REFERENCES bills(bill_id) ON DELETE CASCADE
);

-- 23. INSURANCE
CREATE TABLE insurance (
    insurance_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    provider VARCHAR(100) NOT NULL,
    policy_number VARCHAR(100) NOT NULL,
    coverage_details TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

-- 24. NOTIFICATIONS
CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    message TEXT NOT NULL,
    type VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'Unread' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 25. ACTIVITY LOGS
CREATE TABLE activity_logs (
    activity_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- 26. AUDIT LOGS
CREATE TABLE audit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    module VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- 27. LOGIN HISTORY
CREATE TABLE login_history (
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logout_time TIMESTAMP NULL,
    login_status VARCHAR(20) NOT NULL,
    ip_address VARCHAR(45),
    device_name VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- 28. SETTINGS
CREATE TABLE settings (
    setting_id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(50) UNIQUE NOT NULL,
    setting_value VARCHAR(255) NOT NULL
);

-- Seed Initial App Settings
INSERT INTO settings (setting_key, setting_value) VALUES
('theme', 'light'),
('max_login_attempts', '5'),
('session_timeout_minutes', '30');

-- Seed Departments
INSERT INTO departments (name, description) VALUES
('Emergency', 'Immediate treatment of acute illness and trauma'),
('Cardiology', 'Heart and blood vessel treatments'),
('Pediatrics', 'Medical care for children and infants'),
('General Medicine', 'Primary care and internal medicine');

-- Seed Roles
INSERT INTO roles (name, description) VALUES
('Admin', 'System and Hospital Administrator'),
('Doctor', 'Medical Practitioner'),
('Nurse', 'Clinical Nursing Staff'),
('Receptionist', 'Front Desk Registration Officer'),
('Pharmacist', 'Pharmacy Inventory & Dispensing Agent'),
('Patient', 'Healthcare Consumer / Client');
