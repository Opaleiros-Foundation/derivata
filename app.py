import streamlit as st
import sympy as sp
import pandas as pd
import os
import base64
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração da página - DEVE ser o primeiro comando Streamlit
st.set_page_config(
    page_title="Derivata - Calculadora de Derivadas",
    page_icon="📊",
    layout="wide"
)

# Função para carregar o SVG como base64
def get_svg_base64():
    try:
        with open("static/logo.svg", "r") as file:
            svg_content = file.read()
            b64 = base64.b64encode(svg_content.encode()).decode()
            return b64
    except Exception as e:
        st.error(f"Erro ao carregar o logo SVG: {str(e)}")
        return None

# Dicionário de exemplos para as derivadas
examples = {
    "Polinômio Simples": "x**2 + 3*x + 1",
    "Função Trigonométrica": "sin(x) + cos(x)",
    "Função Exponencial": "exp(x**2)",
    "Função Logarítmica": "log(x**2 + 1)",
    "Função Composta": "sin(exp(x))"
}

def get_partial_derivative_examples():
    """Retorna exemplos de derivadas parciais com explicações."""
    examples = {
        "Função de Duas Variáveis": {
            "expression": "x**2 + x*y + y**2",
            "variables": ["x", "y"],
            "explanation": """
            Esta é uma função quadrática de duas variáveis. As derivadas parciais mostram 
            como a função muda quando alteramos x ou y independentemente.
            """
        },
        "Função Exponencial Multivariável": {
            "expression": "exp(x*y)",
            "variables": ["x", "y"],
            "explanation": """
            Esta função exponencial cresce rapidamente quando x e y aumentam juntos. 
            As derivadas parciais mostram taxas de crescimento diferentes para cada variável.
            """
        },
        "Função Trigonométrica Multivariável": {
            "expression": "sin(x) + cos(y)",
            "variables": ["x", "y"],
            "explanation": """
            Esta função combina seno de x e cosseno de y. As derivadas parciais mostram 
            como a oscilação em cada direção afeta o valor da função.
            """
        },
        "Função Composta Multivariável": {
            "expression": "sin(x*y) + exp(x+y)",
            "variables": ["x", "y"],
            "explanation": """
            Esta função combina uma função trigonométrica do produto xy com uma exponencial da soma x+y. 
            As derivadas parciais requerem a aplicação da regra da cadeia.
            """
        }
    }
    return examples

# Funções para cálculo e formatação
def calculate_derivative(expression, variable, order=1):
    """Calculate the derivative of an expression with respect to a variable."""
    try:
        x, y, z = sp.symbols('x y z')
        expr = sp.sympify(expression)
        derivative = sp.diff(expr, variable, order)
        return derivative
    except Exception as e:
        st.error(f"Erro ao calcular a derivada: {str(e)}")
        return None

def calculate_partial_derivatives(expression, variables):
    """Calculate all partial derivatives for a multivariate function."""
    try:
        x, y, z = sp.symbols('x y z')
        expr = sp.sympify(expression)
        
        results = {}
        for var in variables:
            results[var] = sp.diff(expr, var)
        
        return results
    except Exception as e:
        st.error(f"Erro ao calcular as derivadas parciais: {str(e)}")
        return {}

def get_derivative_steps(expression, variable):
    """Get steps for calculating a derivative."""
    try:
        x, y, z = sp.symbols('x y z')
        expr = sp.sympify(expression)
        var = sp.Symbol(variable)
        
        steps = []
        steps.append(f"Expressão original: {expr}")
        steps.append(f"Calculando a derivada em relação a {variable}...")
        
        # Identificar o tipo de expressão
        if expr.is_polynomial(var):
            steps.append("Aplicando regras para polinômios")
            expanded = sp.expand(expr)
            steps.append(f"Expandir a expressão: {expanded}")
            
            terms = expanded.as_ordered_terms()
            for term in terms:
                steps.append(f"d/d{var}({term}) = {sp.diff(term, var)}")
        
        elif expr.has(sp.sin, sp.cos):
            steps.append("Aplicando regras para funções trigonométricas")
            steps.append("Regras básicas:")
            steps.append("• d/dx(sin(x)) = cos(x)")
            steps.append("• d/dx(cos(x)) = -sin(x)")
        
        elif expr.has(sp.exp):
            steps.append("Aplicando regras para funções exponenciais")
            steps.append("Regra: d/dx(e^u) = e^u · du/dx")
        
        elif expr.has(sp.log):
            steps.append("Aplicando regras para funções logarítmicas")
            steps.append("Regra: d/dx(ln(u)) = (1/u) · du/dx")
        
        derivative = sp.diff(expr, var)
        steps.append(f"Resultado final: {derivative}")
        
        return steps
    except Exception as e:
        st.error(f"Erro ao gerar os passos da derivação: {str(e)}")
        return ["Não foi possível gerar os passos para esta expressão."]

