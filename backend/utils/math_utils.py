"""Mathematical utility functions"""
import math
import random
from typing import Dict, Any, List
from decimal import Decimal, getcontext

def basic_calculator(expression: str) -> Dict[str, Any]:
    """Basic calculator with support for +, -, *, /, %, ^, sqrt, etc."""
    try:
        # Replace common math functions
        expression = expression.replace('^', '**')
        expression = expression.replace('sqrt(', 'math.sqrt(')
        expression = expression.replace('sin(', 'math.sin(')
        expression = expression.replace('cos(', 'math.cos(')
        expression = expression.replace('tan(', 'math.tan(')
        expression = expression.replace('log(', 'math.log10(')
        expression = expression.replace('ln(', 'math.log(')
        expression = expression.replace('pi', 'math.pi')
        expression = expression.replace('e', 'math.e')
        
        # Evaluate safely (in production, use a proper math parser)
        result = eval(expression, {"__builtins__": {}, "math": math})
        
        return {
            "result": result,
            "expression": expression,
            "success": True
        }
    except Exception as e:
        return {
            "result": str(e),
            "expression": expression,
            "success": False
        }

def scientific_calculator(operation: str, values: List[float], **kwargs) -> Dict[str, Any]:
    """Scientific calculator operations"""
    try:
        if operation == "factorial":
            if len(values) != 1 or values[0] < 0 or values[0] != int(values[0]):
                return {"result": "Factorial requires a non-negative integer", "success": False}
            result = math.factorial(int(values[0]))
        
        elif operation == "power":
            if len(values) != 2:
                return {"result": "Power requires exactly 2 values", "success": False}
            result = math.pow(values[0], values[1])
        
        elif operation == "sqrt":
            if len(values) != 1 or values[0] < 0:
                return {"result": "Square root requires a non-negative number", "success": False}
            result = math.sqrt(values[0])
        
        elif operation == "log":
            base = kwargs.get("base", 10)
            if len(values) != 1 or values[0] <= 0:
                return {"result": "Logarithm requires a positive number", "success": False}
            result = math.log(values[0], base)
        
        elif operation == "sin":
            if len(values) != 1:
                return {"result": "Sin requires exactly 1 value", "success": False}
            angle = math.radians(values[0]) if kwargs.get("degrees", True) else values[0]
            result = math.sin(angle)
        
        elif operation == "cos":
            if len(values) != 1:
                return {"result": "Cos requires exactly 1 value", "success": False}
            angle = math.radians(values[0]) if kwargs.get("degrees", True) else values[0]
            result = math.cos(angle)
        
        elif operation == "tan":
            if len(values) != 1:
                return {"result": "Tan requires exactly 1 value", "success": False}
            angle = math.radians(values[0]) if kwargs.get("degrees", True) else values[0]
            result = math.tan(angle)
        
        else:
            return {"result": f"Operation '{operation}' not supported", "success": False}
        
        return {
            "result": result,
            "operation": operation,
            "values": values,
            "success": True
        }
    
    except Exception as e:
        return {
            "result": str(e),
            "operation": operation,
            "success": False
        }

