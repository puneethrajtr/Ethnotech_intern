"""
Calculator Routes Module

This module defines all API endpoints for calculator operations.
Each endpoint receives input from the frontend and delegates computation to the service layer.
"""

from flask import Blueprint, request, jsonify
from backend.services.calculator_service import calculator

# Create blueprint for calculator routes
calculator_bp = Blueprint('calculator', __name__, url_prefix='/api/calculator')


def make_response(success: bool, data=None, error: str = None):
    """Helper function to create consistent API responses."""
    response = {"success": success}
    if data is not None:
        response["result"] = data
    if error:
        response["error"] = error
    return jsonify(response)


def get_number(key: str, data: dict, required: bool = True):
    """Extract and validate a number from request data."""
    value = data.get(key)
    if value is None:
        if required:
            raise ValueError(f"Missing required parameter: {key}")
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid number for parameter: {key}")


# ==================== Basic Arithmetic Routes ====================

@calculator_bp.route('/add', methods=['POST'])
def add():
    """Add two numbers."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        b = get_number('b', data)
        result = calculator.add(a, b)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/subtract', methods=['POST'])
def subtract():
    """Subtract two numbers."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        b = get_number('b', data)
        result = calculator.subtract(a, b)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/multiply', methods=['POST'])
def multiply():
    """Multiply two numbers."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        b = get_number('b', data)
        result = calculator.multiply(a, b)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/divide', methods=['POST'])
def divide():
    """Divide two numbers."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        b = get_number('b', data)
        result = calculator.divide(a, b)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/modulo', methods=['POST'])
def modulo():
    """Get modulo of two numbers."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        b = get_number('b', data)
        result = calculator.modulo(a, b)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


# ==================== Power and Root Routes ====================

@calculator_bp.route('/power', methods=['POST'])
def power():
    """Calculate base raised to exponent."""
    try:
        data = request.get_json()
        base = get_number('base', data)
        exponent = get_number('exponent', data)
        result = calculator.power(base, exponent)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/square', methods=['POST'])
def square():
    """Calculate square of a number."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        result = calculator.square(a)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/cube', methods=['POST'])
def cube():
    """Calculate cube of a number."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        result = calculator.cube(a)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/sqrt', methods=['POST'])
def sqrt():
    """Calculate square root of a number."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        result = calculator.square_root(a)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/cbrt', methods=['POST'])
def cbrt():
    """Calculate cube root of a number."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        result = calculator.cube_root(a)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/nthroot', methods=['POST'])
def nthroot():
    """Calculate nth root of a number."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        n = get_number('n', data)
        result = calculator.nth_root(a, n)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


# ==================== Trigonometric Routes ====================

@calculator_bp.route('/sin', methods=['POST'])
def sin():
    """Calculate sine of angle."""
    try:
        data = request.get_json()
        angle = get_number('angle', data)
        is_degrees = data.get('degrees', False)
        if is_degrees:
            result = calculator.sin_deg(angle)
        else:
            result = calculator.sin(angle)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/cos', methods=['POST'])
def cos():
    """Calculate cosine of angle."""
    try:
        data = request.get_json()
        angle = get_number('angle', data)
        is_degrees = data.get('degrees', False)
        if is_degrees:
            result = calculator.cos_deg(angle)
        else:
            result = calculator.cos(angle)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/tan', methods=['POST'])
def tan():
    """Calculate tangent of angle."""
    try:
        data = request.get_json()
        angle = get_number('angle', data)
        is_degrees = data.get('degrees', False)
        if is_degrees:
            result = calculator.tan_deg(angle)
        else:
            result = calculator.tan(angle)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/asin', methods=['POST'])
def asin():
    """Calculate arc sine."""
    try:
        data = request.get_json()
        value = get_number('value', data)
        return_degrees = data.get('degrees', False)
        if return_degrees:
            result = calculator.asin_deg(value)
        else:
            result = calculator.asin(value)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/acos', methods=['POST'])
def acos():
    """Calculate arc cosine."""
    try:
        data = request.get_json()
        value = get_number('value', data)
        return_degrees = data.get('degrees', False)
        if return_degrees:
            result = calculator.acos_deg(value)
        else:
            result = calculator.acos(value)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/atan', methods=['POST'])
def atan():
    """Calculate arc tangent."""
    try:
        data = request.get_json()
        value = get_number('value', data)
        return_degrees = data.get('degrees', False)
        if return_degrees:
            result = calculator.atan_deg(value)
        else:
            result = calculator.atan(value)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


