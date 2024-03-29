# Tales Of Morocco

### Join us as we uncover the essence of Morocco, one tale at a time

![Project Landing Page](https://github.com/Elbadil/Tales_Of_Morocco/raw/master/static/images/home-page.jpg)

## Table of Contents
- [Introduction](#introduction)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Acknowledgment](#acknowledgment)
- [Contributing](#contributing)

## Introduction

**Tales of Morocco** is a platform dedicated to delving into the captivating landscapes, diverse culture, and dynamic communities of Morocco. Here, travel enthusiasts can immerse themselves in sharing their travel escapades, culinary discoveries, and accommodation experiences, along with picturesque views.

This projects community serves as a hub where adventurers exchange invaluable recommendations for crafting their next unforgettable Moroccan journey.

## Tech Stack
### Backend:
* Python (Framework: Django)
* JavaScript

### Frontend:
* HTML
* CSS
* Javascript
* Base Design by **[HTML5 UP](https://html5up.net)**

### Database:
* SQLite

## Project Structure
### Main Files:
- **base/apps.py**: Django application configuration.
- **base/forms.py**: Form classes for user registration, blog post creation, and profile updates.
- **base/models.py**: Database models for users, blog posts, comments, likes, and cities.
- **base/views.py**: View functions for rendering HTML templates, handling user authentication, and managing CRUD operations for blog posts and user profiles.
- **base/views.py**: URL routing configuration for mapping URLs to view functions.

### Templates and Static:
- **base/templates/**: Directory containing HTML templates used by Django for rendering pages.
- **static/**: Directory for static assets like CSS, JavaScript, and images.

### Additional Files:
- **.gitignore**: Specifies files and directories to be ignored by version control.
- **requirements.txt**: Lists Python dependencies required to run the web app.
- **README.md**: This Documentation file that provides comprehensive information about the project.

### Virtual Environment:
- **tomenv/**: Directory containing the Python virtual environment used for this project.

## Features

- User authentication and registration
- Create, update, and delete blog posts
- Like and comment on blog posts
- Explore blogs by city, cuisine, and accommodation
- View profiles of other users and their activities

## Setup

To run this project locally, follow these steps:

1. Clone this repository. https://github.com/Elbadil/Tales_Of_Morocco.git
2. Install the necessary dependencies by running:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up the database by running migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
4. Run the Django development server:
    ```bash
    python manage.py runserver
    ```
5. Access the application in your web browser at `http://localhost:8000`.

## Usage

Upon launching the application, users can:

- Register for an account or log in if they already have one.
- Create new blog posts with details about their travel experiences.
- Like and comment on blog posts shared by other users.
- Explore blog posts by city, cuisine, and accommodation preferences.
- Update their account details and profile picture.
- View profiles of other users to see their activities and blog posts.

## Acknowledgment

This project was developed by **[Adil EL Bali](https://github.com/Elbadil)** and **[Safouane EL Mail](https://github.com/Safuan04)**.
We extend our thanks to the following resources that have been very helpful:

### Resources
- **[Django Documentation](https://docs.djangoproject.com/en/stable/)**
- **[Python Django 7 Hour Course by Dennis Ivy](https://www.youtube.com/watch?v=PtQiiknWUcI&t=21265s)**
- **[ChatGPT](https://chat.openai.com/)**

## Contributing

Contributions to improve this project are welcome. Feel free to fork the repository, make changes, and create a pull request.
