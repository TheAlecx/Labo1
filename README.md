# Labo1
Backoffice du projet web de dossier Médical

## Base de Données Générale pour les Services Médicaux du Québec
General Database for Quebec Medical Services

Ce projet fournit un modèle de base de données complet pour gérer tous les aspects des services médicaux au Québec.

This project provides a comprehensive database model to manage all aspects of medical services in Quebec.

## Fichiers / Files

- **`database_schema.sql`** - Schéma SQL PostgreSQL complet / Complete PostgreSQL SQL schema
- **`models.py`** - Modèles ORM SQLAlchemy / SQLAlchemy ORM models
- **`init_database.py`** - Script d'initialisation avec données d'exemple / Initialization script with sample data
- **`DATABASE_DOCUMENTATION.md`** - Documentation détaillée / Detailed documentation
- **`requirements.txt`** - Dépendances Python / Python dependencies

## Installation

### Prérequis / Prerequisites

- PostgreSQL 12+ (ou SQLite pour tests / or SQLite for testing)
- Python 3.8+

### Installation des dépendances / Install dependencies

```bash
pip install -r requirements.txt
```

### Créer la base de données / Create the database

Option 1: Utiliser le schéma SQL / Use SQL schema
```bash
psql -U username -d database_name -f database_schema.sql
```

Option 2: Utiliser le script Python / Use Python script
```bash
python init_database.py
```

## Utilisation / Usage

Voir `DATABASE_DOCUMENTATION.md` pour une documentation complète.

See `DATABASE_DOCUMENTATION.md` for complete documentation.

### Exemple rapide / Quick Example

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Patient, MedicalProfessional

# Connexion à la base de données
engine = create_engine('postgresql://user:password@localhost/quebec_medical_db')
Session = sessionmaker(bind=engine)
session = Session()

# Rechercher un patient par RAMQ
patient = session.query(Patient).filter_by(ramq_number='TREM80051501').first()
print(f"Patient: {patient.first_name} {patient.last_name}")

# Obtenir tous les rendez-vous du patient
for appointment in patient.appointments:
    print(f"Rendez-vous: {appointment.appointment_date} à {appointment.appointment_time}")
```

## Fonctionnalités / Features

✅ Gestion complète des patients avec numéros RAMQ
✅ Professionnels de la santé (médecins, infirmières, pharmaciens)
✅ Établissements médicaux (hôpitaux, cliniques, pharmacies)
✅ Rendez-vous et dossiers médicaux
✅ Prescriptions et remplissages en pharmacie
✅ Tests de laboratoire et résultats
✅ Historique médical et antécédents
✅ Informations d'assurance RAMQ
✅ Registre de vaccinations

## Documentation

Consultez `DATABASE_DOCUMENTATION.md` pour:
- Structure détaillée des tables
- Relations entre entités
- Exemples d'utilisation
- Considérations de sécurité
- Extensions possibles

See `DATABASE_DOCUMENTATION.md` for:
- Detailed table structure
- Entity relationships
- Usage examples
- Security considerations
- Possible extensions
