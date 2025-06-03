# student-exam-portal
# Student Exam Portal

A web-based examination system built with Django that allows staff to manage subjects and questions, and students to take timed exams and view their results.

## ✨ Features

### 👨‍🏫 Staff (Admin)
- Create, update, and delete subjects.
- Add, edit, and delete multiple-choice questions for each subject.
- View all student exam results.

### 👨‍🎓 Students
- View available subjects.
- Take timed exams (one attempt per subject).
- Automatically scored multiple-choice answers.
- View their past results and scores.

### 🔐 Authentication
- Separate dashboards for staff and students.
- Login/logout functionality.
- Permission checks for staff vs student access.

## 🛠️ Tech Stack

- **Backend:** Django
- **Frontend:** Bootstrap 5
- **Database:** SQLite (default, can be changed)
- **Auth:** Django's built-in User system

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- pip
- virtualenv (recommended)

### Setup

```bash
# Clone the repository
git clone https://github.com/your-username/student-exam-portal.git
cd student-exam-portal

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver
