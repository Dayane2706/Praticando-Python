import tkinter as tk
from tkinter import messagebox
import random # gerar números aleatorios
import string # manipulação de strings
import pyperclip # interagir com a área de transferência do sistema

# criação da classe "GeradorSenhaGui" para configurar a janela  
class GeradorSenhaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Senhas")
        self.root.geometry("400x500")

        # variáveis de controle para as opções
        self.incluir_maiuscula_var = tk.BooleanVar(value=False) # inicialização em false para garantir que nenhuma opção esteja marcada ao usuario iniciar o programa
        self.incluir_minuscula_var = tk.BooleanVar(value=False)
        self.incluir_numero_var = tk.BooleanVar(value=False)
        self.incluir_simbolo_var = tk.BooleanVar(value=False)
        self.incluir_emoji_var = tk.BooleanVar(value=False)

        self.configurar_interface()

    def configurar_interface(self):
        
        frame_opcoes = tk.Frame(self.root)
        frame_opcoes.pack(pady=10)

        tk.Label(frame_opcoes, text="Opções de Senha").pack()

        # opções de senha
        tk.Checkbutton(frame_opcoes, text="Incluir letra maiúscula", variable=self.incluir_maiuscula_var).pack(anchor="w", padx=10)
        tk.Checkbutton(frame_opcoes, text="Incluir letra minúscula", variable=self.incluir_minuscula_var).pack(anchor="w", padx=10)
        tk.Checkbutton(frame_opcoes, text="Incluir número", variable=self.incluir_numero_var).pack(anchor="w", padx=10)
        tk.Checkbutton(frame_opcoes, text="Incluir símbolo", variable=self.incluir_simbolo_var).pack(anchor="w", padx=10)
        tk.Checkbutton(frame_opcoes, text="Incluir emoji", variable=self.incluir_emoji_var).pack(anchor="w", padx=10)

        # tamanho da senha
        frame_tamanho = tk.Frame(self.root)
        frame_tamanho.pack(pady=10)

        tk.Label(frame_tamanho, text="Tamanho da Senha").pack()

        self.tamanho_entry = tk.Entry(frame_tamanho)
        self.tamanho_entry.pack()

        self.tamanho_entry.insert(0, "Min 10 caracteres")

        # botão para gerar senha
        tk.Button(self.root, text="Gerar Senha", command=self.gerar_senha).pack(pady=20)

        # senha Gerada
        frame_senha = tk.Frame(self.root)
        frame_senha.pack()

        tk.Label(frame_senha, text="Senha Gerada").pack()

        self.senha_text = tk.Entry(frame_senha, state="readonly", font=("Segoe UI Emoji", 14), bd=5, relief="solid", xscrollcommand=self.configurar_rolagem_horizontal)
        self.senha_text.pack()

        # barra de rolagem horizontal
        self.rolagem_horizontal = tk.Scrollbar(frame_senha, orient="horizontal", command=self.senha_text.xview)
        self.rolagem_horizontal.pack(fill="x")

        # sincronizando a barra de rolagem para a o campo da senha gerada
        self.senha_text.config(xscrollcommand=self.rolagem_horizontal.set)

        # força da Senha
        frame_forca = tk.Frame(self.root)
        frame_forca.pack()

        tk.Label(frame_forca, text="Força da Senha").pack()

        self.forca_entry = tk.Entry(frame_forca, state="readonly", font=("Helvetica", 12), bd=5, relief="solid", width=10, justify="center")
        self.forca_entry.pack()

        # botão para copiar para a área de transferência
        tk.Button(self.root, text="Copiar para Área de Transferência", command=self.copiar_para_area_transferencia).pack(pady=20)

    def configurar_rolagem_horizontal(self, *args):
        self.senha_text.xview(*args)

    def gerar_senha(self):
        tamanho_input = self.tamanho_entry.get()

        if not tamanho_input or tamanho_input == "Min 10 caracteres": # padrão estabelecido para garantir a integridade da senha
            messagebox.showerror("Erro", "Insira um valor válido para o tamanho da senha.")
            return

        # verifica se o valor inserido tem apenas dígitos inteiros
        if not tamanho_input.isdigit():
            messagebox.showerror("Erro", "O tamanho da senha deve ser um número inteiro.")
            return
    
        try:
            tamanho = int(tamanho_input)
            limite_caracteres = 30  # padrão definido como maximo de caracteres que o usuario pode ta criando uma senha
            if tamanho < 10 or tamanho > limite_caracteres:
                raise ValueError(f"O tamanho da senha deve ser no mínimo 10 e no máximo {limite_caracteres} caracteres.")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return

        # definindo opções de geração de senha
        opcoes = {
            "incluir_maiuscula": self.incluir_maiuscula_var.get(),
            "incluir_minuscula": self.incluir_minuscula_var.get(),
            "incluir_numero": self.incluir_numero_var.get(),
            "incluir_simbolo": self.incluir_simbolo_var.get(),
            "incluir_emoji": self.incluir_emoji_var.get()
        }

        if not any(opcoes.values()):
            messagebox.showwarning("Aviso", "Selecione pelo menos uma opção para gerar a senha.")
            return

        # a força da senha depennde de quantas opções foram marcadas
        senha_gerada = self.gerar_senha_aleatoria(tamanho, opcoes, limite_caracteres)
        forca_senha = self.forca_senha(opcoes)

        self.senha_text.config(state="normal")
        self.senha_text.delete(0, tk.END)
        self.senha_text.insert(0, senha_gerada)
        self.senha_text.config(state="readonly")

        self.forca_entry.config(state="normal")
        self.forca_entry.delete(0, tk.END)
        self.forca_entry.insert(0, forca_senha)
        self.forca_entry.config(state="readonly")

    def gerar_senha_aleatoria(self, tamanho, opcoes, limite_caracteres):
        caracteres = ""
        senha_gerada = ""

        if sum(opcoes.values()) == 1:
            # se apenas uma opção for selecionada, gerar senha exclusivamente a partir dessa mesma opção somente
            if opcoes["incluir_maiuscula"]:
                caracteres += string.ascii_uppercase
            elif opcoes["incluir_minuscula"]:
                caracteres += string.ascii_lowercase
            elif opcoes["incluir_numero"]:
                caracteres += string.digits
            elif opcoes["incluir_simbolo"]:
                caracteres += string.punctuation
            elif opcoes["incluir_emoji"]:
                caracteres += "😍🥹😡👽🤖🥸"
            
            senha_gerada = ''.join(random.choice(caracteres) for _ in range(tamanho))
        else:
            # se múltiplas opções foram selecionadas, essa é a logica a ser seguida
            if opcoes["incluir_maiuscula"]:
                caracteres += string.ascii_uppercase
                senha_gerada += random.choice(string.ascii_uppercase)
            if opcoes["incluir_minuscula"]:
                caracteres += string.ascii_lowercase
                senha_gerada += random.choice(string.ascii_lowercase)
            if opcoes["incluir_numero"]:
                caracteres += string.digits
                senha_gerada += random.choice(string.digits)
            if opcoes["incluir_simbolo"]:
                caracteres += string.punctuation
                senha_gerada += random.choice(string.punctuation)
            if opcoes["incluir_emoji"]:
                emojis = "😍🥹😡👽🤖🥸"
                caracteres += emojis
                senha_gerada += random.choice(emojis)

            # completando a senha com caracteres aleatórios
            senha_gerada += ''.join(random.sample(caracteres, min(tamanho - len(senha_gerada), limite_caracteres - len(senha_gerada))))

        return senha_gerada

    # função para copiar a senha gerada na área de transferência
    def copiar_para_area_transferencia(self):
        senha = self.senha_text.get()

        if senha:
            pyperclip.copy(senha)
            messagebox.showinfo("Copiado", "Senha copiada para a área de transferência.")
        else:
            messagebox.showwarning("Aviso", "Nenhuma senha gerada para copiar.")
    
    # definição da força da senha de acordo com quantas opções o usuario marcou
    def forca_senha(self, opcoes):
        quantidade_opcoes = sum(opcoes.values())

        if quantidade_opcoes == 1:
            return "Fraca"
        elif quantidade_opcoes == 2:
            return "Média"
        elif quantidade_opcoes == 3:
            return "Boa"
        elif quantidade_opcoes == 4:
            return "Ótima"
        elif quantidade_opcoes == 5:
            return "Excelente"
        else:
            return "Desconhecida"

if __name__ == "__main__":
    root = tk.Tk()
    app = GeradorSenhaGUI(root)
    root.mainloop()
