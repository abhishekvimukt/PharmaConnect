# MR Optimizer DB

A Django REST API for Medical Representative (MR) management system.

## Setup Instructions

1. Clone the repository:
```bash
git clone <your-repository-url>
cd mr_optimizer_db
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
- Copy `.env.example` to `.env`
- Update the values with your actual credentials
- Never commit the `.env` file!

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## API Documentation

The API uses JWT authentication. To access protected endpoints:

1. Get your access token:
```bash
POST /auth/jwt/create/
{
    "username": "your_username",
    "password": "your_password"
}
```

2. Use the token in your requests:
```bash
Authorization: Bearer your_access_token
```

### Available Endpoints

- Authentication:
  - POST /auth/jwt/create/ - Get JWT tokens
  - POST /auth/users/ - Register new user
  - POST /auth/jwt/refresh/ - Refresh JWT token

- MR Operations:
  - GET /api/mrs/ - List all MRs
  - GET /api/mrs/my_profile/ - Get logged-in MR's profile
  - GET /api/mrs/{id}/dashboard/ - Get MR's dashboard data

For detailed API documentation, visit `/api/docs/` when the server is running.

## Frontend Development

For frontend developers:

1. All API endpoints are prefixed with `/api/`
2. Use the provided TypeScript interfaces (if available)
3. Implement proper error handling
4. Store JWT tokens securely
5. Implement token refresh mechanism

## Security Notes

1. Never commit `.env` file
2. Always use environment variables for sensitive data
3. Keep `DEBUG=False` in production
4. Update `ALLOWED_HOSTS` in production
5. Use strong, unique passwords for all credentials 