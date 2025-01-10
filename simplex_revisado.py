
import tkinter as tk
from tkinter import messagebox
import numpy as np
from simplex_revisado import solver, prepara_input

def solve_problem():
    try:
        N = len(coefficients)
        M = len(eq_matrix)

        c = [float(coefficients[i].get() or 0) for i in range(N)]

        A_eq = []
        for i in range(M):
            row = [float(eq_matrix[i][j].get() or 0) for j in range(N)]
            A_eq.append(row)

        b_eq = [float(rhs[i].get() or 0) for i in range(M)]

        bounds = []
        for i in range(N):
            lower = float(bounds_matrix[i][0].get() or 0)
            upper = float(bounds_matrix[i][1].get() or np.inf)
            bounds.append((lower, upper))

        # calcula
        A_eq, c, bounds = prepara_input(A_eq, c, bounds)
        result_revised_simplex = solver(c, A_eq, b_eq)

        result_text.set(f"Coeficientes \n{result_revised_simplex['solution']}\n\nValor objetivo: {result_revised_simplex['objective_value']}\n\nStatus: {result_revised_simplex['status']}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def create_input_fields(*args):
    global coefficients, eq_matrix, rhs, bounds_matrix
    
    for widget in input_frame.winfo_children():
        widget.destroy()

    N = len(coefficients)
    M = len(eq_matrix)

    tk.Button(input_frame, text="Limpar", command=clear_fields, font=("Arial", 18)).grid(row=0, column=N, columnspan=2, pady=(15, 5))
    tk.Label(input_frame, text="Minimize:       ", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=(15, 5))
    for j in range(N):
        tk.Label(input_frame, text=f"x{j+1}", font=("Arial", 16)).grid(row=1, column=j, padx=3, pady=3)

    coefficients = [tk.Entry(input_frame, width=4, font=("Arial", 18)) for _ in range(N)]
    for i, entry in enumerate(coefficients):
        entry.grid(row=2, column=i, padx=3, pady=3)
        tk.Label(input_frame).grid(row=2, column=i + N, sticky="w")

    tk.Button(
        input_frame,
        text="+",
        font=("Arial", 18),
        command=increase_variables,
    ).grid(row=2, column=N+1)

    tk.Button(
        input_frame,
        text="-",
        font=("Arial", 18),
        command=decrease_variables,
    ).grid(row=2, column=N)

    tk.Label(input_frame, text="Sujeito a       ", font=("Arial", 18)).grid(row=3, column=0, columnspan=2, pady=(15, 5))
    eq_matrix = [[tk.Entry(input_frame, width=4, font=("Arial", 18)) for _ in range(N)] for _ in range(M)]
    rhs = [tk.Entry(input_frame, width=4, font=("Arial", 18)) for _ in range(M)]

    for i in range(M):
        for j in range(N):
            eq_matrix[i][j].grid(row=4 + i, column=j, pady=3)
        tk.Label(input_frame, text="≤", font=("Arial", 18)).grid(row=4 + i, column=N)
        rhs[i].grid(row=4 + i, column=N + 1, pady=3)

    tk.Button(
        input_frame,
        text="+",
        font=("Arial", 18),
        command=increase_constraints,
    ).grid(row=4 + M, column=N+1, pady=10)

    tk.Button(
        input_frame,
        text="-",
        font=("Arial", 18),
        command=decrease_constraints,
    ).grid(row=4 + M, column=N, pady=10)

    global bounds_matrix
    bounds_matrix = [[tk.Entry(input_frame, width=4, font=("Arial", 18)), tk.Entry(input_frame, width=4, font=("Arial", 18))] for _ in range(N)]
    for i in range(N):
        bounds_matrix[i][0].grid(row=6 + M + i, column=0, padx=3, pady=3)
        tk.Label(input_frame, text=f"≤ x{i+1} ≤", font=("Arial", 16)).grid(row=6 + M + i, column=1)
        bounds_matrix[i][1].grid(row=6 + M + i, column=2, padx=3, pady=3)

def increase_variables():
    coefficients.append(tk.Entry(input_frame, width=4, font=("Arial", 18)))
    for row in eq_matrix:
        row.append(tk.Entry(input_frame, width=4, font=("Arial", 18)))
    bounds_matrix.append([tk.Entry(input_frame, width=5, font=("Arial", 18)), tk.Entry(input_frame, width=5, font=("Arial", 18))])
    create_input_fields()

def decrease_variables():
    if len(coefficients) > 1:
        coefficients.pop()
        for row in eq_matrix:
            row.pop()
        bounds_matrix.pop()
        create_input_fields()

def increase_constraints():
    global eq_matrix, rhs
    eq_matrix.append([tk.Entry(input_frame, width=4, font=("Arial", 18)) for _ in range(len(coefficients))])
    rhs.append(tk.Entry(input_frame, width=4, font=("Arial", 18)))
    create_input_fields()

def decrease_constraints():
    if len(eq_matrix) > 1:
        eq_matrix.pop()
        rhs.pop()
        create_input_fields()
    
def clear_fields():
    """Clears all input fields."""
    for entry_list in [coefficients, *eq_matrix, rhs, *bounds_matrix]:
        for entry in entry_list:
            entry.delete(0, tk.END)
    result_text.set("")

def generate_pdf():
    """Placeholder for Generate PDF functionality."""
    messagebox.showinfo("Generate PDF", "PDF generation functionality is not implemented yet.")

# GUI setup
root = tk.Tk()
root.title("Calculadora")

input_frame = tk.Frame(root, padx=20, pady=20) 
input_frame.grid(row=2, column=0, columnspan=4, padx=15) 

tk.Button(root, text="Calcule", command=solve_problem, font=("Arial", 18)).grid(
    row=3, column=1, padx=15  
)
tk.Button(root, text="Gerar PDF", command=generate_pdf, font=("Arial", 18)).grid(
    row=3, column=2, padx=15 
)

result_text = tk.StringVar()
tk.Label(
    root, textvariable=result_text, justify="left", wraplength=400, font=("Arial", 18), padx=15, pady=15
).grid(row=4, column=0, columnspan=4) 

N_default = 3
M_default = 2
coefficients = [tk.Entry(input_frame, width=4, font=("Arial", 18)) for _ in range(N_default)]
eq_matrix = [[tk.Entry(input_frame, width=4, font=("Arial", 18)) for _ in range(N_default)] for _ in range(M_default)]
rhs = [tk.Entry(input_frame, width=4, font=("Arial", 18)) for _ in range(M_default)]
bounds_matrix = [
    [tk.Entry(input_frame, width=5, font=("Arial", 18)), tk.Entry(input_frame, width=5, font=("Arial", 18))]
    for _ in range(N_default)
]
create_input_fields()

root.mainloop()
