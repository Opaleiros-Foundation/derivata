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

    @staticmethod
    def create_3d_visualization(expression: Expression, partial_derivatives: PartialDerivativeResult) -> Tuple[
        Optional[go.Figure], Optional[str]]:
        """Cria visualização 3D para funções de duas variáveis e suas derivadas parciais."""
        try:
            variables = expression.variables

            # Verificar se temos exatamente duas variáveis (x e y)
            if len(variables) != 2 or not all(var in ['x', 'y'] for var in variables):
                return None, "Visualização 3D disponível apenas para funções de x e y."

            # Criar símbolos SymPy
            x, y = sp.symbols('x y')
            expr = expression.sympy_expr

            # Obter derivadas parciais
            dx = partial_derivatives.derivatives.get('x')
            dy = partial_derivatives.derivatives.get('y')

            if dx is None or dy is None:
                return None, "Não foi possível obter as derivadas parciais."

            # Converter para funções numéricas
            f_expr = sp.lambdify((x, y), expr, "numpy")
            f_dx = sp.lambdify((x, y), dx, "numpy")
            f_dy = sp.lambdify((x, y), dy, "numpy")

            # Criar grade de pontos
            x_range = np.linspace(-3, 3, 50)
            y_range = np.linspace(-3, 3, 50)
            X, Y = np.meshgrid(x_range, y_range)

            # Calcular valores da função e derivadas
            try:
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

                # Atualizar layout
                fig.update_layout(
                    title_text=f"Visualização 3D de {expression} e suas derivadas parciais",
                    height=600,
                    scene=dict(
                        xaxis_title='x',
                        yaxis_title='y',
                        zaxis_title='f(x,y)',
                        aspectratio=dict(x=1, y=1, z=0.7)
                    ),
                    scene2=dict(
                        xaxis_title='x',
                        yaxis_title='y',
                        zaxis_title='∂f/∂x',
                        aspectratio=dict(x=1, y=1, z=0.7)
                    ),
                    scene3=dict(
                        xaxis_title='x',
                        yaxis_title='y',
                        zaxis_title='∂f/∂y',
                        aspectratio=dict(x=1, y=1, z=0.7)
                    ),
                    font=dict(
                        family="Courier New, monospace",
                        size=12,
                        color="#7eefc4"
                    ),
                    paper_bgcolor='rgba(20, 20, 40, 0.9)',
                    plot_bgcolor='rgba(20, 20, 40, 0.9)',
                    margin=dict(l=0, r=0, t=40, b=0)
                )

                return fig, None

            except Exception as e:
                return None, f"Erro ao calcular valores: {str(e)}"

        except Exception as e:
            return None, f"Erro ao criar visualização: {str(e)}"

    @staticmethod
    def create_gradient_visualization(expression: Expression, partial_derivatives: PartialDerivativeResult) -> Tuple[
        Optional[go.Figure], Optional[str]]:
        """Cria visualização 2D do gradiente (vetores de derivadas parciais)."""
        try:
            variables = expression.variables

            # Verificar se temos exatamente duas variáveis (x e y)
            if len(variables) != 2 or not all(var in ['x', 'y'] for var in variables):
                return None, "Visualização do gradiente disponível apenas para funções de x e y."

            # Criar símbolos SymPy
            x, y = sp.symbols('x y')
            expr = expression.sympy_expr

            # Obter derivadas parciais
            dx = partial_derivatives.derivatives.get('x')
            dy = partial_derivatives.derivatives.get('y')

            if dx is None or dy is None:
                return None, "Não foi possível obter as derivadas parciais."

            # Converter para funções numéricas
            f_expr = sp.lambdify((x, y), expr, "numpy")
            f_dx = sp.lambdify((x, y), dx, "numpy")
            f_dy = sp.lambdify((x, y), dy, "numpy")

            # Criar grade de pontos
            x_range = np.linspace(-3, 3, 20)
            y_range = np.linspace(-3, 3, 20)
            X, Y = np.meshgrid(x_range, y_range)

            # Calcular valores da função e gradiente
            try:
                Z = f_expr(X, Y)
                U = f_dx(X, Y)  # Componente x do gradiente
                V = f_dy(X, Y)  # Componente y do gradiente

                # Lidar com valores infinitos ou NaN
                Z = np.nan_to_num(Z, nan=0, posinf=10, neginf=-10)
                U = np.nan_to_num(U, nan=0, posinf=5, neginf=-5)
                V = np.nan_to_num(V, nan=0, posinf=5, neginf=-5)

                # Normalizar vetores do gradiente para melhor visualização
                norm = np.sqrt(U ** 2 + V ** 2)
                norm_nonzero = np.where(norm > 0.0001, norm, 1)  # Evitar divisão por zero
                U_norm = U / norm_nonzero
                V_norm = V / norm_nonzero

                # Criar figura com subplots
                fig = make_subplots(
                    rows=1, cols=2,
                    specs=[[{'type': 'contour'}, {'type': 'contour'}]],
                    subplot_titles=[
                        f'Curvas de Nível de f(x,y)',
                        f'Campo Vetorial do Gradiente ∇f'
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
                            labelfont=dict(
                                family='Courier New',
                                color='white'
                            )
                        ),
                        colorbar=dict(
                            title='f(x,y)',
                            titleside='right',
                            titlefont=dict(
                                color='#7eefc4'
                            )
                        ),
                        name='f(x,y)'
                    ),
                    row=1, col=1
                )

                # Campo vetorial do gradiente
                fig.add_trace(
                    go.Scatter(
                        x=X.flatten(), y=Y.flatten(),
                        mode='markers+text',
                        marker=dict(
                            size=2,
                            color='rgba(126, 239, 196, 0.5)',
                        ),
                        text='',
                        name='Pontos de Grade'
                    ),
                    row=1, col=2
                )

                # Adicionar vetores do gradiente
                fig.add_trace(
                    go.Scatter(
                        x=X.flatten(), y=Y.flatten(),
                        mode='lines',
                        line=dict(
                            color='rgba(255, 0, 255, 0.7)',
                            width=1
                        ),
                        name='Vetores do Gradiente'
                    ),
                    row=1, col=2
                )

                # Adicionar as linhas dos vetores
                for i in range(X.shape[0]):
                    for j in range(X.shape[1]):
                        x_start = X[i, j]
                        y_start = Y[i, j]
                        x_end = x_start + 0.2 * U_norm[i, j]
                        y_end = y_start + 0.2 * V_norm[i, j]

                        fig.add_shape(
                            type="line",
                            x0=x_start, y0=y_start,
                            x1=x_end, y1=y_end,
                            line=dict(
                                color="rgba(255, 0, 255, 0.7)",
                                width=1,
                                dash="solid"
                            ),
                            row=1, col=2
                        )

                # Atualizar layout
                fig.update_layout(
                    title_text=f"Gradiente de {expression}",
                    height=500,
                    font=dict(
                        family="Courier New, monospace",
                        size=12,
                        color="#7eefc4"
                    ),
                    paper_bgcolor='rgba(20, 20, 40, 0.9)',
                    plot_bgcolor='rgba(20, 20, 40, 0.9)',
                    margin=dict(l=20, r=20, t=60, b=20),
                    showlegend=False
                )

                # Atualizar eixos
                fig.update_xaxes(title_text="x", row=1, col=1)
                fig.update_yaxes(title_text="y", row=1, col=1)
                fig.update_xaxes(title_text="x", row=1, col=2)
                fig.update_yaxes(title_text="y", row=1, col=2)

                return fig, None

            except Exception as e:
                return None, f"Erro ao calcular valores para o gradiente: {str(e)}"

        except Exception as e:
            return None, f"Erro ao criar visualização do gradiente: {str(e)}"
