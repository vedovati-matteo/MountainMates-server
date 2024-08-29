# MountainMates Server 🏔️

Welcome to MountainMates Server, the robust backend powering the MountainMates application! This Flask-based API manages user accounts, hiking trips, and trip templates, making it easier than ever to organize and participate in hiking excursions.

## 🌟 Features

- User account management
- Hiking trip organization
- Trip template creation and management
- RESTful API architecture
- Firebase authentication integration
- Swagger API documentation

## 🛠️ Technologies

- Flask: Web framework for building the API
- Flask-SQLAlchemy: ORM for database interactions
- Flask-Migrate: Database migration management
- Firebase Admin SDK: User authentication
- Flask-RESTX: Simplifies RESTful API creation and Swagger documentation
- PostgreSQL: Relational database for data storage
- Docker: Application containerization
- Gunicorn: Production-grade WSGI server

## 🚀 Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/vedovati-matteo/MountainMates_server.git
   cd MountainMates_server
   ```

2. Set up the necessary environment variables. You can either create a .env file in the project root or set the variables directly in your environment:

- **Option 1**: using a `.env` file
    Create a `.env` file in the project root and add the following  environment variables:
   ```
   FIREBASE_CREDENTIALS_PATH=<path/to/firebase_credential.json>
   FIREBASE_WEB_API_KEY=<firebase-web-api-key>
   POSTGRES_PASSWORD=mysecretpassword
   FLASK_DEBUG=0 # Set 0 for production and 1 for development
   ```
- **Option 2**: Setting environment variables directly
    Set the environment variables in your shell or environment configuration:
   ```
   export FIREBASE_CREDENTIALS_PATH=<path/to/firebase_credential.json>
   export FIREBASE_WEB_API_KEY=<firebase-web-api-key>
   export POSTGRES_PASSWORD=mysecretpassword
   export FLASK_DEBUG=0
   ```

3. Build and start the Docker containers:
   ```
   docker-compose up --build
   ```

4. The API will be available at `http://localhost:5000`

### Database Migrations

If you need to run database migrations, you can use the following commands:

1. Initialize the migration environment (if it's the first time):
    ```
    docker-compose exec app python manage.py db init
    ```

2. Generate a new migration script (after making changes to your models):
    ```
    docker-compose exec app python manage.py db migrate
    ```

3. Apply the migrations:
    ```
    docker-compose exec app python manage.py db upgrade
    ```

## 📚 API Documentation

- Access the Swagger UI documentation at `http://localhost:5000/api/doc/` when the server is running.
- For static documentation, refer to the [swagger docs](https://vedovati-matteo.github.io/MountainMates_server/swagger.html).

## 🧪 Testing

Run the unit tests using:

```
docker-compose exec app python manage.py test
```

## 🔒 Security

- User authentication is handled via Firebase ID tokens.
- Ensure to keep your `.env` file and Firebase credentials secure and never commit them to version control.

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

If you encounter any issues or have questions, please file an issue on the GitHub repository.

Happy hiking with MountainMates! 🥾🏞️