def statistics_calculator(data: List[float]) -> Dict[str, Any]:
    """Calculate various statistical measures"""
    if not data:
        return {"error": "No data provided"}
    
    try:
        n = len(data)
        sorted_data = sorted(data)
        
        # Basic statistics
        mean = sum(data) / n
        median = sorted_data[n//2] if n % 2 == 1 else (sorted_data[n//2-1] + sorted_data[n//2]) / 2
        
        # Mode
        from collections import Counter
        counts = Counter(data)
        max_count = max(counts.values())
        modes = [k for k, v in counts.items() if v == max_count]
        mode = modes[0] if len(modes) == 1 else modes
        
        # Range
        data_range = max(data) - min(data)
        
        # Variance and standard deviation
        variance = sum((x - mean) ** 2 for x in data) / n
        std_dev = math.sqrt(variance)
        
        # Sample variance and standard deviation
        sample_variance = sum((x - mean) ** 2 for x in data) / (n - 1) if n > 1 else 0
        sample_std_dev = math.sqrt(sample_variance) if n > 1 else 0
        
        # Quartiles
        q1_index = n // 4
        q3_index = 3 * n // 4
        q1 = sorted_data[q1_index]
        q3 = sorted_data[q3_index]
        iqr = q3 - q1
        
        return {
            "count": n,
            "mean": round(mean, 6),
            "median": median,
            "mode": mode,
            "range": data_range,
            "min": min(data),
            "max": max(data),
            "variance": round(variance, 6),
            "std_deviation": round(std_dev, 6),
            "sample_variance": round(sample_variance, 6),
            "sample_std_deviation": round(sample_std_dev, 6),
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "sum": sum(data)
        }
    
    except Exception as e:
        return {"error": str(e)}

def prime_checker(number: int) -> Dict[str, Any]:
    """Check if a number is prime and find factors"""
    if not isinstance(number, int) or number < 2:
        return {"is_prime": False, "number": number, "message": "Number must be an integer >= 2"}
    
    # Check for prime
    is_prime = True
    factors = []
    
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            is_prime = False
            factors.extend([i, number // i])
            break
    
    if is_prime:
        factors = [1, number]
    else:
        factors = sorted(list(set(factors + [1, number])))
    
    # Find prime factorization
    prime_factors = []
    temp = number
    d = 2
    
    while d * d <= temp:
        while temp % d == 0:
            prime_factors.append(d)
            temp //= d
        d += 1
    
    if temp > 1:
        prime_factors.append(temp)
    
    return {
        "number": number,
        "is_prime": is_prime,
        "factors": factors,
        "prime_factors": prime_factors,
        "factor_count": len(factors)
    }

def gcd_calculator(a: int, b: int) -> Dict[str, Any]:
    """Calculate Greatest Common Divisor"""
    try:
        original_a, original_b = a, b
        
        # Euclidean algorithm
        while b:
            a, b = b, a % b
        
        gcd = abs(a)
        
        # LCM calculation
        lcm = abs(original_a * original_b) // gcd if gcd != 0 else 0
        
        return {
            "gcd": gcd,
            "lcm": lcm,
            "a": original_a,
            "b": original_b,
            "coprime": gcd == 1
        }
    
    except Exception as e:
        return {"error": str(e)}

def percentage_calculator(operation: str, **kwargs) -> Dict[str, Any]:
    """Calculate various percentage operations"""
    try:
        if operation == "percent_of":
            # What is X% of Y?
            percent = kwargs.get("percent", 0)
            number = kwargs.get("number", 0)
            result = (percent / 100) * number
            
        elif operation == "is_what_percent":
            # X is what percent of Y?
            part = kwargs.get("part", 0)
            whole = kwargs.get("whole", 0)
            if whole == 0:
                return {"error": "Cannot divide by zero"}
            result = (part / whole) * 100
            
        elif operation == "percent_change":
            # Percent change from X to Y
            old_value = kwargs.get("old_value", 0)
            new_value = kwargs.get("new_value", 0)
            if old_value == 0:
                return {"error": "Cannot calculate percent change from zero"}
            result = ((new_value - old_value) / old_value) * 100
            
        elif operation == "add_percent":
            # Add X% to Y
            number = kwargs.get("number", 0)
            percent = kwargs.get("percent", 0)
            result = number * (1 + percent / 100)
            
        elif operation == "subtract_percent":
            # Subtract X% from Y
            number = kwargs.get("number", 0)
            percent = kwargs.get("percent", 0)
            result = number * (1 - percent / 100)
            
        else:
            return {"error": f"Operation '{operation}' not supported"}
        
        return {
            "result": round(result, 6),
            "operation": operation,
            "parameters": kwargs,
            "success": True
        }
    
    except Exception as e:
        return {"error": str(e)}

def loan_calculator(principal: float, rate: float, time: float, compound_frequency: int = 12) -> Dict[str, Any]:
    """Calculate loan payments and details"""
    try:
        # Convert annual rate to decimal
        annual_rate = rate / 100
        
        # Monthly interest rate
        monthly_rate = annual_rate / 12
        
        # Total number of payments
        total_payments = time * 12
        
        # Monthly payment calculation
        if monthly_rate == 0:
            monthly_payment = principal / total_payments
        else:
            monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** total_payments) / ((1 + monthly_rate) ** total_payments - 1)
        
        # Total amount paid
        total_paid = monthly_payment * total_payments
        
        # Total interest
        total_interest = total_paid - principal
        
        # Generate amortization schedule (first 12 months)
        schedule = []
        remaining_balance = principal
        
        for month in range(1, min(13, int(total_payments) + 1)):
            interest_payment = remaining_balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment
            
            schedule.append({
                "month": month,
                "payment": round(monthly_payment, 2),
                "principal": round(principal_payment, 2),
                "interest": round(interest_payment, 2),
                "balance": round(remaining_balance, 2)
            })
        
        return {
            "principal": principal,
            "annual_rate": rate,
            "loan_term_years": time,
            "monthly_payment": round(monthly_payment, 2),
            "total_paid": round(total_paid, 2),
            "total_interest": round(total_interest, 2),
            "schedule_sample": schedule,
            "success": True
        }
    
    except Exception as e:
        return {"error": str(e)}

def unit_circle(angle: float, unit: str = "degrees") -> Dict[str, Any]:
    """Calculate unit circle values"""
    try:
        # Convert to radians if needed
        if unit == "degrees":
            radians = math.radians(angle)
        else:
            radians = angle
        
        # Calculate trig values
        sin_val = math.sin(radians)
        cos_val = math.cos(radians)
        
        # Handle tan (undefined at π/2 + nπ)
        if abs(cos_val) < 1e-10:
            tan_val = "undefined"
        else:
            tan_val = math.tan(radians)
        
        # Calculate other trig functions
        if abs(sin_val) < 1e-10:
            csc_val = "undefined"
        else:
            csc_val = 1 / sin_val
        
        if abs(cos_val) < 1e-10:
            sec_val = "undefined"
        else:
            sec_val = 1 / cos_val
        
        if tan_val == "undefined":
            cot_val = "undefined"
        elif abs(tan_val) < 1e-10:
            cot_val = "undefined"
        else:
            cot_val = 1 / tan_val
        
        # Quadrant
        quadrant = 1
        if cos_val < 0 and sin_val > 0:
            quadrant = 2
        elif cos_val < 0 and sin_val < 0:
            quadrant = 3
        elif cos_val > 0 and sin_val < 0:
            quadrant = 4
        
        return {
            "angle_degrees": angle if unit == "degrees" else math.degrees(angle),
            "angle_radians": radians,
            "sin": round(sin_val, 6) if abs(sin_val) > 1e-10 else 0,
            "cos": round(cos_val, 6) if abs(cos_val) > 1e-10 else 0,
            "tan": round(tan_val, 6) if tan_val != "undefined" and abs(tan_val) > 1e-10 else tan_val,
            "csc": round(csc_val, 6) if csc_val != "undefined" else csc_val,
            "sec": round(sec_val, 6) if sec_val != "undefined" else sec_val,
            "cot": round(cot_val, 6) if cot_val != "undefined" else cot_val,
            "quadrant": quadrant,
            "coordinates": (round(cos_val, 6), round(sin_val, 6))
        }
    
    except Exception as e:
        return {"error": str(e)}