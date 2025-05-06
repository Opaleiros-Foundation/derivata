import sympy as sp

def calculate_partial_derivatives(expression, variables):
    """Calculate all partial derivatives for a multivariate function."""
    x, y, z = sp.symbols('x y z')
    expr = sp.sympify(expression)
    
    results = {}
    for var in variables:
        results[var] = sp.diff(expr, var)
    
    return results

def show_partial_derivative_steps(expression, variable):
    """Show steps for calculating a partial derivative."""
    x, y, z = sp.symbols('x y z')
    expr = sp.sympify(expression)
    
    print(f"Expressão original: {expr}")
    print(f"Calculando a derivada parcial em relação a {variable}...")
    print("Passo 1: Tratamos todas as outras variáveis como constantes")
    
    # Exemplo para função f(x,y) = x^2 + xy + y^2
    if str(expr) == "x**2 + x*y + y**2" and str(variable) == "x":
        print("Passo 2: Para ∂/∂x(x^2 + xy + y^2)")
        print("Passo 3: ∂/∂x(x^2) + ∂/∂x(xy) + ∂/∂x(y^2)")
        print("Passo 4: 2x + y + 0")
        print("Passo 5: Resultado: 2x + y")
    
    derivative = sp.diff(expr, variable)
    print(f"Resultado final: {derivative}")
    return derivative