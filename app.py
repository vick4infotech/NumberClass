from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    """Check if a number is perfect."""
    if n < 2:
        return False
    sum_factors = sum(i for i in range(1, n) if n % i == 0)
    return sum_factors == n

def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    num_digits = len(digits)
    return sum(d ** num_digits for d in digits) == n

def get_fun_fact(n):
    """Fetch a fun fact about the number from Numbers API."""
    url = f"http://numbersapi.com/{n}/math"
    response = requests.get(url)
    return response.text if response.status_code == 200 else "No fun fact available."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')
    
    # Validate input
    if not number or not number.lstrip('-').isdigit():
        return jsonify({
            "number": number,
            "error": True
        }), 400
    
    number = int(number)
    
    # Determine properties
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    
    # Get fun fact
    fun_fact = get_fun_fact(number)
    
    # Prepare response
    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(abs(number))),
        "fun_fact": fun_fact
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)