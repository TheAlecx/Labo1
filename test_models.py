"""
Test script to validate the database models.
Script de test pour valider les modèles de base de données.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, time
import sys

# Import models
from models import (
    Base, Patient, MedicalProfessional, MedicalFacility,
    FacilityStaff, Appointment, MedicalRecord, Prescription,
    PrescriptionFill, LabTest, MedicalHistory,
    InsuranceInformation, Vaccination
)


def test_models():
    """Test that all models can be instantiated and have proper relationships."""
    
    print("Testing Quebec Medical Services Database Models...")
    print("=" * 70)
    
    # Create SQLite in-memory database for testing
    engine = create_engine('sqlite:///:memory:', echo=False)
    
    # Create all tables
    print("\n1. Creating database tables...")
    try:
        Base.metadata.create_all(engine)
        print("   ✓ All tables created successfully")
    except Exception as e:
        print(f"   ✗ Error creating tables: {e}")
        return False
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Test creating a patient
    print("\n2. Testing Patient model...")
    try:
        patient = Patient(
            ramq_number='TEST12345678',
            first_name='Test',
            last_name='Patient',
            date_of_birth=date(1990, 1, 1),
            gender='Other',
            phone_number='555-0000',
            email='test@example.com',
            blood_type='AB+',
            allergies='None'
        )
        session.add(patient)
        session.commit()
        print(f"   ✓ Patient created: {patient}")
    except Exception as e:
        print(f"   ✗ Error creating patient: {e}")
        return False
    
    # Test creating a medical professional
    print("\n3. Testing MedicalProfessional model...")
    try:
        doctor = MedicalProfessional(
            license_number='TEST123',
            professional_type='doctor',
            specialty='Test Medicine',
            first_name='Test',
            last_name='Doctor',
            phone_number='555-1111',
            email='doctor@test.com',
            is_active=True
        )
        session.add(doctor)
        session.commit()
        print(f"   ✓ Medical professional created: {doctor}")
    except Exception as e:
        print(f"   ✗ Error creating medical professional: {e}")
        return False
    
    # Test creating a medical facility
    print("\n4. Testing MedicalFacility model...")
    try:
        facility = MedicalFacility(
            facility_name='Test Hospital',
            facility_type='hospital',
            address_city='Montreal',
            phone_number='555-2222',
            email='info@test.com',
            capacity=100,
            is_active=True
        )
        session.add(facility)
        session.commit()
        print(f"   ✓ Medical facility created: {facility}")
    except Exception as e:
        print(f"   ✗ Error creating medical facility: {e}")
        return False
    
    # Test creating facility staff assignment
    print("\n5. Testing FacilityStaff relationship...")
    try:
        assignment = FacilityStaff(
            facility_id=facility.facility_id,
            professional_id=doctor.professional_id,
            start_date=date(2024, 1, 1),
            is_current=True
        )
        session.add(assignment)
        session.commit()
        print(f"   ✓ Facility staff assignment created: {assignment}")
    except Exception as e:
        print(f"   ✗ Error creating facility staff assignment: {e}")
        return False
    
    # Test creating an appointment
    print("\n6. Testing Appointment model...")
    try:
        appointment = Appointment(
            patient_id=patient.patient_id,
            professional_id=doctor.professional_id,
            facility_id=facility.facility_id,
            appointment_date=date(2024, 3, 15),
            appointment_time=time(10, 0),
            duration_minutes=30,
            status='scheduled',
            reason='Test visit'
        )
        session.add(appointment)
        session.commit()
        print(f"   ✓ Appointment created: {appointment}")
    except Exception as e:
        print(f"   ✗ Error creating appointment: {e}")
        return False
    
    # Test creating a medical record
    print("\n7. Testing MedicalRecord model...")
    try:
        record = MedicalRecord(
            patient_id=patient.patient_id,
            professional_id=doctor.professional_id,
            facility_id=facility.facility_id,
            appointment_id=appointment.appointment_id,
            visit_date=date(2024, 3, 15),
            visit_time=time(10, 0),
            chief_complaint='Test complaint',
            diagnosis='Test diagnosis',
            treatment_plan='Test treatment',
            follow_up_required=False
        )
        session.add(record)
        session.commit()
        print(f"   ✓ Medical record created: {record}")
    except Exception as e:
        print(f"   ✗ Error creating medical record: {e}")
        return False
    
    # Test creating a prescription
    print("\n8. Testing Prescription model...")
    try:
        prescription = Prescription(
            patient_id=patient.patient_id,
            professional_id=doctor.professional_id,
            record_id=record.record_id,
            medication_name='Test Medication',
            medication_code='TEST001',
            dosage='10mg',
            frequency='Once daily',
            quantity=30,
            refills_allowed=2,
            refills_remaining=2,
            prescribed_date=date(2024, 3, 15),
            is_active=True
        )
        session.add(prescription)
        session.commit()
        print(f"   ✓ Prescription created: {prescription}")
    except Exception as e:
        print(f"   ✗ Error creating prescription: {e}")
        return False
    
    # Test creating other models
    print("\n9. Testing additional models...")
    
    # Lab test
    try:
        lab_test = LabTest(
            patient_id=patient.patient_id,
            ordering_professional_id=doctor.professional_id,
            record_id=record.record_id,
            test_name='Test CBC',
            test_code='CBC',
            test_category='blood work',
            order_date=date(2024, 3, 15),
            result_status='pending'
        )
        session.add(lab_test)
        print("   ✓ Lab test created")
    except Exception as e:
        print(f"   ✗ Error creating lab test: {e}")
        return False
    
    # Medical history
    try:
        history = MedicalHistory(
            patient_id=patient.patient_id,
            professional_id=doctor.professional_id,
            condition_type='condition',
            condition_name='Test condition',
            diagnosis_date=date(2024, 1, 1),
            is_active=True,
            severity='mild'
        )
        session.add(history)
        print("   ✓ Medical history entry created")
    except Exception as e:
        print(f"   ✗ Error creating medical history: {e}")
        return False
    
    # Insurance information
    try:
        insurance = InsuranceInformation(
            patient_id=patient.patient_id,
            insurance_type='RAMQ',
            policy_number='TEST12345678',
            provider_name='RAMQ',
            coverage_start_date=date(2024, 1, 1),
            is_active=True
        )
        session.add(insurance)
        print("   ✓ Insurance information created")
    except Exception as e:
        print(f"   ✗ Error creating insurance information: {e}")
        return False
    
    # Vaccination
    try:
        vaccination = Vaccination(
            patient_id=patient.patient_id,
            professional_id=doctor.professional_id,
            facility_id=facility.facility_id,
            vaccine_name='Test Vaccine',
            vaccine_code='TEST-VAX',
            dose_number=1,
            administration_date=date(2024, 1, 1)
        )
        session.add(vaccination)
        print("   ✓ Vaccination record created")
    except Exception as e:
        print(f"   ✗ Error creating vaccination: {e}")
        return False
    
    session.commit()
    
    # Test relationships
    print("\n10. Testing model relationships...")
    try:
        # Refresh patient to load relationships
        session.refresh(patient)
        
        assert len(patient.appointments) > 0, "Patient should have appointments"
        print(f"   ✓ Patient has {len(patient.appointments)} appointment(s)")
        
        assert len(patient.medical_records) > 0, "Patient should have medical records"
        print(f"   ✓ Patient has {len(patient.medical_records)} medical record(s)")
        
        assert len(patient.prescriptions) > 0, "Patient should have prescriptions"
        print(f"   ✓ Patient has {len(patient.prescriptions)} prescription(s)")
        
        assert len(patient.lab_tests) > 0, "Patient should have lab tests"
        print(f"   ✓ Patient has {len(patient.lab_tests)} lab test(s)")
        
        assert len(patient.medical_history) > 0, "Patient should have medical history"
        print(f"   ✓ Patient has {len(patient.medical_history)} medical history entry/entries")
        
        assert len(patient.insurance_info) > 0, "Patient should have insurance info"
        print(f"   ✓ Patient has {len(patient.insurance_info)} insurance record(s)")
        
        assert len(patient.vaccinations) > 0, "Patient should have vaccinations"
        print(f"   ✓ Patient has {len(patient.vaccinations)} vaccination record(s)")
        
    except AssertionError as e:
        print(f"   ✗ Relationship test failed: {e}")
        return False
    except Exception as e:
        print(f"   ✗ Error testing relationships: {e}")
        return False
    
    # Clean up
    session.close()
    
    print("\n" + "=" * 70)
    print("✓ All tests passed successfully!")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    success = test_models()
    sys.exit(0 if success else 1)
