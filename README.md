
# Stores REST API

This project is a RESTful API for managing a store inventory system built using Flask. The API allows users to manage items, stores, tags, and user authentication with JWT (JSON Web Token) for secure access. Swagger documentation is available for easy exploration of API endpoints.

## Features
- **CRUD operations** for items, stores, and tags.
- **User Authentication** with JWT.
- **Token Management** (blocklist, expiration, and refresh).
- **Swagger UI** for interactive API documentation.

## Technologies
- **Flask**: Web framework.
- **Flask-Smorest**: Simplifies API endpoint creation.
- **Flask-Migrate**: Handles database migrations.
- **Flask-JWT-Extended**: Manages JWT for secure authentication.
- **SQLAlchemy**: ORM for database interaction.

## Setup and Installation

### Prerequisites
- Python 3.6+
- `pip` (Python package manager)
- A database (SQLite is used by default)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional):
   - Set the database URL:
     ```bash
     export DATABASE_URL="sqlite:///data.db"  # Default: SQLite database
     ```
   - Configure the JWT secret key:
     ```bash
     export JWT_SECRET_KEY="your_secret_key"
     ```

5. **Run database migrations**:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. **Start the application**:
   ```bash
   flask run
   ```

   The API will run on `http://localhost:5000`.

### Running with Docker (optional)
1. Ensure Docker is installed.
2. Build and run the container:
   ```bash
   docker build -t stores-rest-api .
   docker run -p 5000:5000 stores-rest-api
   ```

## Project Structure

- `app.py`: Application factory with all configurations and setup.
- `resources/`: Contains blueprints for items, stores, tags, and users.
- `blocklist.py`: Defines the blocklist to manage revoked JWTs.
- `db/`: Database setup and migration scripts.

## JWT Token Handling

- **Token Expiration**: Custom callback for expired tokens.
- **Invalid Tokens**: Checks for invalid signatures.
- **Missing Tokens**: Responds to requests without access tokens.
- **Fresh Tokens**: Ensures token freshness.
- **Revoked Tokens**: Handles revoked tokens using a blocklist.

## Swagger UI

To access the API documentation, visit `https://store-api-xoxt.onrender.com/swagger-ui`. This provides a web-based interface to interact with API endpoints.

## License
This project is licensed under the MIT License.
