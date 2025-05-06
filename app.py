import streamlit as st
import sympy as sp
import pandas as pd
import os
import base64

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

def display_steps(steps):
    """Exibe os passos da derivação com formatação aprimorada."""
    with st.expander("Ver passo a passo da derivação", expanded=False):
        for i, step in enumerate(steps):
            # Verifica se o passo contém expressões matemáticas que podem ser renderizadas em LaTeX
            if "=" in step and not step.startswith("Expressão") and not step.startswith("Calculando") and not step.startswith("Aplicando") and not step.startswith("Regra"):
                # Divide o passo em texto e expressão
                parts = step.split("=", 1)
                if len(parts) == 2:
                    left, right = parts
                    try:
                        # Formata o passo com LaTeX
                        formatted_step = f"{left}= ${sp.latex(sp.sympify(right.strip()))}$"
                        st.markdown(f'<div class="step-item">{formatted_step}</div>', unsafe_allow_html=True)
                    except:
                        # Se não conseguir converter para LaTeX, mostra o texto original
                        st.markdown(f'<div class="step-item">{step}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="step-item">{step}</div>', unsafe_allow_html=True)
            else:
                # Para passos sem expressões matemáticas ou que não devem ser processados
                st.markdown(f'<div class="step-item">{step}</div>', unsafe_allow_html=True)

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
        box-shadow: 0 0 10px rgba(138, 43, 226, 0.2);
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
                    
                    if results:
                        # Exibir resultados com formatação aprimorada
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.subheader("Resultados das Derivadas Parciais:")
                        
                        expr = sp.sympify(expression)
                        for var, result in results.items():
                            st.latex(f"\\frac{{\partial}}{{\\partial {var}}}({sp.latex(expr)}) = {sp.latex(result)}")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Criar tabela de resultados estilizada com LaTeX
                        data = []
                        for var, result in results.items():
                            data.append({
                                "Variável": f"${var}$",
                                "Expressão da Derivada": f"${sp.latex(result)}$"
                            })
                        
                        df = pd.DataFrame(data)
                        st.table(df)
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