def get_partial_derivative_steps(expression, variable):
    """Get detailed steps for calculating a partial derivative."""
    try:
        x, y, z = sp.symbols('x y z')
        expr = sp.sympify(expression)
        var = sp.Symbol(variable)
        
        steps = []
        steps.append(f"Expressão original: {expr}")
        steps.append(f"Calculando a derivada parcial em relação a {variable}...")
        steps.append(f"Passo 1: Tratamos todas as outras variáveis como constantes")
        
        # Identificar todas as variáveis na expressão
        all_vars = [str(symbol) for symbol in expr.free_symbols]
        other_vars = [v for v in all_vars if v != variable]
        
        if other_vars:
            steps.append(f"Passo 2: Variáveis tratadas como constantes: {', '.join(other_vars)}")
        
        # Identificar o tipo de expressão e aplicar regras específicas
        if expr.is_polynomial(var):
            steps.append(f"Passo 3: Aplicando regras para polinômios")
            expanded = sp.expand(expr)
            steps.append(f"Passo 4: Expandindo a expressão: {expanded}")
            
            # Mostrar a derivada de cada termo separadamente
            terms = expanded.as_ordered_terms()
            steps.append(f"Passo 5: Derivando cada termo separadamente em relação a {variable}:")
            
            for term in terms:
                # Verificar se o termo contém a variável
                if term.has(var):
                    # Extrair coeficiente e potência para termos do tipo c*x^n
                    if term.is_Pow and term.base == var:
                        coef = 1
                        power = term.exp
                        steps.append(f"  ∂/∂{variable}({term}) = {coef*power}*{variable}^{power-1} (regra: ∂/∂x(x^n) = n*x^(n-1))")
                    elif term.is_Mul:
                        # Separar fatores que contêm a variável
                        var_factors = [f for f in term.args if f.has(var)]
                        const_factors = [f for f in term.args if not f.has(var)]
                        
                        if var_factors:
                            steps.append(f"  Para o termo {term}:")
                            steps.append(f"    - Fatores constantes em relação a {variable}: {sp.Mul(*const_factors) if const_factors else 1}")
                            steps.append(f"    - Fatores contendo {variable}: {sp.Mul(*var_factors) if var_factors else 1}")
                            steps.append(f"    - Aplicando a regra do produto: ∂/∂{variable}({term}) = {sp.diff(term, var)}")
                    else:
                        steps.append(f"  ∂/∂{variable}({term}) = {sp.diff(term, var)}")
                else:
                    steps.append(f"  ∂/∂{variable}({term}) = 0 (termo não contém {variable})")
            
            steps.append(f"Passo 6: Somando todas as derivadas parciais dos termos...")
        
        elif expr.has(sp.sin, sp.cos, sp.tan):
            steps.append(f"Passo 3: Aplicando regras para funções trigonométricas")
            steps.append(f"Regras básicas:")
            steps.append(f"• ∂/∂x(sin(x)) = cos(x)")
            steps.append(f"• ∂/∂x(cos(x)) = -sin(x)")
            steps.append(f"• ∂/∂x(tan(x)) = sec²(x) = 1/cos²(x)")
            
            # Verificar se há composição de funções
            has_composition = False
            for func in expr.atoms(sp.Function):
                if func.args[0] != var and func.args[0].has(var):
                    has_composition = True
                    break
            
            if has_composition:
                steps.append(f"Passo 4: Detectada composição de funções. Aplicando a regra da cadeia:")
                steps.append(f"• Regra da cadeia: ∂/∂{variable}(f(g(x))) = f'(g(x)) · ∂g/∂{variable}")
        
        elif expr.has(sp.exp):
            steps.append(f"Passo 3: Aplicando regras para funções exponenciais")
            steps.append(f"Regra básica: ∂/∂x(e^x) = e^x")
            
            # Verificar se há composição de funções
            has_composition = False
            for func in expr.atoms(sp.Function):
                if func.args[0] != var and func.args[0].has(var):
                    has_composition = True
                    break
            
            if has_composition:
                steps.append(f"Passo 4: Detectada composição de funções. Aplicando a regra da cadeia:")
                steps.append(f"• Regra da cadeia para exponenciais: ∂/∂{variable}(e^(g(x))) = e^(g(x)) · ∂g/∂{variable}")
        
        elif expr.has(sp.log):
            steps.append(f"Passo 3: Aplicando regras para funções logarítmicas")
            steps.append(f"Regra básica: ∂/∂x(ln(x)) = 1/x")
            
            # Verificar se há composição de funções
            has_composition = False
            for func in expr.atoms(sp.Function):
                if func.args[0] != var and func.args[0].has(var):
                    has_composition = True
                    break
            
            if has_composition:
                steps.append(f"Passo 4: Detectada composição de funções. Aplicando a regra da cadeia:")
                steps.append(f"• Regra da cadeia para logaritmos: ∂/∂{variable}(ln(g(x))) = (1/g(x)) · ∂g/∂{variable}")
        
        # Verificar se há produtos ou quocientes
        elif any(arg.is_Mul for arg in expr.args):
            steps.append(f"Passo 3: Aplicando a regra do produto:")
            steps.append(f"• Regra do produto: ∂/∂{variable}(f(x)·g(x)) = ∂f/∂{variable}·g(x) + f(x)·∂g/∂{variable}")
            
            # Identificar os fatores
            if expr.is_Mul:
                factors = expr.args
                steps.append(f"Fatores identificados: {', '.join(str(f) for f in factors)}")
                
                # Mostrar a aplicação da regra do produto
                for i, factor in enumerate(factors):
                    other_factors = [f for j, f in enumerate(factors) if j != i]
                    other_product = sp.Mul(*other_factors)
                    steps.append(f"Termo {i+1}: ∂/∂{variable}({factor}) · ({other_product}) = {sp.diff(factor, var)} · ({other_product})")
                
                steps.append(f"Somando todos os termos...")
        
        elif expr.is_rational_function(var):
            steps.append(f"Passo 3: Aplicando a regra do quociente:")
            num, den = sp.fraction(expr)
            steps.append(f"Identificando numerador: {num}")
            steps.append(f"Identificando denominador: {den}")
            steps.append(f"• Regra do quociente: ∂/∂{variable}(f(x)/g(x)) = (g(x)·∂f/∂{variable} - f(x)·∂g/∂{variable})/g(x)²")
            
            # Mostrar a aplicação da regra do quociente
            steps.append(f"Calculando ∂/∂{variable}({num}) = {sp.diff(num, var)}")
            steps.append(f"Calculando ∂/∂{variable}({den}) = {sp.diff(den, var)}")
            steps.append(f"Aplicando a fórmula: ({den} · {sp.diff(num, var)} - {num} · {sp.diff(den, var)}) / ({den})²")
        
        # Calcular a derivada final
        derivative = sp.diff(expr, var)
        steps.append(f"Resultado final: {derivative}")
        
        # Adicionar passo de simplificação se necessário
        simplified = sp.simplify(derivative)
        if simplified != derivative:
            steps.append(f"Simplificando: {simplified}")
        
        return steps
    except Exception as e:
        st.error(f"Erro ao gerar os passos da derivação parcial: {str(e)}")
        return ["Não foi possível gerar os passos para esta expressão."]

