# Delivery Order Price Calculator (DOPC)

## Overview
The **Delivery Order Price Calculator (DOPC)** is a robust backend service designed to calculate the total price and a detailed price breakdown for delivery orders. This service integrates seamlessly with the Wolt Home Assignment API to fetch real-time venue data, ensuring accurate and dynamic calculations. 

Built using **FastAPI**, this project demonstrates high-quality engineering principles with a focus on correctness, maintainability, and efficiency.

---

## Features
- **Dynamic Pricing**: Calculates the delivery fee, small order surcharge, and total price based on real-time venue and user data.
- **Distance Calculation**: Supports straight-line distance calculation (simple or haversine method).
- **Configurable Logic**: Delivery fee calculation supports various algorithms (O(n), O(log n), O(1)).
- **Error Handling**: Robust input validation and descriptive error messages.
- **Scalable Architecture**: Modular and maintainable codebase built with clean architecture principles.

---

## Technology Stack
- **Programming Language**: Python 3.12.6
- **Framework**: FastAPI
- **HTTP Client**: Requests
- **Configuration**: YAML
- **Testing**: Unittest

---

## Installation

### Prerequisites
- **Python**: Version 3.12.6.
- **pip**: Version 24.2.
- Internet connection to fetch data from the Wolt Home Assignment API.

### Steps
1. **Clone the Repository**
```bash
   git clone https://github.com/ShahinVI/wolt_challenge.git
   cd wolt_challenge
```

2. **Create a Virtual Environment**
```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
    pip install --upgrade pip
    pip install -r requirements.txt
```

4. **Run the Application**
```bash
    uvicorn app:app --reload
```

5. **Access the API Documentation**
    - Swagger UI: http://127.0.0.1:8000/docs
    - ReDoc: http://127.0.0.1:8000/redoc

---

## API Endpoints

### 1. Calculate Delivery Order Price
- **Endpoint**: `/api/v1/delivery-order-price`
- **Method**: `GET`
- **Description**: Calculates the total price and breakdown for a delivery order.
- **Query Parameters**:
  - `venue_slug` (*string*): The unique identifier of the venue.
  - `cart_value` (*integer*): Total value of items in the shopping cart (in cents).
  - `user_lat` (*float*): Latitude of the user's location.
  - `user_lon` (*float*): Longitude of the user's location.
- **Response Example**
```json
    {
    "total_price": 1190,
    "small_order_surcharge": 0,
    "cart_value": 1000,
    "delivery": {
        "fee": 190,
        "distance": 177
    }
    }

```

### 2. Health Check
- **Endpoint**: `/`
- **Method**: `GET`
- **Description**: Verifies that the service is running.
- **Response Example**:
```json
  {
    "message": "Service is running!"
  }
```

---

## Configuration
The application uses a YAML configuration file (`config/config.yaml`) for the following settings:

- **Logging**: Customize log levels and format.
- **API Endpoints**: URLs for fetching venue data.
- **Constants**: Definitions for success/failure codes, calculation methods, etc.

---

## Testing
This project uses **Unittest** for testing. To run the tests:
```bash
    python main_test.py
```

---

## Project Structure
```bash
.
├── app.py                  # Main application entry point
├── config/
│   └── config.yaml         # Application configuration
├── services/               # Core service logic
│   ├── api_client.py       # API request handler
│   ├── delivery_cost.py    # Delivery price calculation
│   ├── distance_calculator.py # Distance calculation methods
│   ├── venue_processor.py  # Venue data processing
├── utils/                  # Utility modules
│   ├── config_loader.py    # Configuration loader
│   ├── validator.py        # Input validation
├── tests/                  # Unit tests
│   ├── test_delivery_cost.py # delivery_cost testing 
│   ├── test_distance_calculator.py # distance_calculator testing
│   ├── test_venue_processor.py # venue_processor testing
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation

```

---

## **Example Usage**
Here’s an example of a request to calculate the delivery price:
```bash
curl "http://127.0.0.1:8000/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1500&user_lat=60.17094&user_lon=24.93087"
```

Example response:
```json
{
    "total_price": 1690,
    "small_order_surcharge": 0,
    "cart_value": 1500,
    "delivery": {
        "fee": 190,
        "distance": 123
    }
}
```

---

## Configuration (config/config.yaml)
The `config.yaml` file contains all the key settings and parameters needed to configure the application. Below is a detailed breakdown of its sections:

---

### 1. Logging
Configures the logging behavior of the application.

**Keys:**
- `level`: The logging level (e.g., INFO, DEBUG, ERROR).
- `format`: The format of log messages, including timestamp, log level, and message.

Example:
```yaml
logging:
  level: INFO
  format: '%(asctime)s - %(levelname)s - %(message)s'
```

---

### 2. Constants
Defines globally used constants for success/failure codes and algorithm options for delivery cost calculations.

**Keys:**
- `SUCCESS`: HTTP status code for successful responses (default: 200).
- `FAILURE`: HTTP status code for error responses (default: 400).
- `SIMPLE`: Option for simple distance calculation using Pythagorean theorem.
- `HAVERSINE`: Option for precise distance calculation using the haversine formula.
- `O_1`, `O_n`, `O_Log_n`: Different algorithmic approaches for delivery cost calculation based on distance ranges.

Example:
```yaml
constants:
  SUCCESS: 200
  FAILURE: 400
  SIMPLE: 0
  HAVERSINE: 1
  O_1: "O_1"
  O_n: "O_n"
  O_Log_n: "O_Log_n"
```

---

### 3. Countries API
Contains API endpoints for fetching venue-related data (static and dynamic) based on the country.

**Keys:**
- Each country is identified by a two-letter code (e.g., DE for Germany, FI for Finland).
  - `static`: The endpoint to fetch static venue data (e.g., coordinates).
  - `dynamic`: The endpoint to fetch dynamic venue data (e.g., delivery fees and distance ranges).

Example:
```yaml
countries_api:
  DE:
    static: "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/home-assignment-venue-berlin/static"
    dynamic: "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/home-assignment-venue-berlin/dynamic"
  FI:
    static: "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/home-assignment-venue-helsinki/static"
    dynamic: "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/home-assignment-venue-helsinki/dynamic"
```

---

### 4. City Acronyms
Maps city names to their respective country codes for easier lookup.

**Keys:**
- City names in lowercase (e.g., helsinki, berlin) with their corresponding country codes.

Example:
```yaml
cities_acronym:
  helsinki: "FI"
  berlin: "DE"
  stockholm: "SE"
  tokyo: "JP"
```

---

### How the Configuration is Used
**Loading Configuration:**  
The application loads the `config.yaml` file using the `load_config` function defined in `config_loader.py`. This function parses the YAML file and provides access to its contents as a Python dictionary.

**Logging Configuration:**  
The logging settings are applied globally during application startup:
```python
logging.basicConfig(
  level=getattr(logging, LOGGING_CONFIG["level"]),
  format=LOGGING_CONFIG["format"],
  handlers=[logging.StreamHandler()]
)
```

**Dynamic API Selection:**  
Depending on the venue's country (extracted from the `venue_slug`), the appropriate static and dynamic API endpoints are fetched from the `countries_api` section.

**Constants:**  
Constants like `SUCCESS`, `FAILURE`, and distance calculation options are used across the application to standardize behavior.

---

## Future Improvements
- Add support for additional pricing models and rules.
- Implement caching for API responses to improve performance.
- Extend input validation for edge cases.
- Add rate-limiting for API requests.
- Write integration tests for end-to-end scenarios.