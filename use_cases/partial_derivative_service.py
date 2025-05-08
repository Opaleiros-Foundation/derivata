"""
Serviço para cálculo de derivadas parciais.
Implementa os casos de uso relacionados a derivadas parciais.
"""
from typing import List, Dict, Optional, Union, Tuple
from domain.models import Expression, PartialDerivativeResult, CriticalPoint
from adapters.sympy_adapter import SymPyAdapter


class PartialDerivativeService:
    """Serviço para cálculo de derivadas parciais."""
    
    def __init__(self, sympy_adapter: SymPyAdapter):
        self.sympy_adapter = sympy_adapter
    
    def calculate_partial_derivatives(self, expression_str: str, variables: List[str]) -> Optional[PartialDerivativeResult]:
        """Calcula todas as derivadas parciais para uma função multivariável."""
        try:
            # Criar objeto Expression
            expression = Expression(raw_expression=expression_str, variables=variables)
            
            # Calcular as derivadas parciais
            result = self.sympy_adapter.calculate_partial_derivatives(expression)
            
            return result
        except Exception as e:
            print(f"Erro no serviço de derivadas parciais: {str(e)}")
            return None
    
    def get_partial_derivative_steps(self, expression_str: str, variable: str) -> List[str]:
        """Obtém os passos para o cálculo de uma derivada parcial."""
        try:
            # Identificar variáveis na expressão
            all_variables = self._extract_variables(expression_str)
            
            # Verificar se a variável de diferenciação está presente
            if variable not in all_variables:
                all_variables.append(variable)
            
            # Criar objeto Expression
            expression = Expression(raw_expression=expression_str, variables=all_variables)
            
            # Calcular as derivadas parciais para obter os passos
            result = self.sympy_adapter.calculate_partial_derivatives(expression)
            
            if result and variable in result.steps:
                return result.steps[variable]
            return ["Não foi possível gerar os passos para esta derivada parcial."]
        except Exception as e:
            print(f"Erro ao gerar passos da derivada parcial: {str(e)}")
            return ["Não foi possível gerar os passos para esta derivada parcial."]
    
    def find_critical_points(self, expression_str: str, variables: List[str]) -> List[CriticalPoint]:
        """Encontra pontos críticos de uma função multivariável."""
        try:
            # Criar objeto Expression
            expression = Expression(raw_expression=expression_str, variables=variables)
            
            # Encontrar pontos críticos
            critical_points = self.sympy_adapter.find_critical_points(expression)
            
            return critical_points
        except Exception as e:
            print(f"Erro ao encontrar pontos críticos: {str(e)}")
            return []
    
    def get_geometric_interpretation(self, expression_str: str, variables: List[str]) -> str:
        """Retorna uma explicação do significado geométrico das derivadas parciais."""
        try:
            # Criar objeto Expression
            expression = Expression(raw_expression=expression_str, variables=variables)
            
            # Calcular derivadas parciais
            partial_derivatives = self.sympy_adapter.calculate_partial_derivatives(expression)
            
            if not partial_derivatives:
                return "Não foi possível gerar a interpretação geométrica."
            
            # Criar explicação
            explanation = f"""
            ### Significado Geométrico das Derivadas Parciais
            
            Para a função f({', '.join(variables)}) = {expression.sympy_expr}:
            
            """
            
            # Adicionar explicação para cada variável
            for var in variables:
                if var in partial_derivatives.derivatives:
                    explanation += f"""
                    #### Derivada Parcial em relação a {var}:
                    
                    ∂f/∂{var} = {partial_derivatives.derivatives[var]}
                    
                    Esta derivada representa a taxa de variação instantânea da função quando {var} varia, 
                    mantendo todas as outras variáveis constantes. Geometricamente, é a inclinação da curva 
                    obtida ao cortar a superfície da função com um plano perpendicular ao eixo {var}.
                    """
            
            # Adicionar explicação sobre o gradiente se tivermos múltiplas variáveis
            if len(variables) > 1:
                explanation += """
                #### Gradiente da Função:
                
                O gradiente ∇f é um vetor cujas componentes são as derivadas parciais da função:
                
                ∇f = (∂f/∂x₁, ∂f/∂x₂, ..., ∂f/∂xₙ)
                
                O gradiente tem duas propriedades importantes:
                1. Aponta na direção de maior crescimento da função
                2. É perpendicular às curvas/superfícies de nível da função
                
                A magnitude do gradiente |∇f| indica a taxa desse crescimento.
                """
            
            return explanation
        except Exception as e:
            print(f"Erro ao gerar interpretação geométrica: {str(e)}")
            return "Não foi possível gerar a interpretação geométrica."
    
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