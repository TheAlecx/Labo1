-- =====================================================
-- Quebec Medical Services Database Schema
-- Base de données générale pour tous les services médicaux du Québec
-- =====================================================

-- =====================================================
-- Table: patients
-- Description: Stores patient information with Quebec health card (RAMQ)
-- =====================================================
CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    ramq_number VARCHAR(12) UNIQUE NOT NULL, -- Quebec health card number (RAMQ)
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(20),
    address_street VARCHAR(200),
    address_city VARCHAR(100),
    address_province VARCHAR(50) DEFAULT 'Quebec',
    address_postal_code VARCHAR(7),
    phone_number VARCHAR(15),
    email VARCHAR(100),
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(15),
    blood_type VARCHAR(5),
    allergies TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Table: medical_professionals
-- Description: Doctors, nurses, specialists, and other medical staff
-- =====================================================
CREATE TABLE medical_professionals (
    professional_id SERIAL PRIMARY KEY,
    license_number VARCHAR(50) UNIQUE NOT NULL, -- Professional license number
    professional_type VARCHAR(50) NOT NULL, -- doctor, nurse, specialist, pharmacist, etc.
    specialty VARCHAR(100), -- For specialists
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15),
    email VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Table: medical_facilities
-- Description: Hospitals, clinics, pharmacies, and other medical facilities
-- =====================================================
CREATE TABLE medical_facilities (
    facility_id SERIAL PRIMARY KEY,
    facility_name VARCHAR(200) NOT NULL,
    facility_type VARCHAR(50) NOT NULL, -- hospital, clinic, pharmacy, lab, etc.
    address_street VARCHAR(200),
    address_city VARCHAR(100),
    address_province VARCHAR(50) DEFAULT 'Quebec',
    address_postal_code VARCHAR(7),
    phone_number VARCHAR(15),
    email VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    capacity INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Table: facility_staff
-- Description: Junction table linking professionals to facilities
-- =====================================================
CREATE TABLE facility_staff (
    facility_staff_id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL REFERENCES medical_facilities(facility_id) ON DELETE CASCADE,
    professional_id INTEGER NOT NULL REFERENCES medical_professionals(professional_id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE,
    is_current BOOLEAN DEFAULT TRUE,
    UNIQUE(facility_id, professional_id, start_date)
);

-- =====================================================
-- Table: appointments
-- Description: Medical appointments between patients and professionals
-- =====================================================
CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    professional_id INTEGER NOT NULL REFERENCES medical_professionals(professional_id) ON DELETE CASCADE,
    facility_id INTEGER NOT NULL REFERENCES medical_facilities(facility_id) ON DELETE CASCADE,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    duration_minutes INTEGER DEFAULT 30,
    status VARCHAR(20) DEFAULT 'scheduled', -- scheduled, completed, cancelled, no-show
    reason TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Table: medical_records
-- Description: Medical consultations and examination records
-- =====================================================
CREATE TABLE medical_records (
    record_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    professional_id INTEGER NOT NULL REFERENCES medical_professionals(professional_id) ON DELETE CASCADE,
    facility_id INTEGER NOT NULL REFERENCES medical_facilities(facility_id) ON DELETE CASCADE,
    appointment_id INTEGER REFERENCES appointments(appointment_id) ON DELETE SET NULL,
    visit_date DATE NOT NULL,
    visit_time TIME NOT NULL,
    chief_complaint TEXT,
    diagnosis TEXT,
    treatment_plan TEXT,
    notes TEXT,
    follow_up_required BOOLEAN DEFAULT FALSE,
    follow_up_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Table: prescriptions
-- Description: Medical prescriptions issued by professionals
-- =====================================================
CREATE TABLE prescriptions (
    prescription_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    professional_id INTEGER NOT NULL REFERENCES medical_professionals(professional_id) ON DELETE CASCADE,
    record_id INTEGER REFERENCES medical_records(record_id) ON DELETE SET NULL,
    medication_name VARCHAR(200) NOT NULL,
    medication_code VARCHAR(50), -- DIN (Drug Identification Number)
    dosage VARCHAR(100) NOT NULL,
    frequency VARCHAR(100) NOT NULL,
    duration VARCHAR(100),
    quantity INTEGER,
    refills_allowed INTEGER DEFAULT 0,
    refills_remaining INTEGER DEFAULT 0,
    instructions TEXT,
    prescribed_date DATE NOT NULL,
    expiry_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Table: prescription_fills
-- Description: Tracks when prescriptions are filled at pharmacies
-- =====================================================
CREATE TABLE prescription_fills (
    fill_id SERIAL PRIMARY KEY,
    prescription_id INTEGER NOT NULL REFERENCES prescriptions(prescription_id) ON DELETE CASCADE,
    pharmacy_id INTEGER NOT NULL REFERENCES medical_facilities(facility_id) ON DELETE CASCADE,
    pharmacist_id INTEGER REFERENCES medical_professionals(professional_id) ON DELETE SET NULL,
    fill_date DATE NOT NULL,
    quantity_dispensed INTEGER NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Table: lab_tests
-- Description: Laboratory tests and results
-- =====================================================
CREATE TABLE lab_tests (
    test_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    ordering_professional_id INTEGER NOT NULL REFERENCES medical_professionals(professional_id) ON DELETE CASCADE,
    record_id INTEGER REFERENCES medical_records(record_id) ON DELETE SET NULL,
    test_name VARCHAR(200) NOT NULL,
    test_code VARCHAR(50),
    test_category VARCHAR(100), -- blood work, imaging, etc.
    order_date DATE NOT NULL,
    collection_date DATE,
    result_date DATE,
    result_value TEXT,
    result_status VARCHAR(50) DEFAULT 'pending', -- pending, completed, cancelled
    reference_range VARCHAR(100),
    is_abnormal BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Table: medical_history
-- Description: Patient medical history including conditions and surgeries
-- =====================================================
CREATE TABLE medical_history (
    history_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    professional_id INTEGER REFERENCES medical_professionals(professional_id) ON DELETE SET NULL,
    condition_type VARCHAR(50) NOT NULL, -- condition, surgery, family_history, etc.
    condition_name VARCHAR(200) NOT NULL,
    diagnosis_date DATE,
    resolution_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    severity VARCHAR(20), -- mild, moderate, severe
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Table: insurance_information
-- Description: Insurance and RAMQ coverage information
-- =====================================================
CREATE TABLE insurance_information (
    insurance_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    insurance_type VARCHAR(50) NOT NULL, -- RAMQ, private, supplemental
    policy_number VARCHAR(100),
    provider_name VARCHAR(200),
    coverage_start_date DATE NOT NULL,
    coverage_end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Table: vaccinations
-- Description: Patient vaccination records
-- =====================================================
CREATE TABLE vaccinations (
    vaccination_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    professional_id INTEGER REFERENCES medical_professionals(professional_id) ON DELETE SET NULL,
    facility_id INTEGER REFERENCES medical_facilities(facility_id) ON DELETE SET NULL,
    vaccine_name VARCHAR(200) NOT NULL,
    vaccine_code VARCHAR(50),
    dose_number INTEGER,
    administration_date DATE NOT NULL,
    expiry_date DATE,
    lot_number VARCHAR(100),
    site VARCHAR(100), -- injection site
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Indexes for better query performance
-- =====================================================

-- Patients
CREATE INDEX idx_patients_ramq ON patients(ramq_number);
CREATE INDEX idx_patients_name ON patients(last_name, first_name);
CREATE INDEX idx_patients_dob ON patients(date_of_birth);

-- Medical Professionals
CREATE INDEX idx_professionals_license ON medical_professionals(license_number);
CREATE INDEX idx_professionals_type ON medical_professionals(professional_type);
CREATE INDEX idx_professionals_name ON medical_professionals(last_name, first_name);

-- Medical Facilities
CREATE INDEX idx_facilities_type ON medical_facilities(facility_type);
CREATE INDEX idx_facilities_city ON medical_facilities(address_city);

-- Appointments
CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_appointments_professional ON appointments(professional_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_appointments_status ON appointments(status);

-- Medical Records
CREATE INDEX idx_records_patient ON medical_records(patient_id);
CREATE INDEX idx_records_professional ON medical_records(professional_id);
CREATE INDEX idx_records_visit_date ON medical_records(visit_date);

-- Prescriptions
CREATE INDEX idx_prescriptions_patient ON prescriptions(patient_id);
CREATE INDEX idx_prescriptions_professional ON prescriptions(professional_id);
CREATE INDEX idx_prescriptions_active ON prescriptions(is_active);

-- Lab Tests
CREATE INDEX idx_lab_tests_patient ON lab_tests(patient_id);
CREATE INDEX idx_lab_tests_status ON lab_tests(result_status);

-- Medical History
CREATE INDEX idx_medical_history_patient ON medical_history(patient_id);
CREATE INDEX idx_medical_history_active ON medical_history(is_active);

-- Insurance
CREATE INDEX idx_insurance_patient ON insurance_information(patient_id);
CREATE INDEX idx_insurance_active ON insurance_information(is_active);

-- Vaccinations
CREATE INDEX idx_vaccinations_patient ON vaccinations(patient_id);
CREATE INDEX idx_vaccinations_date ON vaccinations(administration_date);
