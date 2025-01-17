from fastapi import FastAPI, HTTPException, Query
from typing import Dict, Any
from services.delivery_cost import delivery_order_price
from utils.config_loader import SUCCESS, FAILURE

# Create the FastAPI app
app = FastAPI(title="Delivery Order Price Calculator", version="1.0.0")

@app.get("/api/v1/delivery-order-price", response_model=Dict[str, Any])
async def get_delivery_order_price(
    venue_slug: str = Query(..., description="The unique identifier for the venue"),
    cart_value: int = Query(..., description="The total value of the items in the shopping cart"),
    user_lat: float = Query(..., description="The latitude of the user's location"),
    user_lon: float = Query(..., description="The longitude of the user's location")
):
    """
    Calculates the total price and provides a detailed breakdown for a delivery order.

    This endpoint considers the distance between the user and the venue to calculate the delivery fee.
    Depending on the distance, additional delivery costs are applied. If the distance exceeds
    the deliverable range, the API responds with a `400 Bad Request` and an explanatory message.

    ### Features:
    - **Input Parameters**:
    - `venue_slug`: The unique identifier for the venue.
    - `cart_value`: The total value of items in the shopping cart (in cents).
    - `user_lat`: Latitude of the user's location.
    - `user_lon`: Longitude of the user's location.

    - **Functionality**:
    1. Fetches venue details from the Home Assignment API (both static and dynamic data).
    2. Parses the static data to extract:
        - Venue coordinates.
    3. Parses the dynamic data to extract:
        - Minimum order value to avoid small order surcharge.
        - Base price for delivery.
        - Additional delivery costs based on distance ranges.
    4. Calculates the delivery distance between the user and the venue.
    5. Returns a detailed response including:
        - Total price.
        - Breakdown of delivery costs.
        - Distance between the user and the venue.

    - **Error Handling**:
        - If the distance is too large, returns `400 Bad Request` with an explanatory message.
        - If there is missing data or any other type of error with the data processing,  returns `400 Bad Request` with an explanatory message.
        - For any other errors, returns `500 Internal Server Error` with an error message.
        - Logs provide additional error details for debugging purposes.

    ### Response Structure:
    - `total_price` (int): The total calculated price.
    - `small_order_surcharge` (int): Additional surcharge for small orders.
    - `cart_value` (int): Original cart value.
    - `delivery` (object):
    - `fee` (int): Delivery fee.
    - `distance` (int): Distance between the user and the venue (in meters).
    """
    try:
        # Call the delivery order price function
        response, status, message = delivery_order_price(venue_slug, cart_value, user_lat, user_lon)

        if status == SUCCESS:
            return response
        else:
            raise HTTPException(status_code=FAILURE, detail=message)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# Health check endpoint
@app.get("/")
async def health_check():
    return {"message": "Service is running!"}
