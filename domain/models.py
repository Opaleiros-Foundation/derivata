"""
Modelos de domínio para a aplicação Derivata.
Contém as entidades principais e regras de negócio.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional, Union, Tuple
import sympy as sp


@dataclass(frozen=True)
class Expression:
    """Representa uma expressão matemática."""
    raw_expression: str
    variables: List[str]
    
    @property
    def sympy_expr(self) -> sp.Expr:
        """Converte a expressão para um objeto SymPy."""
        return sp.sympify(self.raw_expression)
    
    def __str__(self) -> str:
        return self.raw_expression


@dataclass(frozen=True)
class DerivativeResult:
    """Resultado de uma operação de derivação."""
    original_expression: Expression
    variable: str
    order: int
    result: sp.Expr
    steps: List[str]
    
    @property
    def latex(self) -> str:
        """Retorna a representação LaTeX do resultado."""
        return sp.latex(self.result)


@dataclass(frozen=True)
class PartialDerivativeResult:
    """Resultado de derivadas parciais para uma função multivariável."""
    original_expression: Expression
    derivatives: Dict[str, sp.Expr]
    steps: Dict[str, List[str]]
    
    @property
    def gradient(self) -> List[sp.Expr]:
        """Retorna o gradiente como uma lista de expressões."""
        return list(self.derivatives.values())
    
    def get_hessian(self) -> sp.Matrix:
        """Calcula a matriz Hessiana."""
        variables = list(self.derivatives.keys())
        n = len(variables)
        hessian = sp.zeros(n, n)
        
        expr = self.original_expression.sympy_expr
        for i, var_i in enumerate(variables):
            for j, var_j in enumerate(variables):
                hessian[i, j] = sp.diff(expr, var_i, var_j)
                
        return hessian


@dataclass(frozen=True)
class CriticalPoint:
    """Representa um ponto crítico de uma função multivariável."""
    coordinates: Dict[str, sp.Expr]
    classification: Optional[str] = None  # "minimum", "maximum", "saddle", or None if unknown
    
    def __str__(self) -> str:
        coords = ", ".join([f"{var}={val}" for var, val in self.coordinates.items()])
        return f"({coords})"