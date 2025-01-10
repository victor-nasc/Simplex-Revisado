import numpy as np

def solver(c: list, A_eq: list, b_eq: list) -> dict:
    """
    Implementação do Algoritmo Simplex Revisado para resolver problemas de programação linear.
    Minimizar: c^T x
    Sujeito a: A_eq x = b_eq, bounds.

    Parâmetros:
        c: Coeficientes da função objetivo.
        A_eq: Matriz de restrições de igualdade.
        b_eq: Lado direito das restrições de igualdade.
        bounds: Lista de tuplas especificando os limites das variáveis (inferior <= x <= superior).

    Retorna:
        Um dicionário contendo a solução, o status e outros detalhes relevantes.
    """

    # Inicializa as variáveis
    num_vars = len(c)
    num_constraints = len(b_eq)

    # Cria a solução viável básica inicial
    A = np.array(A_eq, dtype=float)
    B_indices = list(range(num_vars - num_constraints, num_vars))
    N_indices = list(range(num_vars - num_constraints))

    B = A[:, B_indices]  # Matriz de base
    c_B = np.array(c)[B_indices]

    iteration = 0
    while True:
        iteration += 1

        # Calcula a solução básica
        x_B = np.linalg.solve(B, b_eq)

        # Calcula os custos reduzidos
        N = A[:, N_indices]
        c_N = np.array(c)[N_indices]
        B_inv = np.linalg.inv(B)

        y = c_B @ B_inv
        reduced_costs = c_N - y @ N

        # Verifica a otimalidade
        if all(reduced_costs >= 0):
            x = np.zeros(num_vars)
            x[B_indices] = x_B
            objective_value = c @ x
            return {"solution": x, "objective_value": objective_value, "status": "Optimal"}

        # Determina a variável de entrada
        entering_index = np.argmin(reduced_costs)
        entering_var = N_indices[entering_index]

        # Calcula o vetor de direção
        direction = B_inv @ A[:, entering_var]

        # Verifica a não limitabilidade
        if all(direction <= 0):
            return {"status": "Unbounded"}

        # Determina a variável de saída
        ratios = np.array([x_B[i] / direction[i] if direction[i] > 0 else np.inf for i in range(len(direction))])
        leaving_index = np.argmin(ratios)
        leaving_var = B_indices[leaving_index]

        # Atualiza a base
        B_indices[leaving_index] = entering_var
        N_indices[entering_index] = leaving_var
        B = A[:, B_indices]
        c_B = np.array(c)[B_indices]


def prepara_input(A_eq: list, c: list, bounds: list) -> tuple:
    """
    Prepara a entrada para o Algoritmo Simplex Revisado adicionando variáveis de folga 
    e convertendo para a forma padrão.

    Parâmetros:
        A_eq: Matriz de restrições de igualdade.
        c: Coeficientes da função objetivo.

    Retorna:
        Uma tupla contendo as matrizes A_eq e c modificadas.
    """

    num_constraints = len(A_eq)

    # Adiciona variáveis de folga para converter para a forma padrão
    identidade = np.eye(num_constraints)
    A_eq = np.hstack((A_eq, identidade))

    # Adiciona coeficientes zero para as variáveis de folga na função objetivo
    c.extend([0] * num_constraints)

    # Expande os limites com (0.0, inf)
    bounds.extend([(0.0, np.inf)] * num_constraints)

    return A_eq, c, bounds
