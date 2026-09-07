# Rider API

A Django REST Framework API for managing and retrieving rider information. The API supports creating, retrieving, updating, deleting, filtering rider records, rider statistics, rider filter options, and managing rider rate configurations.

## Technologies Used

* Python

* Django

* Django REST Framework

* SQLite

* Postman

## Rider Model

The `Rider` model stores rider personal, payout, document, account, and delivery-related information.

### Fields

| Field | Type | Description |
|---|---|---|
| id | Integer | Automatically generated rider ID |
| name | String | Rider name |
| phone | String | Rider phone number |
| address | Text | Rider address |
| rider_type | Enum | Salary-based or Per-order |
| assigned_store | String | Store assigned to the rider |
| assigned_zone | String | Zone assigned to the rider |
| payout_method | Enum | UPI or Bank Account |
| upi_id | String | Rider UPI ID |
| bank_account_number | String | Bank account number |
| ifsc_code | String | Bank IFSC code |
| account_holder_name | String | Bank account holder name |
| driving_license_number | String | Driving license number |
| driving_license_document | URL | Driving license document URL |
| aadhaar_number | String | Aadhaar number |
| aadhaar_document | URL | Aadhaar document URL |
| vehicle_rc_number | String | Vehicle RC number |
| vehicle_rc_document | URL | Vehicle RC document URL |
| account_status | Enum | Active or Inactive |
| activate_immediately | Boolean | Whether the rider should be activated immediately |
| online_status | Enum | Online, Offline, On Break, or On Delivery |
| current_order | String/Null | Current order assigned to the rider |
| cash_in_hand | Decimal | Current cash held by the rider |
| has_undeposited_cash | Boolean | Indicates whether the rider has undeposited cash |
| created_at | DateTime | Automatically generated creation date and time |

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

### Rider APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/rider/` | Get all riders |
| POST | `/rider/` | Create a new rider |
| GET | `/rider/<id>/` | Get rider details by ID |
| PATCH | `/rider/<id>/` | Update rider details |
| DELETE | `/rider/<id>/` | Delete a rider |
| GET | `/rider/stats/` | Get rider statistics |
| GET | `/rider/filter-options/` | Get available rider filter options |

### Rider Rate APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/rates/` | Create a new rider rate |
| PATCH | `/rates/<id>/` | Update an existing rider rate |

## Rider API Details

### Create Rider

Creates a new rider record.

**Method:**

```http
POST /rider/