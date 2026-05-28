# Breathe ESG Ingestion & Audit Prototype

A Django REST and React pipeline built to ingest, normalize, and audit enterprise activity data across disparate sources (SAP, Utilities, Corporate Travel).

## Links & Credentials

- **Live App URL:** []

## Install

pip install -r requirements.txt

## Run

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

## Routes

POST /api/upload/
GET /api/activities/
GET /api/audits/
PATCH /api/approve/:id/
PATCH /api/reject/:id/

## Core Tech Stack

- **Backend:** Django, Django REST Framework, SQLite/PostgreSQL
- **Frontend:** React, Tailwind CSS (Optimized for quick scannability)
