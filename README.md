
# e-commerce-shop

Fully working shop app. It's focused only on backend to polish it as much as possible.






## Features

It has several usefull features like:
- advanced modern login by JWT
- wishlist
- advanced filtering to serach for products
- pagination
- autimatic mail sender after:
  - create user
  - create order
  - reminder about payment
## Technologies


Technologies used:
- Django
- Django Rest Framework
- PostgreSQL
- Docker
- Celery
- Redis
- Pre-commit
- Pytest
- Django Filters
## Requirements


All necessary requirements are placed in requirements.txt file.
## Environment Variables

To run this project, you will not need to add any environment variables. They all are stored in env dir. The are publicated only to help with local run.

`SECRET_KEY_VALUE` Django secret key

`SERVER_IP` server ip at which it will be running

`PORT` server port at which it will be running

`CACHE_TTL` time in secunds. Describe how long data will be stored in cache

`CORS_API` for proper cross origi. I reccomend `locahost` because of traditions.

### Email

Email Variables depends on your email service. The project was tested for `Outlook` service. If you want use other service you may need even to change more than the values.
Needed Variables:

- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST`
- `EMAIL_HOST_PASSWORD`

## Run Locally

### First Time

Clone the project

```bash
  git clone https://github.com/Bombozaur666/e-commerce-shop
```

For Proper initialization I recommend set envimental variable `in django.env`
```
  FIRST_USE='True'
```
Thanks to that Django will wait for proper initialization of Postgres database.

Build Containers

```bash
  docker-compose build
```

Then to prepare databse for our data:

```bash
  docker-compose run django python manage.py migrate
```

All needed and custom migrations are in project.

After succesfull you should change variable to:

```bash
  FIRST_USE='False'
```

To save your time.
### Every Other Time


To start server

```bash
  docker-compose up
```

To start server in detached mode
```bash
  docker-compose up -d
```

To start server and get acces to all logs generated ONLY by a Django

```bash
  docker-compose run --service-ports django
```


## PRE-COMMIT

Pre-commit is simple code formater with github hooks. Configured utilities:
- autoromating to PEP8
- Python standarts
- max line lenght
- end of file
- yaml checker
- trailing whitespace

It will check files before every commit and block if it will not fulfill standarts.

### Instalation

You have to install it in your local machine so I strongly reccomend useing virtual enviroment.

```bash
python -m venv env
env\Scripts\activate
```

If you want install all packeges (for example for your IDE autocompletion):

```bash
pip install -r ./requirements.txt
```

If you want install only pre-commit:

```bash
pip install pre-commit==3.5.0
```

After installation you need to install pre-commit to local git:

```bash
pre-commit install
```

### Run

To run filechecker:

```bash
pre-commit run --all-files
```
### Update

To update versions of hooks:

```bash
pre-commit autoupdate
```

## Running Tests

To run tests, run the following command

```bash
  docker-compose run --service-ports django pytest -rP
```


## Authentication

For Authentication I used JWT

### Header

```
  Authorization: Bearer xxx
```

### Get Token

```html
  POST /account/token/
```

| Body Key | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. Username for login |
| `password` | `string` | **Required**. User password for login|

Response:

```json
{
    "refresh": "...",
    "access": "..."
}
```
`Acces` key is used for veryfication in other views

### Refresh Token

```html
  POST /account/token/refresh/
```

| Body Key | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `refresh` | `string` | **Required**. Acces token to refresh |

Response:

```json
{
    "access": "..."
}
```

`Acces` key is new token that will last 24h. After that user will need login in again.
## API Reference

The most configurable API
### Create User

All users created by api will belong to `Client` group. To create user with `Seller` group you need to make them manually with superuser account.

```http
  POST /orders/create/
```

| Body Key | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**|
| `password` | `string` | **Required** |
| `first_name` | `string` | **Required** |
| `last_name` | `string` | **Required** |
| `email` | `string` | **Required** |

Example:

```json
{
    "username": "userJoe",
    "password": "LongPasswordIsSave78",
    "first_name": "Joe",
    "last_name": "Doe",
    "email": "joe.doe@gmail.com"
}
```


Response:

```json
{
    "username": "userJoe",
    "email": "joe.doe@gmail.com"
}
```



### Create Order

```http
  POST /orders/create/
```

| Body Key | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `address` | `string` | **Required**|
| `city` | `string` | **Required** |
| `postal_code` | `string` | **Required** |
| `order` | `array` | **Required**  Array of products and quantity|

Example:

```json
{
    "address": "userJoe",
    "city": "LongPasswordIsSave78",
    "postal_code": "Joe",
    "order": [
      {
        "product": 1, "quantity": 3
      },
      {
        "product": 2, "quantity": 4
      }
    ]
}
```


Response:

```json
{
    "receivable": 18.0,
    "date of payment": "2023-11-07"
}
```


### Orders Statistics

Most popular products in specific time period. Query number limited by Seller request.

```http
  GET /orders/statistics/
```

| Params | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `date_start` | `string` | Starting date for filter |
| `date_end` | `string` | Ending date for filter |
| `limit` | `string` | How many best products |


Example:

```http
  GET orders/statistics/?date_start=2023-10-10&date_end=2023-12-12&limit=1
```


Response:

```json
[
    {
        "product__name": "marchewka",
        "the_amount": 8
    }
]
```


### Product List

```http
  POST /products/list/
```

| Params | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | Exact name.|
| `name__contains` | `string` | Name contains. |
| `description` | `string` | Exact description. |
| `description__contains` | `array` | Description contains. |
| `price` | `string` | Price exact. |
| `price__gte` | `array` | Price greater then or equal. |
| `price__lte` | `string` |Price less then or equal. |


Example:

```json
    GET products/list/?name=ziemniak&description__contains=ziemniak&price__lte=2.5
```
