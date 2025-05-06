import streamlit as st
import sympy as sp
import pandas as pd

def calculate_derivative(expression, variable, order=1):
    """Calculate the derivative of an expression with respect to a variable."""
    x, y, z = sp.symbols('x y z')
    expr = sp.sympify(expression)
    derivative = sp.diff(expr, variable, order)
    return derivative

def calculate_partial_derivatives(expression, variables):
    """Calculate all partial derivatives for a multivariate function."""
    x, y, z = sp.symbols('x y z')
    expr = sp.sympify(expression)
    
    results = {}
    for var in variables:
        results[var] = sp.diff(expr, var)
    
    return results

def get_derivative_steps(expression, variable):
    """Get steps for calculating a derivative."""
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

# Configuração da página
st.set_page_config(
    page_title="Calculadora de Derivadas",
    page_icon="📊",
    layout="centered"
)

# Título e descrição
st.title("Calculadora de Derivadas")
st.markdown("""
Esta aplicação calcula derivadas de expressões matemáticas usando SymPy.
Escolha o tipo de derivada que deseja calcular e insira a expressão.
""")

# Exemplos de expressões
examples = {
    "Polinômio": "x**2 + 3*x + 1",
    "Trigonométrica": "sin(x)",
    "Exponencial": "exp(x)",
    "Logarítmica": "log(x)",
    "Produto": "x*sin(x)",
    "Cadeia": "sin(x**2)",
    "Quociente": "(x**2 + 1)/(x - 2)",
    "Multivariável": "x**2 + x*y + y**2"
}

# Abas para diferentes tipos de derivadas
tab1, tab2, tab3 = st.tabs(["Derivada Normal", "Derivada Parcial", "Derivada de Ordem Superior"])

with tab1:
    st.header("Derivada Normal")
    
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
                
                # Exibir resultado
                st.subheader("Resultado:")
                st.latex(f"\\frac{{d}}{{d{variable}}}({expression}) = {result}")
                
                # Exibir passos
                st.subheader("Passos da derivação:")
                steps = get_derivative_steps(expression, variable)
                for step in steps:
                    st.markdown(f"- {step}")
            except Exception as e:
                st.error(f"Erro ao calcular a derivada: {str(e)}")
        else:
            st.warning("Por favor, preencha todos os campos.")

with tab2:
    st.header("Derivada Parcial")
    
    # Seleção de exemplo ou entrada manual
    example_choice = st.selectbox(
        "Escolha um exemplo ou digite sua própria expressão:",
        ["Digite sua expressão", "Função de Duas Variáveis", "Função Exponencial Multivariável", "Função Trigonométrica Multivariável"],
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
    
    variables = st.text_input(
        "Variáveis (separadas por espaço):",
        value="x y",
        key="partial_variables"
    )
    
    if st.button("Calcular Derivadas Parciais", key="partial_calculate"):
        if expression and variables:
            try:
                vars_list = variables.split()
                results = calculate_partial_derivatives(expression, vars_list)
                
                # Exibir resultados
                st.subheader("Resultados:")
                for var, result in results.items():
                    st.latex(f"\\frac{{\partial}}{{\partial {var}}}({expression}) = {result}")
                
                # Criar tabela de resultados
                df = pd.DataFrame({
                    "Variável": list(results.keys()),
                    "Derivada Parcial": [str(results[var]) for var in results.keys()]
                })
                st.table(df)
            except Exception as e:
                st.error(f"Erro ao calcular as derivadas parciais: {str(e)}")
        else:
            st.warning("Por favor, preencha todos os campos.")

with tab3:
    st.header("Derivada de Ordem Superior")
    
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
                
                # Exibir resultado
                st.subheader("Resultado:")
                st.latex(f"\\frac{{d^{order}}}{{d{variable}^{order}}}({expression}) = {result}")
            except Exception as e:
                st.error(f"Erro ao calcular a derivada: {str(e)}")
        else:
            st.warning("Por favor, preencha todos os campos.")

# Adicionar informações sobre notação
st.sidebar.header("Notação Suportada")
st.sidebar.markdown("""
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
st.sidebar.header("Sobre")
st.sidebar.info("""
Esta aplicação foi desenvolvida usando:
- Streamlit para a interface web
- SymPy para cálculos simbólicos

Desenvolvido para fins educacionais.
""")