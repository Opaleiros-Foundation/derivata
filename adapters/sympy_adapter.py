"""
Adaptador para a biblioteca SymPy.
Isola a lógica de interação com o SymPy do resto da aplicação.
"""
from typing import List, Dict, Optional, Tuple, Any
import sympy as sp
from domain.models import Expression, DerivativeResult, PartialDerivativeResult, CriticalPoint


class SymPyAdapter:
    """Adaptador para a biblioteca SymPy."""
    
    @staticmethod
    def calculate_derivative(expression: Expression, variable: str, order: int = 1) -> Optional[DerivativeResult]:
        """Calcula a derivada de uma expressão em relação a uma variável."""
        try:
            expr = expression.sympy_expr
            result = sp.diff(expr, variable, order)
            steps = SymPyAdapter._generate_derivative_steps(expr, variable, order)
            
            return DerivativeResult(
                original_expression=expression,
                variable=variable,
                order=order,
                result=result,
                steps=steps
            )
        except Exception as e:
            print(f"Erro ao calcular derivada: {str(e)}")
            return None
    
    @staticmethod
    def calculate_partial_derivatives(expression: Expression) -> Optional[PartialDerivativeResult]:
        """Calcula todas as derivadas parciais para uma função multivariável."""
        try:
            expr = expression.sympy_expr
            variables = expression.variables
            
            derivatives = {}
            steps = {}
            
            for var in variables:
                derivatives[var] = sp.diff(expr, var)
                steps[var] = SymPyAdapter._generate_partial_derivative_steps(expr, var)
            
            return PartialDerivativeResult(
                original_expression=expression,
                derivatives=derivatives,
                steps=steps
            )
        except Exception as e:
            print(f"Erro ao calcular derivadas parciais: {str(e)}")
            return None
    
    @staticmethod
    def find_critical_points(expression: Expression) -> List[CriticalPoint]:
        """Encontra pontos críticos de uma função multivariável."""
        try:
            expr = expression.sympy_expr
            variables = expression.variables
            
            # Calcular derivadas parciais
            derivatives = [sp.diff(expr, var) for var in variables]
            
            # Resolver o sistema de equações (todas as derivadas parciais = 0)
            solutions = sp.solve(derivatives, variables, dict=True)
            
            critical_points = []
            for solution in solutions:
                # Verificar se a solução é completa (tem valores para todas as variáveis)
                if all(var in solution for var in variables):
                    # Classificar o ponto crítico se possível
                    classification = SymPyAdapter._classify_critical_point(expr, variables, solution)
                    critical_points.append(CriticalPoint(coordinates=solution, classification=classification))
            
            return critical_points
        except Exception as e:
            print(f"Erro ao encontrar pontos críticos: {str(e)}")
            return []
    
    @staticmethod
    def _generate_derivative_steps(expr: sp.Expr, variable: str, order: int = 1) -> List[str]:
        """Gera os passos para o cálculo de uma derivada."""
        steps = []
        steps.append(f"Expressão original: {expr}")
        steps.append(f"Calculando a derivada em relação a {variable}...")
        
        var = sp.Symbol(variable)
        
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
        
        derivative = sp.diff(expr, var, order)
        steps.append(f"Resultado final: {derivative}")
        
        return steps
    
    @staticmethod
    def _generate_partial_derivative_steps(expr: sp.Expr, variable: str) -> List[str]:
        """Gera os passos para o cálculo de uma derivada parcial."""
        steps = []
        steps.append(f"Expressão original: {expr}")
        steps.append(f"Calculando a derivada parcial em relação a {variable}...")
        steps.append(f"Passo 1: Tratamos todas as outras variáveis como constantes")
        
        # Identificar todas as variáveis na expressão
        all_vars = [str(symbol) for symbol in expr.free_symbols]
        other_vars = [v for v in all_vars if v != variable]
        
        if other_vars:
            steps.append(f"Passo 2: Variáveis tratadas como constantes: {', '.join(other_vars)}")
        
        # Calcular a derivada final
        derivative = sp.diff(expr, variable)
        steps.append(f"Resultado final: {derivative}")
        
        # Adicionar passo de simplificação se necessário
        simplified = sp.simplify(derivative)
        if simplified != derivative:
            steps.append(f"Simplificando: {simplified}")
        
        return steps
    
    @staticmethod
    def _classify_critical_point(expr: sp.Expr, variables: List[str], point: Dict[str, sp.Expr]) -> Optional[str]:
        """Classifica um ponto crítico como mínimo, máximo ou ponto de sela."""
        try:
            # Calcular a matriz Hessiana no ponto crítico
            n = len(variables)
            hessian = sp.zeros(n, n)
            
            for i, var_i in enumerate(variables):
                for j, var_j in enumerate(variables):
                    hessian[i, j] = sp.diff(expr, var_i, var_j)
            
            # Substituir os valores do ponto crítico na matriz Hessiana
            hessian_at_point = hessian.subs(point)
            
            # Calcular os autovalores da matriz Hessiana
            eigenvalues = list(hessian_at_point.eigenvals().keys())
            
            # Classificar com base nos autovalores
            if all(val > 0 for val in eigenvalues):
                return "minimum"
            elif all(val < 0 for val in eigenvalues):
                return "maximum"
            elif any(val > 0 for val in eigenvalues) and any(val < 0 for val in eigenvalues):
                return "saddle"
            else:
                return None  # Caso indeterminado (autovalores zero)
        except Exception:
            return None