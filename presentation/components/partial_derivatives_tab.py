"""
Componente para a aba de derivadas parciais.
"""
import streamlit as st
import sympy as sp
import pandas as pd
from domain.models import Expression
from use_cases.partial_derivative_service import PartialDerivativeService
from use_cases.visualization_service import VisualizationService
from presentation.styles.cyberpunk_theme import (
    display_partial_derivative_result,
    display_partial_derivative_steps,
    display_geometric_interpretation,
    display_critical_points,
    display_visualization,
    display_gradient_visualization
)


def render_partial_derivatives_tab(
    partial_derivative_service: PartialDerivativeService,
    visualization_service: VisualizationService
):
    """Renderiza a aba de derivadas parciais."""
    st.markdown('<h2>Derivada Parcial</h2>', unsafe_allow_html=True)
    
    # Exemplos de funções multivariáveis
    examples = {
        "Função de Duas Variáveis": "x**2 + x*y + y**2",
        "Função Exponencial Multivariável": "exp(x*y)",
        "Função Trigonométrica Multivariável": "sin(x) + cos(y)",
        "Função Composta Multivariável": "sin(x*y) + exp(x+y)"
    }
    
    # Seleção de exemplo ou entrada manual
    example_choice = st.selectbox(
        "Escolha um exemplo ou digite sua própria expressão:",
        ["Digite sua expressão"] + list(examples.keys()),
        key="partial_example"
    )
    
    if example_choice == "Digite sua expressão":
        expression = st.text_input(
            "Expressão multivariável:",
            placeholder="Ex: x**2 + x*y + y**2",
            key="partial_expression"
        )
    else:
        expression = examples[example_choice]
        st.text_input("Expressão:", value=expression, key="partial_expression_display", disabled=True)
    
    # Entrada de variáveis
    variables_input = st.text_input(
        "Variáveis (separadas por vírgula):",
        value="x, y",
        key="partial_variables"
    )
    
    # Processar variáveis
    variables = [var.strip() for var in variables_input.split(",") if var.strip()]
    
    # Botão para calcular
    if st.button("Calcular Derivadas Parciais", key="partial_calculate"):
        if expression and variables:
            try:
                # Calcular derivadas parciais
                result = partial_derivative_service.calculate_partial_derivatives(expression, variables)
                
                if result:
                    # Criar objeto Expression para exibição
                    expr = Expression(raw_expression=expression, variables=variables)
                    
                    # Exibir resultados
                    display_partial_derivative_result(
                        "Resultados das Derivadas Parciais",
                        expr.sympy_expr,
                        result.derivatives,
                        variables
                    )
                    
                    # Exibir passos para cada derivada parcial
                    with st.expander("Ver passos das derivações", expanded=False):
                        for var in variables:
                            if var in result.steps:
                                display_partial_derivative_steps(var, result.steps[var])
                    
                    # Exibir interpretação geométrica
                    with st.expander("Interpretação Geométrica", expanded=False):
                        interpretation = partial_derivative_service.get_geometric_interpretation(expression, variables)
                        display_geometric_interpretation(interpretation)
                    
                    # Encontrar pontos críticos
                    critical_points = partial_derivative_service.find_critical_points(expression, variables)
                    if critical_points:
                        with st.expander("Pontos Críticos", expanded=True):
                            display_critical_points(critical_points)
                    
                    # Mostrar tabela de resultados em um expander
                    with st.expander("Ver tabela de resultados", expanded=False):
                        # Criar tabela de resultados estilizada com LaTeX
                        data = []
                        for var, derivative in result.derivatives.items():
                            data.append({
                                "Variável": f"${var}$",
                                "Expressão da Derivada": f"${sp.latex(derivative)}$",
                                "Forma Simplificada": f"${sp.latex(sp.simplify(derivative))}$"
                            })
                        
                        df = pd.DataFrame(data)
                        st.table(df)
                    
                    # Adicionar visualização interativa para funções de duas variáveis
                    if len(variables) == 2 and all(var in ['x', 'y'] for var in variables):
                        with st.expander("Visualização 3D da Função e Derivadas Parciais", expanded=True):
                            # Criar visualização 3D
                            fig_3d, error_3d = visualization_service.create_3d_visualization(expression, variables)
                            display_visualization(fig_3d, error_3d)
                        
                        with st.expander("Visualização do Gradiente", expanded=True):
                            # Criar visualização do gradiente
                            fig_grad, error_grad = visualization_service.create_gradient_visualization(expression, variables)
                            display_gradient_visualization(fig_grad, error_grad)
                
                else:
                    st.error("Não foi possível calcular as derivadas parciais.")
            
            except Exception as e:
                st.error(f"Erro ao calcular as derivadas parciais: {str(e)}")
        else:
            st.warning("Por favor, preencha todos os campos.")