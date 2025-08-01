# Django REST API Template

A modern, production-ready Django REST API template with authentication, email verification, and comprehensive development tools. Built with Django REST Framework, this template provides a solid foundation for building scalable web applications.

## 🚀 Features

### Authentication & Security
- **Custom User Model** - Email-based authentication with UUID support
- **JWT Authentication** - Secure token-based authentication with cookies
- **Email Verification** - Complete email verification flow with beautiful HTML templates
- **Password Reset** - Secure password reset with email verification
- **Verified Users Only** - Login restricted to verified users only
- **CSRF Protection** - Built-in CSRF protection with configurable settings

### API & Development
- **Django REST Framework** - Full REST API support with browsable interface
- **Browsable API** - Interactive web interface for testing APIs
- **Django Debug Toolbar** - Comprehensive debugging and profiling tools
- **CORS Support** - Cross-origin resource sharing configuration
- **Import/Export** - Data import/export functionality for admin

### Email System
- **Beautiful HTML Templates** - Professional email templates for verification and password reset
- **SMTP Configuration** - Configurable email backend with TLS support
- **Template Customization** - Easy-to-customize email templates
- **Generic Design** - Templates work for any application

### Database & Storage
- **Multi-Environment Support** - SQLite for development, PostgreSQL for production
- **Media File Handling** - User upload support with proper file management
- **Static Files** - Optimized static file serving with WhiteNoise

## 📋 Prerequisites

- Python 3.8+
- pip
- Git

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Alien501/django-drf-template.git
cd django-template
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
Create a `.env` file in the root directory:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
JWT_KEY=your-jwt-key-here
ENVIRONMENT=development
COOKIE_DOMAIN=localhost

# Database (Production)
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host

# Email Configuration
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password

# Frontend URLs
VERIFICATION_URL=http://localhost:3000/verify-email
PASSWORD_RESET_URL=http://localhost:3000/reset-password
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run the Server
```bash
python manage.py runserver
```

## 🔧 Configuration

### Environment Variables

The project uses `python-decouple` for environment variable management. Key variables:

- `ENVIRONMENT`: Set to `development` for debug mode, `production` for production
- `SECRET_KEY`: Django secret key
- `JWT_KEY`: JWT signing key
- `EMAIL_HOST_USER`: SMTP email address
- `EMAIL_HOST_PASSWORD`: SMTP password
- `VERIFICATION_URL`: Frontend verification page URL
- `PASSWORD_RESET_URL`: Frontend password reset page URL

### Database Configuration

**Development (SQLite):**
- Automatically configured when `DEBUG=True`

**Production (PostgreSQL):**
- Configure `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` in `.env`

### Email Configuration

The template uses SMTP for email delivery. Configure your email provider settings:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zeptomail.in'  # Change to your provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
```

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123",
  "password_confirm": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Login
```http
POST /api/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123"
}
```

#### Verify Email
```http
GET /api/verify/?email=user@example.com&token=ABC123
```

#### Resend Verification
```http
GET /api/resend_token/?email=user@example.com
```

#### Forgot Password
```http
POST /api/forgot_password/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "newpassword123"
}
```

#### Reset Password
```http
GET /api/forgot_password/?email=user@example.com&token=ABC123
```

#### Get Profile
```http
GET /api/profile/
Authorization: Bearer <jwt-token>
```

#### Logout
```http
POST /api/logout/
Authorization: Bearer <jwt-token>
```

### Testing APIs

Visit `http://localhost:8000/api/` to see the browsable API interface where you can test all endpoints interactively.

## 🎨 Email Templates

### Customization

The project includes beautiful HTML email templates:

- **Verification Email**: `templates/email/verification_email.html`
- **Password Reset**: `templates/email/forgot_password_email.html`

### Template Variables

Customize templates by modifying these variables in `authentication/models.py`:

```python
context = {
    "app_name": "Your App Name",
    "user_name": self.first_name,
    "contact_email": "support@yourapp.com",
    "contact_phone": "+1-234-567-8900",
    "social_media": "@yourapp"
}
```

## 🔍 Development Tools

### Django Debug Toolbar

When `DEBUG=True`, the debug toolbar provides:
- SQL query analysis
- Request/response inspection
- Template rendering details
- Performance profiling
- Cache analysis

Access at: `http://localhost:8000/__debug__/`

### API Testing

- **Browsable API**: Interactive web interface at each endpoint
- **Admin Interface**: `http://localhost:8000/admin/`
- **API Root**: `http://localhost:8000/api/`

## 🚀 Deployment

### Production Checklist

1. **Environment Variables**
   ```env
   ENVIRONMENT=production
   SECRET_KEY=your-production-secret-key
   JWT_KEY=your-production-jwt-key
   ```

2. **Database**
   - Configure PostgreSQL connection
   - Run migrations: `python manage.py migrate`

3. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

4. **Security**
   - Set `DEBUG=False`
   - Configure `ALLOWED_HOSTS`
   - Use HTTPS in production
   - Set secure cookie settings

5. **Email**
   - Configure production SMTP settings
   - Update verification URLs to production domain

## 📁 Project Structure

```
django-template/
├── AppName/                 # Main project settings
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI application
├── authentication/         # Authentication app
│   ├── models.py          # User model and related models
│   ├── views.py           # API views
│   ├── serializers.py     # DRF serializers
│   ├── urls.py           # Authentication URLs
│   └── authentication.py  # Custom authentication
├── templates/             # Email templates
│   └── email/
│       ├── verification_email.html
│       └── forgot_password_email.html
├── utils/                 # Utility functions
│   └── send_mail.py      # Email sending utilities
├── static/               # Static files
├── media/                # User uploaded files
├── requirements.txt      # Python dependencies
├── manage.py            # Django management script
└── README.md           # This file
```

## 🛡️ Security Features

- **JWT Authentication**: Secure token-based authentication
- **Email Verification**: Prevents unauthorized account creation
- **Password Validation**: Django's built-in password validators
- **CSRF Protection**: Cross-site request forgery protection
- **CORS Configuration**: Controlled cross-origin requests
- **Secure Cookies**: HttpOnly and SameSite cookie settings

## 🔧 Customization

### Adding New Apps

1. Create new app: `python manage.py startapp your_app`
2. Add to `INSTALLED_APPS` in `settings.py`
3. Create models, views, serializers
4. Add URLs to main `urls.py`

### Custom User Fields

Modify the User model in `authentication/models.py`:

```python
class User(AbstractUser):
    # Add your custom fields here
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
```

### Email Template Styling

Modify the CSS in email templates:
- `templates/email/verification_email.html`
- `templates/email/forgot_password_email.html`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Django documentation](https://docs.djangoproject.com/)
2. Review the [Django REST Framework docs](https://www.django-rest-framework.org/)
3. Open an issue in the repository

## 🎯 Roadmap

- [ ] Add user profile management
- [ ] Implement social authentication
- [ ] Add API rate limiting
- [ ] Create comprehensive test suite
- [ ] Add Docker support
- [ ] Implement caching layer
- [ ] Add API documentation with drf-spectacular

---

**Built with ❤️ using Django and Django REST Framework** 