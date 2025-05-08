"""
Adaptador para a biblioteca Plotly.
Isola a lógica de visualização do resto da aplicação.
"""
from typing import List, Dict, Optional, Tuple, Any
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sympy as sp
from domain.models import Expression, PartialDerivativeResult


class PlotlyAdapter:
    """Adaptador para a biblioteca Plotly."""
    
    def create_3d_visualization(
        self, 
        expression: Expression, 
        partial_derivatives: PartialDerivativeResult
    ) -> Tuple[Optional[go.Figure], Optional[str]]:
        """Cria visualização 3D para funções de duas variáveis e suas derivadas parciais."""
        try:
            # Verificar se a expressão tem exatamente duas variáveis
            variables = expression.variables
            if len(variables) != 2 or not all(var in ['x', 'y'] for var in variables):
                return None, "A visualização 3D só está disponível para funções de duas variáveis (x, y)."
            
            # Criar símbolos SymPy
            x, y = sp.symbols('x y')
            expr = expression.sympy_expr
            
            # Calcular derivadas parciais
            dx = partial_derivatives.derivatives.get('x')
            dy = partial_derivatives.derivatives.get('y')
            
            if not dx or not dy:
                return None, "Não foi possível obter as derivadas parciais necessárias."
            
            # Converter para funções numéricas
            f_expr = sp.lambdify((x, y), expr, "numpy")
            f_dx = sp.lambdify((x, y), dx, "numpy")
            f_dy = sp.lambdify((x, y), dy, "numpy")
            
            # Criar grade de pontos
            x_range = np.linspace(-3, 3, 50)
            y_range = np.linspace(-3, 3, 50)
            X, Y = np.meshgrid(x_range, y_range)
            
            # Calcular valores da função e derivadas
            Z = f_expr(X, Y)
            Z_dx = f_dx(X, Y)
            Z_dy = f_dy(X, Y)
            
            # Lidar com valores infinitos ou NaN
            Z = np.nan_to_num(Z, nan=0, posinf=10, neginf=-10)
            Z_dx = np.nan_to_num(Z_dx, nan=0, posinf=5, neginf=-5)
            Z_dy = np.nan_to_num(Z_dy, nan=0, posinf=5, neginf=-5)
            
            # Criar subplots: função original, derivada em x, derivada em y
            fig = make_subplots(
                rows=1, cols=3,
                specs=[[{'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}]],
                subplot_titles=[
                    f'Função f(x,y)', 
                    f'Derivada parcial ∂f/∂x', 
                    f'Derivada parcial ∂f/∂y'
                ],
                horizontal_spacing=0.05
            )
            
            # Superfície da função original
            fig.add_trace(
                go.Surface(
                    z=Z, x=X, y=Y, 
                    colorscale='Viridis',
                    name='f(x,y)'
                ),
                row=1, col=1
            )
            
            # Superfície da derivada parcial em relação a x
            fig.add_trace(
                go.Surface(
                    z=Z_dx, x=X, y=Y, 
                    colorscale='Plasma',
                    name='∂f/∂x'
                ),
                row=1, col=2
            )
            
            # Superfície da derivada parcial em relação a y
            fig.add_trace(
                go.Surface(
                    z=Z_dy, x=X, y=Y, 
                    colorscale='Cividis',
                    name='∂f/∂y'
                ),
                row=1, col=3
            )
            
            # Configurar layout
            fig.update_layout(
                title_text="Visualização 3D da Função e suas Derivadas Parciais",
                height=600,
                scene=dict(
                    xaxis_title='x',
                    yaxis_title='y',
                    zaxis_title='f(x,y)'
                ),
                scene2=dict(
                    xaxis_title='x',
                    yaxis_title='y',
                    zaxis_title='∂f/∂x'
                ),
                scene3=dict(
                    xaxis_title='x',
                    yaxis_title='y',
                    zaxis_title='∂f/∂y'
                ),
                template="plotly_dark"
            )
            
            return fig, None
        
        except Exception as e:
            return None, f"Erro ao criar visualização 3D: {str(e)}"
    
    def create_gradient_visualization(
        self, 
        expression: Expression, 
        partial_derivatives: PartialDerivativeResult
    ) -> Tuple[Optional[go.Figure], Optional[str]]:
        """Cria visualização 2D do gradiente (vetores de derivadas parciais)."""
        try:
            # Verificar se a expressão tem exatamente duas variáveis
            variables = expression.variables
            if len(variables) != 2 or not all(var in ['x', 'y'] for var in variables):
                return None, "A visualização do gradiente só está disponível para funções de duas variáveis (x, y)."
            
            # Criar símbolos SymPy
            x, y = sp.symbols('x y')
            expr = expression.sympy_expr
            
            # Calcular derivadas parciais
            dx = partial_derivatives.derivatives.get('x')
            dy = partial_derivatives.derivatives.get('y')
            
            if not dx or not dy:
                return None, "Não foi possível obter as derivadas parciais necessárias."
            
            # Converter para funções numéricas
            f_expr = sp.lambdify((x, y), expr, "numpy")
            f_dx = sp.lambdify((x, y), dx, "numpy")
            f_dy = sp.lambdify((x, y), dy, "numpy")
            
            # Criar grade de pontos
            x_range = np.linspace(-3, 3, 20)
            y_range = np.linspace(-3, 3, 20)
            X, Y = np.meshgrid(x_range, y_range)
            
            # Calcular valores da função e derivadas
            Z = f_expr(X, Y)
            U = f_dx(X, Y)  # Componente x do gradiente
            V = f_dy(X, Y)  # Componente y do gradiente
            
            # Lidar com valores infinitos ou NaN
            Z = np.nan_to_num(Z, nan=0, posinf=10, neginf=-10)
            U = np.nan_to_num(U, nan=0, posinf=5, neginf=-5)
            V = np.nan_to_num(V, nan=0, posinf=5, neginf=-5)
            
            # Normalizar vetores do gradiente para melhor visualização
            norm = np.sqrt(U**2 + V**2)
            norm_nonzero = np.where(norm > 0.1, norm, 1)  # Evitar divisão por zero
            U_norm = U / norm_nonzero
            V_norm = V / norm_nonzero
            
            # Criar subplots: contorno da função e campo vetorial do gradiente
            fig = make_subplots(
                rows=1, cols=2,
                specs=[[{'type': 'contour'}, {'type': 'xy'}]],
                subplot_titles=[
                    'Curvas de Nível da Função f(x,y)',
                    'Campo Vetorial do Gradiente ∇f'
                ],
                horizontal_spacing=0.1
            )
            
            # Curvas de nível da função
            fig.add_trace(
                go.Contour(
                    z=Z, x=x_range, y=y_range,
                    colorscale='Viridis',
                    contours=dict(
                        showlabels=True,
                        labelfont=dict(size=10, color='white')
                    ),
                    name='f(x,y)'
                ),
                row=1, col=1
            )
            
            # Campo vetorial do gradiente
            fig.add_trace(
                go.Quiver(
                    x=X.flatten(), y=Y.flatten(),
                    u=U_norm.flatten(), v=V_norm.flatten(),
                    scale=0.1,
                    line=dict(width=1, color='#7eefc4'),
                    name='∇f'
                ),
                row=1, col=2
            )
            
            # Configurar layout
            fig.update_layout(
                title_text="Visualização do Gradiente",
                height=500,
                template="plotly_dark",
                xaxis=dict(title='x'),
                yaxis=dict(title='y'),
                xaxis2=dict(title='x'),
                yaxis2=dict(title='y')
            )
            
            return fig, None
        
        except Exception as e:
            return None, f"Erro ao criar visualização do gradiente: {str(e)}"