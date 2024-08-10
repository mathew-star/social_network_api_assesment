

# Social Network API-assesment

This project is a Django-based API for a social networking application. The application includes functionalities for user authentication, friend requests, and managing friendships. The API is containerized using Docker to ensure a consistent environment for development and production.

## Features

- User registration and login
- Sending and accepting friend requests
- Viewing friends list
- Rate limiting on friend requests (maximum 3 requests per minute)
- API documentation via Postman collection

## Installation

Follow these steps to set up the project on your local machine.

### Prerequisites

- Docker and Docker Compose installed on your machine.
- Python 3.10 or above (if running locally without Docker).
- Git installed on your machine.

### Clone the Repository

```bash
git clone https://github.com/mathew-star/social_network_api_assesment.git
cd social-network-api
```

### Environment Variables

Create a `.env` file in the root directory with the following content:

```bash
SECRET_KEY='django_secret_key_here'

```

### Docker Setup

1. **Build and Run the Docker Containers**

   ```bash
   docker compose up --build
   ```

   This command will build the Docker images and start the containers.

2. **Apply Migrations**

   After the containers are up and running, apply the migrations to set up the database schema.

   ```bash
   docker compose exec web python manage.py migrate
   ```

3. **Create a Superuser (Optional)**

   If you want to create a superuser for accessing the Django admin panel, run:

   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

### Running Locally Without Docker

If you prefer to run the project locally without Docker, follow these steps:

1. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the Database**

   Ensure PostgreSQL is installed and running on your machine. Create a database named `postgres`, or update the `.env` file with your custom database details.

4. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

### API Documentation

A Postman collection has been provided to test the API endpoints easily.

- [Postman Collection](https://documenter.getpostman.com/view/31420357/2sA3s3GqWf)



### Dockerfile

The Dockerfile is configured to ensure that the application waits for the PostgreSQL database to be ready before starting the Django development server.

### Docker Compose

The `docker-compose.yml` file sets up two services:

- `web`: The Django application.
- `db`: A PostgreSQL database.

The database data is stored in a Docker volume named `postgres_data`.





### License

This project is licensed under the MIT License.

### Contact

For any inquiries or issues, please contact [mathewjosef41@gmail.com](mailto:your.email@example.com).

---
