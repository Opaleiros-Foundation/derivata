"""
Serviço para visualização de funções e derivadas.
Implementa os casos de uso relacionados a visualizações.
"""
from typing import List, Dict, Optional, Union, Tuple
import plotly.graph_objects as go
from domain.models import Expression, PartialDerivativeResult
from adapters.plotly_adapter import PlotlyAdapter
from adapters.sympy_adapter import SymPyAdapter


class VisualizationService:
    """Serviço para visualização de funções e derivadas."""
    
    def __init__(self, plotly_adapter: PlotlyAdapter, sympy_adapter: SymPyAdapter):
        self.plotly_adapter = plotly_adapter
        self.sympy_adapter = sympy_adapter
    
    def create_3d_visualization(self, expression_str: str, variables: List[str]) -> Tuple[Optional[go.Figure], Optional[str]]:
        """Cria visualização 3D para funções de duas variáveis e suas derivadas parciais."""
        try:
            # Criar objeto Expression
            expression = Expression(raw_expression=expression_str, variables=variables)
            
            # Calcular derivadas parciais
            partial_derivatives = self.sympy_adapter.calculate_partial_derivatives(expression)
            
            if not partial_derivatives:
                return None, "Não foi possível calcular as derivadas parciais."
            
            # Criar visualização 3D
            fig, error = self.plotly_adapter.create_3d_visualization(expression, partial_derivatives)
            
            return fig, error
        except Exception as e:
            return None, f"Erro ao criar visualização 3D: {str(e)}"
    
    def create_gradient_visualization(self, expression_str: str, variables: List[str]) -> Tuple[Optional[go.Figure], Optional[str]]:
        """Cria visualização 2D do gradiente (vetores de derivadas parciais)."""
        try:
            # Criar objeto Expression
            expression = Expression(raw_expression=expression_str, variables=variables)
            
            # Calcular derivadas parciais
            partial_derivatives = self.sympy_adapter.calculate_partial_derivatives(expression)
            
            if not partial_derivatives:
                return None, "Não foi possível calcular as derivadas parciais."
            
            # Criar visualização do gradiente
            fig, error = self.plotly_adapter.create_gradient_visualization(expression, partial_derivatives)
            
            return fig, error
        except Exception as e:
            return None, f"Erro ao criar visualização do gradiente: {str(e)}"