"""
Componente para a aba de derivadas de ordem superior.
"""
import streamlit as st
import sympy as sp
from domain.models import Expression
from use_cases.derivative_service import DerivativeService
from presentation.styles.cyberpunk_theme import display_result, display_steps


def render_higher_order_tab(derivative_service: DerivativeService):
    """Renderiza a aba de derivadas de ordem superior."""
    st.markdown('<h2>Derivada de Ordem Superior</h2>', unsafe_allow_html=True)
    
    # Exemplos de funções
    examples = {
        "Polinômio de Ordem 3": "x**3 + 2*x**2 + 3*x + 4",
        "Função Trigonométrica": "sin(x)",
        "Função Exponencial": "exp(x)"
    }
    
    # Seleção de exemplo ou entrada manual
    example_choice = st.selectbox(
        "Escolha um exemplo ou digite sua própria expressão:",
        ["Digite sua expressão"] + list(examples.keys()),
        key="higher_example"
    )
    
    if example_choice == "Digite sua expressão":
        expression = st.text_input(
            "Expressão:",
            placeholder="Ex: x**3 + 2*x**2 + 3*x + 4",
            key="higher_expression"
        )
    else:
        expression = examples[example_choice]
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
                # Calcular a derivada de ordem superior
                result = derivative_service.calculate_derivative(expression, variable, order)
                
                if result:
                    # Exibir o resultado formatado
                    display_result(
                        "Resultado da Der