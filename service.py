"""
Service layer for Taxi Booking Application.
Contains business logic for taxi allocation and fare calculation.
"""

from models import Taxi, Booking


class TaxiService:
    """Service class to manage taxi operations and bookings."""
    
    # Valid pickup/drop points
    VALID_POINTS = {'A', 'B', 'C', 'D', 'E', 'F'}
    
    # Distance between adjacent points in km
    DISTANCE_PER_POINT = 15
    
    # Travel time between adjacent points in hours
    TIME_PER_POINT = 1
    
    # Fare constants
    BASE_FARE = 100  # Rs. for first 5 km
    BASE_KM = 5
    RATE_PER_KM = 10  # Rs. per km after 5 km
    
    def __init__(self, num_taxis: int = 4):
        """
        Initialize the TaxiService with given number of taxis.
        
        Args:
            num_taxis: Number of taxis to initialize (default 4)
        """
        self.taxis: list[Taxi] = []
        self.booking_counter = 0
        self.initialize_taxis(num_taxis)
    
    def initialize_taxis(self, num_taxis: int):
        """
        Initialize all taxis at starting point A.
        
        Args:
            num_taxis: Number of taxis to create
        """
        self.taxis = [Taxi(taxi_id=i + 1, initial_location='A') for i in range(num_taxis)]
    
    @staticmethod
    def calculate_distance(pickup: str, drop: str) -> int:
        """
        Calculate distance between two points.
        
        Args:
            pickup: Pickup point (A-F)
            drop: Drop point (A-F)
            
        Returns:
            Distance in km
        """
        return abs(ord(drop) - ord(pickup)) * TaxiService.DISTANCE_PER_POINT
    
    @staticmethod
    def calculate_travel_time(pickup: str, drop: str) -> int:
        """
        Calculate travel time between two points.
        
        Args:
            pickup: Pickup point (A-F)
            drop: Drop point (A-F)
            
        Returns:
            Travel time in hours
        """
        return abs(ord(drop) - ord(pickup)) * TaxiService.TIME_PER_POINT
    
    def calculate_fare(self, distance: int) -> float:
        """
        Calculate fare based on distance.
        
        Fare structure:
        - Rs.100 for first 5 km
        - Rs.10 per km after 5 km
        
        Args:
            distance: Distance in km
            
        Returns:
            Fare amount in Rs.
        """
        if distance <= self.BASE_KM:
            return self.BASE_FARE
        return self.BASE_FARE + (distance - self.BASE_KM) * self.RATE_PER_KM
    
    def find_nearest_taxi(self, pickup_point: str, pickup_time: int) -> Taxi | None:
        """
        Find the most suitable taxi for booking.
        
        Priority:
        1. Taxi available at pickup location
        2. Nearest available taxi
        3. If tied, taxi with lowest earnings
        
        Args:
            pickup_point: Requested pickup location
            pickup_time: Requested pickup time
            
        Returns:
            Best available Taxi or None if no taxi available
        """
        available_taxis = []
        
        for taxi in self.taxis:
            if taxi.is_available(pickup_time):
                # Calculate distance from taxi's current location to pickup point
                distance_to_pickup = abs(ord(pickup_point) - ord(taxi.current_location))
                available_taxis.append((taxi, distance_to_pickup))
        
        if not available_taxis:
            return None
        
        # Sort by: distance to pickup (ascending), then by total earnings (ascending)
        available_taxis.sort(key=lambda x: (x[1], x[0].total_earnings))
        
        return available_taxis[0][0]
    
    def book_taxi(self, customer_id: int, pickup_point: str, drop_point: str, 
                  pickup_time: int) -> dict:
        """
        Book a taxi for the customer.
        
        Args:
            customer_id: Customer identifier
            pickup_point: Pickup location (A-F)
            drop_point: Drop location (A-F)
            pickup_time: Pickup time in hours
            
        Returns:
            Dictionary with booking status and details
        """
        # Validate pickup and drop points
        if pickup_point not in self.VALID_POINTS:
            return {
                "status": "error",
                "message": f"Invalid pickup point: {pickup_point}. Valid points are A-F."
            }
        
        if drop_point not in self.VALID_POINTS:
            return {
                "status": "error",
                "message": f"Invalid drop point: {drop_point}. Valid points are A-F."
            }
        
        if pickup_point == drop_point:
            return {
                "status": "error",
                "message": "Pickup and drop points cannot be the same."
            }
        
        if pickup_time < 0:
            return {
                "status": "error",
                "message": "Pickup time cannot be negative."
            }
        
        # Find nearest available taxi
        taxi = self.find_nearest_taxi(pickup_point, pickup_time)
        
        if taxi is None:
            return {
                "status": "rejected",
                "message": "No taxi available at the requested time."
            }
        
        # Calculate trip details
        distance = self.calculate_distance(pickup_point, drop_point)
        travel_time = self.calculate_travel_time(pickup_point, drop_point)
        drop_time = pickup_time + travel_time
        fare = self.calculate_fare(distance)
        
        # Create booking
        self.booking_counter += 1
        booking = Booking(
            booking_id=self.booking_counter,
            customer_id=customer_id,
            from_point=pickup_point,
            to_point=drop_point,
            pickup_time=pickup_time,
            drop_time=drop_time,
            amount=fare
        )
        
        # Assign booking to taxi
        taxi.add_booking(booking, drop_point)
        
        return {
            "status": "success",
            "booking_id": self.booking_counter,
            "taxi_id": taxi.taxi_id,
            "pickup_point": pickup_point,
            "drop_point": drop_point,
            "pickup_time": pickup_time,
            "drop_time": drop_time,
            "amount": fare
        }
    
    def get_taxi_details(self) -> list[dict]:
        """
        Get details of all taxis.
        
        Returns:
            List of taxi dictionaries with earnings and bookings
        """
        return [taxi.to_dict() for taxi in self.taxis]
