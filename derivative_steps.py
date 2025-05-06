import sympy as sp

def show_derivative_steps(expression, variable):
    """Show detailed steps for calculating derivatives."""
    x, y, z = sp.symbols('x y z')
    expr = sp.sympify(expression)
    var = sp.Symbol(variable)
    
    print(f"Expressão original: {expr}")
    print(f"Calculando a derivada em relação a {variable}...")
    
    # Identificar o tipo de expressão e aplicar a regra apropriada
    if expr.is_polynomial(var):
        _show_polynomial_steps(expr, var)
    elif expr.has(sp.sin, sp.cos):
        _show_trig_steps(expr, var)
    elif expr.has(sp.exp):
        _show_exp_steps(expr, var)
    elif expr.has(sp.log):
        _show_log_steps(expr, var)
    elif expr.is_rational_function(var):
        _show_rational_steps(expr, var)
    else:
        print("Aplicando regras gerais de derivação...")
    
    derivative = sp.diff(expr, var)
    print(f"Resultado final: {derivative}")
    return derivative

def _show_polynomial_steps(expr, var):
    """Show steps for polynomial differentiation."""
    print("Aplicando regras para polinômios:")
    
    # Expandir a expressão em termos de potências
    expanded = sp.expand(expr)
    print(f"Passo 1: Expandir a expressão: {expanded}")
    
    # Mostrar a derivada de cada termo
    print("Passo 2: Derivar cada termo separadamente:")
    terms = expanded.as_ordered_terms()
    for term in terms:
        print(f"  d/d{var}({term}) = {sp.diff(term, var)}")
    
    print("Passo 3: Somar as derivadas dos termos")

def _show_trig_steps(expr, var):
    """Show steps for trigonometric function differentiation."""
    print("Aplicando regras para funções trigonométricas:")
    print(f"Passo 1: Identificar funções trigonométricas na expressão")
    
    # Regras básicas
    print("Passo 2: Aplicar regras de derivação:")
    print("  • d/dx(sin(x)) = cos(x)")
    print("  • d/dx(cos(x)) = -sin(x)")
    print("  • d/dx(tan(x)) = sec²(x)")
    
    # Se houver composição, mostrar regra da cadeia
    if any(arg != var for func in expr.atoms(sp.Function) for arg in func.args):
        print("Passo 3: Aplicar regra da cadeia para composições")

def _show_exp_steps(expr, var):
    """Show steps for exponential function differentiation."""
    print("Aplicando regras para funções exponenciais:")
    print("Passo 1: Identificar funções exponenciais na expressão")
    print("Passo 2: Aplicar a regra: d/dx(e^u) = e^u · du/dx")

def _show_log_steps(expr, var):
    """Show steps for logarithmic function differentiation."""
    print("Aplicando regras para funções logarítmicas:")
    print("Passo 1: Identificar funções logarítmicas na expressão")
    print("Passo 2: Aplicar a regra: d/dx(ln(u)) = (1/u) · du/dx")

def _show_rational_steps(expr, var):
    """Show steps for rational function differentiation."""
    print("Aplicando regras para funções racionais:")
    
    # Decompor em numerador e denominador
    num, den = sp.fraction(expr)
    print(f"Passo 1: Identificar numerador ({num}) e denominador ({den})")
    print("Passo 2: Aplicar a regra do quociente:")
    print("  d/dx(f(x)/g(x)) = (g(x)·f'(x) - f(x)·g'(x))/g(x)²")