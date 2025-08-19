# Book Management API - Prasanna Assessment JKTECH

A Flask-based REST API for managing books, users, and reviews. This project provides a complete book management system with user authentication, book CRUD operations, and review functionality.

## 🚀 Features

- **User Management**: Registration, login, and profile management with JWT authentication
- **Book Management**: Full CRUD operations for books
- **Review System**: Add and view reviews for books with ratings
- **Book Recommendations**: Get personalized book recommendations
- **API Documentation**: Interactive Swagger UI documentation
- **Database**: SQLAlchemy ORM with PostgreSQL support
- **Testing**: Comprehensive test suite with pytest
- **Docker Support**: Containerized deployment ready

## 📋 Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Local Development](#local-development)
  - [Docker Setup](#docker-setup)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Documentation](#documentation)
- [Deployment](#deployment)
- [Contributing](#contributing)

## 📁 Project Structure

```
project_folder/
│
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration settings
│   ├── models.py                # Database models
│   ├── utils.py                 # Utility functions
│   ├── routes/
│   │   ├── book_routes.py       # Book-related endpoints
│   │   └── user_routes.py       # User authentication endpoints
│   ├── services/
│   │   └── auth_service.py      # Authentication service
│   └── static/
│       └── swagger.json         # API documentation
├── migrations/                  # Database migration files
│   ├── versions/
│   │   └── f52ba00f649a_books_users_migration.py
│   ├── alembic.ini
│   ├── env.py
│   └── script.py.mako
├── tests/
│   └── test_book_routes.py      # Test cases
├── .env                         # Environment variables (create this)
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── init_db.py                   # Database initialization script
├── Dockerfile                   # Docker configuration
├── pytest.ini                  # Pytest configuration
└── README.md                    # This file
```

## 🔧 Prerequisites

- Python 3.11+
- PostgreSQL (for production) or SQLite (for development)
- Docker and Docker Compose (optional)

## 💾 Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd book-management-api
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=sqlite:///dev.db
   FLASK_ENV=development
   FLASK_DEBUG=1
   ```

5. **Initialize the database**
   ```bash
   python init_db.py
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5000`

### Docker Setup

1. **Build and run with Docker**
   ```bash
   docker build -t book-management-api .
   docker run -p 5000:5000 book-management-api
   ```

2. **Or use Docker Compose (recommended)**
   Create a `docker-compose.yml` file:
   ```yaml
   version: '3.8'
   services:
     web:
       build: .
       ports:
         - "5000:5000"
       environment:
         - FLASK_ENV=development
         - FLASK_DEBUG=1
         - DATABASE_URL=sqlite:///app.db
       volumes:
         - .:/app
   ```
   
   Run:
   ```bash
   docker-compose up --build
   ```

## ⚙️ Configuration

The application supports multiple environments through configuration classes:

- **Development**: SQLite database, debug mode enabled
- **Testing**: In-memory SQLite for tests
- **Production**: PostgreSQL database, debug mode disabled

Environment variables:
- `SECRET_KEY`: Secret key for JWT token generation
- `DATABASE_URL`: Database connection string
- `FLASK_ENV`: Environment mode (development/production)
- `FLASK_DEBUG`: Enable/disable debug mode

## 🔌 API Endpoints

### Authentication
- `POST /api/register` - Register a new user
- `POST /api/login` - Login and get JWT token
- `GET /api/profile` - Get user profile (authenticated)

### Books
- `GET /api/books` - Get all books
- `POST /api/books` - Add a new book
- `GET /api/books/{id}` - Get book by ID
- `PUT /api/books/{id}` - Update book by ID
- `DELETE /api/books/{id}` - Delete book by ID

### Reviews
- `POST /api/books/{id}/reviews` - Add review to a book
- `GET /api/books/{id}/reviews` - Get all reviews for a book
- `GET /api/books/{id}/summary` - Get book summary with average rating

### Recommendations
- `GET /api/recommendations` - Get book recommendations

### Documentation
- `GET /api/docs` - Interactive Swagger UI documentation

## 📝 Usage Examples

### 1. User Registration
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### 2. User Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```
Response:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 3. Add a Book (Authentication Required)
```bash
curl -X POST http://localhost:5000/api/books \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "genre": "Fiction",
    "year_published": 1925
  }'
```

### 4. Get All Books
```bash
curl -X GET http://localhost:5000/api/books \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 5. Add a Review
```bash
curl -X POST http://localhost:5000/api/books/1/reviews \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "user_id": 1,
    "review_text": "Excellent book!",
    "rating": 5
  }'
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=app

# Run specific test file
pytest tests/test_book_routes.py
```

Test coverage includes:
- User authentication
- Book CRUD operations
- Review functionality
- Error handling
- Authorization checks

## 📚 Documentation

### Interactive API Documentation
Visit `http://localhost:5000/api/docs` when the server is running to access the interactive Swagger UI documentation.

### Authentication
All endpoints except `/register` and `/login` require authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer YOUR_TOKEN_HERE
```

### Error Responses
The API returns appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `409`: Conflict

## 🚀 Deployment

### Production Deployment with Docker

1. **Build production image**
   ```bash
   docker build -t book-management-api:prod .
   ```

2. **Run with production environment**
   ```bash
   docker run -p 5000:5000 \
     -e FLASK_ENV=production \
     -e FLASK_DEBUG=0 \
     -e DATABASE_URL=postgresql://user:password@localhost/dbname \
     -e SECRET_KEY=your_production_secret_key \
     book-management-api:prod
   ```

### Environment Variables for Production
```env
SECRET_KEY=your_super_secret_production_key
DATABASE_URL=postgresql://username:password@host:port/database
FLASK_ENV=production
FLASK_DEBUG=0
```

## 🛠️ Development

### Adding New Features

1. **Models**: Add new database models in `app/models.py`
2. **Routes**: Create new route files in `app/routes/`
3. **Services**: Add business logic in `app/services/`
4. **Tests**: Write tests in `tests/`
5. **Documentation**: Update `app/static/swagger.json`

### Database Migrations

```bash
# Initialize migrations (first time only)
flask db init

# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Prasanna Raja**

## 🆘 Support

For support and questions, please open an issue in the GitHub repository.

---

**Happy Coding! 🚀**
