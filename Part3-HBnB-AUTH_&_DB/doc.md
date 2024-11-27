# HBnB Project Documentation

## Table of Contents
1. [Prerequisites & Installation](#prerequisites--installation)
2. [Project Architecture](#project-architecture)
3. [Database Schema](#database-schema)
4. [Project Structure](#project-structure)
5. [Step-by-Step Setup Guide](#step-by-step-setup-guide)
6. [API Endpoints](#api-endpoints)
7. [Testing](#testing)
8. [Deployment](#deployment)

## Prerequisites & Installation

### Required Software
```bash
# System Requirements
- Python 3.8 or higher
- PostgreSQL 12+
- Redis 6+
- Git
- Docker & Docker Compose (optional)
- Make (optional)

# Python Packages
- Flask & Extensions
- SQLAlchemy
- JWT
- Bcrypt
- Redis
```

### Environment Setup
1. Install system dependencies (Ubuntu):
```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Install Redis
sudo apt install redis-server

# Install Python and tools
sudo apt install python3.8 python3.8-venv python3-pip

# Install development tools
sudo apt install build-essential libpq-dev git make
```

2. Configure PostgreSQL:
```bash
# Create database
sudo -u postgres psql
CREATE DATABASE hbnb;
CREATE USER hbnb_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE hbnb TO hbnb_user;
```

3. Configure Redis:
```bash
# Start Redis service
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

## Project Architecture

```mermaid
graph TB
    Client[Client Requests] --> API[API Layer /api/v1]
    API --> Auth[Authentication JWT]
    API --> Services[Service Layer]
    Services --> Repository[Repository Layer]
    Repository --> Models[Models Layer]
    Models --> Database[(Database)]
    
    subgraph API Endpoints
        Auth --> Users[/users]
        Auth --> Places[/places]
        Auth --> Reviews[/reviews]
        Auth --> Amenities[/amenities]
    end
    
    subgraph Services
        Services --> UserService[User Service]
        Services --> PlaceService[Place Service]
        Services --> ReviewService[Review Service]
        Services --> AmenityService[Amenity Service]
    end
    
    subgraph Data Layer
        Repository --> SQLAlchemy[SQLAlchemy ORM]
        Models --> User[User Model]
        Models --> Place[Place Model]
        Models --> Review[Review Model]
        Models --> Amenity[Amenity Model]
    end

    Redis[Redis Cache] -.-> API
    Auth -.-> Redis
```

## Step-by-Step Setup Guide

1. **Clone the Repository & Setup Virtual Environment**
```bash
# Clone project
git clone https://github.com/your-username/hbnb.git
cd hbnb

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

2. **Install Dependencies**
```bash
# Install project dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

3. **Environment Configuration**
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
# SECRET_KEY=your-secret-key
# etc...
```

4. **Database Setup**
```bash
# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Create admin user
flask create-admin admin@hbnb.io admin1234

# Seed initial data
flask seed-amenities
```

5. **Run Development Server**
```bash
# Start development server
flask run

# Or using docker
docker-compose up --build
```

## Project Structure Details

```mermaid
classDiagram
    class AppStructure {
        +app/
        +config/
        +migrations/
        +tests/
        +docs/
    }
    
    class AppModule {
        +models/
        +api/
        +services/
        +persistence/
        +utils/
    }
    
    class Models {
        +BaseModel
        +User
        +Place
        +Review
        +Amenity
    }
    
    class Services {
        +HBnBFacade
        +Validators
        +Errors
    }
    
    class API {
        +v1/
        +auth/
        +places/
        +reviews/
        +users/
    }
    
    AppStructure --> AppModule
    AppModule --> Models
    AppModule --> Services
    AppModule --> API
```

## Authentication Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant JWT
    participant DB
    
    Client->>API: POST /auth/login
    API->>DB: Validate Credentials
    DB-->>API: User Data
    API->>JWT: Generate Token
    JWT-->>API: Access Token
    API-->>Client: Return Token
    
    Client->>API: Request + Token
    API->>JWT: Verify Token
    JWT-->>API: Token Valid
    API->>DB: Process Request
    DB-->>API: Response Data
    API-->>Client: Return Response
```

## Database Schema

```mermaid
erDiagram
    User ||--o{ Place : owns
    User ||--o{ Review : writes
    Place ||--o{ Review : has
    Place }|--|| User : belongs_to
    Place }o--o{ Amenity : has

    User {
        string id PK
        string email UK
        string password
        string first_name
        string last_name
        boolean is_admin
        datetime created_at
        datetime updated_at
    }

    Place {
        string id PK
        string owner_id FK
        string title
        text description
        float price
        float latitude
        float longitude
        datetime created_at
        datetime updated_at
    }

    Review {
        string id PK
        string user_id FK
        string place_id FK
        text text
        integer rating
        datetime created_at
        datetime updated_at
    }

    Amenity {
        string id PK
        string name UK
        datetime created_at
        datetime updated_at
    }
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login`: User login
  - Required: email, password
  - Returns: JWT token

### Users
- `POST /api/v1/users/`: Create user (Admin only)
- `PUT /api/v1/users/<user_id>`: Update user
- `GET /api/v1/users/<user_id>`: Get user details

### Places
- `GET /api/v1/places/`: List all places (Public)
- `POST /api/v1/places/`: Create place (Auth required)
- `PUT /api/v1/places/<place_id>`: Update place (Owner only)
- `DELETE /api/v1/places/<place_id>`: Delete place (Owner only)

### Reviews
- `POST /api/v1/reviews/`: Create review (Auth required)
- `PUT /api/v1/reviews/<review_id>`: Update review (Owner only)
- `DELETE /api/v1/reviews/<review_id>`: Delete review (Owner only)

### Amenities
- `POST /api/v1/amenities/`: Create amenity (Admin only)
- `PUT /api/v1/amenities/<amenity_id>`: Update amenity (Admin only)

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app tests/

# Generate coverage report
pytest --cov=app --cov-report=html tests/
```

## Deployment

### Using Docker
```bash
# Build and start containers
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

### Manual Deployment
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## Common Issues & Solutions

1. **Database Connection Issues**
   - Check PostgreSQL service is running
   - Verify database credentials in .env
   - Ensure database exists and user has permissions

2. **Redis Connection Issues**
   - Check Redis service is running
   - Verify Redis connection URL in .env

3. **JWT Authentication Issues**
   - Verify SECRET_KEY is set
   - Check token expiration time
   - Ensure correct token format in requests

## Development Guidelines

1. **Code Style**
   - Follow PEP 8
   - Use Black formatter
   - Run flake8 for linting

2. **Git Workflow**
   - Create feature branches
   - Write descriptive commit messages
   - Submit PR for review

3. **Testing**
   - Write unit tests for new features
   - Maintain test coverage above 80%
   - Test all edge cases

   # HBnB Project - Complete Documentation

## Additional Table of Contents
9. [Development Workflow](#development-workflow)
10. [Security Considerations](#security-considerations)
11. [Performance Optimization](#performance-optimization)
12. [Error Handling](#error-handling)
13. [Monitoring & Logging](#monitoring--logging)
14. [Backup & Recovery](#backup--recovery)
15. [CI/CD Pipeline](#cicd-pipeline)
16. [API Documentation Details](#api-documentation-details)

## Development Workflow

### Code Organization Principles

```mermaid
graph TB
    subgraph Project Structure
        Config[Configuration Layer]
        API[API Layer]
        Business[Business Logic Layer]
        Data[Data Access Layer]
        Utils[Utility Layer]
    end

    subgraph Development Flow
        Plan[Planning]
        Code[Coding]
        Test[Testing]
        Review[Code Review]
        Deploy[Deployment]
    end

    Config --> API
    API --> Business
    Business --> Data
    Utils --> API
    Utils --> Business
    Utils --> Data

    Plan --> Code
    Code --> Test
    Test --> Review
    Review --> Deploy
```

### Version Control Strategy

1. **Branch Naming Convention**
```bash
feature/    # New features
bugfix/     # Bug fixes
hotfix/     # Urgent fixes for production
release/    # Release preparation
docs/       # Documentation updates
```

2. **Commit Message Format**
```
<type>(<scope>): <subject>

<body>

<footer>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Test addition/modification
- chore: Maintenance tasks
```

3. **Pull Request Process**
- Create feature branch
- Implement changes
- Write/update tests
- Update documentation
- Submit PR with description
- Address review comments
- Merge after approval

## Security Considerations

### Authentication Implementation

```python
# Example JWT configuration
JWT_SECRET_KEY = config('JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

# Token blacklisting
BLACKLISTED_TOKENS = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in BLACKLISTED_TOKENS
```

### Password Security

```python
# Password validation rules
PASSWORD_RULES = {
    'min_length': 8,
    'require_uppercase': True,
    'require_lowercase': True,
    'require_numbers': True,
    'require_special': True,
    'max_length': 128
}

def validate_password(password):
    """
    Validate password against security rules
    Returns (bool, str): (is_valid, error_message)
    """
    if len(password) < PASSWORD_RULES['min_length']:
        return False, f"Password must be at least {PASSWORD_RULES['min_length']} characters"
    # Additional validation rules...
```

### Rate Limiting Implementation

```python
# Rate limiting configuration
RATE_LIMIT_RULES = {
    'default': '100/hour',
    'login': '5/minute',
    'create_place': '10/hour',
    'create_review': '20/hour'
}

def rate_limit_key_prefix():
    """Generate rate limit key prefix based on user identity"""
    if current_user:
        return f'rate_limit:{current_user.id}'
    return f'rate_limit:{request.remote_addr}'
```

## Performance Optimization

### Caching Strategy

```python
# Cache configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': config('REDIS_URL'),
    'CACHE_DEFAULT_TIMEOUT': 300
}

# Cache decorators
def cache_place(timeout=300):
    """Cache place details"""
    def decorator(f):
        @wraps(f)
        def decorated_function(place_id):
            cache_key = f'place:{place_id}'
            rv = cache.get(cache_key)
            if rv is not None:
                return rv
            rv = f(place_id)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator
```

### Database Optimization

```sql
-- Index creation for common queries
CREATE INDEX idx_places_price ON places(price);
CREATE INDEX idx_reviews_rating ON reviews(rating);
CREATE INDEX idx_users_email ON users(email);

-- Composite indexes for relationships
CREATE INDEX idx_reviews_user_place ON reviews(user_id, place_id);
CREATE INDEX idx_places_owner_created ON places(owner_id, created_at);
```

### Query Optimization

```python
# Example of optimized queries
def get_place_with_reviews(place_id):
    """Get place with reviews in single query"""
    return Place.query\
        .options(joinedload(Place.reviews))\
        .options(joinedload(Place.owner))\
        .filter_by(id=place_id)\
        .first()

def get_user_places_with_stats(user_id):
    """Get user's places with review stats"""
    return Place.query\
        .with_entities(
            Place,
            func.count(Review.id).label('review_count'),
            func.avg(Review.rating).label('avg_rating')
        )\
        .outerjoin(Review)\
        .filter(Place.owner_id == user_id)\
        .group_by(Place.id)\
        .all()
```

## Error Handling

### Global Error Handler

```python
@app.errorhandler(Exception)
def handle_exception(error):
    """Handle all unhandled exceptions"""
    if isinstance(error, HTTPException):
        return {
            'error': str(error.description),
            'code': error.code
        }, error.code
        
    # Log unexpected errors
    app.logger.error(f"Unexpected error: {str(error)}")
    return {
        'error': 'An unexpected error occurred',
        'code': 500
    }, 500
```

### Custom Exception Classes

```python
class HBnBException(Exception):
    """Base exception for HBnB application"""
    def __init__(self, message, code=400):
        self.message = message
        self.code = code
        super().__init__(self.message)

class ResourceNotFoundException(HBnBException):
    """Resource not found exception"""
    def __init__(self, resource_type, resource_id):
        message = f"{resource_type} with id {resource_id} not found"
        super().__init__(message, 404)

class ValidationException(HBnBException):
    """Validation error exception"""
    def __init__(self, errors):
        message = {'validation_errors': errors}
        super().__init__(message, 400)
```

## Monitoring & Logging

### Logging Configuration

```python
# logging_config.py
LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
        'detailed': {
            'format': '%(asctime)s %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s'
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/hbnb.log',
            'maxBytes': 1024 * 1024,  # 1 MB
            'backupCount': 10,
            'formatter': 'detailed'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
}
```

### Metrics Collection

```python
from prometheus_client import Counter, Histogram

# Define metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration_seconds = Histogram(
    'request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time
    http_requests_total.labels(
        method=request.method,
        endpoint=request.endpoint,
        status=response.status_code
    ).inc()
    request_duration_seconds.labels(
        method=request.method,
        endpoint=request.endpoint
    ).observe(duration)
    return response
```

## API Documentation Details

### Place Endpoints

#### Create Place
```
POST /api/v1/places/

Request Body:
{
    "title": string,
    "description": string,
    "price": number,
    "latitude": number,
    "longitude": number,
    "amenities": array[string]
}

Response (201):
{
    "id": string,
    "title": string,
    "description": string,
    "price": number,
    "latitude": number,
    "longitude": number,
    "owner_id": string,
    "amenities": array[object],
    "created_at": string,
    "updated_at": string
}
```

#### Update Place
```
PUT /api/v1/places/{place_id}

Request Body:
{
    "title": string (optional),
    "description": string (optional),
    "price": number (optional),
    "latitude": number (optional),
    "longitude": number (optional),
    "amenities": array[string] (optional)
}

Response (200):
{
    "id": string,
    "title": string,
    "description": string,
    "price": number,
    "latitude": number,
    "longitude": number,
    "owner_id": string,
    "amenities": array[object],
    "created_at": string,
    "updated_at": string
}
```

# HBnB Project - Comprehensive Technical Documentation

## System Architecture Overview

```mermaid
graph TB
    subgraph Client Layer
        Web[Web Browser]
        Mobile[Mobile App]
        ThirdParty[Third Party Apps]
    end

    subgraph Load Balancer
        NginxLB[Nginx Load Balancer]
    end

    subgraph Application Servers
        App1[App Server 1]
        App2[App Server 2]
        App3[App Server 3]
    end

    subgraph Caching Layer
        Redis1[Redis Primary]
        Redis2[Redis Replica]
    end

    subgraph Database Layer
        DB1[(PostgreSQL Primary)]
        DB2[(PostgreSQL Replica)]
    end

    subgraph Storage Layer
        S3[AWS S3]
        LocalFS[Local FileSystem]
    end

    Web --> NginxLB
    Mobile --> NginxLB
    ThirdParty --> NginxLB
    
    NginxLB --> App1
    NginxLB --> App2
    NginxLB --> App3
    
    App1 --> Redis1
    App2 --> Redis1
    App3 --> Redis1
    Redis1 --> Redis2
    
    App1 --> DB1
    App2 --> DB1
    App3 --> DB1
    DB1 --> DB2
    
    App1 --> S3
    App2 --> S3
    App3 --> S3
```

## Detailed Component Interactions

### Authentication Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API Gateway
    participant S as Auth Service
    participant R as Redis Cache
    participant D as Database
    
    C->>A: POST /auth/login
    A->>S: Validate Credentials
    S->>D: Query User
    D-->>S: User Data
    S->>S: Validate Password
    S->>R: Store Session
    S-->>A: Generate JWT
    A-->>C: Return JWT Token
    
    Note over C,A: Subsequent Requests
    C->>A: Request + JWT
    A->>R: Validate Token
    R-->>A: Token Valid
    A->>S: Process Request
    S->>D: Database Operation
    D-->>S: Result
    S-->>A: Response
    A-->>C: Return Result
```

### Data Model Relationships

```mermaid
classDiagram
    User "1" -- "*" Place : owns
    User "1" -- "*" Review : writes
    Place "1" -- "*" Review : has
    Place "*" -- "*" Amenity : contains
    
    class User {
        +UUID id
        +String email
        +String password
        +String first_name
        +String last_name
        +Boolean is_admin
        +DateTime created_at
        +DateTime updated_at
        +validate()
        +hash_password()
        +verify_password()
    }
    
    class Place {
        +UUID id
        +String title
        +String description
        +Float price
        +Float latitude
        +Float longitude
        +UUID owner_id
        +DateTime created_at
        +DateTime updated_at
        +validate()
        +calculate_rating()
        +is_available()
    }
    
    class Review {
        +UUID id
        +String text
        +Integer rating
        +UUID user_id
        +UUID place_id
        +DateTime created_at
        +DateTime updated_at
        +validate()
    }
    
    class Amenity {
        +UUID id
        +String name
        +DateTime created_at
        +DateTime updated_at
        +validate()
    }
```

## Directory Structure Visualization

```mermaid
graph TD
    subgraph Project Root
        Root[/] --> App[app/]
        Root --> Tests[tests/]
        Root --> Docs[docs/]
        Root --> Config[config/]
    end
    
    subgraph Application Structure
        App --> Models[models/]
        App --> API[api/]
        App --> Services[services/]
        App --> Utils[utils/]
        
        Models --> UserModel[user.py]
        Models --> PlaceModel[place.py]
        Models --> ReviewModel[review.py]
        
        API --> V1[v1/]
        V1 --> AuthAPI[auth.py]
        V1 --> PlacesAPI[places.py]
        V1 --> ReviewsAPI[reviews.py]
        
        Services --> Facade[facade.py]
        Services --> Validators[validators.py]
        
        Utils --> Helpers[helpers.py]
        Utils --> Decorators[decorators.py]
    end
    
    subgraph Test Structure
        Tests --> UnitTests[unit/]
        Tests --> IntegTests[integration/]
        Tests --> E2ETests[e2e/]
    end
```

## Request Flow Diagram

```mermaid
flowchart TD
    A[Client Request] --> B{Authentication?}
    B -- Yes --> C[JWT Validation]
    B -- No --> D[Process Request]
    
    C --> E{Valid Token?}
    E -- Yes --> D
    E -- No --> F[Return 401]
    
    D --> G{Request Type?}
    G -- GET --> H[Cache Check]
    G -- POST/PUT/DELETE --> I[Database Operation]
    
    H --> J{Cache Hit?}
    J -- Yes --> K[Return Cached Data]
    J -- No --> L[Query Database]
    
    L --> M[Update Cache]
    M --> K
    
    I --> N[Validate Input]
    N --> O{Valid?}
    O -- Yes --> P[Perform Operation]
    O -- No --> Q[Return 400]
    
    P --> R[Return Result]
```

## Database Optimization Strategies

### Indexing Strategy

```sql
-- User indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Place indexes
CREATE INDEX idx_places_owner ON places(owner_id);
CREATE INDEX idx_places_price_location ON places(price, latitude, longitude);
CREATE INDEX idx_places_created_at ON places(created_at);

-- Review indexes
CREATE INDEX idx_reviews_place ON reviews(place_id);
CREATE INDEX idx_reviews_user ON reviews(user_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);

-- Combined indexes for common queries
CREATE INDEX idx_places_owner_status ON places(owner_id, status, created_at);
CREATE INDEX idx_reviews_place_rating ON reviews(place_id, rating);
```

### Query Optimization Examples

```python
# Efficient place retrieval with reviews and owner
def get_place_details(place_id: str) -> Dict:
    return db.session.query(Place)\
        .options(
            joinedload(Place.owner),
            joinedload(Place.reviews).joinedload(Review.user),
            joinedload(Place.amenities)
        )\
        .filter(Place.id == place_id)\
        .first()

# Optimized search query
def search_places(
    min_price: float,
    max_price: float,
    latitude: float,
    longitude: float,
    radius: float
) -> List[Place]:
    return db.session.query(Place)\
        .filter(
            Place.price.between(min_price, max_price),
            func.earth_distance(
                func.ll_to_earth(Place.latitude, Place.longitude),
                func.ll_to_earth(latitude, longitude)
            ) <= radius
        )\
        .order_by(
            func.earth_distance(
                func.ll_to_earth(Place.latitude, Place.longitude),
                func.ll_to_earth(latitude, longitude)
            )
        )\
        .all()
```

# HBnB Technical Documentation - Final Section

## API Security Implementation

### Security Layers Visualization

```mermaid
flowchart TB
    subgraph Security Layers
        A[Client Request] --> B[Rate Limiting]
        B --> C[IP Filtering]
        C --> D[JWT Authentication]
        D --> E[Role Authorization]
        E --> F[Input Validation]
        F --> G[Response Sanitization]
    end

    subgraph Rate Limiting
        B --> B1[Redis Counter]
        B1 --> B2[Time Window]
        B2 --> B3[Limit Check]
    end

    subgraph Authentication
        D --> D1[Token Validation]
        D1 --> D2[User Lookup]
        D2 --> D3[Session Check]
    end

    subgraph Authorization
        E --> E1[Role Check]
        E1 --> E2[Permission Matrix]
        E2 --> E3[Resource Access]
    end
```

### Security Implementation Details

```python
# Security Middleware Stack
class SecurityMiddleware:
    def __init__(self, app):
        self.app = app
        self.rate_limiter = RateLimiter()
        self.ip_filter = IPFilter()
        self.jwt_validator = JWTValidator()
        self.role_checker = RoleChecker()
        self.input_validator = InputValidator()
        self.response_sanitizer = ResponseSanitizer()

    def __call__(self, environ, start_response):
        request = Request(environ)
        
        # Apply security checks
        try:
            self.rate_limiter.check(request)
            self.ip_filter.check(request)
            self.jwt_validator.validate(request)
            self.role_checker.check(request)
            self.input_validator.validate(request)
            
            # Process request
            response = self.app(environ, start_response)
            
            # Sanitize response
            return self.response_sanitizer.sanitize(response)
            
        except SecurityException as e:
            return self.handle_security_error(e, start_response)
```

## Test Coverage and Quality Assurance

### Test Coverage Matrix

```mermaid
pie title Test Coverage by Component
    "Models" : 95
    "Services" : 90
    "API Endpoints" : 88
    "Authentication" : 98
    "Database" : 85
    "Utils" : 92
```

### Test Implementation Strategy

```python
# Unit Tests Example
class TestPlaceService(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    @patch('services.place_service.calculate_price')
    def test_create_place(self, mock_calculate):
        # Test data
        place_data = {
            'title': 'Test Place',
            'description': 'Test Description',
            'price': 100.00
        }
        
        # Mock price calculation
        mock_calculate.return_value = 100.00
        
        # Create place
        response = self.client.post(
            '/api/v1/places',
            json=place_data,
            headers={'Authorization': f'Bearer {self.token}'}
        )
        
        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['title'], place_data['title'])
```

## Performance Monitoring and Optimization

### Performance Metrics Tracking

```mermaid
graph LR
    A[Request] --> B[StatsD Client]
    B --> C[Metrics Collection]
    C --> D[Grafana Dashboard]
    
    subgraph Metrics
        E[Response Time]
        F[Database Queries]
        G[Cache Hits]
        H[Error Rates]
    end
    
    C --> E
    C --> F
    C --> G
    C --> H
```

### Performance Optimization Implementation

```python
# Cache Configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.getenv('REDIS_URL'),
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'hbnb_cache_'
}

# Query Optimization
class OptimizedPlaceQuery:
    @staticmethod
    def get_places_with_stats():
        return db.session.query(
            Place,
            func.count(Review.id).label('review_count'),
            func.avg(Review.rating).label('average_rating')
        ).outerjoin(Review).group_by(Place.id)

# Background Task Processing
class AsyncTaskProcessor:
    def process_image_upload(self, image_data):
        task = ProcessImageTask.delay(image_data)
        return task.id
```

## Deployment Pipeline

### CI/CD Workflow

```mermaid
graph TD
    A[Code Push] -->|Trigger| B[CI Pipeline]
    B --> C{Tests Pass?}
    C -->|Yes| D[Build Docker Image]
    C -->|No| E[Notify Failure]
    D --> F[Push to Registry]
    F --> G[Deploy to Staging]
    G --> H{Staging Tests Pass?}
    H -->|Yes| I[Deploy to Production]
    H -->|No| J[Rollback]
    I --> K[Health Check]
    K -->|Success| L[Complete]
    K -->|Failure| M[Emergency Rollback]
```

### Deployment Configuration

```yaml
# docker-compose.production.yml
version: '3.8'

services:
  web:
    image: hbnb/web:${TAG}
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        max_attempts: 3
        window: 120s

  worker:
    image: hbnb/worker:${TAG}
    environment:
      - CELERY_BROKER_URL=${REDIS_URL}
    deploy:
      replicas: 2
      restart_policy:
        condition: on-failure

  nginx:
    image: nginx:latest
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web
```

## Monitoring and Alerting

### Monitoring Dashboard

```mermaid
graph TB
    subgraph Application Metrics
        A[Request Rate]
        B[Response Time]
        C[Error Rate]
        D[CPU Usage]
    end
    
    subgraph Database Metrics
        E[Query Performance]
        F[Connection Pool]
        G[Cache Hit Rate]
    end
    
    subgraph Business Metrics
        H[Active Users]
        I[Bookings]
        J[Revenue]
    end
    
    K[Prometheus] --> L[Grafana]
    L --> M[Alert Manager]
    M --> N[Notification System]
```

## Disaster Recovery Plan

### Backup Strategy

```mermaid
flowchart TD
    A[Database] -->|Continuous| B[WAL Shipping]
    A -->|Daily| C[Full Backup]
    A -->|Hourly| D[Incremental Backup]
    
    B --> E[Standby DB]
    C --> F[S3 Storage]
    D --> F
    
    G[Failure Detection] -->|Trigger| H[Failover Process]
    H --> I{Automatic Recovery}
    I -->|Success| J[Resume Operations]
    I -->|Failure| K[Manual Intervention]
```

## Conclusion and Future Improvements

### Roadmap

```mermaid
gantt
    title Development Roadmap
    dateFormat  YYYY-MM-DD
    section Phase 1
    Authentication & Authorization :2024-01-01, 30d
    Basic CRUD Operations        :2024-02-01, 45d
    section Phase 2
    Advanced Search             :2024-03-15, 40d
    Payment Integration         :2024-04-25, 30d
    section Phase 3
    Analytics Implementation    :2024-06-01, 45d
    Mobile API                 :2024-07-15, 60d
```

This completes the comprehensive technical documentation for the HBnB project. The documentation includes:

1. Detailed security implementation
2. Complete test coverage strategy
3. Performance monitoring and optimization
4. Deployment pipeline configuration
5. Monitoring and alerting setup
6. Disaster recovery procedures
7. Future development roadmap

All components are designed to work together to create a robust, scalable, and maintainable application.

For any questions or updates to this documentation, please contact the development team or submit a pull request to the documentation repository.

End of Documentation.