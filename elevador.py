import tkinter as tk
import winsound  # módulo para reprodução de som no Windows

# constantes
TEMPO_ABERTURA_PORTA = 5
TEMPO_INATIVIDADE_MAXIMO = 5

class ElevadorInterface:
    def __init__(self, master):
        self.master = master
        master.title("Elevador")

        # variáveis de controle
        self.andares = 5
        self.andar_atual = 0  # inicio no térreo
        self.solicitacoes = []
        self.em_movimento = False
        self.porta_tempo_aberta = 0
        self.tempo_inativo = 0

        # frame principal
        self.frame_principal = tk.Frame(master)
        self.frame_principal.grid(row=0, column=0, padx=10, pady=10)

        # diagrama de seção transversal e representação do elevador
        self.diagrama = tk.Canvas(self.frame_principal, width=400, height=400, bg="lightgray")
        self.diagrama.grid(row=0, column=0, rowspan=self.andares)

        # adicionando a porta
        self.porta = self.diagrama.create_rectangle(150, 380, 160, 400, fill="black")

        # adicionando andares à esquerda do diagrama
        for i in range(self.andares):
            andar_texto = "T" if i == 0 else str(i)
            self.diagrama.create_text(130, 380 - i * 80 - 40, text=andar_texto, font=("Helvetica", 10), anchor="e")

        # painel de controle do elevador
        self.painel_controle = tk.Frame(self.frame_principal)
        self.painel_controle.grid(row=0, column=1, padx=10)

        self.botoes_andar = []

        for i in reversed(range(self.andares)):
            andar_texto = "T" if i == 0 else str(i)
            botao = tk.Button(self.painel_controle, text=andar_texto, command=lambda i=i: self.selecionar_andar(i),
                              width=5, height=2)
            botao.grid(row=self.andares - 1 - i, column=0, pady=5)
            self.botoes_andar.append(botao)

        # adicionando botão para subir (setinha para cima) ao 1º andar ao ser chamado
        self.botao_chamar_cima = tk.Button(self.painel_controle, text="↑", command=self.chamar_elevador_cima, width=5, height=2)
        self.botao_chamar_cima.grid(row=self.andares, column=0, pady=5)

        # indicador de andar atual
        self.luz_indicadora = tk.Label(self.frame_principal, text="Andar Atual: T", font=("Helvetica", 10))
        self.luz_indicadora.grid(row=self.andares + 1, column=0, columnspan=2)

        # adicionando evento de clique no diagrama para selecionar o andar
        self.diagrama.bind("<Button-1>", self.clique_diagrama)

        # inicio do temporizador de retorno ao térreo
        self.master.after(5000, self.retornar_ao_terreo)
        # inicio do temporizador para verificar inatividade
        self.master.after(1000, self.verificar_inatividade)

    def chamar_elevador_cima(self):
        if not self.em_movimento and not self.porta_tempo_aberta and self.andar_atual == 0:
            self.solicitacoes.append(1)  # adiciona solicitação para o segundo andar
            self.atender_solicitacoes()

    def selecionar_andar(self, andar):
        self.solicitacoes.append(andar)
        self.atender_solicitacoes()

    def atender_solicitacoes(self):
        if not self.em_movimento and not self.porta_tempo_aberta:
            if self.solicitacoes:
                proximo_andar = self.solicitacoes.pop(0)
                self.movimentar_elevador(proximo_andar)
            else:
                self.verificar_inatividade()  # verificação de inatividade

    def movimentar_elevador(self, destino):
        if self.andar_atual < destino:
            self.move_para_cima(destino)
        elif self.andar_atual > destino:
            self.move_para_baixo(destino)
        else:
            # se o destino for o mesmo andar atual, apenas abre a porta
            self.abrir_porta()

    def move_para_cima(self, destino):
        self.em_movimento = True
        for i in range(self.andar_atual, destino + 1):
            self.diagrama.coords(self.porta, 150, 380 - i * 80, 160, 400 - i * 80)
            self.andar_atual = i
            self.atualizar_luz_indicadora()  # atualiza o indicador de andar atual
            self.master.update()
            self.master.after(1000)  # padronizando o atraso de 1 segundo

            if i == destino:
                self.abrir_porta()
                self.reproduzir_som("chegada")
                self.atualizar_status("Porta Aberta")
                self.master.after(5000, self.fechar_porta)  # aguarda 5 segundos antes de fechar a porta

        self.em_movimento = False
        self.atender_solicitacoes()  # atende a próxima solicitação

    def move_para_baixo(self, destino):
        self.em_movimento = True
        for i in range(self.andar_atual, destino - 1, -1):
            self.diagrama.coords(self.porta, 150, 380 - i * 80, 160, 400 - i * 80)
            self.andar_atual = i
            self.atualizar_luz_indicadora()
            self.master.update()
            self.master.after(1000)

            if i == destino:
                self.abrir_porta()
                self.reproduzir_som("chegada")
                self.atualizar_status("Porta Aberta")
                self.master.after(5000, self.fechar_porta)

        self.em_movimento = False
        self.atender_solicitacoes()

    def abrir_porta(self):
        self.porta_tempo_aberta = TEMPO_ABERTURA_PORTA
        self.atualizar_status("Porta Aberta")
        self.diagrama.itemconfig(self.porta, fill="gray")
        self.atualizar_status(f"Porta Aberta - Tempo Restante: {self.porta_tempo_aberta}s")
        self.master.after(1000, self.fechar_porta)

    def fechar_porta(self):
        if self.porta_tempo_aberta > 0:
            self.atualizar_status(f"Porta Aberta - Tempo Restante: {self.porta_tempo_aberta}s")
            self.porta_tempo_aberta -= 1
            self.master.after(1000, self.fechar_porta)
        elif self.porta_tempo_aberta == 0:
            self.diagrama.itemconfig(self.porta, fill="black")
            self.atualizar_status("Porta Fechada")
            self.atender_solicitacoes()  # atende a próxima solicitação após fechar a porta

    def retornar_ao_terreo(self):
        if not self.em_movimento and not self.porta_tempo_aberta and self.andar_atual != 0:
            self.movimentar_elevador(0)
            self.atualizar_status("Retornando ao Térreo")

    def verificar_inatividade(self):
        if not self.em_movimento and not self.porta_tempo_aberta:
            self.tempo_inativo += 1
            if self.tempo_inativo == TEMPO_INATIVIDADE_MAXIMO:  
                self.retornar_ao_terreo()
            else:
                self.master.after(1000, self.verificar_inatividade)
        else:
            # reinicia o temporizador se houver alguma atividade
            self.tempo_inativo = 0
            self.master.after(1000, self.verificar_inatividade)

    def reproduzir_som(self, tipo):
        if tipo == "chegada":
            winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

    def atualizar_luz_indicadora(self):
        andar_texto = "T" if self.andar_atual == 0 else str(self.andar_atual)
        self.luz_indicadora.config(text=f"Andar Atual: {andar_texto}")

    def atualizar_status(self, mensagem):
        andar_texto = "T" if self.andar_atual == 0 else str(self.andar_atual)
        self.luz_indicadora.config(text=f"Andar Atual: {andar_texto} - {mensagem}")

    def clique_diagrama(self, event):
        if not self.em_movimento and not self.porta_tempo_aberta:
            x, y = event.x, event.y

            if 150 <= x <= 250 and 0 <= y <= 400:
                andar = (400 - y) // 80
                self.selecionar_andar(andar)


if __name__ == "__main__":
    root = tk.Tk()
    interface = ElevadorInterface(root)
    root.mainloop()