# ==================== Hyperbolic Routes ====================

@calculator_bp.route('/sinh', methods=['POST'])
def sinh():
    """Calculate hyperbolic sine."""
    try:
        data = request.get_json()
        value = get_number('value', data)
        result = calculator.sinh(value)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/cosh', methods=['POST'])
def cosh():
    """Calculate hyperbolic cosine."""
    try:
        data = request.get_json()
        value = get_number('value', data)
        result = calculator.cosh(value)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/tanh', methods=['POST'])
def tanh():
    """Calculate hyperbolic tangent."""
    try:
        data = request.get_json()
        value = get_number('value', data)
        result = calculator.tanh(value)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


# ==================== Logarithmic Routes ====================

@calculator_bp.route('/log', methods=['POST'])
def log():
    """Calculate natural logarithm."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        result = calculator.log(a)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/log10', methods=['POST'])
def log10():
    """Calculate logarithm base 10."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        result = calculator.log10(a)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/log2', methods=['POST'])
def log2():
    """Calculate logarithm base 2."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        result = calculator.log2(a)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/logbase', methods=['POST'])
def logbase():
    """Calculate logarithm with custom base."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        base = get_number('base', data)
        result = calculator.log_base(a, base)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


# ==================== Exponential Routes ====================

@calculator_bp.route('/exp', methods=['POST'])
def exp():
    """Calculate e^x."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        result = calculator.exp(a)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/exp2', methods=['POST'])
def exp2():
    """Calculate 2^x."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        result = calculator.exp2(a)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/exp10', methods=['POST'])
def exp10():
    """Calculate 10^x."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        result = calculator.exp10(a)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


# ==================== Special Function Routes ====================

@calculator_bp.route('/factorial', methods=['POST'])
def factorial():
    """Calculate factorial of n."""
    try:
        data = request.get_json()
        n = get_number('n', data)
        result = calculator.factorial(int(n))
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/abs', methods=['POST'])
def abs_val():
    """Calculate absolute value."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        result = calculator.abs_value(a)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/floor', methods=['POST'])
def floor():
    """Round down to nearest integer."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        result = calculator.floor(a)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/ceil', methods=['POST'])
def ceil():
    """Round up to nearest integer."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        result = calculator.ceil(a)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/round', methods=['POST'])
def round_num():
    """Round to specified decimal places."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        decimals = int(get_number('decimals', data, required=False) or 0)
        result = calculator.round_num(a, decimals)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/reciprocal', methods=['POST'])
def reciprocal():
    """Calculate reciprocal (1/x)."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        result = calculator.reciprocal(a)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/negate', methods=['POST'])
def negate():
    """Negate a number."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        result = calculator.negate(a)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/percentage', methods=['POST'])
def percentage():
    """Convert to percentage."""
    try:
        data = request.get_json()
        a = get_number('a', data)
        result = calculator.percentage(a)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


# ==================== Constants Routes ====================

@calculator_bp.route('/pi', methods=['GET'])
def get_pi():
    """Get the value of Pi."""
    return make_response(True, calculator.get_pi())


@calculator_bp.route('/e', methods=['GET'])
def get_e():
    """Get the value of Euler's number."""
    return make_response(True, calculator.get_e())


# ==================== Angle Conversion Routes ====================

@calculator_bp.route('/deg-to-rad', methods=['POST'])
def deg_to_rad():
    """Convert degrees to radians."""
    try:
        data = request.get_json()
        degrees = get_number('degrees', data)
        result = calculator.deg_to_rad(degrees)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/rad-to-deg', methods=['POST'])
def rad_to_deg():
    """Convert radians to degrees."""
    try:
        data = request.get_json()
        radians = get_number('radians', data)
        result = calculator.rad_to_deg(radians)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


# ==================== Permutation and Combination Routes ====================

@calculator_bp.route('/permutation', methods=['POST'])
def permutation():
    """Calculate permutation nPr."""
    try:
        data = request.get_json()
        n = int(get_number('n', data))
        r = int(get_number('r', data))
        result = calculator.permutation(n, r)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


@calculator_bp.route('/combination', methods=['POST'])
def combination():
    """Calculate combination nCr."""
    try:
        data = request.get_json()
        n = int(get_number('n', data))
        r = int(get_number('r', data))
        result = calculator.combination(n, r)
        return make_response(True, result)
    except Exception as e:
        return make_response(False, error=str(e)), 400


# ==================== Generic Calculate Route ====================

