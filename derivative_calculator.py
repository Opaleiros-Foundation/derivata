import sympy as sp
from derivative_steps import show_derivative_steps

def calculate_derivative(expression, variable, order=1):
    """Calculate the derivative of an expression with respect to a variable."""
    x, y, z = sp.symbols('x y z')
    expr = sp.sympify(expression)
    derivative = sp.diff(expr, variable, order)
    return derivative

def calculate_partial_derivative(expression, variable, order=1):
    """Calculate the partial derivative of an expression with respect to a variable."""
    x, y, z = sp.symbols('x y z')
    expr = sp.sympify(expression)
    derivative = sp.diff(expr, variable, order)
    return derivative

def show_steps(expression, variable):
    """Show the steps of differentiation."""
    return show_derivative_steps(expression, variable)

def main():
    print("Calculadora de Derivadas")
    print("------------------------")
    
    while True:
        print("\nEscolha o tipo de derivada:")
        print("1. Derivada normal")
        print("2. Derivada parcial")
        print("3. Derivada de ordem superior")
        print("4. Sair")
        
        choice = input("Digite sua escolha (1, 2, 3 ou 4): ")
        
        if choice == "1":
            # Derivada normal
            expression = input("Digite a expressão (ex: x**2 + 3*x + 1): ")
            variable = input("Digite a variável de diferenciação (ex: x): ")
            
            print("\nResultado:")
            result = calculate_derivative(expression, variable)
            print(f"A derivada de {expression} em relação a {variable} é: {result}")
            
            print("\nPassos da derivação:")
            show_steps(expression, variable)
        
        elif choice == "2":
            # Derivada parcial
            from partial_derivatives import calculate_partial_derivatives, show_partial_derivative_steps
            
            expression = input("Digite a expressão multivariável (ex: x**2 + x*y + y**2): ")
            variables = input("Digite as variáveis separadas por espaço (ex: x y): ").split()
            
            print("\nResultados:")
            results = calculate_partial_derivatives(expression, variables)
            for var, result in results.items():
                print(f"∂/∂{var}({expression}) = {result}")
            
            # Mostrar passos para uma variável específica
            if len(variables) > 0:
                print("\nDeseja ver os passos para alguma variável específica?")
                var_choice = input(f"Digite a variável ({', '.join(variables)}) ou pressione Enter para pular: ")
                
                if var_choice in variables:
                    print(f"\nPassos da derivação parcial em relação a {var_choice}:")
                    show_partial_derivative_steps(expression, var_choice)
        
        elif choice == "3":
            # Derivada de ordem superior
            expression = input("Digite a expressão (ex: x**2 + 3*x + 1): ")
            variable = input("Digite a variável de diferenciação (ex: x): ")
            
            try:
                order = int(input("Digite a ordem da derivada (ex: 2 para segunda derivada): "))
                if order < 1:
                    print("A ordem deve ser um número positivo.")
                    continue
            except ValueError:
                print("Por favor, digite um número inteiro válido para a ordem.")
                continue
            
            print("\nResultado:")
            result = calculate_derivative(expression, variable, order)
            print(f"A {order}ª derivada de {expression} em relação a {variable} é: {result}")
        
        elif choice == "4":
            print("Obrigado por usar a Calculadora de Derivadas!")
            break
        
        else:
            print("Escolha inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()