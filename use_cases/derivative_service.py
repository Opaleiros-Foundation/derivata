"""
Serviço para cálculo de derivadas.
Implementa os casos de uso relacionados a derivadas.
"""
from typing import List, Dict, Optional, Union
from domain.models import Expression, DerivativeResult
from adapters.sympy_adapter import SymPyAdapter


class DerivativeService:
    """Serviço para cálculo de derivadas."""
    
    def __init__(self, sympy_adapter: SymPyAdapter):
        self.sympy_adapter = sympy_adapter
    
    def calculate_derivative(self, expression_str: str, variable: str, order: int = 1) -> Optional[DerivativeResult]:
        """Calcula a derivada de uma expressão."""
        try:
            # Identificar variáveis na expressão
            variables = self._extract_variables(expression_str)
            
            # Verificar se a variável de diferenciação está presente
            if variable not in variables:
                variables.append(variable)
            
            # Criar objeto Expression
            expression = Expression(raw_expression=expression_str, variables=variables)
            
            # Calcular a derivada
            result = self.sympy_adapter.calculate_derivative(expression, variable, order)
            
            return result
        except Exception as e:
            print(f"Erro no serviço de derivadas: {str(e)}")
            return None
    
    def get_derivative_steps(self, expression_str: str, variable: str) -> List[str]:
        """Obtém os passos para o cálculo de uma derivada."""
        try:
            # Identificar variáveis na expressão
            variables = self._extract_variables(expression_str)
            
            # Verificar se a variável de diferenciação está presente
            if variable not in variables:
                variables.append(variable)
            
            # Criar objeto Expression
            expression = Expression(raw_expression=expression_str, variables=variables)
            
            # Calcular a derivada para obter os passos
            result = self.sympy_adapter.calculate_derivative(expression, variable)
            
            if result:
                return result.steps
            return ["Não foi possível gerar os passos para esta expressão."]
        except Exception as e:
            print(f"Erro ao gerar passos da derivada: {str(e)}")
            return ["Não foi possível gerar os passos para esta expressão."]
    
    def _extract_variables(self, expression_str: str) -> List[str]:
        """Extrai as variáveis de uma expressão."""
        import sympy as sp
        
        try:
            expr = sp.sympify(expression_str)
            return [str(symbol) for symbol in expr.free_symbols]
        except Exception:
            # Fallback: tentar extrair variáveis por análise de string
            import re
            potential_vars = re.findall(r'[a-zA-Z]', expression_str)
            return list(set(potential_vars))