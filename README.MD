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
   git clone <repository-url>
   cd <repository-directory>
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

## Future Improvements
- Add support for additional pricing models and rules.
- Implement caching for API responses to improve performance.
- Extend input validation for edge cases.
- Add rate-limiting for API requests.
- Write integration tests for end-to-end scenarios.