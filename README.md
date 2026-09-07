# Rider API

A Django REST Framework API for managing and retrieving rider information. The API supports creating, retrieving, updating, deleting, and filtering rider records.

## Technologies Used

* Python
* Django
* Django REST Framework
* SQLite
* Postman

## Rider Model

The `Rider` model stores rider personal, payout, document, account, and delivery-related information.

### Fields

| Field                    | Type        | Description                                       |
| ------------------------ | ----------- | ------------------------------------------------- |
| id                       | Integer     | Automatically generated rider ID                  |
| name                     | String      | Rider name                                        |
| phone                    | String      | Rider phone number                                |
| address                  | Text        | Rider address                                     |
| rider_type               | Enum        | Salary-based or Per-order                         |
| assigned_store           | String      | Store assigned to the rider                       |
| assigned_zone            | String      | Zone assigned to the rider                        |
| payout_method            | Enum        | UPI or Bank Account                               |
| upi_id                   | String      | Rider UPI ID                                      |
| bank_account_number      | String      | Bank account number                               |
| ifsc_code                | String      | Bank IFSC code                                    |
| account_holder_name      | String      | Bank account holder name                          |
| driving_license_number   | String      | Driving license number                            |
| driving_license_document | URL         | Driving license document URL                      |
| aadhaar_number           | String      | Aadhaar number                                    |
| aadhaar_document         | URL         | Aadhaar document URL                              |
| vehicle_rc_number        | String      | Vehicle RC number                                 |
| vehicle_rc_document      | URL         | Vehicle RC document URL                           |
| account_status           | Enum        | Active or Inactive                                |
| activate_immediately     | Boolean     | Whether the rider should be activated immediately |
| online_status            | Enum        | Online, Offline, On Break, or On Delivery         |
| current_order            | String/Null | Current order assigned to the rider               |
| cash_in_hand             | Decimal     | Current cash held by the rider                    |
| has_undeposited_cash     | Boolean     | Indicates whether the rider has undeposited cash  |
| created_at               | DateTime    | Automatically generated creation date and time    |

## Choice Fields

### Rider Type

* Salary-based
* Per-order

### Payout Method

* UPI
* Bank Account

### Account Status

* Active
* Inactive

### Online Status

* Online
* Offline
* On Break
* On Delivery

## API Endpoints

### List Riders

```http
GET /rider/
```

Returns a list of riders.

### Create Rider

```http
POST /rider/
```

Creates a new rider.

### Retrieve Rider

```http
GET /rider/<id>/
```

Returns details of a specific rider.

### Update Rider

```http
PUT /rider/<id>/
```

Updates an existing rider.

### Delete Rider

```http
DELETE /rider/<id>/
```

Deletes a rider.

## Filtering

The rider list API supports filtering rider records based on available query parameters.

Example:

```http
GET /rider/?name=John
```

Multiple filters can be combined using query parameters.

## API Testing

The APIs can be tested using Postman.

Example base URL:

```text
http://127.0.0.1:8000
```

## Running the Project

Clone the repository and navigate to the project directory.

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```
