import tkinter as tk
from ui.escrever import abrir_janela_escrever
from ui.ler import abrir_janela_leitura

def criar_menu(janela):
    # Usar tk.Label e tk.Button para manter padrão
    tk.Label(janela, text="Diário Digital", font=("Arial", 16, "bold")).pack(pady=20)

    tk.Button(janela, text="Escrever Anotação", width=25, command=lambda: abrir_janela_escrever(janela)).pack(pady=5)
    tk.Button(janela, text="Ler Anotações", width=25, command=lambda: abrir_janela_leitura(janela)).pack(pady=5)
    tk.Button(janela, text="Sair", width=25, command=janela.quit).pack(pady=20)
    
