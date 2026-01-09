"""
Database initialization script for Quebec Medical Services Database.
Script d'initialisation de la base de données pour les services médicaux du Québec.

This script creates the database tables and can populate them with sample data.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, time, datetime
from models import (
    Base, Patient, MedicalProfessional, MedicalFacility, 
    FacilityStaff, Appointment, MedicalRecord, Prescription,
    PrescriptionFill, LabTest, MedicalHistory, 
    InsuranceInformation, Vaccination
)


def create_database(database_url: str):
    """
    Create all database tables.
    
    Args:
        database_url: Database connection string (e.g., 'postgresql://user:pass@localhost/dbname')
    """
    engine = create_engine(database_url, echo=True)
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")
    return engine


def populate_sample_data(session):
    """
    Populate the database with sample data for testing.
    """
    print("Populating sample data...")
    
    # Create sample patients
    patient1 = Patient(
        ramq_number='TREM80051501',
        first_name='Jean',
        last_name='Tremblay',
        date_of_birth=date(1980, 5, 15),
        gender='Male',
        address_street='123 Rue Principale',
        address_city='Montreal',
        address_province='Quebec',
        address_postal_code='H1A 1A1',
        phone_number='514-555-1234',
        email='jean.tremblay@example.com',
        blood_type='A+',
        allergies='Penicillin'
    )
    
    patient2 = Patient(
        ramq_number='LARO85102002',
        first_name='Marie',
        last_name='Larose',
        date_of_birth=date(1985, 10, 20),
        gender='Female',
        address_street='456 Avenue du Parc',
        address_city='Quebec City',
        address_province='Quebec',
        address_postal_code='G1R 2B5',
        phone_number='418-555-5678',
        email='marie.larose@example.com',
        blood_type='O-',
        allergies='None'
    )
    
    session.add_all([patient1, patient2])
    
    # Create sample medical professionals
    doctor1 = MedicalProfessional(
        license_number='MD123456',
        professional_type='doctor',
        specialty='Family Medicine',
        first_name='Dr. Robert',
        last_name='Gagnon',
        phone_number='514-555-9999',
        email='r.gagnon@hospital.qc.ca',
        is_active=True
    )
    
    nurse1 = MedicalProfessional(
        license_number='RN789012',
        professional_type='nurse',
        specialty='Emergency',
        first_name='Sophie',
        last_name='Bouchard',
        phone_number='514-555-8888',
        email='s.bouchard@hospital.qc.ca',
        is_active=True
    )
    
    pharmacist1 = MedicalProfessional(
        license_number='PH345678',
        professional_type='pharmacist',
        specialty=None,
        first_name='Marc',
        last_name='Fortin',
        phone_number='514-555-7777',
        email='m.fortin@pharmacy.qc.ca',
        is_active=True
    )
    
    session.add_all([doctor1, nurse1, pharmacist1])
    
    # Create sample medical facilities
    hospital1 = MedicalFacility(
        facility_name='Hôpital Général de Montreal',
        facility_type='hospital',
        address_street='1000 Rue de la Santé',
        address_city='Montreal',
        address_province='Quebec',
        address_postal_code='H2X 1K9',
        phone_number='514-555-0000',
        email='info@hgm.qc.ca',
        capacity=500,
        is_active=True
    )
    
    clinic1 = MedicalFacility(
        facility_name='Clinique Médicale du Plateau',
        facility_type='clinic',
        address_street='555 Avenue Mont-Royal',
        address_city='Montreal',
        address_province='Quebec',
        address_postal_code='H2J 1W5',
        phone_number='514-555-2222',
        email='info@clinique-plateau.qc.ca',
        capacity=20,
        is_active=True
    )
    
    pharmacy1 = MedicalFacility(
        facility_name='Pharmacie Jean Coutu',
        facility_type='pharmacy',
        address_street='789 Boulevard Saint-Laurent',
        address_city='Montreal',
        address_province='Quebec',
        address_postal_code='H2Z 1C4',
        phone_number='514-555-3333',
        email='info@jc-pharmacy.qc.ca',
        is_active=True
    )
    
    session.add_all([hospital1, clinic1, pharmacy1])
    session.commit()
    
    # Create facility-staff relationships
    assignment1 = FacilityStaff(
        facility_id=hospital1.facility_id,
        professional_id=doctor1.professional_id,
        start_date=date(2020, 1, 1),
        is_current=True
    )
    
    assignment2 = FacilityStaff(
        facility_id=clinic1.facility_id,
        professional_id=doctor1.professional_id,
        start_date=date(2022, 6, 1),
        is_current=True
    )
    
    assignment3 = FacilityStaff(
        facility_id=pharmacy1.facility_id,
        professional_id=pharmacist1.professional_id,
        start_date=date(2018, 3, 15),
        is_current=True
    )
    
    session.add_all([assignment1, assignment2, assignment3])
    
    # Create sample appointments
    appointment1 = Appointment(
        patient_id=patient1.patient_id,
        professional_id=doctor1.professional_id,
        facility_id=clinic1.facility_id,
        appointment_date=date(2024, 2, 15),
        appointment_time=time(10, 0),
        duration_minutes=30,
        status='completed',
        reason='Annual checkup'
    )
    
    appointment2 = Appointment(
        patient_id=patient2.patient_id,
        professional_id=doctor1.professional_id,
        facility_id=clinic1.facility_id,
        appointment_date=date(2024, 3, 20),
        appointment_time=time(14, 30),
        duration_minutes=45,
        status='scheduled',
        reason='Follow-up consultation'
    )
    
    session.add_all([appointment1, appointment2])
    session.commit()
    
    # Create medical records
    record1 = MedicalRecord(
        patient_id=patient1.patient_id,
        professional_id=doctor1.professional_id,
        facility_id=clinic1.facility_id,
        appointment_id=appointment1.appointment_id,
        visit_date=date(2024, 2, 15),
        visit_time=time(10, 0),
        chief_complaint='Annual physical examination',
        diagnosis='Patient is healthy overall. Mild hypertension noted.',
        treatment_plan='Monitor blood pressure. Lifestyle modifications recommended.',
        follow_up_required=True,
        follow_up_date=date(2024, 8, 15)
    )
    
    session.add(record1)
    session.commit()
    
    # Create prescription
    prescription1 = Prescription(
        patient_id=patient1.patient_id,
        professional_id=doctor1.professional_id,
        record_id=record1.record_id,
        medication_name='Lisinopril',
        medication_code='DIN02240524',
        dosage='10mg',
        frequency='Once daily',
        duration='90 days',
        quantity=90,
        refills_allowed=3,
        refills_remaining=3,
        instructions='Take in the morning with water',
        prescribed_date=date(2024, 2, 15),
        expiry_date=date(2025, 2, 15),
        is_active=True
    )
    
    session.add(prescription1)
    session.commit()
    
    # Create prescription fill
    fill1 = PrescriptionFill(
        prescription_id=prescription1.prescription_id,
        pharmacy_id=pharmacy1.facility_id,
        pharmacist_id=pharmacist1.professional_id,
        fill_date=date(2024, 2, 16),
        quantity_dispensed=90
    )
    
    session.add(fill1)
    
    # Create lab test
    lab_test1 = LabTest(
        patient_id=patient1.patient_id,
        ordering_professional_id=doctor1.professional_id,
        record_id=record1.record_id,
        test_name='Complete Blood Count',
        test_code='CBC',
        test_category='blood work',
        order_date=date(2024, 2, 15),
        collection_date=date(2024, 2, 16),
        result_date=date(2024, 2, 18),
        result_value='WBC: 7.5, RBC: 4.8, HGB: 14.5',
        result_status='completed',
        reference_range='WBC: 4.5-11.0, RBC: 4.5-5.9, HGB: 13.5-17.5',
        is_abnormal=False
    )
    
    session.add(lab_test1)
    
    # Create medical history
    history1 = MedicalHistory(
        patient_id=patient1.patient_id,
        professional_id=doctor1.professional_id,
        condition_type='condition',
        condition_name='Hypertension',
        diagnosis_date=date(2024, 2, 15),
        is_active=True,
        severity='mild'
    )
    
    session.add(history1)
    
    # Create insurance information
    insurance1 = InsuranceInformation(
        patient_id=patient1.patient_id,
        insurance_type='RAMQ',
        policy_number='TREM80051501',
        provider_name='RAMQ - Régie de l\'assurance maladie du Québec',
        coverage_start_date=date(1980, 5, 15),
        is_active=True
    )
    
    insurance2 = InsuranceInformation(
        patient_id=patient2.patient_id,
        insurance_type='RAMQ',
        policy_number='LARO85102002',
        provider_name='RAMQ - Régie de l\'assurance maladie du Québec',
        coverage_start_date=date(1985, 10, 20),
        is_active=True
    )
    
    session.add_all([insurance1, insurance2])
    
    # Create vaccination record
    vaccination1 = Vaccination(
        patient_id=patient1.patient_id,
        professional_id=nurse1.professional_id,
        facility_id=clinic1.facility_id,
        vaccine_name='Influenza Vaccine',
        vaccine_code='FLU2024',
        dose_number=1,
        administration_date=date(2023, 11, 1),
        lot_number='FLU20231001',
        site='Left deltoid'
    )
    
    session.add(vaccination1)
    
    session.commit()
    print("Sample data populated successfully!")


def main():
    """
    Main function to initialize the database.
    """
    import os
    
    # Database connection string from environment variable or use SQLite for testing
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        'sqlite:///quebec_medical.db'  # Default to SQLite for testing
    )
    
    # Example for PostgreSQL: Set DATABASE_URL environment variable to:
    # "postgresql://username:password@localhost:5432/quebec_medical_db"
    
    print("Quebec Medical Services Database Initialization")
    print("=" * 50)
    
    try:
        # Create database tables
        engine = create_database(DATABASE_URL)
        
        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Ask if user wants to populate sample data
        response = input("\nDo you want to populate the database with sample data? (yes/no): ")
        if response.lower() in ['yes', 'y']:
            populate_sample_data(session)
        
        session.close()
        print("\nDatabase initialization completed successfully!")
        
    except Exception as e:
        print(f"\nError during database initialization: {e}")
        raise


if __name__ == "__main__":
    main()
