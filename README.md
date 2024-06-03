# Grocery Management Tool

## Overview
The Grocery Management Tool is designed to help users manage their groceries, generate grocery lists, and find recipes based on the ingredients they have. It includes family integration with a team lead and up to 5 family members, OTP-based authentication for secure access, and nutritional information for recipes.

## Features
- **OTP-based Authentication**: Secure login and registration using One-Time Passwords (OTP) sent via email or SMS.
- **Family Integration**: Team lead can invite family members to join the household account using a unique team code.
- **Inventory Management**: Track groceries with notifications for items nearing expiration.
- **Recipe Integration**: Find recipes based on available ingredients and view nutritional information.
- **Grocery List Generation**: Create grocery lists based on selected recipes.

## Tech Stack
- **Backend**: Django
- **Database**: PostgreSQL
- **API Integrations**: Twilio (SMS OTP), SendGrid (Email OTP), Edamam/Spoonacular (Recipes)

## Setup Instructions
### Prerequisites
- Python 3.8+
- Django 3.2+
- PostgreSQL or MongoDB
- Twilio Account (for SMS OTP)
- SendGrid Account (for Email OTP)
- Edamam/Spoonacular API keys

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/weshy007/grocery-management-tool.git

2. Set up PostgreSQL
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'grocery_management',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

3. Install dependencies:
- Create an environment with `pipenv shell` then install depandancies with `pipenv sync`.
4. Configure settings:
- Rename `example.env` to `.env` and update the configuration variables accordingly.

## Usage
1. Run migrations: `make migrate`. 
2. Create a superuser for accessing the admin panel: `python manage.py createsuperuser`
3. Start the development server: `make serve`
4. Access the application in your web browser at `http://localhost:8000`.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Create a new pull request.

## License
This project is licensed under the [MIT License](LICENSE).

## Contact
For any inquiries or suggestions, please contact [Waithaka Waweru](https://twitter.com/ItsWeshy) on X.