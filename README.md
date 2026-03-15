# AI Food Waste Management Backend

A FastAPI-based backend system designed to reduce food waste by connecting food donors with NGOs and people in need.

The system allows users to donate food, claim available food, search nearby food donations, and predict food expiry using an AI model.


# Project Features

• User Registration and Login with JWT Authentication  
• Secure API access using Bearer Tokens  
• Add and manage food donations  
• Claim available food donations  
• Search for food by name  
• Discover nearby food donations  
• Track personal donations and claims  
• Admin statistics dashboard  
• AI-based food expiry prediction



# Tech Stack

Backend Framework  
• FastAPI

Programming Language  
• Python

Database  
• SQLite

ORM  
• SQLAlchemy

Authentication  
• JWT Token Authentication

Validation  
• Pydantic

AI Component  
• Food expiry prediction model

Server  
• Uvicorn


# Project Structure
backend/
│
├── main.py # FastAPI application and API routes
├── models.py # Database models
├── schemas.py # Request/response schemas
├── database.py # Database connection setup
├── security.py # JWT authentication and password hashing
├── ai_utils.py # AI expiry prediction logic
├── requirements.txt # Project dependencies
└── zerowaste.db # SQLite database




# API Endpoints

## Authentication

POST /register  
Register a new user

POST /login  
Login user and generate JWT token



## Food Donation

POST /add-food  
Add a new food donation

GET /available-food  
View all available food donations

POST /claim-food  
Claim donated food


## User Dashboard

GET /my-donations  
View food donated by the logged-in user

GET /my-claims  
View food claimed by the logged-in user



## Search & Discovery

GET /search-food  
Search food donations by food name

GET /nearby-food  
Find food donations near a location


## AI Feature

POST /predict-expiry  
Predict food expiry time using AI model



# Example API Request

### Add Food Donation

POST `/add-food`

Request Body

{
"food_name": "Rice",
"quantity": 20,
"location": "Bangalore"
}


Headers

# Installation Guide

## 1 Clone the repository
git clone https://github.com/sathwik07/AI-Food-Waste-Management-Backend.git


## 2 Navigate to project folder
cd AI-Food-Waste-Management-Backend/backend



---

## 3 Install dependencies
pip install -r requirements.txt


## Setup Virtual Environment

Create virtual environment

python -m venv venv

Activate virtual environment (Windows)

venv\Scripts\activate

Activate virtual environment (Mac/Linux)

source venv/bin/activate

---

## 4 Run the FastAPI server
uvicorn main:app --reload


---

## 5 Open API Documentation

FastAPI automatically generates interactive API documentation.

Open in browser:
http://127.0.0.1:8000/docs




1️⃣ User registers an account  
2️⃣ User logs in and receives JWT token  
3️⃣ Donor adds food donation  
4️⃣ Other users view available food  
5️⃣ User claims food  
6️⃣ System tracks donations and claims  
7️⃣ AI predicts food expiry to avoid unsafe distribution


# Author

Sathwik Naik  
Information Technology Student

GitHub  
https://github.com/sathwik07


# Future Improvements

• Add real-time location tracking  
• Integrate Google Maps API  
• Deploy backend using Docker  
• Add email notification system  
• Build mobile application frontend