def format_expression(expr, use_latex=True):
    """Formata uma expressão matemática para exibição."""
    if use_latex:
        return f"$${sp.latex(expr)}$$"
    return str(expr)

def display_result(title, expression, result, variable=None, order=1):
    """Exibe o resultado de um cálculo com formatação aprimorada."""
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.subheader(title)
    
    # Criar duas colunas para expressão original e resultado
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Expressão original:**")
        st.latex(sp.latex(expression))
    
    with col2:
        st.markdown("**Resultado:**")
        if variable:
            if order == 1:
                # Primeira derivada
                st.latex(f"\\frac{{d}}{{d{variable}}}({sp.latex(expression)}) = {sp.latex(result)}")
            else:
                # Derivada de ordem superior
                st.latex(f"\\frac{{d^{order}}}{{d{variable}^{order}}}({sp.latex(expression)}) = {sp.latex(result)}")
        else:
            # Caso genérico
            st.latex(sp.latex(result))
    
    # Adicionar uma linha de separação
    st.markdown("<hr style='border: 1px solid rgba(106, 43, 162, 0.3); margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Adicionar o resultado simplificado
    st.markdown("**Forma simplificada:**")
    simplified = sp.simplify(result)
    st.latex(sp.latex(simplified))
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_steps(steps, is_partial=False):
    """Exibe os passos da derivação com formatação aprimorada."""
    for i, step in enumerate(steps):
        # Verifica se o passo contém expressões matemáticas que podem ser renderizadas em LaTeX
        if "=" in step and not step.startswith("Expressão") and not step.startswith("Calculando") and not step.startswith("Aplicando") and not step.startswith("Regra") and not step.startswith("Passo") and not step.startswith("•") and not step.startswith("  Para") and not step.startswith("    -"):
            # Divide o passo em texto e expressão
            parts = step.split("=", 1)
            if len(parts) == 2:
                left, right = parts
                try:
                    # Formata o passo com LaTeX
                    formatted_step = f"{left}= ${sp.latex(sp.sympify(right.strip()))}$"
                    st.markdown(f'<div class="step-item{" partial-step" if is_partial else ""}">{formatted_step}</div>', unsafe_allow_html=True)
                except:
                    st.markdown(f'<div class="step-item{" partial-step" if is_partial else ""}">{step}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="step-item{" partial-step" if is_partial else ""}">{step}</div>', unsafe_allow_html=True)
        else:
            # Destacar passos importantes
            if step.startswith("Passo") or step.startswith("Regra") or step.startswith("•"):
                st.markdown(f'<div class="step-item{" partial-step" if is_partial else ""} important-step">{step}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="step-item{" partial-step" if is_partial else ""}">{step}</div>', unsafe_allow_html=True)

def display_partial_derivative_results(expression, results):
    """Exibe os resultados das derivadas parciais com formatação aprimorada."""
    st.markdown('<div class="result-box partial-result-box">', unsafe_allow_html=True)
    st.subheader("Resultados das Derivadas Parciais")
    
    # Expressão original
    st.markdown("**Expressão original:**")
    expr = sp.sympify(expression)
    st.latex(sp.latex(expr))
    
    # Adicionar uma linha de separação
    st.markdown("<hr style='border: 1px solid rgba(106, 43, 162, 0.3); margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Resultados das derivadas parciais
    st.markdown("**Derivadas parciais:**")
    
    # Criar colunas para os resultados
    vars_list = list(results.keys())
    cols = st.columns(min(3, len(vars_list)))
    for i, (var, result) in enumerate(results.items()):
        with cols[i % len(cols)]:
            st.markdown(f'<span class="variable-tag">∂/∂{var}</span>', unsafe_allow_html=True)
            st.latex(f"\\frac{{\partial}}{{\\partial {var}}}({sp.latex(expr)}) = {sp.latex(result)}")
    
    # Adicionar uma linha de separação
    st.markdown("<hr style='border: 1px solid rgba(106, 43, 162, 0.3); margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Mostrar formas simplificadas
    st.markdown("**Formas simplificadas:**")
    cols = st.columns(min(3, len(vars_list)))
    for i, (var, result) in enumerate(results.items()):
        with cols[i % len(cols)]:
            simplified = sp.simplify(result)
            st.markdown(f'<span class="variable-tag">∂/∂{var}</span>', unsafe_allow_html=True)
            st.latex(f"\\frac{{\partial}}{{\\partial {var}}}f = {sp.latex(simplified)}")
    
    # Adicionar uma linha de separação
    st.markdown("<hr style='border: 1px solid rgba(106, 43, 162, 0.3); margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Adicionar interpretação geométrica
    st.markdown("**Interpretação Geométrica:**")
    st.markdown("""
    As derivadas parciais representam a taxa de variação da função em relação a cada variável, 
    mantendo as outras variáveis constantes. Geometricamente:
    """)
    
    cols = st.columns(min(3, len(vars_list)))
    for i, var in enumerate(vars_list):
        with cols[i % len(cols)]:
            st.markdown(f"""
            <div class="interpretation-box">
                <span class="variable-tag">∂/∂{var}</span>
                <p>Representa a inclinação da curva na direção do eixo {var}, 
                mantendo as outras variáveis fixas.</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_3d_visualization(expression, variables):
    """Cria visualização 3D para funções de duas variáveis e suas derivadas parciais."""
    try:
        # Verificar se temos exatamente duas variáveis (x e y)
        if len(variables) != 2 or not all(var in ['x', 'y'] for var in variables):
            return None, "Visualização 3D disponível apenas para funções de x e y."
        
        # Criar símbolos SymPy
        x, y = sp.symbols('x y')
        expr = sp.sympify(expression)
        
        # Calcular derivadas parciais
        dx = sp.diff(expr, x)
        dy = sp.diff(expr, y)
        
        # Converter para funções numéricas
        f_expr = sp.lambdify((x, y), expr, "numpy")
        f_dx = sp.lambdify((x, y), dx, "numpy")
        f_dy = sp.lambdify((x, y), dy, "numpy")
        
        # Criar grade de pontos
        x_range = np.linspace(-3, 3, 50)
        y_range = np.linspace(-3, 3, 50)
        X, Y = np.meshgrid(x_range, y_range)
        
        # Calcular valores da função e derivadas
        try:
            Z = f_expr(X, Y)
            Z_dx = f_dx(X, Y)
            Z_dy = f_dy(X, Y)
            
            # Lidar com valores infinitos ou NaN
            Z = np.nan_to_num(Z, nan=0, posinf=10, neginf=-10)
            Z_dx = np.nan_to_num(Z_dx, nan=0, posinf=5, neginf=-5)
            Z_dy = np.nan_to_num(Z_dy, nan=0, posinf=5, neginf=-5)
            
            # Criar subplots: função original, derivada em x, derivada em y
            fig = make_subplots(
                rows=1, cols=3,
                specs=[[{'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}]],
                subplot_titles=[
                    f'Função f(x,y)', 
                    f'Derivada parcial ∂f/∂x', 
                    f'Derivada parcial ∂f/∂y'
                ],
                horizontal_spacing=0.05
            )
            
            # Superfície da função original
            fig.add_trace(
                go.Surface(
                    z=Z, x=X, y=Y, 
                    colorscale='Viridis',
                    name='f(x,y)'
                ),
                row=1, col=1
            )
            
            # Superfície da derivada parcial em relação a x
            fig.add_trace(
                go.Surface(
                    z=Z_dx, x=X, y=Y, 
                    colorscale='Plasma',
                    name='∂f/∂x'
                ),
                row=1, col=2
            )
            
            # Superfície da derivada parcial em relação a y
            fig.add_trace(
                go.Surface(
                    z=Z_dy, x=X, y=Y, 
                    colorscale='Cividis',
                    name='∂f/∂y'
                ),
                row=1, col=3
            )
            
            # Atualizar layout
            fig.update_layout(
                title_text=f"Visualização 3D de {expression} e suas derivadas parciais",
                height=600,
                scene=dict(
                    xaxis_title='x',
                    yaxis_title='y',
                    zaxis_title='f(x,y)',
                    aspectratio=dict(x=1, y=1, z=0.7)
                ),
                scene2=dict(
                    xaxis_title='x',
                    yaxis_title='y',
                    zaxis_title='∂f/∂x',
                    aspectratio=dict(x=1, y=1, z=0.7)
                ),
                scene3=dict(
                    xaxis_title='x',
                    yaxis_title='y',
                    zaxis_title='∂f/∂y',
                    aspectratio=dict(x=1, y=1, z=0.7)
                ),
                font=dict(
                    family="Courier New, monospace",
                    size=12,
                    color="#7eefc4"
                ),
                paper_bgcolor='rgba(20, 20, 40, 0.9)',
                plot_bgcolor='rgba(20, 20, 40, 0.9)',
                margin=dict(l=0, r=0, t=40, b=0)
            )
            
            return fig, None
            
        except Exception as e:
            return None, f"Erro ao calcular valores: {str(e)}"
            
    except Exception as e:
        return None, f"Erro ao criar visualização: {str(e)}"

def get_geometric_interpretation(expression, variables):
    """Retorna uma explicação do significado geométrico das derivadas parciais."""
    try:
        x, y, z = sp.symbols('x y z')
        expr = sp.sympify(expression)
        
        # Calcular derivadas parciais
        derivatives = {}
        for var in variables:
            derivatives[var] = sp.diff(expr, var)
        
        # Criar explicação
        explanation = f"""
        ### Significado Geométrico das Derivadas Parciais
        
        Para a função f({', '.join(variables)}) = {expr}:
        
        """
        
        # Adicionar explicação para cada variável
        for var in variables:
            explanation += f"""
            #### Derivada Parcial em relação a {var}:
            
            ∂f/∂{var} = {derivatives[var]}
            
            Esta derivada representa a taxa de variação instantânea da função quando {var} varia, 
            mantendo todas as outras variáveis constantes. Geometricamente, é a inclinação da curva 
            obtida ao cortar a superfície da função com um plano perpendicular ao eixo {var}.
            """
        
        # Adicionar explicação sobre o gradiente se tivermos múltiplas variáveis
        if len(variables) > 1:
            explanation += """
            #### Gradiente da Função:
            
            O gradiente ∇f é um vetor cujas componentes são as derivadas parciais da função:
            
            ∇f = (∂f/∂x₁, ∂f/∂x₂, ..., ∂f/∂xₙ)
            
            O gradiente tem duas propriedades importantes:
            1. Aponta na direção de maior crescimento da função
            2. É perpendicular às curvas/superfícies de nível da função
            
            A magnitude do gradiente |∇f| indica a taxa desse crescimento.
            """
        
        return explanation
    except Exception as e:
        return f"Erro ao gerar interpretação geométrica: {str(e)}"

def generate_report_html(expression, variables, results):
    """Gera um relatório HTML para as derivadas parciais."""
    x, y, z = sp.symbols('x y z')
    expr = sp.sympify(expression)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Relatório de Derivadas Parciais</title>
        <style>
            body {{
                font-family: 'Courier New', monospace;
                background-color: #121236;
                color: #e0e0e0;
                padding: 20px;
            }}
            h1, h2, h3 {{
                color: #7eefc4;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background-color: rgba(30, 30, 50, 0.7);
                padding: 20px;
                border-radius: 10px;
                border: 1px solid rgba(106, 43, 162, 0.5);
            }}
            .result-box {{
                background-color: rgba(20, 20, 40, 0.7);
                padding: 15px;
                border-radius: 5px;
                margin: 10px 0;
                border-left: 3px solid #ff00ff;
            }}
            .variable-tag {{
                display: inline-block;
                background-color: rgba(106, 43, 162, 0.5);
                color: #7eefc4;
                padding: 2px 8px;
                border-radius: 4px;
                margin-right: 5px;
                font-weight: bold;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                font-size: 0.8em;
                color: #7eefc4;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Relatório de Derivadas Parciais</h1>
            
            <h2>Função Original</h2>
            <div class="result-box">
                f({', '.join(variables)}) = {expr}
            </div>
            
            <h2>Derivadas Parciais</h2>
    """
    
    # Adicionar cada derivada parcial
    for var, result in results.items():
        html += f"""
            <div class="result-box">
                <span class="variable-tag">∂/∂{var}</span>
                <p>∂f/∂{var} = {result}</p>
                <p>Forma simplificada: {sp.simplify(result)}</p>
            </div>
        """
    
    # Adicionar interpretação geométrica
    html += f"""
            <h2>Interpretação Geométrica</h2>
            <div class="result-box">
                <p>As derivadas parciais representam a taxa de variação da função em relação a cada variável, 
                mantendo as outras variáveis constantes.</p>
                
                <p>O gradiente ∇f = ({', '.join([f'∂f/∂{var}' for var in variables])}) aponta na direção 
                de maior crescimento da função e é perpendicular às curvas de nível.</p>
            </div>
            
            <div class="footer">
                Gerado por Derivata - Calculadora de Derivadas Cyberpunk
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def create_download_link(html, filename="derivadas_parciais_relatorio.html"):
    """Cria um link para download do relatório HTML."""
    b64 = base64.b64encode(html.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="{filename}" class="download-button">Baixar Relatório HTML</a>'
    return href

# Aplicar estilo cyberpunk mais suave
st.markdown("""
<style>
    /* Fundo e gradientes - mais suave */
    .stApp {
        background: linear-gradient(135deg, #121236 0%, #1e1e4f 50%, #2a1a3a 100%);
    }
    
    /* Tipografia - reduzindo o brilho */
    h1, h2, h3 {
        color: #7eefc4 !important;
        text-shadow: 0 0 5px rgba(0, 255, 170, 0.3);
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
    }
    
    /* Containers e cards */
    .stTabs [data-baseweb="tab-panel"] {
        background-color: rgba(20, 20, 40, 0.7);
        border-radius: 10px;
        padding: 20px;
        border: 1px solid rgba(138, 43, 226, 0.2);
        box-shadow: 0 0 10px rgba(138, 43, 226, 0.1);
    }
    
    /* Botões */
    .stButton>button {
        background: linear-gradient(90deg, #6a2ba2, #7a3bd2);
        color: white;
        border: 1px solid #7eefc4;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #7a3bd2, #8a4be2);
        border: 1px solid #a0f0d0;
        box-shadow: 0 0 5px rgba(0, 255, 170, 0.3);
        transform: translateY(-2px);
    }
    
    /* Campos de entrada */
    .stTextInput>div>div>input {
        background-color: rgba(30, 30, 50, 0.7);
        color: #e0e0e0;
        border: 1px solid #6a2ba2;
        border-radius: 5px;
        padding: 10px;
    }
    .stTextInput>div>div>input:focus {
        border: 1px solid #7eefc4;
        box-shadow: 0 0 5px rgba(0, 255, 170, 0.2);
    }
    
    /* Selectbox */
    .stSelectbox>div>div>div {
        background-color: rgba(30, 30, 50, 0.7);
        color: #e0e0e0;
        border: 1px solid #6a2ba2;
        border-radius: 5px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        color: #7eefc4;
        background-color: rgba(30, 30, 50, 0.7);
        border-radius: 5px 5px 0 0;
        padding: 10px 20px;
        margin-right: 5px;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(138, 43, 226, 0.3);
        border-bottom: 2px solid #7eefc4;
        box-shadow: 0 0 5px rgba(0, 255, 170, 0.2);
    }
    
    /* Texto e markdown */
    .stMarkdown {
        color: #e0e0e0;
    }
    
    /* Tabelas */
    .stTable {
        background-color: rgba(30, 30, 50, 0.7);
        border-radius: 10px;
        overflow: hidden;
    }
    .dataframe {
        border: 1px solid #6a2ba2 !important;
    }
    .dataframe th {
        background-color: rgba(138, 43, 226, 0.3) !important;
        color: #7eefc4 !important;
        text-align: center !important;
    }
    .dataframe td {
        background-color: rgba(30, 30, 50, 0.7) !important;
        color: #e0e0e0 !important;
    }
    
    /* Efeito de brilho para resultados */
    .result-box {
        background-color: rgba(30, 30, 50, 0.7);
        border: 1px solid #6a2ba2;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 0 10px rgba(138, 43, 162, 0.2);
    }
    
    /* Animação de gradiente para cabeçalhos - mais suave */
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .header-gradient {
        background: linear-gradient(90deg, #6a2ba2, #7eefc4, #6a2ba2);
        background-size: 200% 200%;
        animation: gradient 15s ease infinite;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    /* Estilo para cards de exemplos */
    .example-card {
        background-color: rgba(30, 30, 50, 0.7);
        border: 1px solid #6a2ba2;
        border-radius: 5px;
        padding: 10px;
        margin: 5px 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .example-card:hover {
        background-color: rgba(138, 43, 226, 0.2);
        border: 1px solid #7eefc4;
        transform: translateY(-2px);
    }
    
    /* Estilo para passos da derivação */
    .step-item {
        background-color: rgba(30, 30, 50, 0.7);
        border-left: 3px solid #7eefc4;
        padding: 10px;
        margin: 10px 0;
        border-radius: 0 5px 5px 0;
    }
    
    /* Estilo específico para passos de derivadas parciais */
    .partial-step {
        background-color: rgba(30, 30, 60, 0.7);
        border-left: 3px solid #ff00ff;
    }
    
    /* Estilo para passos importantes */
    .important-step {
        background-color: rgba(40, 20, 60, 0.7);
        border-left: 5px solid #ff00ff;
        font-weight: bold;
    }
    
    /* Estilo para o resultado final da derivada parcial */
    .partial-result-box {
        background-color: rgba(25, 25, 45, 0.8);
        border: 1px solid rgba(106, 43, 162, 0.5);
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 0 15px rgba(106, 43, 162, 0.3);
    }
    
    /* Estilo para as variáveis nas derivadas parciais */
    .variable-tag {
        display: inline-block;
        background-color: rgba(106, 43, 162, 0.5);
        color: #7eefc4;
        padding: 2px 8px;
        border-radius: 4px;
        margin-right: 5px;
        font-family: monospace;
        font-weight: bold;
    }
    
    /* Estilo para a caixa de interpretação */
    .interpretation-box {
        background-color: rgba(30, 30, 50, 0.7);
        border-left: 3px solid #ff00ff;
        padding: 10px;
        margin: 10px 0;
        border-radius: 0 5px 5px 0;
    }
    
    /* Melhorar a aparência dos expanders para derivadas parciais */
    .streamlit-expanderHeader:has(span:contains("∂/∂")) {
        background: linear-gradient(90deg, rgba(30, 30, 50, 0.7), rgba(106, 43, 162, 0.3));
        border-radius: 5px;
        padding: 10px;
        border: 1px solid rgba(106, 43, 162, 0.3);
        margin-bottom: 10px;
        color: #7eefc4 !important;
        font-weight: bold;
    }
    
    /* Estilo para a tabela de resultados */
    .dataframe {
        background-color: rgba(30, 30, 50, 0.7);
        border-collapse: collapse;
        border: 1px solid rgba(106, 43, 162, 0.5);
        font-family: monospace;
    }
    
    .dataframe th {
        background-color: rgba(106, 43, 162, 0.5);
        color: #7eefc4;
        padding: 8px;
        border: 1px solid rgba(106, 43, 162, 0.3);
    }
    
    .dataframe td {
        padding: 8px;
        border: 1px solid rgba(106, 43, 162, 0.3);
    }
    
    /* Estilo para o título principal - menos brilhante */
    .main-title {
        text-align: center;
        font-size: 3rem;
        margin-bottom: 10px;
        background: -webkit-linear-gradient(#7eefc4, #70ccff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 5px rgba(0, 255, 170, 0.3);
    }
    
    /* Estilo para o subtítulo */
    .subtitle {
        text-align: center;
        color: #d070d0 !important;
        margin-bottom: 30px;
        font-size: 1.2rem;
    }
    
    /* Estilo para o logo */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .logo-container img {
        max-width: 150px;
        height: auto;
    }
    
    /* Melhorar a aparência dos expanders */
    .streamlit-expanderHeader {
        background-color: rgba(30, 30, 50, 0.7);
        border-radius: 5px;
        padding: 10px;
        border: 1px solid rgba(106, 43, 162, 0.3);
        margin-bottom: 10px;
        color: #7eefc4 !important;
        font-weight: bold;
    }
    
    .streamlit-expanderContent {
        background-color: rgba(20, 20, 40, 0.7);
        border-radius: 0 0 5px 5px;
        padding: 15px;
        border: 1px solid rgba(106, 43, 162, 0.3);
        border-top: none;
    }
    
    /* Estilo para separadores */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(126, 239, 196, 0.5), transparent);
        margin: 20px 0;
    }
    
    /* Melhorar o contraste das expressões matemáticas */
    .katex-display {
        background-color: rgba(30, 30, 50, 0.5);
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        border-left: 3px solid #7eefc4;
    }
    
    /* Estilo para o resultado final destacado */
    .final-result {
        background-color: rgba(40, 40, 60, 0.7);
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #ff00ff;
        margin: 20px 0;
        box-shadow: 0 0 10px rgba(255, 0, 255, 0.2);
    }
    
    /* Estilo para explicações de visualização */
    .visualization-explanation {
        background-color: rgba(30, 30, 50, 0.7);
        border-left: 3px solid #ff00ff;
        padding: 15px;
        margin: 15px 0;
        border-radius: 0 5px 5px 0;
    }
    
    .visualization-explanation h4 {
        color: #7eefc4;
        margin-top: 0;
        margin-bottom: 10px;
    }
    
    .visualization-explanation ul {
        margin-left: 20px;
        padding-left: 0;
    }
    
    .visualization-explanation li {
        margin-bottom: 5px;
        color: #e0e0e0;
    }
    
    .visualization-explanation p {
        margin-top: 10px;
        color: #e0e0e0;
    }
    
    /* Estilo para os gráficos Plotly */
    .js-plotly-plot {
        border: 1px solid rgba(106, 43, 162, 0.3);
        border-radius: 5px;
        box-shadow: 0 0 15px rgba(106, 43, 162, 0.2);
    }
    
    /* Estilo para os expanders de visualização */
    .streamlit-expanderHeader:has(span:contains("Visualização")) {
        background: linear-gradient(90deg, rgba(30, 30, 50, 0.7), rgba(106, 43, 162, 0.3));
        border-radius: 5px;
        padding: 10px;
        border: 1px solid rgba(106, 43, 162, 0.3);
        margin-bottom: 10px;
        color: #7eefc4 !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Exibir logo SVG e título
svg_base64 = get_svg_base64()
if svg_base64:
    st.markdown(f'<div class="logo-container"><img src="data:image/svg+xml;base64,{svg_base64}" alt="Derivata Logo"></div>', unsafe_allow_html=True)
else:
    # Fallback para título sem logo
    st.markdown('<h1 class="main-title">DERIVATA</h1>', unsafe_allow_html=True)

st.markdown('<p class="subtitle">Calculadora de Derivadas Cyberpunk</p>', unsafe_allow_html=True)

# Descrição em um container estilizado
with st.container():
    st.markdown('<div class="header-gradient">', unsafe_allow_html=True)
    st.markdown("""
    Esta aplicação calcula derivadas de expressões matemáticas usando SymPy.
    Escolha o tipo de derivada que deseja calcular e insira a expressão.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Layout em colunas para melhor organização
col1, col2 = st.columns([2, 1])

with col1:
    # Abas para diferentes tipos de derivadas
    tab1, tab2, tab3 = st.tabs(["Derivada Normal", "Derivada Parcial", "Derivada de Ordem Superior"])
    
    with tab1:
        st.markdown('<h2>Derivada Normal</h2>', unsafe_allow_html=True)
        
        # Seleção de exemplo ou entrada manual
        example_choice = st.selectbox(
            "Escolha um exemplo ou digite sua própria expressão:",
            ["Digite sua expressão"] + list(examples.keys()),
            key="normal_example"
        )
        
        if example_choice == "Digite sua expressão":
            expression = st.text_input(
                "Expressão:",
                placeholder="Ex: x**2 + 3*x + 1",
                key="normal_expression"
            )
        else:
            expression = examples[example_choice]
            st.text_input("Expressão:", value=expression, key="normal_expression_display", disabled=True)
        
        variable = st.text_input("Variável de diferenciação:", value="x", key="normal_variable")
        
        if st.button("Calcular Derivada", key="normal_calculate"):
            if expression and variable:
                try:
                    result = calculate_derivative(expression, variable)
                    if result is not None:
                        # Usar a nova função para exibir o resultado formatado
                        expr = sp.sympify(expression)
                        display_result("Resultado da Derivada", expr, result, variable)
                        
                        # Exibir passos com formatação aprimorada
                        steps = get_derivative_steps(expression, variable)
                        display_steps(steps)
                except Exception as e:
                    st.error(f"Erro ao calcular a derivada: {str(e)}")
            else:
                st.warning("Por favor, preencha todos os campos.")
    
    with tab2:
        st.markdown('<h2>Derivada Parcial</h2>', unsafe_allow_html=True)
        
        # Seleção de exemplo ou entrada manual
        example_choice = st.selectbox(
            "Escolha um exemplo ou digite sua própria expressão:",
            ["Digite sua expressão", "Função de Duas Variáveis", "Função Exponencial Multivariável", "Função Trigonométrica Multivariável", "Função Composta Multivariável"],
            key="partial_example"
        )
        
        if example_choice == "Digite sua expressão":
            expression = st.text_input(
                "Expressão multivariável:",
                placeholder="Ex: x**2 + x*y + y**2",
                key="partial_expression"
            )
        elif example_choice == "Função de Duas Variáveis":
            expression = "x**2 + x*y + y**2"
            st.text_input("Expressão:", value=expression, key="partial_expression_display", disabled=True)
        elif example_choice == "Função Exponencial Multivariável":
            expression = "exp(x*y)"
            st.text_input("Expressão:", value=expression, key="partial_expression_display", disabled=True)
        elif example_choice == "Função Trigonométrica Multivariável":
            expression = "sin(x) + cos(y)"
            st.text_input("Expressão:", value=expression, key="partial_expression_display", disabled=True)
        elif example_choice == "Função Composta Multivariável":
            expression = "sin(x*y) + exp(x+y)"
            st.text_input("Expressão:", value=expression, key="partial_expression_display", disabled=True)
        
        variables = st.text_input(
            "Variáveis (separadas por espaço):",
            value="x y",
            key="partial_variables"
        )
        
        show_steps = st.checkbox("Mostrar passo a passo", value=True, key="show_partial_steps")
        
        if st.button("Calcular Derivadas Parciais", key="partial_calculate"):
            if expression and variables:
                try:
                    vars_list = variables.split()
                    results = calculate_partial_derivatives(expression, vars_list)
                    
                    if results:
                        # Exibir resultados com formatação aprimorada
                        display_partial_derivative_results(expression, results)
                        
                        # Exibir os passos para cada variável se solicitado
                        if show_steps:
                            st.markdown("### Passo a Passo da Derivação")
                            for var in vars_list:
                                with st.expander(f"Ver passo a passo para ∂/∂{var}", expanded=False):
                                    steps = get_partial_derivative_steps(expression, var)
                                    display_steps(steps, is_partial=True)
                    
                    # Mostrar tabela de resultados em um expander
                    with st.expander("Ver tabela de resultados", expanded=False):
                        # Criar tabela de resultados estilizada com LaTeX
                        data = []
                        for var, result in results.items():
                            data.append({
                                "Variável": f"${var}$",
                                "Expressão da Derivada": f"${sp.latex(result)}$",
                                "Forma Simplificada": f"${sp.latex(sp.simplify(result))}$"
                            })
                        
                        df = pd.DataFrame(data)
                        st.table(df)
                    
                    # Adicionar visualização interativa para funções de duas variáveis
                    if len(vars_list) == 2 and all(var in ['x', 'y'] for var in vars_list):
                        with st.expander("Visualização 3D da Função e Derivadas Parciais", expanded=True):
                            # Criar visualização 3D
                            fig_3d, error_3d = create_3d_visualization(expression, vars_list)
                            if fig_3d:
                                st.plotly_chart(fig_3d, use_container_width=True)
                                
                                # Adicionar explicação
                                st.markdown("""
                                <div class="visualization-explanation">
                                    <h4>Interpretação da Visualização 3D:</h4>
                                    <ul>
                                        <li>O primeiro gráfico mostra a superfície da função f(x,y).</li>
                                        <li>O segundo gráfico mostra a derivada parcial em relação a x (∂f/∂x).</li>
                                        <li>O terceiro gráfico mostra a derivada parcial em relação a y (∂f/∂y).</li>
                                    </ul>
                                    <p>As cores indicam a altura (valor) em cada ponto. Observe como as derivadas parciais 
                                    mostram a taxa de variação da função em cada direção.</p>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.warning(f"Não foi possível criar a visualização 3D: {error_3d}")
                        
                        with st.expander("Visualização do Gradiente (Campo Vetorial)", expanded=False):
                            # Criar visualização do gradiente
                            fig_grad, error_grad = create_gradient_visualization(expression, vars_list)
                            if fig_grad:
                                st.plotly_chart(fig_grad, use_container_width=True)
                                
                                # Adicionar explicação
                                st.markdown("""
                                <div class="visualization-explanation">
                                    <h4>Interpretação do Gradiente:</h4>
                                    <p>O gradiente ∇f(x,y) = (∂f/∂x, ∂f/∂y) é um vetor que:</p>
                                    <ul>
                                        <li>Aponta na direção de maior crescimento da função.</li>
                                        <li>Tem magnitude proporcional à taxa desse crescimento.</li>
                                        <li>É perpendicular às curvas de nível (contornos) da função.</li>
                                    </ul>
                                    <p>No gráfico acima, as linhas coloridas são as curvas de nível da função, 
                                    e as setas roxas representam o gradiente em cada ponto.</p>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.warning(f"Não foi possível criar a visualização do gradiente: {error_grad}")
                except Exception as e:
                    st.error(f"Erro ao calcular as derivadas parciais: {str(e)}")
            else:
                st.warning("Por favor, preencha todos os campos.")
    
    with tab3:
        st.markdown('<h2>Derivada de Ordem Superior</h2>', unsafe_allow_html=True)
        
        # Seleção de exemplo ou entrada manual
        example_choice = st.selectbox(
            "Escolha um exemplo ou digite sua própria expressão:",
            ["Digite sua expressão", "Polinômio de Ordem 3", "Função Trigonométrica", "Função Exponencial"],
            key="higher_example"
        )
        
        if example_choice == "Digite sua expressão":
            expression = st.text_input(
                "Expressão:",
                placeholder="Ex: x**3 + 2*x**2 + 3*x + 4",
                key="higher_expression"
            )
        elif example_choice == "Polinômio de Ordem 3":
            expression = "x**3 + 2*x**2 + 3*x + 4"
            st.text_input("Expressão:", value=expression, key="higher_expression_display", disabled=True)
        elif example_choice == "Função Trigonométrica":
            expression = "sin(x)"
            st.text_input("Expressão:", value=expression, key="higher_expression_display", disabled=True)
        elif example_choice == "Função Exponencial":
            expression = "exp(x)"
            st.text_input("Expressão:", value=expression, key="higher_expression_display", disabled=True)
        
        variable = st.text_input("Variável de diferenciação:", value="x", key="higher_variable")
        
        order = st.number_input(
            "Ordem da derivada:",
            min_value=1,
            max_value=10,
            value=2,
            step=1,
            key="higher_order"
        )
        
        if st.button("Calcular Derivada de Ordem Superior", key="higher_calculate"):
            if expression and variable:
                try:
                    result = calculate_derivative(expression, variable, order)
                    if result is not None:
                        # Usar a nova função para exibir o resultado formatado
                        expr = sp.sympify(expression)
                        display_result("Resultado da Derivada de Ordem Superior", expr, result, variable, order)
                except Exception as e:
                    st.error(f"Erro ao calcular a derivada: {str(e)}")
            else:
                st.warning("Por favor, preencha todos os campos.")

with col2:
    # Adicionar informações sobre notação
    st.markdown('<h3>Notação Suportada</h3>', unsafe_allow_html=True)
    st.markdown("""
    ### Operadores:
    - Adição: `+`
    - Subtração: `-`
    - Multiplicação: `*`
    - Divisão: `/`
    - Potência: `**`

    ### Funções:
    - Trigonométricas: `sin(x)`, `cos(x)`, `tan(x)`
    - Exponencial: `exp(x)`
    - Logaritmo: `log(x)`
    - Raiz quadrada: `sqrt(x)`

    ### Exemplos:
    - Polinômio: `x**2 + 3*x + 1`
    - Trigonométrica: `sin(x) + cos(x)`
    - Exponencial: `exp(x**2)`
    - Logarítmica: `log(x**2 + 1)`
    - Composta: `sin(exp(x))`
    """)

    # Adicionar informações sobre o projeto
    st.markdown('<h3>Sobre</h3>', unsafe_allow_html=True)
    st.markdown("""
    Esta aplicação foi desenvolvida usando:
    - Streamlit para a interface web
    - SymPy para cálculos simbólicos

    Desenvolvido para fins educacionais.
    """)
