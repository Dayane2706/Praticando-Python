
# importação da biblioteca tkinter para configurar a interface grafica
import tkinter as tk 
from tkinter import messagebox

# dicionario com os valores respectivos a cada simbolo romano
class ConversorRomanoInteiro:
    def __init__(self):
        self.valores_romanos = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        
    # criando o metodo "romano_para_inteiro"
    def romano_para_inteiro(self, romano):
        inteiro = 0 # esta variável serve para acumular o valor numérico total correspondente ao numeral romano
        anterior = 0  #  ja essa variável é usada para armazenar o valor do numeral romano anterior durante o processo de conversão, para saber se deve somar ou subtrair

        for simbolo in reversed(romano): #  iteraração sobre os caracteres do numeral romano na ordem inversa
            valor = self.valores_romanos.get(simbolo) # pegando o valor associado a um determinado simbolo na biblioteca valores_romanos
            if valor is None:
                raise ValueError(f"Símbolo romano inválido: {simbolo}")

            if valor < anterior:
                inteiro -= valor # exemplo: o simbolo "IV". Deve subtarir "I" do "V" para resultar valor 4(IV) em inteiro
            else:
                inteiro += valor

            anterior = valor

        return inteiro
    
    # criando o metodo "inteiro_para_romano"
    def inteiro_para_romano(self, inteiro):
        if not 0 < inteiro < 10000: # estabelecendo um padrao  de numeros validos entre 1 e 9999
            raise ValueError("Digite um número entre 1 e 9999.")

        valores_romanos = {1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL', 50: 'L', 90: 'XC',
                           100: 'C', 400: 'CD', 500: 'D', 900: 'CM', 1000: 'M'}

        resultado_romano = "" # armazenar o resultado da conversão
        for valor, simbolo in sorted(valores_romanos.items(), key=lambda x: x[0], reverse=True): # lambda utilizada para extrair o valor numérico associado a cada símbolo romano
            while inteiro >= valor:
                resultado_romano += simbolo
                inteiro -= valor

        return resultado_romano

class InterfaceGrafica:
    def __init__(self, root):
        self.root = root
        self.conversor = ConversorRomanoInteiro()
        self.configurar_interface()
        
    # método para criar e empacotar um frame na interface gráfica
    def criar_label_entry(self, texto, var=None, evento=None):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        label = tk.Label(frame, text=texto)
        label.pack(side=tk.LEFT)

        entry = tk.Entry(frame, textvariable=var)
        entry.pack(side=tk.LEFT)

        if evento:
            entry.bind("<KeyRelease>", evento)

        return entry
    
    # criando metodo "converter_romano"
    def converter_romano(self, event):
        simbolo_romano = self.var_romano.get().upper()  # caso o usuario digite em miniscula, seja garantido que a função ocorra normalmente

        if not simbolo_romano:
            self.resultado_label.config(text="")
            self.romano_automatico_label.config(text="")
            return  

        try:
            inteiro_resultado = self.conversor.romano_para_inteiro(simbolo_romano) # converte o simbolo romano para inteiro
            self.resultado_label.config(text=f"Resultado em inteiro: {inteiro_resultado}")  # configuração para exibir o formato eem inteiro
            self.romano_automatico_label.config(text=f"Resultado em romano: {self.conversor.inteiro_para_romano(inteiro_resultado)}") # para exibir o resultado convertido em romano
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def atualizar_resultados_inteiros(self, event):
        inteiro_input = self.entry_inteiro.get()

        if not inteiro_input:
            self.resultado_romano_para_inteiro_label.config(text="")
            return 

        try:
            inteiro_input = int(inteiro_input)
            romano_resultado = self.conversor.inteiro_para_romano(inteiro_input)
            self.resultado_romano_para_inteiro_label.config(text=f"Resultado em romano: {romano_resultado}")
        except ValueError as e:
            mensagem = str(e)
            
        if "invalid literal for int() with base 10" in mensagem:
            mensagem = "Digite um número inteiro válido!"
        messagebox.showerror("Erro", mensagem)
        
    # configuração da interface
    def configurar_interface(self):
        self.root.title("Conversor Romano-Inteiro")

        # Conversão Romano para Inteiro
        self.var_romano = tk.StringVar()
        self.entry_romano = self.criar_label_entry("Digite um número romano:", var=self.var_romano, evento=self.converter_romano)
        self.resultado_label = tk.Label(self.root, text="")
        self.resultado_label.pack()
        self.romano_automatico_label = tk.Label(self.root, text="")
        self.romano_automatico_label.pack()

        # Conversão Inteiro para Romano
        self.entry_inteiro = self.criar_label_entry("Digite um número inteiro:", evento=self.atualizar_resultados_inteiros)
        self.resultado_romano_para_inteiro_label = tk.Label(self.root, text="")
        self.resultado_romano_para_inteiro_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x150") 
    app = InterfaceGrafica(root)
    root.mainloop()
