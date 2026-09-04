# Blood Bank Management System

A Python-based Enterprise Web Application for managing blood bank operations,
built with Django, Django REST Framework, and Oracle Database.

## Built By
**Kumud Ratna Dangol**  
KFA Business School  
Module: Database Management Systems  
Lecturer: Bikash Khadka  

## Features
- Full CRUD operations for Donors, Blood Banks, Hospitals, Blood Units, Requests
- REST API with Django REST Framework
- 3 navigational queries and 2 complex multi-entity queries
- Background task for automatic blood unit expiry detection
- Web-based frontend (HTML/CSS/JavaScript)
- Django Admin panel

## Tech Stack
- Python 3.x
- Django 6.1
- Django REST Framework 3.18
- Oracle Database
- HTML/CSS/JavaScript

## Installation
See `report.md` for full installation instructions.

### Quick Start
1. Clone the repository
2. Create and activate virtual environment:
   `python -m venv venv` then `.\venv\Scripts\activate`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Configure Oracle database in `config/settings.py`
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Start server: `python manage.py runserver`
8. Visit: `http://127.0.0.1:8000`

## Pages
| URL | Description |
|---|---|
| /donors/ | Manage blood donors |
| /banks/ | Manage blood banks |
| /hospitals/ | Manage hospitals |
| /units/ | Manage blood units |
| /requests/ | Manage blood requests |
| /reports/ | Reports and background task |
| /admin/ | Django admin panel |
| /api/ | REST API endpoints |