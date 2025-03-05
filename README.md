# Django Solana Wallet Authentication

A Django project that implements authentication using Solana wallet signatures, with PostgreSQL and TimescaleDB integration.

## Features

- Solana wallet-based authentication
- PostgreSQL with TimescaleDB for data storage
- Docker setup for database
- Challenge-response authentication flow
- JWT token-based session management

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Solana wallet (e.g., Phantom, Solflare)

## Setup

1. Clone the repository and create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the PostgreSQL/TimescaleDB container:

```bash
docker-compose up -d
```

4. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```

## Authentication Flow

1. Request a challenge:

```bash
POST /auth/request-challenge/
{
    "wallet_address": "your_solana_wallet_address"
}
```

2. Sign the challenge with your Solana wallet and verify:

```bash
POST /auth/verify-signature/
{
    "wallet_address": "your_solana_wallet_address",
    "signature": "signed_challenge_signature",
    "challenge_string": "challenge_string_from_step_1"
}
```

3. Logout:

```bash
POST /auth/logout/
```

## API Endpoints

- `POST /auth/request-challenge/`: Request a challenge string for authentication
- `POST /auth/verify-signature/`: Verify the signed challenge and authenticate
- `POST /auth/logout/`: Log out the current user

## Database Configuration

The project uses PostgreSQL with TimescaleDB extension. The database configuration can be modified in `settings.py` and `docker-compose.yml`.

Default database settings:

- Database: solana_auth_db
- User: postgres
- Password: postgres
- Host: localhost
- Port: 5432

## Security Considerations

- Always use HTTPS in production
- Keep your Solana wallet private keys secure
- Regularly rotate challenge strings
- Monitor for unusual authentication patterns
- Consider rate limiting for challenge requests

## Development

To run tests:

```bash
python manage.py test
```

## License

MIT License
