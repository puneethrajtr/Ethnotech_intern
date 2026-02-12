"""
Models for Taxi Booking Application.
Contains Taxi and Booking data classes.
"""


class Booking:
    """Represents a booking record."""
    
    def __init__(self, booking_id: int, customer_id: int, from_point: str, 
                 to_point: str, pickup_time: int, drop_time: int, amount: float):
        """
        Initialize a Booking instance.
        
        Args:
            booking_id: Unique identifier for the booking
            customer_id: Customer identifier
            from_point: Pickup location (A-F)
            to_point: Drop location (A-F)
            pickup_time: Pickup time in hours
            drop_time: Drop time in hours
            amount: Fare amount in Rs.
        """
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.from_point = from_point
        self.to_point = to_point
        self.pickup_time = pickup_time
        self.drop_time = drop_time
        self.amount = amount
    
    def to_dict(self) -> dict:
        """Convert booking to dictionary for API response."""
        return {
            "booking_id": self.booking_id,
            "customer_id": self.customer_id,
            "from": self.from_point,
            "to": self.to_point,
            "pickup_time": self.pickup_time,
            "drop_time": self.drop_time,
            "amount": self.amount
        }


class Taxi:
    """Represents a Taxi with its state and bookings."""
    
    def __init__(self, taxi_id: int, initial_location: str = 'A'):
        """
        Initialize a Taxi instance.
        
        Args:
            taxi_id: Unique identifier for the taxi
            initial_location: Starting location (default 'A')
        """
        self.taxi_id = taxi_id
        self.current_location = initial_location
        self.free_time = 0  # Time when taxi becomes available
        self.total_earnings = 0.0
        self.bookings: list[Booking] = []
    
    def is_available(self, pickup_time: int) -> bool:
        """
        Check if taxi is available at the given pickup time.
        
        Args:
            pickup_time: Requested pickup time in hours
            
        Returns:
            True if taxi is free by pickup_time, False otherwise
        """
        return self.free_time <= pickup_time
    
    def add_booking(self, booking: Booking, new_location: str):
        """
        Add a booking to this taxi and update its state.
        
        Args:
            booking: The Booking instance to add
            new_location: The drop location (taxi's new current location)
        """
        self.bookings.append(booking)
        self.total_earnings += booking.amount
        self.current_location = new_location
        self.free_time = booking.drop_time
    
    def to_dict(self) -> dict:
        """Convert taxi to dictionary for API response."""
        return {
            "taxi_id": self.taxi_id,
            "total_earnings": self.total_earnings,
            "bookings": [booking.to_dict() for booking in self.bookings]
        }
