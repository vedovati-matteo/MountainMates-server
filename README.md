# MountainMates API

## Overview

This Flask-based RESTful API powers the MountainMates web application, providing functionalities for user management, hike organization, and more.

## Features

- **User Management:** User registration, profile updates, friend management.
- **Hike Management:** Create, view, update, and delete hikes.
- **Hike Templates:** Create and manage templates for recurring hikes.
- **Authentication:** Secure user authentication using Firebase.
- **Swagger Documentation:** Interactive API documentation at `/api/doc/`.
- **Unit Testing:** Comprehensive unit test suite for ensuring code quality.
- **Database Integration:** Utilizes SQLAlchemy for seamless database interactions.

## Technologies Used

- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-RESTX (for Swagger)
- Firebase Admin SDK
- unittest (for unit testing)

## Installation

1. Start the Application
- Run `docker-compose up --build` to build the images and start the containers.
- Run (if already built): `docker-compose up`
- Your Flask app will be accessible at `http://localhost:5000`, and the PostgreSQL database will be running in the background.

2. Run Database Migrations
`docker-compose exec app python manage.py db init` (if it's the first time)
`docker-compose exec app python manage.py db migrate` (to generate a new migration script)
`docker-compose exec app python manage.py db upgrade` (to apply the migrations)

3. Run Tests
Execute within the app container: `docker-compose exec app python manage.py test`

## API Documentation

Access the Swagger UI documentation at `http://localhost:5000/api/doc/` after running the application.

## Running Tests

Execute the unit tests using: `flask test`

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.