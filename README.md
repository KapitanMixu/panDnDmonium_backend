# PanDnDmonium Backend

This is the backend server for the PanDnDmonium project, a D&D character management system.

## Getting Started

### Prerequisites

Make sure you have Python 3.x installed on your system.

### Installation

1. Install project dependencies:
   ```bash
   pip install -r requirements.txt

Running the Server
To start the development server:
python3 manage.py runserver

The server will start at http://127.0.0.1:8000
API Documentation
• Swagger UI: http://127.0.0.1:8000/swagger/
    • View and test all available API endpoints
    • Interactive API documentation
Initial Setup
After starting the server for the first time, follow these steps:
1. Run database migrations:
1. python3 manage.py migrate

2. Import initial data:
2. python3 manage.py import_spells
python3 manage.py import_phb_classes
python3 manage.py import_class_spell_list

These commands will load spells, Player's Handbook classes, and class-spell associations into the database.
