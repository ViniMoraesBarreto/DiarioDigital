import tkinter as tk
from tkinter import scrolledtext, messagebox
from core.armazenamento import salvar_anotacao

def abrir_janela_escrever(pai):
    janela = tk.Toplevel(pai)
    janela.title("Nova Anotação")
    janela.geometry("400x300")

    tk.Label(janela, text="Escreva sua anotação:").pack(pady=5)
    entrada = scrolledtext.ScrolledText(janela, width=45, height=10)
    entrada.pack(pady=5)

    def salvar():
        texto = entrada.get("1.0", tk.END)
        if salvar_anotacao(texto):
            messagebox.showinfo("Sucesso", "Anotação salva!")
            janela.destroy()
        else:
            messagebox.showwarning("Erro", "A anotação está vazia.")

    tk.Button(janela, text="Salvar", command=salvar).pack(pady=5)
