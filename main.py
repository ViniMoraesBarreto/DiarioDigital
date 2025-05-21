import tkinter as tk
from login.tela_login import iniciar_tela_login
from ui import menu

def iniciar_aplicacao():
    janela = tk.Tk()
    janela.title("Diário Digital")
    janela.geometry("300x230")
    janela.resizable(False, False)

    menu.criar_menu(janela)

    janela.mainloop()

if __name__ == "__main__":
    iniciar_tela_login(callback_sucesso=iniciar_aplicacao)
