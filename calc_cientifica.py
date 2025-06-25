import tkinter as tk
from math import sin, cos, tan, log, sqrt, pi, e, radians

# Clase principal de la calculadora científica
class CalculadoraCientifica:
    def __init__(self, root):
        # Inicializa la ventana principal
        self.root = root
        self.root.title("Calculadora Científica")
        self.root.resizable(False, False)
        self.expresion = ""
        self.resultado = tk.StringVar()

        # Crea la interfaz de usuario
        self.crear_interfaz()

    def crear_interfaz(self):
        # Colores y fuentes para la interfaz
        color_fondo = "#2d2d2d"
        color_boton = "#444444"
        color_operador = "#f39c12"
        color_texto = "#ffffff"
        fuente = ("Arial", 22)

        # Configura el color de fondo de la ventana
        self.root.configure(bg=color_fondo)

        # Pantalla de la calculadora
        pantalla = tk.Entry(self.root, textvariable=self.resultado, font=("Arial", 28), bd=0, bg=color_fondo, fg=color_texto, justify="right")
        pantalla.grid(row=0, column=0, columnspan=5, ipadx=8, ipady=25, sticky="we", padx=10, pady=10)

        # Definición de los botones de la calculadora
        botones = [
            ('C', 1, 0, color_boton), ('+/-', 1, 1, color_boton), ('%', 1, 2, color_boton), ('÷', 1, 3, color_operador), ('√', 1, 4, color_boton),
            ('7', 2, 0, color_boton), ('8', 2, 1, color_boton), ('9', 2, 2, color_boton), ('×', 2, 3, color_operador), ('sin', 2, 4, color_boton),
            ('4', 3, 0, color_boton), ('5', 3, 1, color_boton), ('6', 3, 2, color_boton), ('-', 3, 3, color_operador), ('cos', 3, 4, color_boton),
            ('1', 4, 0, color_boton), ('2', 4, 1, color_boton), ('3', 4, 2, color_boton), ('+', 4, 3, color_operador), ('tan', 4, 4, color_boton),
            ('0', 5, 0, color_boton), ('.', 5, 1, color_boton), ('(', 5, 2, color_boton), (')', 5, 3, color_boton), ('log', 5, 4, color_boton),
            ('π', 6, 0, color_boton), ('e', 6, 1, color_boton), ('^', 6, 2, color_boton), ('=', 6, 3, color_operador), ('', 6, 4, color_fondo)
        ]

        # Creación de los botones en la interfaz
        for (texto, fila, columna, color) in botones:
            if texto:
                accion = lambda x=texto: self.pulsar_boton(x)
                tk.Button(self.root, text=texto, width=4, height=2, font=fuente, bg=color, fg=color_texto, bd=0, command=accion)\
                    .grid(row=fila, column=columna, padx=4, pady=4, sticky="nsew")

        # Configuración de la expansión de columnas y filas
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)

    # Método para manejar la pulsación de botones
    def pulsar_boton(self, tecla):
        if tecla == "C":
            # Limpiar la expresión y el resultado
            self.expresion = ""
            self.resultado.set("")
        elif tecla == "=":
            # Evaluar la expresión matemática
            try:
                expresion_eval = self.expresion.replace('÷', '/').replace('×', '*').replace('^', '**')
                expresion_eval = expresion_eval.replace('π', str(pi)).replace('e', str(e))
                expresion_eval = expresion_eval.replace('%', '/100')
                self.resultado.set(str(eval(expresion_eval, {"__builtins__": None}, {
                    "sin": lambda x: sin(radians(x)),
                    "cos": lambda x: cos(radians(x)),
                    "tan": lambda x: tan(radians(x)),
                    "log": log,
                    "sqrt": sqrt,
                    "pi": pi,
                    "e": e
                })))
                self.expresion = self.resultado.get()
            except Exception:
                # Manejo de errores en la evaluación
                self.resultado.set("Error")
                self.expresion = ""
        elif tecla == "+/-":
            # Cambiar el signo de la expresión
            if self.expresion:
                if self.expresion[0] == "-":
                    self.expresion = self.expresion[1:]
                else:
                    self.expresion = "-" + self.expresion
                self.resultado.set(self.expresion)
        elif tecla in ("sin", "cos", "tan", "log", "√"):
            # Funciones matemáticas avanzadas
            try:
                valor = float(self.expresion) if self.expresion else 0
                if tecla == "sin":
                    res = sin(radians(valor))
                elif tecla == "cos":
                    res = cos(radians(valor))
                elif tecla == "tan":
                    res = tan(radians(valor))
                elif tecla == "log":
                    res = log(valor)
                elif tecla == "√":
                    res = sqrt(valor)
                self.expresion = str(res)
                self.resultado.set(self.expresion)
            except Exception:
                self.resultado.set("Error")
                self.expresion = ""
        elif tecla == "%":
            # Calcular el porcentaje
            try:
                valor = float(self.expresion) if self.expresion else 0
                res = valor / 100
                self.expresion = str(res)
                self.resultado.set(self.expresion)
            except Exception:
                self.resultado.set("Error")
                self.expresion = ""
        elif tecla in ("π", "e"):
            # Agregar constantes matemáticas
            self.expresion += str(pi) if tecla == "π" else str(e)
            self.resultado.set(self.expresion)
        else:
            # Agregar caracteres a la expresión
            self.expresion += str(tecla)
            self.resultado.set(self.expresion)

# Punto de entrada de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraCientifica(root)
    root.mainloop()