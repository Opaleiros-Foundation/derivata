"""
Aplicação principal Derivata - Calculadora de Derivadas Cyberpunk.
"""
import streamlit as st
import sympy as sp

# Importar adaptadores
from adapters.sympy_adapter import SymPyAdapter
from adapters.plotly_adapter import PlotlyAdapter

# Importar serviços
from use_cases.derivative_service import DerivativeService
from use_cases.partial_derivative_service import PartialDerivativeService
from use_cases.visualization_service import VisualizationService

# Importar componentes de apresentação
from presentation.components.normal_derivatives_tab import render_normal_derivatives_tab
from presentation.components.partial_derivatives_tab import render_partial_derivatives_tab
from presentation.components.higher_order_tab import render_higher_order_tab
from presentation.styles.cyberpunk_theme import apply_cyberpunk_theme, display_header, display_footer


def main():
    """Função principal da aplicação."""
    # Configurar a página
    st.set_page_config(
        page_title="Derivata - Calculadora de Derivadas Cyberpunk",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Aplicar tema cyberpunk
    apply_cyberpunk_theme()
    
    # Exibir cabeçalho
    display_header()
    
    # Inicializar adaptadores
    sympy_adapter = SymPyAdapter()
    plotly_adapter = PlotlyAdapter()
    
    # Inicializar serviços
    derivative_service = DerivativeService(sympy_adapter)
    partial_derivative_service = PartialDerivativeService(sympy_adapter)
    visualization_service = VisualizationService(plotly_adapter, sympy_adapter)
    
    # Layout em colunas para melhor organização
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Abas para diferentes tipos de derivadas
        tab1, tab2, tab3 = st.tabs(["Derivada Normal", "Derivada Parcial", "Derivada de Ordem Superior"])
        
        with tab1:
            render_normal_derivatives_tab(derivative_service)
        
        with tab2:
            render_partial_derivatives_tab(partial_derivative_service, visualization_service)
        
        with tab3:
            render_higher_order_tab(derivative_service)
    
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
        - Plotly para visualizações interativas
        
        O código-fonte está disponível no [GitHub](https://github.com/seu-usuario/derivata).
        """)
    
    # Exibir rodapé
    display_footer()


if __name__ == "__main__":
    main()