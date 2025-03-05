# College Link Up for Events (C.L.U.E)

C.L.U.E is a Django-based web application designed to manage and streamline information about college clubs, events, and festivals. The platform provides details about upcoming events, allowing students and visitors to stay informed and engaged.

## Features
- User authentication and authorization
- Event creation and management
- Department-based categorization
- Admin panel for handling user roles
- Media upload for event posters
- Interactive UI for better accessibility

## Installation

### 1. Install Django
Ensure you have Python installed, then install Django:
```sh
pip install django
```

### 2. Clone the Repository
```sh
git clone https://github.com/AkAnK1407/Clue_Django.git
cd Clue_Django
```

### 3. Set Up a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 4. Install Dependencies
```sh
pip install -r requirements.txt
```

### 5. Configure MySQL Database
Modify `settings.py` to set up MySQL connection:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 6. Apply Migrations
```sh
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser
```sh
python manage.py createsuperuser
```
Use the following credentials:
- **Username**: akank
- **Password**: akank

### 8. Run the Development Server
```sh
python manage.py runserver
```
Access the application at `http://127.0.0.1:8000/`

## Project Structure
```
C:.
├───admin_handling
│   ├───migrations
│   │   └───__pycache__
│   └───__pycache__
├───clue
│   └───__pycache__
├───department
│   ├───migrations
│   │   └───__pycache__
│   └───__pycache__
├───event
│   ├───migrations
│   │   └───__pycache__
│   └───__pycache__
├───home
│   ├───event
│   │   ├───migrations
│   │   │   └───__pycache__
│   │   ├───static
│   │   │   ├───css
│   │   │   └───img
│   │   ├───template
│   │   │   └───store
│   │   └───__pycache__
│   ├───migrations
│   │   └───__pycache__
│   └───__pycache__
├───signup
│   ├───migrations
│   │   └───__pycache__
│   └───__pycache__
├───static
│   ├───css
│   ├───img
│   └───media
│       ├───club_posters
│       ├───department_posters
│       ├───event_posters
│       └───fest_posters
└───template
```

## Usage
- Users can browse and register for events.
- Admins can create and manage events.
- The application maintains department-based event categorization.

---
This README provides a complete guide to setting up and running the **College Link Up for Events (C.L.U.E)** web application.

