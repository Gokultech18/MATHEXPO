from flask import Flask, request, render_template, jsonify
import sympy as sp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/double_integral', methods=['POST'])
def double_integral():
    data = request.get_json()
    function_expr = data.get('function')  # Function to integrate
    var1 = data.get('variable1', 'x')  # Variable x
    var2 = data.get('variable2', 'y')  # Variable y
    lower_limit_x = data.get('lower_limit_x', 0)  # Lower limit of x
    upper_limit_x = data.get('upper_limit_x', 1)  # Upper limit of x
    lower_limit_y = data.get('lower_limit_y', 0)  # Lower limit of y
    upper_limit_y = data.get('upper_limit_y', 1)  # Upper limit of y

    if not function_expr:
        return jsonify({"error": "Function is required"}), 400

    try:
        # Define the symbols (variables)
        x, y = sp.symbols([var1, var2])

        # Convert the input function string to a sympy expression
        f = sp.sympify(function_expr)

        # Perform double integration
        integral_result = sp.integrate(f, (x, lower_limit_x, upper_limit_x), (y, lower_limit_y, upper_limit_y))

        # Return the result as a string
        return jsonify({
            "result": str(integral_result)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
