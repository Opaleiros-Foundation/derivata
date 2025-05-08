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
                        "Resultado da Derivada de Ordem Superior",
                        result.original_expression.sympy_expr,
                        result.result,
                        variable,
                        order
                    )
                    
                    # Exibir passos com formatação aprimorada
                    display_steps(result.steps)
                    
                    # Adicionar explicação sobre derivadas de ordem superior
                    with st.expander("Sobre Derivadas de Ordem Superior", expanded=False):
                        st.markdown("""
                        <div class="interpretation-box">
                            <h4>O que são derivadas de ordem superior?</h4>
                            <p>
                                Derivadas de ordem superior são obtidas aplicando o processo de derivação 
                                repetidamente a uma função. Por exemplo:
                            </p>
                            <ul>
                                <li>A primeira derivada (ordem 1) representa a taxa de variação da função original.</li>
                                <li>A segunda derivada (ordem 2) representa a taxa de variação da primeira derivada, 
                                ou a aceleração da função original.</li>
                                <li>A terceira derivada (ordem 3) representa a taxa de variação da segunda derivada, 
                                e assim por diante.</li>
                            </ul>
                            <p>
                                Em física, por exemplo, se f(t) representa a posição de um objeto em função do tempo, 
                                então f'(t) é a velocidade, f''(t) é a aceleração, e f'''(t) é a taxa de variação da aceleração.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Adicionar análise do comportamento da função
                    if order == 2:
                        with st.expander("Análise de Concavidade", expanded=True):
                            st.markdown("""
                            <div class="interpretation-box">
                                <h4>Análise de Concavidade</h4>
                                <p>
                                    A segunda derivada de uma função nos dá informações sobre sua concavidade:
                                </p>
                                <ul>
                                    <li>Se f''(x) > 0, a função é côncava para cima (formato de U).</li>
                                    <li>Se f''(x) < 0, a função é côncava para baixo (formato de ∩).</li>
                                    <li>Se f''(x) = 0, pode haver um ponto de inflexão (mudança de concavidade).</li>
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.error("Não foi possível calcular a derivada de ordem superior.")
            except Exception as e:
                st.error(f"Erro ao calcular a derivada de ordem superior: {str(e)}")
        else:
            st.warning("Por favor, preencha todos os campos.")