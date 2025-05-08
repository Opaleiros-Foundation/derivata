# Derivata - Calculadora de Derivadas Cyberpunk

Uma aplicação web interativa para calcular derivadas com estilo visual cyberpunk.

## Recursos

- Cálculo de derivadas normais
- Cálculo de derivadas parciais
- Cálculo de derivadas de ordem superior
- Visualização passo a passo do processo de derivação
- Interface com tema cyberpunk

## Executando com Docker

### Pré-requisitos

- Docker
- Docker Compose

### Instruções

1. Clone este repositório:
   ```
   git clone https://github.com/seu-usuario/derivata.git
   cd derivata
   ```

2. Inicie a aplicação com Docker Compose:
   ```
   docker-compose up -d
   ```

3. Acesse a aplicação em seu navegador:
   ```
   http://localhost:8501
   ```

4. Para parar a aplicação:
   ```
   docker-compose down
   ```

## Executando sem Docker

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instruções

1. Clone este repositório:
   ```
   git clone https://github.com/seu-usuario/derivata.git
   cd derivata
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```
   streamlit run app.py
   ```

4. Acesse a aplicação em seu navegador:
   ```
   http://localhost:8501
   ```

## Exemplos de uso

- Derivada de um polinômio: `x**2 + 3*x + 1`
- Derivada de uma função trigonométrica: `sin(x) + cos(x)`
- Derivada de uma função exponencial: `exp(x**2)`
- Derivada de uma função logarítmica: `log(x**2 + 1)`
- Derivada de uma função composta: `sin(exp(x))`

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.