## DiscountU: Student Discount Aggregator
![image](https://github.com/user-attachments/assets/2cc1b02c-4ecf-446f-84e6-811d8c1cba2d)


DiscountU is a web application that allows students to explore and access discounts with student IDs. This README will guide you through the setup, installation, and usage of the DiscountU application.

### Table of Contents

* Introduction
* Prerequisites
* Installation
* Getting Started
* Usage
* Features

### Introduction

DiscountU is designed to provide students with a streamlined way to find discounts applicable to them through their student IDs. Users can register, log in, and view various categories and details of discounts from different brands.
### Prerequisites

Before setting up DiscountU, ensure you have the following installed:
* Python 3.8 or higher
* Django 3.x or higher
* Required Python packages:
    * django
    * djangorestframework
    * pillow (for image handling)
* Any other dependencies mentioned in requirements.txt

### Installation

**Clone the repository:**

* git clone [invalid URL removed]
* cd DiscountU


**Create a Python virtual environment (optional but recommended):**

* python -m venv venv
* source venv/bin/activate  # On Windows: venv\Scripts\activate

**Install Required Packages:**

* pip install -r requirements.txt   

**Set Up the Django Project:**

* python manage.py migrate
* python manage.py createsuperuser

**Start the Development Server:**

* python manage.py runserver

### Getting Started

To get started with DiscountU:

1. Clone the repository and install the required dependencies described in the Installation section.
2. Run the server and access the application through http://localhost:8000.

### Usage

Once the development server is running:

* **Sign up/Login:** Users can register or log in to their accounts.
* **Browse Discounts:** View available discounts across various categories.
* **User Profile:** Manage profile information.
* **Bookmark Discounts:** Save favorite discounts for quick access later.

### Features

* **User Authentication:** Secure login and registration functionality.
* **Discount Listing:** View discounts by category and brand.
* **User Profile Management:** Update and manage user profile details..
* **Responsive Design:** Device-friendly UI for easy access on any device.
