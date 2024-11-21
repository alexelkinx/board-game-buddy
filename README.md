# Board Game Buddy

## Overview

**Board Game Buddy** is a web application designed to help groups of friends manage their board game collections and lending activities. The application keeps track of board games, users (gamers), and loan statuses. It allows users to:

- Register and manage their accounts.
- Add, edit, and delete their board games.
- View all games available in the system.
- Borrow currently available games (up to 3 at a time).
- Return games they have borrowed.
- View lending and borrowing histories.

The system ensures a gamer cannot borrow more than three games simultaneously, prompting them to return one before borrowing another. It also records the creation and modification timestamps for all data, enabling users to track who borrowed a game and when.

---

## Directory Structure

```
board-game-buddy/
├── bgb_project/                    # Django project folder
│   ├── __init__.py
│   ├── asgi.py                     # ASGI configuration
│   ├── settings.py                 # Project settings
│   ├── urls.py                     # Root URL configuration
│   └── wsgi.py                     # WSGI configuration for deployment
├── boardgames/                     # Main app for the Board Game Buddy functionality
│   ├── fixtures/                   # JSON files for initial data (e.g., default categories, games)
│   │   └── example_data.json
│   ├── migrations/                 # Database migrations
│   │   └── __init__.py
│   ├── static/                     # Static files for the boardgames app
│   │   ├── images/
│   │   │   └── logo.png
│   │   └── favicin.ico
│   ├── templates/                  # Templates for the boardgames app
│   │   └── boardgames/
│   │       ├── base.html
│   │       ├── game_detail.html
│   │       └── edit_game.html
│   ├── __init__.py
│   ├── admin.py                    # Admin interface for models
│   ├── apps.py                     # App configuration
│   ├── forms.py                    # Forms for user input (e.g., GameForm, ProfileForm)
│   ├── models.py                   # Database models for BoardGame, Loan, and Gamer
│   ├── signals.py                  # Signals for handling model events (e.g., post-save actions)
│   ├── tests.py
│   ├── urls.py                     # App-specific URL configuration
│   └── views.py                    # Views for handling HTTP requests
├── media/                          # User-uploaded files (e.g., images for profiles or games)
├── .gitignore
├── manage.py                       # Django management script
├── README.md
└── requirements.txt                # Python dependencies for the project
```

## Getting Started

### Prerequisites

- Python 3.x installed on your system
- Pip for Python package management

### Installation Steps

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd board-game-buddy
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:

   ```bash
   source .venv/bin/activate # On macOS/Linux
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Apply database migrations**:

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**:

   ```bash
   python manage.py createsuperuser
   ```

7. **Load initial data** (optional, for predefined categories and games):

   ```bash
   python manage.py loaddata categories.json
   python manage.py loaddata games.json
   ```

8. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

9. **Access the application**:

   ```bash
   Open a browser and go to `http://127.0.0.1:8000/`.
   ```

---

## Usage

1. **Sign up** and log in to start using the application.
2. **Add your board games** via the "Add Game" feature.
3. **View and borrow games** listed by other users.
4. **Track your borrowed games** and return them when done.
5. **View borrowing history** and manage your lending activity.

---

## License

This project is for educational and personal use. Feel free to contribute! 😊
