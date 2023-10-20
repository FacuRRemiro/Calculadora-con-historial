import tkinter as tk
from tkinter import messagebox, scrolledtext

# Clase que representa la calculadora
class Calculadora:
    def __init__(self, master):
        # Inicialización de la calculadora
        self.master = master
        self.master.title("Calculadora")  # Título de la ventana
        self.master.resizable(width=False, height=False)  # No se puede redimensionar
        self.master.configure(bg='#0597F2')  # Color de fondo

        # Inicialización de elementos de la interfaz
        self.history_text = None

        # Botón para abrir el historial
        log_calc = tk.Button(master, text="LOG", command=self.show_history, font=('Arial', 8), borderwidth=0, background="#0597F2", foreground="#FFFFFF",)
        log_calc.grid(row=0, column=3, sticky="W,E")

        # Entrada de texto
        self.entry = tk.Entry(master, width=10, font=('Arial', 40), bd=5, insertwidth=4, justify='right', background="#3866F2", foreground="#FFFFFF", borderwidth=0)
        self.entry.grid(row=1, column=0, columnspan=4)

        # Label para mostrar la operación anterior
        self.last_op = tk.Label(master, text="", font=('Arial', 12), bg='#3866F2', fg='#FFFFFF', anchor="e")
        self.last_op.grid(row=2, column=0, columnspan=4, sticky="W,E")

        # Obtener las dimensiones de la pantalla
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Definir el tamaño de la ventana
        window_width = 290
        window_height = 450

        # Calcular la posición para centrar la ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Configurar la geometría de la ventana
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Definir botones y sus posiciones en la interfaz
        buttons = [
            ('(', 3, 0), (')', 3, 1), ('√', 3, 2), ('^', 3, 3),
            ('CE', 4, 0), ('x', 4, 1), ('÷', 4, 2), ('DEL', 4, 3),
            ('7', 5, 0), ('8', 5, 1), ('9', 5, 2), ('-', 5, 3),
            ('4', 6, 0), ('5', 6, 1), ('6', 6, 2), ('+', 6, 3),
            ('1', 7, 0), ('2', 7, 1), ('3', 7, 2), ('=', 7, 3),
            ('.', 8, 0), ('0', 8, 1), ('%', 8, 2)
        ]

        # Crear botones en la interfaz y definir sus propiedades
        for (text, row, col) in buttons:
            if text == '=':
                tk.Button(master, text=text, width=5, height=5, command=lambda t=text: self.button_click(t), font=('Arial', 16), borderwidth=0, background="#3866F2", foreground="#FFFFFF").grid(row=row, column=col, rowspan=2, sticky=("W,E"))
            elif row == 3:
                tk.Button(master, text=text, width=5, height=1, command=lambda t=text: self.button_click(t), font=('Arial', 12), borderwidth=0, background="#1B0273", foreground="#FFFFFF").grid(row=row, column=col, sticky=("W,E"))
            elif row == 4:
                tk.Button(master, text=text, width=5, height=2, command=lambda t=text: self.button_click(t), font=('Arial', 16), borderwidth=0, background="#3866F2", foreground="#FFFFFF").grid(row=row, column=col, sticky=("W,E"))
            elif col == 3:
                tk.Button(master, text=text, width=5, height=2, command=lambda t=text: self.button_click(t), font=('Arial', 16), borderwidth=0, background="#3866F2", foreground="#FFFFFF").grid(row=row, column=col, sticky=("W,E"))
            else:
                tk.Button(master, text=text, width=5, height=2, command=lambda t=text: self.button_click(t), font=('Arial', 16), borderwidth=0, background="#0597F2", foreground="#FFFFFF").grid(row=row, column=col, sticky=("W,E"))

        # Símbolos temporales para la calculadora
        self.temp_symbols = {
            '^': '**',
            '√': '**0.5',
            'x': '*',
            '%': '/100',
            '÷': '/'
        }

        # arreglo historial de operaciones
        self.history = []

    def button_click(self, symbol):
        # Método para manejar el clic en los botones
        if symbol == "=":
            try:
                # Intenta evaluar la expresión y mostrar el resultado
                expression = self.entry.get()
                for temp_symbol, real_symbol in self.temp_symbols.items():
                    expression = expression.replace(temp_symbol, real_symbol)
                result = eval(expression)
                self.last_op.config(text=f"{expression} =")
                self.history.append(f"{expression} = {round(result, 3)}")
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(round(result, 3)))
            except Exception as e:
                # En caso de error, muestra un mensaje de error y registra la operación como inválida
                self.last_op.config(text=f"{expression}= Error")
                self.history.append(f"{expression} = Error: Operación no válida")
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
                messagebox.showerror("Error", "Operación inválida")
       
        elif symbol == "CE":
            # Limpiar la entrada y la última operación
            self.entry.delete(0, tk.END)
            self.last_op.config(text="")
        elif symbol == "DEL":
            # Eliminar el último carácter de la entrada
            current_text = self.entry.get()
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, current_text[:-1])
        elif symbol == '%':
            # Agregar el símbolo de porcentaje
            self.entry.insert(tk.END, '%')
        elif symbol in self.temp_symbols:
            # Reemplazar los símbolos temporales con sus representaciones reales
            self.entry.insert(tk.END, symbol)
        else:
            # Agregar el símbolo presionado a la entrada
            self.entry.insert(tk.END, symbol)
    
    def show_history(self):
        # Método para mostrar el historial de operaciones
        x_calc = self.master.winfo_x()
        y_calc = self.master.winfo_y()
        w_calc = self.master.winfo_width()
        history_x = x_calc + w_calc
        history_y = y_calc

        # Crear una nueva ventana para mostrar el historial
        history_window = tk.Toplevel(self.master)
        history_window.title("Historial")
        history_window.resizable(width=False, height=False)
        history_window.geometry(f"300x450+{history_x}+{history_y}")
        history_window.configure(background="#0597F2")

        # Crear un widget de texto desplazable para mostrar el historial
        history_text = scrolledtext.ScrolledText(history_window, width=30, height=20, wrap=tk.WORD, font=('Arial', 12))
        history_text.grid(row=0, column=0, padx=5, pady=5, sticky="W,E")
        history_text.configure(background="#3866F2", foreground="#FFFFFF")

        # Insertar las operaciones en el cuadro de texto
        for operation in self.history:
            history_text.insert(tk.END, f"{operation}\n")

        # Hacer que la ventana sea solo de lectura
        history_text.config(state=tk.DISABLED)

        # Botones adicionales en la ventana de historial
        delete_button = tk.Button(history_window, text="Limpiar", command=self.delete_history, font=('Arial', 10), borderwidth=0, background="#1B0273", foreground="#FFFFFF", width=20)
        delete_button.grid(row=1, column=0, pady=5)

        close_button = tk.Button(history_window, text="Cerrar", command=history_window.destroy, font=('Arial', 10), borderwidth=0, background="#1B0273", foreground="#FFFFFF", width=20)
        close_button.grid(row=2, column=0)

    def delete_history(self):
        # Método para eliminar el historial
        self.history = []
        self.last_op.config(text="")
        messagebox.showinfo("Eliminado", "Se eliminó el historial de operaciones de forma exitosa.")


if __name__ == "__main__":
    # Crear la ventana principal y la calculadora
    root = tk.Tk()
    app = Calculadora(root)
    root.mainloop()

