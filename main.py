from services.delivery_cost import delivery_order_price


def main():
    venue_slug="home-assignment-venue-helsinki"
    cart_value=1000
    user_lat=60.17094
    user_lon=24.93087
    
    endpoint_response, SUCCESS, message_code = delivery_order_price(venue_slug,cart_value,user_lat,user_lon)
    print(SUCCESS,endpoint_response, message_code)


if __name__ == "__main__":
    main()
