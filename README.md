# gym-management-django

A web-based Gym and Fitness Management App built with Django. Allows admins to manage users, workouts, and memberships, while members can view routines and track progress. Includes PostgreSQL, Bootstrap 5 UI, and OpenWeather API integration.

# Project contribution - Group Assingment

Leader - Martin Quintero - My favorite quote is from Elder David A. Bednar that states that "Technology in and of itself is neither inherently good nor bad. Rather, the purposes accomplished with and through technology are the ultimate indicators of goodness or badness," and urges members to use it to "advance the work of salvation".

Member - Johann Tellez - My favorite quote is “Arise now, ye Tarnished.
Ye dead, who yet live.
The call of long-lost grace speaks to us all.” from FromSoftware, Inc, Elden Ring(2022)

Member - Ailen Rocio Mansilla - Favorite quote "Love is spelled T-I-M-E"

# 🏋️‍♂️ Gym and Fitness Management App (Python/Django)

## 📖 Overview

The **Gym and Fitness Management App** is a web-based platform built with **Python (Django)** that enables gym owners, instructors, and members to manage fitness-related activities efficiently.

The app provides two main user roles — **Admin** and **User** — each with specific features and permissions, such as managing workouts, memberships, and instructors.  
It also integrates the **OpenWeather API** to show real-time weather data for outdoor training sessions.

---

## 🎯 Features

### 👤 User Features

- Secure registration and login
- Personalized workout routine view
- Membership tracking and expiration alerts
- Real-time weather display via OpenWeather API
- Profile management

### 🧑‍💼 Admin Features

- Admin authentication and dashboard
- Manage users, instructors, and workout plans
- Define pricing and membership durations
- Approve/reject participant registrations
- View statistics (active users, revenue, membership reports)

### ⚙️ General Features

- Responsive design using **Bootstrap 5**
- **Role-based access control** for Admins and Users
- **PostgreSQL** database integration
- **Heroku** cloud deployment
- RESTful API integration with OpenWeather

---

## 🏗️ Tech Stack

| Component           | Technology      | Description                                     |
| ------------------- | --------------- | ----------------------------------------------- |
| **Backend**         | Python (Django) | Core logic, authentication, and API integration |
| **Frontend**        | HTML, CSS       | Responsive and user-friendly interface          |
| **Database**        | PostgreSQL      | Stores users, workouts, and membership data     |
| **Hosting**         | Heroku          | Cloud deployment and scalability                |
| **API Integration** | OpenWeather API | Real-time weather data                          |
| **Version Control** | Git + GitHub    | Collaboration and source control                |

---

## 🚀 Installation & Setup

Follow these steps to set up the project locally:

### 1. Clone the repository

git clone https://github.com/<your-username>/gym-management-django.git
cd gym-management-django

---

### 2. Create and activate a virtual environment

python -m venv venv
source venv/bin/activate # For Mac/Linux
venv\Scripts\activate # For Windows

---

### 3. Install dependencies

pip install -r requirements.txt

---

### 4. Create .env file

OPENWEATHER_API_KEY=your_openweather_api_key

---

### 5. Apply migrations and run server

Migration in progress - not needed
python manage.py runserver

---

### 6. Access the App

Go to http://localhost:8000

## 🧩 Project Structure

gym-management-django/
│
├── core/ # Main Django app (settings, urls, wsgi)
├── users/ # User and authentication logic
├── workouts/ # Workout routines and assignments
├── memberships/ # Membership management
├── templates/ # HTML templates (Bootstrap 5)
├── static/ # CSS, JS, images
├── requirements.txt # Python dependencies
├── Procfile # Heroku deployment file
├── runtime.txt # Python version for Heroku
└── README.md # Project documentation

## 🧮 Database Schema (ERD Overview)

Entities:

User → Role (Admin/User), profile info

Instructor → Assigned routines

Membership → Plan type, start/end date, status

Workout Routine → Exercises, schedule, linked to User & Instructor

## 🖥️ Deployment (Heroku)

heroku login
heroku git:remote -a gym-management-proj

git add .
git commit -m "Deploy update"
git push heroku <branch>:main

## Migrations

heroku run python website/manage.py migrate --app gym-management-proj

## Update Requirements with

pip freeze > requirements.txt