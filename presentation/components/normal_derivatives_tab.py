"""
Componente para a aba de derivadas normais.
"""
import streamlit as st
import sympy as sp
from domain.models import Expression
from use_cases.derivative_service import DerivativeService
from presentation.styles.cyberpunk_theme import display_result, display_steps


def render_normal_derivatives_tab(derivative_service: DerivativeService):
    """Renderiza a aba de derivadas normais."""
    st.markdown('<h2>Derivada Normal</h2>', unsafe_allow_html=True)
    
    # Exemplos de funções
    examples = {
        "Polinômio Simples": "x**2 + 3*x + 1",
        "Função Trigonométrica": "sin(x) + cos(x)",
        "Função Exponencial": "exp(x**2)",
        "Função Logarítmica": "log(x**2 + 1)",
        "Função Composta": "sin(exp(x))"
    }
    
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
                # Calcular a derivada
                result = derivative_service.calculate_derivative(expression, variable)
                
                if result:
                    # Exibir o resultado formatado
                    display_result(
                        "Resultado da Derivada",
                        result.original_expression.sympy_expr,
                        result.result,
                        variable
                    )
                    
                    # Exibir passos com formatação aprimorada
                    display_steps(result.steps)
                else:
                    st.error("Não foi possível calcular a derivada.")
            except Exception as e:
                st.error(f"Erro ao calcular a derivada: {str(e)}")
        else:
            st.warning("Por favor, preencha todos os campos.")