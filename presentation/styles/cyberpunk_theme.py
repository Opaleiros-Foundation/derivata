"""
Definição do tema cyberpunk para a aplicação.
"""
import streamlit as st


def apply_cyberpunk_theme():
    """Aplica o tema cyberpunk à aplicação Streamlit."""
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


def get_svg_base64():
    """Carrega o logo SVG como base64."""
    import base64
    try:
        with open("static/logo.svg", "r") as file:
            svg_content = file.read()
            b64 = base64.b64encode(svg_content.encode()).decode()
            return b64
    except Exception as e:
        print(f"Erro ao carregar o logo SVG: {str(e)}")
        return None


def display_logo():
    """Exibe o logo da aplicação."""
    svg_base64 = get_svg_base64()
    if svg_base64:
        st.markdown(
            f'<div class="logo-container"><img src="data:image/svg+xml;base64,{svg_base64}" alt="Derivata Logo"></div>',
            unsafe_allow_html=True
        )
    else:
        # Fallback para título sem logo
        st.markdown('<h1 class="main-title">DERIVATA</h1>', unsafe_allow_html=True)


def display_header():
    """Exibe o cabeçalho da aplicação."""
    display_logo()
    st.markdown('<p class="subtitle">Calculadora de Derivadas Cyberpunk</p>', unsafe_allow_html=True)
    
    # Descrição em um container estilizado
    with st.container():
        st.markdown('<div class="header-gradient">', unsafe_allow_html=True)
        st.markdown("""
        Esta aplicação calcula derivadas de expressões matemáticas usando SymPy.
        Escolha o tipo de derivada que deseja calcular e insira a expressão.
        """)
        st.markdown('</div>', unsafe_allow_html=True)


def display_result(title, expression, result, variable=None, order=1):
    """Exibe o resultado de um cálculo com formatação aprimorada."""
    import sympy as sp
    
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
    
    st.markdown('</div>', unsafe_allow_html=True)


def display_steps(steps):
    """Exibe os passos de uma derivação com formatação aprimorada."""
    st.markdown("### Passos da Derivação")
    
    for i, step in enumerate(steps):
        # Determinar se é um passo importante
        is_important = "Resultado final" in step or "Simplificando" in step
        
        # Aplicar classe CSS apropriada
        if is_important:
            st.markdown(f'<div class="step-item important-step">{step}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="step-item">{step}</div>', unsafe_allow_html=True)


def display_partial_derivative_result(title, expression, results, variables):
    """Exibe o resultado de derivadas parciais com formatação aprimorada."""
    import sympy as sp
    
    st.markdown('<div class="partial-result-box">', unsafe_allow_html=True)
    st.subheader(title)
    
    # Expressão original
    st.markdown("**Expressão original:**")
    st.latex(sp.latex(expression))
    
    # Resultados das derivadas parciais
    st.markdown("**Derivadas Parciais:**")
    
    # Criar colunas para cada derivada parcial
    cols = st.columns(len(results))
    
    for i, (var, result) in enumerate(results.items()):
        with cols[i]:
            st.markdown(f'<span class="variable-tag">∂/∂{var}</span>', unsafe_allow_html=True)
            st.latex(f"\\frac{{\partial}}{{\partial {var}}}({sp.latex(expression)}) = {sp.latex(result)}")
    
    st.markdown('</div>', unsafe_allow_html=True)


def display_partial_derivative_steps(var, steps):
    """Exibe os passos de uma derivada parcial com formatação aprimorada."""
    st.markdown(f'<h4>Passos para ∂/∂{var}</h4>', unsafe_allow_html=True)
    
    for i, step in enumerate(steps):
        # Determinar se é um passo importante
        is_important = "Resultado final" in step or "Simplificando" in step
        
        # Aplicar classe CSS apropriada
        if is_important:
            st.markdown(f'<div class="step-item partial-step important-step">{step}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="step-item partial-step">{step}</div>', unsafe_allow_html=True)


def display_geometric_interpretation(interpretation):
    """Exibe a interpretação geométrica das derivadas parciais."""
    st.markdown('<div class="interpretation-box">', unsafe_allow_html=True)
    st.markdown(interpretation, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def display_critical_points(critical_points):
    """Exibe os pontos críticos de uma função multivariável."""
    if not critical_points:
        st.warning("Não foram encontrados pontos críticos para esta função.")
        return
    
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.subheader("Pontos Críticos")
    
    for i, point in enumerate(critical_points):
        coords = ", ".join([f"{var} = {val}" for var, val in point.coordinates.items()])
        
        # Classificação do ponto crítico
        if point.classification == "minimum":
            classification = "Mínimo local"
            emoji = "🔽"
        elif point.classification == "maximum":
            classification = "Máximo local"
            emoji = "🔼"
        elif point.classification == "saddle":
            classification = "Ponto de sela"
            emoji = "↔️"
        else:
            classification = "Classificação indeterminada"
            emoji = "❓"
        
        st.markdown(f"**Ponto {i+1}:** ({coords}) {emoji}")
        st.markdown(f"**Classificação:** {classification}")
        st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def display_visualization(fig, error=None):
    """Exibe uma visualização com formatação aprimorada."""
    if error:
        st.error(error)
        return
    
    if fig:
        st.plotly_chart(fig, use_container_width=True)
        
        # Adicionar explicação
        st.markdown('<div class="visualization-explanation">', unsafe_allow_html=True)
        st.markdown("""
        <h4>Como interpretar este gráfico:</h4>
        <ul>
            <li>A superfície à esquerda mostra a função original f(x,y).</li>
            <li>A superfície do meio mostra a derivada parcial em relação a x (∂f/∂x).</li>
            <li>A superfície à direita mostra a derivada parcial em relação a y (∂f/∂y).</li>
        </ul>
        <p>As cores indicam a altura (valor) de cada função em cada ponto (x,y).</p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def display_gradient_visualization(fig, error=None):
    """Exibe uma visualização do gradiente com formatação aprimorada."""
    if error:
        st.error(error)
        return
    
    if fig:
        st.plotly_chart(fig, use_container_width=True)
        
        # Adicionar explicação
        st.markdown('<div class="visualization-explanation">', unsafe_allow_html=True)
        st.markdown("""
        <h4>Como interpretar este gráfico:</h4>
        <ul>
            <li>À esquerda: As curvas de nível da função f(x,y) - linhas onde a função tem o mesmo valor.</li>
            <li>À direita: O campo vetorial do gradiente ∇f - cada seta aponta na direção de maior crescimento da função.</li>
        </ul>
        <p>Observe que os vetores do gradiente são perpendiculares às curvas de nível da função.</p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def create_example_card(title, expression, on_click=None):
    """Cria um card para um exemplo de expressão."""
    html = f"""
    <div class="example-card" onclick="{on_click}">
        <strong>{title}</strong><br>
        <code>{expression}</code>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def display_footer():
    """Exibe o rodapé da aplicação."""
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #7eefc4; font-size: 0.8rem;">
        Derivata - Calculadora de Derivadas Cyberpunk © 2023<br>
        Desenvolvido com Streamlit, SymPy e Plotly
    </div>
    """, unsafe_allow_html=True)