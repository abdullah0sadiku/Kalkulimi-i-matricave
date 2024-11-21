import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

# Global Styles
def apply_styles():
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=10)
    style.configure("TLabel", font=("Arial", 12))
    style.configure("Header.TLabel", font=("Arial", 16, "bold"))
    style.configure("Grid.TLabel", font=("Arial", 12), borderwidth=1, relief="solid", anchor="center", width=10)

def calculate_minor(matrix, i, j):
    sub_matrix = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
    return round(np.linalg.det(sub_matrix), 2)

def calculate_cofactor(matrix, i, j):
    return round(((-1) ** (i + j)) * calculate_minor(matrix, i, j), 2)

def sarrus_rule(matrix):
    if matrix.shape != (3, 3):
        raise ValueError("Sarrus' rule is only applicable for 3x3 matrices.")
    return round(
        matrix[0, 0] * matrix[1, 1] * matrix[2, 2]
        + matrix[0, 1] * matrix[1, 2] * matrix[2, 0]
        + matrix[0, 2] * matrix[1, 0] * matrix[2, 1]
        - matrix[0, 2] * matrix[1, 1] * matrix[2, 0]
        - matrix[0, 0] * matrix[1, 2] * matrix[2, 1]
        - matrix[0, 1] * matrix[1, 0] * matrix[2, 2], 2)

def gaussian_determinant(matrix):
    n = matrix.shape[0]
    det = 1
    for i in range(n):
        pivot = matrix[i, i]
        if pivot == 0:
            return 0
        det *= pivot
        for j in range(i + 1, n):
            factor = matrix[j, i] / pivot
            matrix[j, i:] -= factor * matrix[i, i:]
    return round(det, 2)

class MatrixApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kalkulator Matricash")
        self.geometry("800x600")
        apply_styles()
        self.entries_a = []
        self.entries_b = []
        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.clear_frame()

        # Create a frame to align elements in a column layout
        column_frame = ttk.Frame(self)
        column_frame.pack(side='left', padx=20, pady=20, fill='y', anchor='w')

        ttk.Label(
            column_frame,
            text="Mirë se vini në Kalkulatorin e Matricave!",
            style="Header.TLabel"
        ).pack(pady=20, anchor='w')

        ttk.Button(
            column_frame,
            text="Veprime me Matrica",
            command=self.show_operations
        ).pack(pady=10, anchor='w')

        ttk.Button(
            column_frame,
            text="Kalkulimi i Kofaktorëve",
            command=self.show_cofactors
        ).pack(pady=10, anchor='w')

        ttk.Button(
            column_frame,
            text="Determinantat",
            command=self.show_determinants
        ).pack(pady=10, anchor='w')

        ttk.Button(
            column_frame,
            text="Kalkulimi i Minorëve",
            command=self.show_minoret
        ).pack(pady=10, anchor='w')

    def show_operations(self):
        self.clear_frame()

        ttk.Label(self, text="Veprime me Matrica", style="Header.TLabel").pack(pady=20, anchor="w")
        rows = tk.IntVar()
        cols = tk.IntVar()
        selected_matrix = tk.StringVar(value="matrix_a")

        def create_inputs():
            self.entries_a.clear()
            self.entries_b.clear()
            for widget in input_frame.winfo_children():
                widget.destroy()
            for i in range(rows.get()):
                row_a, row_b = [], []
                for j in range(cols.get()):
                    e_a = ttk.Entry(input_frame, width=5)
                    e_a.grid(row=i, column=j, padx=5, pady=5, sticky="w")
                    row_a.append(e_a)
                    e_b = ttk.Entry(input_frame, width=5)
                    e_b.grid(row=i, column=j + cols.get() + 1, padx=5, pady=5, sticky="w")
                    row_b.append(e_b)
                self.entries_a.append(row_a)
                self.entries_b.append(row_b)

        def perform_operation(op):
            try:
                matrix_a = np.array([[float(e.get()) for e in row] for row in self.entries_a])
                matrix_b = np.array([[float(e.get()) for e in row] for row in self.entries_b])
                result = None
                if op == "Mbledhje":
                    result = matrix_a + matrix_b
                elif op == "Zbritje":
                    result = matrix_a - matrix_b
                elif op == "Shumzim":
                    result = np.dot(matrix_a, matrix_b)
                elif op == "Transpozo":
                    selected = selected_matrix.get()
                    if selected == "matrix_a":
                        result = np.transpose(matrix_a)
                    elif selected == "matrix_b":
                        result = np.transpose(matrix_b)
                    else:
                        raise ValueError("Matrica e zgjedhur është e panjohur.")
                display_result(result)
            except Exception as e:
                messagebox.showerror("Gabim", f"Input jo valid: {e}")

        def display_result(matrix):
            for widget in result_frame.winfo_children():
                widget.destroy()
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    ttk.Label(result_frame, text=f"{matrix[i, j]:.2f}", style="Grid.TLabel").grid(row=i, column=j, padx=5, pady=5, sticky="w")

        # Layout for matrix size input
        ttk.Label(self, text="Numri i rreshtave:", anchor="w").pack()
        ttk.Entry(self, textvariable=rows, width=5).pack(pady=5, anchor="w")
        ttk.Label(self, text="Numri i kolonave:", anchor="w").pack()
        ttk.Entry(self, textvariable=cols, width=5).pack(pady=5, anchor="w")
        ttk.Button(self, text="Krijo Inputet", command=create_inputs).pack(pady=10, anchor="w")

        input_frame = ttk.Frame(self)
        input_frame.pack(pady=20, anchor="w")

        # Operation buttons
        operation_frame = ttk.Frame(self)
        operation_frame.pack(pady=10, anchor="w")
        ttk.Button(operation_frame, text="Mbledhje", command=lambda: perform_operation("Mbledhje")).pack(side="left", padx=10)
        ttk.Button(operation_frame, text="Zbritje", command=lambda: perform_operation("Zbritje")).pack(side="left", padx=10)
        ttk.Button(operation_frame, text="Shumzim", command=lambda: perform_operation("Shumzim")).pack(side="left", padx=10)

        ttk.Label(operation_frame, text="Zgjedh Matriken:", anchor="w").pack(side="left", padx=5)
        ttk.Combobox(operation_frame, textvariable=selected_matrix, values=["matrix_a", "matrix_b"], state="readonly").pack(side="left", padx=10)

        ttk.Button(operation_frame, text="Transpozo", command=lambda: perform_operation("Transpozo")).pack(side="left", padx=10)

        result_frame = ttk.Frame(self)
        result_frame.pack(pady=20, anchor="w")

        ttk.Button(self, text="Kthehu në Menunë Kryesore", command=self.show_welcome_screen).pack(pady=10, anchor="w")

    # Other sections remain unchanged with translations as needed...


    def show_cofactors(self):
        self.clear_frame()
        ttk.Label(self, text="Kofaktoret", style="Header.TLabel").pack(pady=20)
        size = tk.IntVar()

        def create_inputs():
            self.entries_a.clear()
            for widget in input_frame.winfo_children():
                widget.destroy()
            for i in range(size.get()):
                row_a = []
                for j in range(size.get()):
                    e_a = ttk.Entry(input_frame, width=5)
                    e_a.grid(row=i, column=j, padx=5, pady=5)
                    row_a.append(e_a)
                self.entries_a.append(row_a)

        def calculate_cofactors():
            try:
                matrix = np.array([[float(e.get()) for e in row] for row in self.entries_a])
                cofactor_matrix = np.zeros_like(matrix)
                for i in range(matrix.shape[0]):
                    for j in range(matrix.shape[1]):
                        cofactor_matrix[i, j] = calculate_cofactor(matrix, i, j)
                display_result(cofactor_matrix)
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        def display_result(matrix):
            for widget in result_frame.winfo_children():
                widget.destroy()
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    ttk.Label(result_frame, text=f"{matrix[i, j]:.2f}", style="Grid.TLabel").grid(row=i, column=j, padx=5, pady=5)

        ttk.Label(self, text="Rendi i matrices :").pack()
        ttk.Entry(self, textvariable=size, width=5).pack()
        ttk.Button(self, text="Create Inputs", command=create_inputs).pack(pady=10)

        input_frame = ttk.Frame(self)
        input_frame.pack(pady=20)
        ttk.Button(self, text="Kalkulo kofaktorin", command=calculate_cofactors).pack(pady=10)

        result_frame = ttk.Frame(self)
        result_frame.pack(pady=20)
        ttk.Button(self, text="Ktheu ne menu kryesore", command=self.show_welcome_screen).pack(pady=10)

    def show_determinants(self):
        self.clear_frame()
        ttk.Label(self, text="Kalkulo determinantet", style="Header.TLabel").pack(pady=20)
        size = tk.IntVar()

        def create_inputs():
            self.entries_a.clear()
            for widget in input_frame.winfo_children():
                widget.destroy()
            for i in range(size.get()):
                row_a = []
                for j in range(size.get()):
                    e_a = ttk.Entry(input_frame, width=5)
                    e_a.grid(row=i, column=j, padx=5, pady=5)
                    row_a.append(e_a)
                self.entries_a.append(row_a)

        def calculate_determinant(method):
            try:
                matrix = np.array([[float(e.get()) for e in row] for row in self.entries_a])
                det = None
                if method == "Gaussian":
                    det = gaussian_determinant(matrix)
                elif method == "Sarrus":
                    det = sarrus_rule(matrix)
                elif method == "Default":
                    det = round(np.linalg.det(matrix), 2)
                messagebox.showinfo("Determinant Result", f"The determinant is: {det}")
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")
        ttk.Label(self, text="Matrix Size:").pack()
        ttk.Entry(self, textvariable=size, width=5).pack()
        ttk.Button(self, text="Krijo inputat", command=create_inputs).pack(pady=10)
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=20)
        ttk.Button(self, text="Metoda e Gaussianit", command=lambda: calculate_determinant("Gaussian")).pack(pady=5)
        ttk.Button(self, text="Ligji i Sarrusit", command=lambda: calculate_determinant("Sarrus")).pack(pady=5)
        ttk.Button(self, text="Metoda klasike", command=lambda: calculate_determinant("Default")).pack(pady=5)
        ttk.Button(self, text="Ktheu ne menu kryesore", command=self.show_welcome_screen).pack(pady=10)
    
    def show_minoret(self):
        self.clear_frame()
        ttk.Label(self, text="Kalkulo Minorët e Matrices", style="Header.TLabel").pack(pady=20)

        size = tk.IntVar()

        def create_inputs():
            self.entries_a.clear()
            for widget in input_frame.winfo_children():
                widget.destroy()
            for i in range(size.get()):
                row_a = []
                for j in range(size.get()):
                    e_a = ttk.Entry(input_frame, width=5)
                    e_a.grid(row=i, column=j, padx=5, pady=5)
                    row_a.append(e_a)
                self.entries_a.append(row_a)

        def display_result(matrix):
                for widget in result_frame.winfo_children():
                    widget.destroy()
                for i in range(matrix.shape[0]):
                    for j in range(matrix.shape[1]):
                        ttk.Label(result_frame, text=f"{matrix[i, j]:.2f}", style="Grid.TLabel").grid(row=i, column=j, padx=5, pady=5)
        
        def calculate_minors():
            try:
                matrix = np.array([[float(e.get()) for e in row] for row in self.entries_a])
                minors_matrix = np.zeros_like(matrix)

                for i in range(matrix.shape[0]):
                    for j in range(matrix.shape[1]):
                        submatrix = np.delete(np.delete(matrix, i, axis=0), j, axis=1)  # Remove i-th row and j-th column
                        minors_matrix[i, j] = round(np.linalg.det(submatrix), 2)  # Determinant of submatrix
                        display_result(minors_matrix)
            except Exception as e:
                messagebox.showerror("Gabim", f"Input jo valid: {e}")

           
        ttk.Label(self, text="Rendi i matrices").pack()
        ttk.Entry(self, textvariable=size, width=5).pack(pady=5)
        ttk.Button(self, text="Krijo Inputet", command=create_inputs).pack(pady=10)
    
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=20)
    
        ttk.Button(self, text="Kalkulo Minorët", command=calculate_minors).pack(pady=10)
    
        result_frame = ttk.Frame(self)
        result_frame.pack(pady=20)
    
        ttk.Button(self, text="Kthehu në Menunë Kryesore", command=self.show_welcome_screen).pack(pady=10)

        
        
    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

# Run the Application
if __name__ == "__main__":
    app = MatrixApp()
    app.mainloop()
