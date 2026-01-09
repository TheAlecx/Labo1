# Base de Données Générale pour les Services Médicaux du Québec
## General Database for Quebec Medical Services

## Vue d'ensemble / Overview

Cette base de données fournit un modèle complet pour gérer tous les aspects des services médicaux au Québec, incluant les patients, les professionnels de la santé, les établissements médicaux, les rendez-vous, les dossiers médicaux, les prescriptions et plus encore.

This database provides a comprehensive model for managing all aspects of medical services in Quebec, including patients, healthcare professionals, medical facilities, appointments, medical records, prescriptions, and more.

## Structure de la Base de Données / Database Structure

### Tables Principales / Main Tables

#### 1. **patients**
Stocke les informations des patients avec leur numéro de carte RAMQ (Régie de l'assurance maladie du Québec).

Stores patient information with their Quebec health card number (RAMQ).

**Champs principaux / Key fields:**
- `ramq_number`: Numéro unique de carte RAMQ (12 caractères)
- `first_name`, `last_name`: Nom du patient
- `date_of_birth`: Date de naissance
- `address_*`: Adresse complète
- `phone_number`, `email`: Coordonnées
- `emergency_contact_*`: Contact d'urgence
- `blood_type`: Groupe sanguin
- `allergies`: Allergies connues

#### 2. **medical_professionals**
Docteurs, infirmières, spécialistes, pharmaciens et autres professionnels de la santé.

Doctors, nurses, specialists, pharmacists, and other healthcare professionals.

**Champs principaux / Key fields:**
- `license_number`: Numéro de permis professionnel
- `professional_type`: Type (docteur, infirmière, pharmacien, etc.)
- `specialty`: Spécialité médicale
- `first_name`, `last_name`: Nom du professionnel
- `is_active`: Statut actif

#### 3. **medical_facilities**
Hôpitaux, cliniques, pharmacies, laboratoires et autres établissements médicaux.

Hospitals, clinics, pharmacies, laboratories, and other medical facilities.

**Champs principaux / Key fields:**
- `facility_name`: Nom de l'établissement
- `facility_type`: Type (hôpital, clinique, pharmacie, laboratoire)
- `address_*`: Adresse complète
- `capacity`: Capacité de l'établissement
- `is_active`: Statut actif

#### 4. **facility_staff**
Table de liaison entre les professionnels et les établissements.

Junction table linking professionals to facilities.

**Champs principaux / Key fields:**
- `facility_id`: Référence à l'établissement
- `professional_id`: Référence au professionnel
- `start_date`, `end_date`: Période d'affectation
- `is_current`: Affectation actuelle

#### 5. **appointments**
Rendez-vous médicaux entre patients et professionnels.

Medical appointments between patients and professionals.

**Champs principaux / Key fields:**
- `patient_id`: Référence au patient
- `professional_id`: Référence au professionnel
- `facility_id`: Référence à l'établissement
- `appointment_date`, `appointment_time`: Date et heure
- `duration_minutes`: Durée en minutes
- `status`: Statut (prévu, complété, annulé, absent)
- `reason`: Raison de la consultation

#### 6. **medical_records**
Dossiers médicaux et consultations.

Medical consultation and examination records.

**Champs principaux / Key fields:**
- `patient_id`: Référence au patient
- `professional_id`: Référence au professionnel
- `visit_date`, `visit_time`: Date et heure de visite
- `chief_complaint`: Plainte principale
- `diagnosis`: Diagnostic
- `treatment_plan`: Plan de traitement
- `follow_up_required`: Suivi requis
- `follow_up_date`: Date de suivi

#### 7. **prescriptions**
Prescriptions médicales émises par les professionnels.

Medical prescriptions issued by professionals.

**Champs principaux / Key fields:**
- `patient_id`: Référence au patient
- `professional_id`: Référence au professionnel
- `medication_name`: Nom du médicament
- `medication_code`: Code DIN (Drug Identification Number)
- `dosage`: Dosage
- `frequency`: Fréquence d'administration
- `refills_allowed`, `refills_remaining`: Renouvellements
- `prescribed_date`, `expiry_date`: Dates de validité
- `is_active`: Statut actif

#### 8. **prescription_fills**
Suivi des prescriptions remplies en pharmacie.

Tracks when prescriptions are filled at pharmacies.

**Champs principaux / Key fields:**
- `prescription_id`: Référence à la prescription
- `pharmacy_id`: Référence à la pharmacie
- `pharmacist_id`: Référence au pharmacien
- `fill_date`: Date de remplissage
- `quantity_dispensed`: Quantité dispensée

#### 9. **lab_tests**
Tests de laboratoire et résultats.

Laboratory tests and results.

**Champs principaux / Key fields:**
- `patient_id`: Référence au patient
- `ordering_professional_id`: Professionnel prescripteur
- `test_name`: Nom du test
- `test_code`: Code du test
- `test_category`: Catégorie (analyse sanguine, imagerie, etc.)
- `order_date`, `collection_date`, `result_date`: Dates
- `result_value`: Valeur du résultat
- `result_status`: Statut (en attente, complété, annulé)
- `is_abnormal`: Résultat anormal

#### 10. **medical_history**
Historique médical des patients incluant conditions et chirurgies.

Patient medical history including conditions and surgeries.

**Champs principaux / Key fields:**
- `patient_id`: Référence au patient
- `condition_type`: Type (condition, chirurgie, antécédents familiaux)
- `condition_name`: Nom de la condition
- `diagnosis_date`, `resolution_date`: Dates
- `is_active`: Condition active
- `severity`: Sévérité (légère, modérée, sévère)

#### 11. **insurance_information**
Informations d'assurance et couverture RAMQ.

Insurance and RAMQ coverage information.

**Champs principaux / Key fields:**
- `patient_id`: Référence au patient
- `insurance_type`: Type (RAMQ, privée, supplémentaire)
- `policy_number`: Numéro de police
- `provider_name`: Nom du fournisseur
- `coverage_start_date`, `coverage_end_date`: Période de couverture
- `is_active`: Couverture active

#### 12. **vaccinations**
Registre des vaccinations des patients.

Patient vaccination records.

**Champs principaux / Key fields:**
- `patient_id`: Référence au patient
- `vaccine_name`: Nom du vaccin
- `vaccine_code`: Code du vaccin
- `dose_number`: Numéro de dose
- `administration_date`: Date d'administration
- `lot_number`: Numéro de lot
- `site`: Site d'injection

## Relations entre les Tables / Table Relationships

```
patients (1) ----< (N) appointments
patients (1) ----< (N) medical_records
patients (1) ----< (N) prescriptions
patients (1) ----< (N) lab_tests
patients (1) ----< (N) medical_history
patients (1) ----< (N) insurance_information
patients (1) ----< (N) vaccinations

medical_professionals (1) ----< (N) appointments
medical_professionals (1) ----< (N) medical_records
medical_professionals (1) ----< (N) prescriptions
medical_professionals (1) ----< (N) lab_tests
medical_professionals (1) ----< (N) facility_staff

medical_facilities (1) ----< (N) appointments
medical_facilities (1) ----< (N) medical_records
medical_facilities (1) ----< (N) facility_staff
medical_facilities (1) ----< (N) prescription_fills

appointments (1) ----< (1) medical_records

prescriptions (1) ----< (N) prescription_fills

medical_records (1) ----< (N) prescriptions
medical_records (1) ----< (N) lab_tests
```

## Utilisation / Usage

### SQL Schema
Le fichier `database_schema.sql` contient le schéma SQL complet pour créer la base de données avec PostgreSQL.

The `database_schema.sql` file contains the complete SQL schema to create the database with PostgreSQL.

```sql
psql -U username -d database_name -f database_schema.sql
```

### Python ORM Models
Le fichier `models.py` contient les modèles ORM SQLAlchemy pour interagir avec la base de données en Python.

The `models.py` file contains SQLAlchemy ORM models to interact with the database in Python.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Patient, MedicalProfessional, Appointment

# Créer la connexion à la base de données
engine = create_engine('postgresql://user:password@localhost/medical_db')

# Créer toutes les tables
Base.metadata.create_all(engine)

# Créer une session
Session = sessionmaker(bind=engine)
session = Session()

# Exemple: Ajouter un nouveau patient
new_patient = Patient(
    ramq_number='ABCD12345678',
    first_name='Jean',
    last_name='Tremblay',
    date_of_birth='1980-05-15',
    phone_number='514-555-1234',
    email='jean.tremblay@example.com'
)
session.add(new_patient)
session.commit()
```

## Indexes et Performance

La base de données inclut plusieurs index pour améliorer les performances des requêtes fréquentes:

The database includes several indexes to improve performance of common queries:

- Index sur les numéros RAMQ pour recherche rapide des patients
- Index sur les noms de patients et professionnels
- Index sur les dates de rendez-vous et visites
- Index sur les statuts (rendez-vous, prescriptions, tests)
- Index sur les types de professionnels et établissements

## Sécurité et Conformité / Security and Compliance

Cette base de données est conçue pour:
- Respecter les normes de confidentialité RAMQ
- Protéger les informations personnelles de santé (IPS)
- Suivre les réglementations provinciales du Québec
- Permettre l'audit et le suivi des accès

This database is designed to:
- Comply with RAMQ privacy standards
- Protect Personal Health Information (PHI)
- Follow Quebec provincial regulations
- Enable audit and access tracking

**Note importante**: Cette implémentation doit être complétée par:
- Chiffrement des données sensibles
- Contrôles d'accès basés sur les rôles (RBAC)
- Journalisation des accès et modifications
- Sauvegardes régulières et plan de reprise après sinistre

**Important note**: This implementation must be complemented by:
- Encryption of sensitive data
- Role-Based Access Control (RBAC)
- Access and modification logging
- Regular backups and disaster recovery plan

## Extensions Possibles / Possible Extensions

- **Système de messagerie**: Communication entre patients et professionnels
- **Gestion de lits**: Pour les hôpitaux
- **Planification des salles**: Gestion des salles d'opération et d'examen
- **Facturation**: Intégration avec les systèmes de facturation RAMQ
- **Télémédecine**: Support pour les consultations à distance
- **Imagerie médicale**: Stockage et gestion des images (PACS)
- **Pharmacie**: Gestion d'inventaire et interactions médicamenteuses

## Licence / License

Ce modèle de base de données est fourni comme référence pour les systèmes de gestion médicale au Québec.

This database model is provided as a reference for medical management systems in Quebec.
