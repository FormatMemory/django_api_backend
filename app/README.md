
##Django Project Setup

Install required packages:
```
pip3 install -r requirements/local.txt
```

Initialize database:
```
python3 manage.py makemigrations
python3 manage.py migrate
```

Run Server:
```
python3 manage.py runserver 127.0.0.1:8000
```

## Fixtures

To load in sample data for all tables at once:
```
bash scripts/load_sample_data.sh
```

For Windows users:
```
python manage.py loaddata v1\accounts\fixtures\user.json
```

This will create an initial superuser account with the following credentials:
```
admin@email.com
pass1234
```

## Authentication

To login, send a POST request to `/login` with the data:
* email
* password

On success, user information and API token will be returned:
```json
{
  "id": 1,
  "email": "admin@email.com",
  "first_name": "David",
  "last_name": "Ding",
  "profile": {
    "id": 2,
    "image": "/media/bucky_256.png",
    "user": 1
  },
  "role": "administrator",
  "token": "cb810da7d03b85335ea18babf3536fbf2a31ccdf"
}
```

All subsequent API requests must include this token in the HTTP header for user identification.
Header key will be `Authorization` with value of 'Token' followed by a single space and then token string:
```
Authorization: Token 653dw61b4c39bd195282310c82fe3c3b1e7f746b
```

## API Documentation

To view API documentation, run development server and visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
