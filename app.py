from flask import Flask, request, render_template, jsonify
import sympy as sp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/double_integral', methods=['POST'])
def double_integral():
    data = request.get_json()

    function_expr = data.get('function')
    lower_limit_x = data.get('lower_limit_x', 0)
    upper_limit_x = data.get('upper_limit_x', 1)
    lower_limit_y = data.get('lower_limit_y', 0)
    upper_limit_y = data.get('upper_limit_y', 1)

    if not function_expr:
        return jsonify({"error": "Function is required"}), 400

    try:
        # Convert limits to float, then to integer (whole number limits)
        lower_limit_x = int(float(lower_limit_x))
        upper_limit_x = int(float(upper_limit_x))
        lower_limit_y = int(float(lower_limit_y))
        upper_limit_y = int(float(upper_limit_y))

        # Sympify the function
        f = sp.sympify(function_expr)

        # Detect variables automatically
        variables = sorted(list(f.free_symbols), key=lambda x: str(x))
        if len(variables) != 2:
            return jsonify({"error": "Function must have exactly 2 variables."}), 400

        var1, var2 = variables  # outer and inner variables

        # Perform definite double integration
        integral_result = sp.integrate(f, (var2, lower_limit_y, upper_limit_y), (var1, lower_limit_x, upper_limit_x))

        # Force the result to be a whole number by converting it to an integer
        evaluated_result = integral_result.evalf()

        # Convert the result to an integer, regardless of whether it's a float or integer
        evaluated_result = int(evaluated_result)

        # Prepare LaTeX formatted integral with whole number limits
        latex_expr = r"\int_{{{}}}^{{{}}} \int_{{{}}}^{{{}}} {} \, d{} \, d{}".format(
            lower_limit_x, upper_limit_x,
            lower_limit_y, upper_limit_y,
            sp.latex(f),
            sp.latex(var2),
            sp.latex(var1)
        )

        return jsonify({
            "result": str(evaluated_result),
            "latex": latex_expr
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
