"""
Flask REST API for Taxi Booking Application.
Provides endpoints for booking taxis and viewing taxi details.
"""

from flask import Flask, request, jsonify, render_template
from service import TaxiService

# Initialize Flask app
app = Flask(__name__)

# Initialize TaxiService with default 4 taxis
taxi_service = TaxiService(num_taxis=4)


@app.route('/')
def index():
    """Serve the main UI page."""
    return render_template('index.html')


@app.route('/book', methods=['POST'])
def book_taxi():
    """
    Book a taxi.
    
    Request JSON:
    {
        "customer_id": int,
        "pickup_point": str (A-F),
        "drop_point": str (A-F),
        "pickup_time": int (hours)
    }
    
    Response JSON (success):
    {
        "status": "success",
        "taxi_id": int,
        "drop_time": int,
        "amount": float
    }
    
    Response JSON (error/rejected):
    {
        "status": "error" or "rejected",
        "message": str
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['customer_id', 'pickup_point', 'drop_point', 'pickup_time']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "status": "error",
                    "message": f"Missing required field: {field}"
                }), 400
        
        # Extract booking details
        customer_id = data['customer_id']
        pickup_point = data['pickup_point'].upper()
        drop_point = data['drop_point'].upper()
        pickup_time = data['pickup_time']
        
        # Validate data types
        if not isinstance(customer_id, int):
            return jsonify({
                "status": "error",
                "message": "customer_id must be an integer"
            }), 400
        
        if not isinstance(pickup_time, int):
            return jsonify({
                "status": "error",
                "message": "pickup_time must be an integer"
            }), 400
        
        # Book the taxi
        result = taxi_service.book_taxi(
            customer_id=customer_id,
            pickup_point=pickup_point,
            drop_point=drop_point,
            pickup_time=pickup_time
        )
        
        # Return appropriate HTTP status code
        if result['status'] == 'success':
            return jsonify(result), 200
        elif result['status'] == 'rejected':
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/taxis', methods=['GET'])
def get_taxis():
    """
    Get details of all taxis.
    
    Response JSON:
    [
        {
            "taxi_id": int,
            "total_earnings": float,
            "bookings": [
                {
                    "booking_id": int,
                    "customer_id": int,
                    "from": str,
                    "to": str,
                    "pickup_time": int,
                    "drop_time": int,
                    "amount": float
                }
            ]
        }
    ]
    """
    try:
        taxis = taxi_service.get_taxi_details()
        return jsonify(taxis), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/reset', methods=['POST'])
def reset_taxis():
    """
    Reset all taxis to initial state.
    Optional: Pass num_taxis in request body to change taxi count.
    
    Request JSON (optional):
    {
        "num_taxis": int (default 4)
    }
    
    Response JSON:
    {
        "status": "success",
        "message": str
    }
    """
    try:
        global taxi_service
        data = request.get_json() or {}
        num_taxis = data.get('num_taxis', 4)
        
        if not isinstance(num_taxis, int) or num_taxis < 1:
            return jsonify({
                "status": "error",
                "message": "num_taxis must be a positive integer"
            }), 400
        
        taxi_service = TaxiService(num_taxis=num_taxis)
        
        return jsonify({
            "status": "success",
            "message": f"System reset with {num_taxis} taxis"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)
