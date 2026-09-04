# Rider API

A simple Django REST Framework API for managing and retrieving rider information.

## Features

* Get a list of riders
* Search riders by name
* Filter riders by vehicle number
* Pagination support
* Returns total rider count

## Rider Model

The Rider model contains the following fields:

* Name
* Email
* Phone
* Vehicle Number
* Created At

## API Endpoint

### Get Riders

```text
GET /rider/
```

### Example Request

```text
/rider/?page=1&page_size=10
```

### Search by Name

```text
/rider/?search=John
```

### Filter by Vehicle Number

```text
/rider/?vehicle_number=KA01
```

## Example Response

```json
{
    "status": true,
    "data": [],
    "page": 1,
    "page_size": 10,
    "total_count": 0,
    "message": "Riders retrieved successfully"
}
```

## Technologies Used

* Python
* Django
* Django REST Framework

## Installation

Clone the repository:

```bash
git clone https://github.com/Anjum-aforro/rider.git
```

Go to the project directory:

```bash
cd rider
```

Create and activate a virtual environment, then install the required dependencies.

Run migrations:

```bash
python manage.py migrate
```

Start the server:

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/rider/
```
