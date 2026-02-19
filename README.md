# Django E-commerce Backend

## Overview
A production-style backend built with Django and Django REST Framework.  
Features include authentication, cart management, checkout, payments, and order tracking.

## Features
- User registration & login
- Product listing
- Cart management
- Checkout flow with stock validation
- Payment flow (PayPal, Stripe, Credit Card)
- Order history

## Tech Stack
- Django
- Django REST Framework
- SQLite (default, can switch to PostgreSQL)
- Coverage for testing

## Setup
```bash
git clone <your-repo-url>
cd <repo-folder>
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
