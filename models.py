"""
Quebec Medical Services Database Models
Base de données générale pour tous les services médicaux du Québec

This module defines the ORM models for the Quebec medical services database
using SQLAlchemy.
"""

from datetime import datetime, date, time
from typing import List, Optional
from sqlalchemy import (
    Boolean, Column, Date, DateTime, ForeignKey, Integer, 
    String, Text, Time, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Patient(Base):
    """
    Patient information with Quebec health card (RAMQ).
    """
    __tablename__ = 'patients'
    
    patient_id = Column(Integer, primary_key=True, autoincrement=True)
    ramq_number = Column(String(12), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(20))
    address_street = Column(String(200))
    address_city = Column(String(100))
    address_province = Column(String(50), default='Quebec')
    address_postal_code = Column(String(7))
    phone_number = Column(String(15))
    email = Column(String(100))
    emergency_contact_name = Column(String(100))
    emergency_contact_phone = Column(String(15))
    blood_type = Column(String(5))
    allergies = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointments = relationship('Appointment', back_populates='patient', cascade='all, delete-orphan')
    medical_records = relationship('MedicalRecord', back_populates='patient', cascade='all, delete-orphan')
    prescriptions = relationship('Prescription', back_populates='patient', cascade='all, delete-orphan')
    lab_tests = relationship('LabTest', back_populates='patient', cascade='all, delete-orphan')
    medical_history = relationship('MedicalHistory', back_populates='patient', cascade='all, delete-orphan')
    insurance_info = relationship('InsuranceInformation', back_populates='patient', cascade='all, delete-orphan')
    vaccinations = relationship('Vaccination', back_populates='patient', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Patient(id={self.patient_id}, name={self.first_name} {self.last_name}, ramq={self.ramq_number})>"


class MedicalProfessional(Base):
    """
    Medical professionals including doctors, nurses, specialists, and pharmacists.
    """
    __tablename__ = 'medical_professionals'
    
    professional_id = Column(Integer, primary_key=True, autoincrement=True)
    license_number = Column(String(50), unique=True, nullable=False)
    professional_type = Column(String(50), nullable=False)
    specialty = Column(String(100))
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(15))
    email = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    facility_assignments = relationship('FacilityStaff', back_populates='professional', cascade='all, delete-orphan')
    appointments = relationship('Appointment', back_populates='professional', cascade='all, delete-orphan')
    medical_records = relationship('MedicalRecord', back_populates='professional', cascade='all, delete-orphan')
    prescriptions = relationship('Prescription', back_populates='professional', cascade='all, delete-orphan')
    lab_tests_ordered = relationship('LabTest', back_populates='ordering_professional', cascade='all, delete-orphan')
    medical_history_entries = relationship('MedicalHistory', back_populates='professional', cascade='all, delete-orphan')
    prescription_fills = relationship('PrescriptionFill', back_populates='pharmacist', cascade='all, delete-orphan')
    vaccinations = relationship('Vaccination', back_populates='professional', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<MedicalProfessional(id={self.professional_id}, name={self.first_name} {self.last_name}, type={self.professional_type})>"


class MedicalFacility(Base):
    """
    Medical facilities including hospitals, clinics, pharmacies, and labs.
    """
    __tablename__ = 'medical_facilities'
    
    facility_id = Column(Integer, primary_key=True, autoincrement=True)
    facility_name = Column(String(200), nullable=False)
    facility_type = Column(String(50), nullable=False)
    address_street = Column(String(200))
    address_city = Column(String(100))
    address_province = Column(String(50), default='Quebec')
    address_postal_code = Column(String(7))
    phone_number = Column(String(15))
    email = Column(String(100))
    is_active = Column(Boolean, default=True)
    capacity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    staff_assignments = relationship('FacilityStaff', back_populates='facility', cascade='all, delete-orphan')
    appointments = relationship('Appointment', back_populates='facility', cascade='all, delete-orphan')
    medical_records = relationship('MedicalRecord', back_populates='facility', cascade='all, delete-orphan')
    prescription_fills = relationship('PrescriptionFill', back_populates='pharmacy', cascade='all, delete-orphan')
    vaccinations = relationship('Vaccination', back_populates='facility')
    
    def __repr__(self):
        return f"<MedicalFacility(id={self.facility_id}, name={self.facility_name}, type={self.facility_type})>"


class FacilityStaff(Base):
    """
    Junction table linking medical professionals to facilities.
    """
    __tablename__ = 'facility_staff'
    
    facility_staff_id = Column(Integer, primary_key=True, autoincrement=True)
    facility_id = Column(Integer, ForeignKey('medical_facilities.facility_id', ondelete='CASCADE'), nullable=False)
    professional_id = Column(Integer, ForeignKey('medical_professionals.professional_id', ondelete='CASCADE'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    is_current = Column(Boolean, default=True)
    
    __table_args__ = (
        UniqueConstraint('facility_id', 'professional_id', 'start_date', name='uq_facility_professional_start'),
    )
    
    # Relationships
    facility = relationship('MedicalFacility', back_populates='staff_assignments')
    professional = relationship('MedicalProfessional', back_populates='facility_assignments')
    
    def __repr__(self):
        return f"<FacilityStaff(facility_id={self.facility_id}, professional_id={self.professional_id})>"


class Appointment(Base):
    """
    Medical appointments between patients and professionals.
    """
    __tablename__ = 'appointments'
    
    appointment_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id', ondelete='CASCADE'), nullable=False)
    professional_id = Column(Integer, ForeignKey('medical_professionals.professional_id', ondelete='CASCADE'), nullable=False)
    facility_id = Column(Integer, ForeignKey('medical_facilities.facility_id', ondelete='CASCADE'), nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    duration_minutes = Column(Integer, default=30)
    status = Column(String(20), default='scheduled')
    reason = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship('Patient', back_populates='appointments')
    professional = relationship('MedicalProfessional', back_populates='appointments')
    facility = relationship('MedicalFacility', back_populates='appointments')
    medical_record = relationship('MedicalRecord', back_populates='appointment', uselist=False)
    
    def __repr__(self):
        return f"<Appointment(id={self.appointment_id}, date={self.appointment_date}, status={self.status})>"


class MedicalRecord(Base):
    """
    Medical consultation and examination records.
    """
    __tablename__ = 'medical_records'
    
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id', ondelete='CASCADE'), nullable=False)
    professional_id = Column(Integer, ForeignKey('medical_professionals.professional_id', ondelete='CASCADE'), nullable=False)
    facility_id = Column(Integer, ForeignKey('medical_facilities.facility_id', ondelete='CASCADE'), nullable=False)
    appointment_id = Column(Integer, ForeignKey('appointments.appointment_id', ondelete='SET NULL'))
    visit_date = Column(Date, nullable=False)
    visit_time = Column(Time, nullable=False)
    chief_complaint = Column(Text)
    diagnosis = Column(Text)
    treatment_plan = Column(Text)
    notes = Column(Text)
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship('Patient', back_populates='medical_records')
    professional = relationship('MedicalProfessional', back_populates='medical_records')
    facility = relationship('MedicalFacility', back_populates='medical_records')
    appointment = relationship('Appointment', back_populates='medical_record')
    prescriptions = relationship('Prescription', back_populates='medical_record')
    lab_tests = relationship('LabTest', back_populates='medical_record')
    
    def __repr__(self):
        return f"<MedicalRecord(id={self.record_id}, patient_id={self.patient_id}, date={self.visit_date})>"


class Prescription(Base):
    """
    Medical prescriptions issued by professionals.
    """
    __tablename__ = 'prescriptions'
    
    prescription_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id', ondelete='CASCADE'), nullable=False)
    professional_id = Column(Integer, ForeignKey('medical_professionals.professional_id', ondelete='CASCADE'), nullable=False)
    record_id = Column(Integer, ForeignKey('medical_records.record_id', ondelete='SET NULL'))
    medication_name = Column(String(200), nullable=False)
    medication_code = Column(String(50))
    dosage = Column(String(100), nullable=False)
    frequency = Column(String(100), nullable=False)
    duration = Column(String(100))
    quantity = Column(Integer)
    refills_allowed = Column(Integer, default=0)
    refills_remaining = Column(Integer, default=0)
    instructions = Column(Text)
    prescribed_date = Column(Date, nullable=False)
    expiry_date = Column(Date)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship('Patient', back_populates='prescriptions')
    professional = relationship('MedicalProfessional', back_populates='prescriptions')
    medical_record = relationship('MedicalRecord', back_populates='prescriptions')
    fills = relationship('PrescriptionFill', back_populates='prescription', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Prescription(id={self.prescription_id}, medication={self.medication_name}, patient_id={self.patient_id})>"


class PrescriptionFill(Base):
    """
    Tracks when prescriptions are filled at pharmacies.
    """
    __tablename__ = 'prescription_fills'
    
    fill_id = Column(Integer, primary_key=True, autoincrement=True)
    prescription_id = Column(Integer, ForeignKey('prescriptions.prescription_id', ondelete='CASCADE'), nullable=False)
    pharmacy_id = Column(Integer, ForeignKey('medical_facilities.facility_id', ondelete='CASCADE'), nullable=False)
    pharmacist_id = Column(Integer, ForeignKey('medical_professionals.professional_id', ondelete='SET NULL'))
    fill_date = Column(Date, nullable=False)
    quantity_dispensed = Column(Integer, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    prescription = relationship('Prescription', back_populates='fills')
    pharmacy = relationship('MedicalFacility', back_populates='prescription_fills')
    pharmacist = relationship('MedicalProfessional', back_populates='prescription_fills')
    
    def __repr__(self):
        return f"<PrescriptionFill(id={self.fill_id}, prescription_id={self.prescription_id}, date={self.fill_date})>"


class LabTest(Base):
    """
    Laboratory tests and results.
    """
    __tablename__ = 'lab_tests'
    
    test_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id', ondelete='CASCADE'), nullable=False)
    ordering_professional_id = Column(Integer, ForeignKey('medical_professionals.professional_id', ondelete='CASCADE'), nullable=False)
    record_id = Column(Integer, ForeignKey('medical_records.record_id', ondelete='SET NULL'))
    test_name = Column(String(200), nullable=False)
    test_code = Column(String(50))
    test_category = Column(String(100))
    order_date = Column(Date, nullable=False)
    collection_date = Column(Date)
    result_date = Column(Date)
    result_value = Column(Text)
    result_status = Column(String(50), default='pending')
    reference_range = Column(String(100))
    is_abnormal = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship('Patient', back_populates='lab_tests')
    ordering_professional = relationship('MedicalProfessional', back_populates='lab_tests_ordered')
    medical_record = relationship('MedicalRecord', back_populates='lab_tests')
    
    def __repr__(self):
        return f"<LabTest(id={self.test_id}, name={self.test_name}, patient_id={self.patient_id}, status={self.result_status})>"


class MedicalHistory(Base):
    """
    Patient medical history including conditions, surgeries, and family history.
    """
    __tablename__ = 'medical_history'
    
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id', ondelete='CASCADE'), nullable=False)
    professional_id = Column(Integer, ForeignKey('medical_professionals.professional_id', ondelete='SET NULL'))
    condition_type = Column(String(50), nullable=False)
    condition_name = Column(String(200), nullable=False)
    diagnosis_date = Column(Date)
    resolution_date = Column(Date)
    is_active = Column(Boolean, default=True)
    severity = Column(String(20))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship('Patient', back_populates='medical_history')
    professional = relationship('MedicalProfessional', back_populates='medical_history_entries')
    
    def __repr__(self):
        return f"<MedicalHistory(id={self.history_id}, patient_id={self.patient_id}, condition={self.condition_name})>"


class InsuranceInformation(Base):
    """
    Insurance and RAMQ coverage information.
    """
    __tablename__ = 'insurance_information'
    
    insurance_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id', ondelete='CASCADE'), nullable=False)
    insurance_type = Column(String(50), nullable=False)
    policy_number = Column(String(100))
    provider_name = Column(String(200))
    coverage_start_date = Column(Date, nullable=False)
    coverage_end_date = Column(Date)
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship('Patient', back_populates='insurance_info')
    
    def __repr__(self):
        return f"<InsuranceInformation(id={self.insurance_id}, patient_id={self.patient_id}, type={self.insurance_type})>"


class Vaccination(Base):
    """
    Patient vaccination records.
    """
    __tablename__ = 'vaccinations'
    
    vaccination_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id', ondelete='CASCADE'), nullable=False)
    professional_id = Column(Integer, ForeignKey('medical_professionals.professional_id', ondelete='SET NULL'))
    facility_id = Column(Integer, ForeignKey('medical_facilities.facility_id', ondelete='SET NULL'))
    vaccine_name = Column(String(200), nullable=False)
    vaccine_code = Column(String(50))
    dose_number = Column(Integer)
    administration_date = Column(Date, nullable=False)
    expiry_date = Column(Date)
    lot_number = Column(String(100))
    site = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship('Patient', back_populates='vaccinations')
    professional = relationship('MedicalProfessional', back_populates='vaccinations')
    facility = relationship('MedicalFacility', back_populates='vaccinations')
    
    def __repr__(self):
        return f"<Vaccination(id={self.vaccination_id}, vaccine={self.vaccine_name}, patient_id={self.patient_id})>"
