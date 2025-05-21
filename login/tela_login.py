import tkinter as tk
from tkinter import messagebox
from core.armazenamento import set_usuario
from login.auth import criar_tabela, verificar_login, cadastrar_usuario

def iniciar_tela_login(callback_sucesso):
    criar_tabela()

    janela = tk.Tk()
    janela.title("Login")
    janela.geometry("300x220")

    tk.Label(janela, text="Usuário:").pack()
    entry_usuario = tk.Entry(janela)
    entry_usuario.pack()

    tk.Label(janela, text="Senha:").pack()
    entry_senha = tk.Entry(janela, show="*")
    entry_senha.pack()

    def fazer_login():
        usuario = entry_usuario.get().strip()
        senha = entry_senha.get().strip()
        if verificar_login(usuario, senha):  # Verifica credenciais
            set_usuario(usuario)            # Salva o usuário logado
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            janela.destroy()                # Fecha a janela de login
            callback_sucesso()              # Abre a aplicação principal
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    def registrar():
        usuario = entry_usuario.get().strip()
        senha = entry_senha.get().strip()
        if not usuario or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return
        if cadastrar_usuario(usuario, senha):
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        else:
            messagebox.showerror("Erro", "Usuário já existe.")

    tk.Button(janela, text="Login", command=fazer_login).pack(pady=5)
    tk.Button(janela, text="Cadastrar", command=registrar).pack()

    janela.mainloop()

