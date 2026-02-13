"""
Calculator Service Module

This module provides all mathematical operations for the scientific calculator.
It includes basic arithmetic, trigonometric, logarithmic, and other scientific functions.
"""

import math
from typing import Union

Number = Union[int, float]


class CalculatorService:
    """
    Service class that handles all calculator operations.
    All arithmetic and scientific operations are performed here.
    """

    # ==================== Basic Arithmetic Operations ====================

    @staticmethod
    def add(a: Number, b: Number) -> Number:
        """Add two numbers."""
        return a + b

    @staticmethod
    def subtract(a: Number, b: Number) -> Number:
        """Subtract b from a."""
        return a - b

    @staticmethod
    def multiply(a: Number, b: Number) -> Number:
        """Multiply two numbers."""
        return a * b

    @staticmethod
    def divide(a: Number, b: Number) -> Number:
        """
        Divide a by b.
        
        Raises:
            ValueError: If b is zero.
        """
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b

    @staticmethod
    def modulo(a: Number, b: Number) -> Number:
        """
        Get remainder of a divided by b.
        
        Raises:
            ValueError: If b is zero.
        """
        if b == 0:
            raise ValueError("Modulo by zero is not allowed")
        return a % b

    # ==================== Power and Root Operations ====================

    @staticmethod
    def power(base: Number, exponent: Number) -> Number:
        """Raise base to the power of exponent."""
        return math.pow(base, exponent)

    @staticmethod
    def square(a: Number) -> Number:
        """Calculate the square of a number."""
        return a ** 2

    @staticmethod
    def cube(a: Number) -> Number:
        """Calculate the cube of a number."""
        return a ** 3

    @staticmethod
    def square_root(a: Number) -> Number:
        """
        Calculate the square root of a number.
        
        Raises:
            ValueError: If a is negative.
        """
        if a < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(a)

    @staticmethod
    def cube_root(a: Number) -> Number:
        """Calculate the cube root of a number."""
        return a ** (1/3) if a >= 0 else -(-a) ** (1/3)

    @staticmethod
    def nth_root(a: Number, n: Number) -> Number:
        """
        Calculate the nth root of a number.
        
        Raises:
            ValueError: If n is zero or if a is negative with even n.
        """
        if n == 0:
            raise ValueError("Root index cannot be zero")
        if a < 0 and n % 2 == 0:
            raise ValueError("Cannot calculate even root of negative number")
        return a ** (1/n) if a >= 0 else -(-a) ** (1/n)

    # ==================== Trigonometric Functions (Radians) ====================

    @staticmethod
    def sin(angle: Number) -> Number:
        """Calculate sine of angle (in radians)."""
        return math.sin(angle)

    @staticmethod
    def cos(angle: Number) -> Number:
        """Calculate cosine of angle (in radians)."""
        return math.cos(angle)

    @staticmethod
    def tan(angle: Number) -> Number:
        """Calculate tangent of angle (in radians)."""
        return math.tan(angle)

    @staticmethod
    def asin(value: Number) -> Number:
        """
        Calculate arc sine (inverse sine) of value.
        
        Raises:
            ValueError: If value is not in range [-1, 1].
        """
        if value < -1 or value > 1:
            raise ValueError("Value must be in range [-1, 1] for asin")
        return math.asin(value)

    @staticmethod
    def acos(value: Number) -> Number:
        """
        Calculate arc cosine (inverse cosine) of value.
        
        Raises:
            ValueError: If value is not in range [-1, 1].
        """
        if value < -1 or value > 1:
            raise ValueError("Value must be in range [-1, 1] for acos")
        return math.acos(value)

    @staticmethod
    def atan(value: Number) -> Number:
        """Calculate arc tangent (inverse tangent) of value."""
        return math.atan(value)

    # ==================== Trigonometric Functions (Degrees) ====================

    @staticmethod
    def sin_deg(angle: Number) -> Number:
        """Calculate sine of angle (in degrees)."""
        return math.sin(math.radians(angle))

    @staticmethod
    def cos_deg(angle: Number) -> Number:
        """Calculate cosine of angle (in degrees)."""
        return math.cos(math.radians(angle))

    @staticmethod
    def tan_deg(angle: Number) -> Number:
        """Calculate tangent of angle (in degrees)."""
        return math.tan(math.radians(angle))

    @staticmethod
    def asin_deg(value: Number) -> Number:
        """Calculate arc sine and return result in degrees."""
        if value < -1 or value > 1:
            raise ValueError("Value must be in range [-1, 1] for asin")
        return math.degrees(math.asin(value))

    @staticmethod
    def acos_deg(value: Number) -> Number:
        """Calculate arc cosine and return result in degrees."""
        if value < -1 or value > 1:
            raise ValueError("Value must be in range [-1, 1] for acos")
        return math.degrees(math.acos(value))

    @staticmethod
    def atan_deg(value: Number) -> Number:
        """Calculate arc tangent and return result in degrees."""
        return math.degrees(math.atan(value))

    # ==================== Hyperbolic Functions ====================

    @staticmethod
    def sinh(value: Number) -> Number:
        """Calculate hyperbolic sine."""
        return math.sinh(value)

    @staticmethod
    def cosh(value: Number) -> Number:
        """Calculate hyperbolic cosine."""
        return math.cosh(value)

    @staticmethod
    def tanh(value: Number) -> Number:
        """Calculate hyperbolic tangent."""
        return math.tanh(value)

    # ==================== Logarithmic Functions ====================

    @staticmethod
    def log(a: Number) -> Number:
        """
        Calculate natural logarithm (base e).
        
        Raises:
            ValueError: If a is not positive.
        """
        if a <= 0:
            raise ValueError("Logarithm requires positive number")
        return math.log(a)

    @staticmethod
    def log10(a: Number) -> Number:
        """
        Calculate logarithm base 10.
        
        Raises:
            ValueError: If a is not positive.
        """
        if a <= 0:
            raise ValueError("Logarithm requires positive number")
        return math.log10(a)

    @staticmethod
    def log2(a: Number) -> Number:
        """
        Calculate logarithm base 2.
        
        Raises:
            ValueError: If a is not positive.
        """
        if a <= 0:
            raise ValueError("Logarithm requires positive number")
        return math.log2(a)

    @staticmethod
    def log_base(a: Number, base: Number) -> Number:
        """
        Calculate logarithm with custom base.
        
        Raises:
            ValueError: If a or base is not positive, or if base is 1.
        """
        if a <= 0 or base <= 0:
            raise ValueError("Logarithm requires positive numbers")
        if base == 1:
            raise ValueError("Logarithm base cannot be 1")
        return math.log(a, base)

    # ==================== Exponential Functions ====================

    @staticmethod
    def exp(a: Number) -> Number:
        """Calculate e raised to the power of a."""
        return math.exp(a)

    @staticmethod
    def exp2(a: Number) -> Number:
        """Calculate 2 raised to the power of a."""
        return 2 ** a

    @staticmethod
    def exp10(a: Number) -> Number:
        """Calculate 10 raised to the power of a."""
        return 10 ** a

    # ==================== Special Functions ====================

    @staticmethod
    def factorial(n: int) -> int:
        """
        Calculate factorial of n.
        
        Raises:
            ValueError: If n is negative or not an integer.
        """
        if not isinstance(n, int) and not (isinstance(n, float) and n.is_integer()):
            raise ValueError("Factorial requires an integer")
        n = int(n)
        if n < 0:
            raise ValueError("Factorial requires non-negative integer")
        return math.factorial(n)

    @staticmethod
    def abs_value(a: Number) -> Number:
        """Calculate absolute value."""
        return abs(a)

    @staticmethod
    def floor(a: Number) -> int:
        """Round down to nearest integer."""
        return math.floor(a)

    @staticmethod
    def ceil(a: Number) -> int:
        """Round up to nearest integer."""
        return math.ceil(a)

    @staticmethod
    def round_num(a: Number, decimals: int = 0) -> Number:
        """Round to specified number of decimal places."""
        return round(a, decimals)

    @staticmethod
    def reciprocal(a: Number) -> Number:
        """
        Calculate 1/a (reciprocal).
        
        Raises:
            ValueError: If a is zero.
        """
        if a == 0:
            raise ValueError("Cannot calculate reciprocal of zero")
        return 1 / a

    @staticmethod
    def negate(a: Number) -> Number:
        """Negate a number (change sign)."""
        return -a

    @staticmethod
    def percentage(a: Number) -> Number:
        """Convert number to percentage (divide by 100)."""
        return a / 100

    # ==================== Constants ====================

    @staticmethod
    def get_pi() -> float:
        """Return the value of Pi."""
        return math.pi

    @staticmethod
    def get_e() -> float:
        """Return the value of Euler's number (e)."""
        return math.e

    # ==================== Angle Conversions ====================

    @staticmethod
    def deg_to_rad(degrees: Number) -> Number:
        """Convert degrees to radians."""
        return math.radians(degrees)

    @staticmethod
    def rad_to_deg(radians: Number) -> Number:
        """Convert radians to degrees."""
        return math.degrees(radians)

    # ==================== Permutation and Combination ====================

    @staticmethod
    def permutation(n: int, r: int) -> int:
        """
        Calculate permutation nPr.
        
        Raises:
            ValueError: If n or r is negative, or if r > n.
        """
        n, r = int(n), int(r)
        if n < 0 or r < 0:
            raise ValueError("Permutation requires non-negative integers")
        if r > n:
            raise ValueError("r cannot be greater than n in permutation")
        return math.perm(n, r)

    @staticmethod
    def combination(n: int, r: int) -> int:
        """
        Calculate combination nCr.
        
        Raises:
            ValueError: If n or r is negative, or if r > n.
        """
        n, r = int(n), int(r)
        if n < 0 or r < 0:
            raise ValueError("Combination requires non-negative integers")
        if r > n:
            raise ValueError("r cannot be greater than n in combination")
        return math.comb(n, r)


# Create a singleton instance for easy access
calculator = CalculatorService()