@calculator_bp.route('/calculate', methods=['POST'])
def calculate():
    """
    Generic calculation endpoint that can perform any operation.
    
    Expected JSON body:
    {
        "operation": "add",  // Operation name
        "params": {          // Parameters for the operation
            "a": 5,
            "b": 3
        }
    }
    """
    try:
        data = request.get_json()
        operation = data.get('operation')
        params = data.get('params', {})
        
        if not operation:
            return make_response(False, error="Missing operation parameter"), 400
        
        # Map operation names to calculator methods
        operations = {
            # Basic arithmetic
            'add': lambda: calculator.add(float(params['a']), float(params['b'])),
            'subtract': lambda: calculator.subtract(float(params['a']), float(params['b'])),
            'multiply': lambda: calculator.multiply(float(params['a']), float(params['b'])),
            'divide': lambda: calculator.divide(float(params['a']), float(params['b'])),
            'modulo': lambda: calculator.modulo(float(params['a']), float(params['b'])),
            
            # Power and roots
            'power': lambda: calculator.power(float(params['base']), float(params['exponent'])),
            'square': lambda: calculator.square(float(params['a'])),
            'cube': lambda: calculator.cube(float(params['a'])),
            'sqrt': lambda: calculator.square_root(float(params['a'])),
            'cbrt': lambda: calculator.cube_root(float(params['a'])),
            'nthroot': lambda: calculator.nth_root(float(params['a']), float(params['n'])),
            
            # Trigonometric
            'sin': lambda: calculator.sin_deg(float(params['angle'])) if params.get('degrees') else calculator.sin(float(params['angle'])),
            'cos': lambda: calculator.cos_deg(float(params['angle'])) if params.get('degrees') else calculator.cos(float(params['angle'])),
            'tan': lambda: calculator.tan_deg(float(params['angle'])) if params.get('degrees') else calculator.tan(float(params['angle'])),
            'asin': lambda: calculator.asin_deg(float(params['value'])) if params.get('degrees') else calculator.asin(float(params['value'])),
            'acos': lambda: calculator.acos_deg(float(params['value'])) if params.get('degrees') else calculator.acos(float(params['value'])),
            'atan': lambda: calculator.atan_deg(float(params['value'])) if params.get('degrees') else calculator.atan(float(params['value'])),
            
            # Hyperbolic
            'sinh': lambda: calculator.sinh(float(params['value'])),
            'cosh': lambda: calculator.cosh(float(params['value'])),
            'tanh': lambda: calculator.tanh(float(params['value'])),
            
            # Logarithmic
            'log': lambda: calculator.log(float(params['a'])),
            'log10': lambda: calculator.log10(float(params['a'])),
            'log2': lambda: calculator.log2(float(params['a'])),
            'logbase': lambda: calculator.log_base(float(params['a']), float(params['base'])),
            
            # Exponential
            'exp': lambda: calculator.exp(float(params['a'])),
            'exp2': lambda: calculator.exp2(float(params['a'])),
            'exp10': lambda: calculator.exp10(float(params['a'])),
            
            # Special functions
            'factorial': lambda: calculator.factorial(int(float(params['n']))),
            'abs': lambda: calculator.abs_value(float(params['a'])),
            'floor': lambda: calculator.floor(float(params['a'])),
            'ceil': lambda: calculator.ceil(float(params['a'])),
            'round': lambda: calculator.round_num(float(params['a']), int(params.get('decimals', 0))),
            'reciprocal': lambda: calculator.reciprocal(float(params['a'])),
            'negate': lambda: calculator.negate(float(params['a'])),
            'percentage': lambda: calculator.percentage(float(params['a'])),
            
            # Constants
            'pi': lambda: calculator.get_pi(),
            'e': lambda: calculator.get_e(),
            
            # Angle conversions
            'deg_to_rad': lambda: calculator.deg_to_rad(float(params['degrees'])),
            'rad_to_deg': lambda: calculator.rad_to_deg(float(params['radians'])),
            
            # Permutation and combination
            'permutation': lambda: calculator.permutation(int(float(params['n'])), int(float(params['r']))),
            'combination': lambda: calculator.combination(int(float(params['n'])), int(float(params['r']))),
        }
        
        if operation not in operations:
            return make_response(False, error=f"Unknown operation: {operation}"), 400
        
        result = operations[operation]()
        return make_response(True, result)
        
    except KeyError as e:
        return make_response(False, error=f"Missing parameter: {e}"), 400
    except Exception as e:
        return make_response(False, error=str(e)), 400
