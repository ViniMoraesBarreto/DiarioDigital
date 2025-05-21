import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from core.armazenamento import ler_anotacoes, buscar_por_palavra, excluir_anotacao, editar_anotacao

# Janela principal de leitura busca edicao e exclusao
def abrir_janela_leitura(pai):
    janela = tk.Toplevel(pai)
    janela.title("Anotações Salvas")
    janela.geometry("550x400")

    frame = tk.Frame(janela)
    frame.pack(pady=5)

    def buscar():
        termo = simpledialog.askstring("Buscar", "Digite a palavra-chave:")
        if termo:
            resultado = buscar_por_palavra(termo)
            texto.config(state='normal')
            texto.delete("1.0", tk.END)
            texto.insert(tk.END, resultado)
            texto.config(state='disabled')

    tk.Button(frame, text="Buscar", command=buscar).pack(side=tk.LEFT, padx=5)
    tk.Button(frame, text="Editar Anotação", command=lambda: abrir_janela_edicao(janela)).pack(side=tk.LEFT, padx=5)
    tk.Button(frame, text="Excluir Anotação", command=lambda: abrir_janela_excluir(janela)).pack(side=tk.LEFT, padx=5)

    texto = scrolledtext.ScrolledText(janela, width=70, height=20)
    texto.pack(pady=10)

    conteudo = ler_anotacoes()
    texto.insert(tk.END, conteudo)
    texto.config(state='disabled')


# Funcao para abrir a janela de edicao
def abrir_janela_edicao(pai):
    janela = tk.Toplevel(pai)
    janela.title("Editar Anotação")
    janela.geometry("550x470")

    # Ler anotações e mostrar com índice
    linhas = ler_anotacoes().splitlines()
    if not linhas:
        messagebox.showinfo("Info", "Não há anotações para editar.")
        janela.destroy()
        return
    
    texto_anotacoes = ""
    for i, linha in enumerate(linhas):
        texto_anotacoes += f"{i}: {linha}\n"
    
    # Mostra as anotações com índices
    lbl = tk.Label(janela, text="Anotações:")
    lbl.pack()
    
    txt_anotacoes = tk.Text(janela, width=70, height=15)
    txt_anotacoes.insert(tk.END, texto_anotacoes)
    txt_anotacoes.config(state="disabled")
    txt_anotacoes.pack(pady=5)

    # Entrada para índice a editar
    lbl_indice = tk.Label(janela, text="Digite o número da anotação que deseja editar:")
    lbl_indice.pack()
    entry_indice = tk.Entry(janela)
    entry_indice.pack()

    # Entrada para novo texto
    lbl_novo = tk.Label(janela, text="Digite o novo texto para a anotação:")
    lbl_novo.pack()
    entry_novo = tk.Text(janela, width=70, height=5)
    entry_novo.pack()

    def salvar_edicao():
        try:
            idx = int(entry_indice.get())
            novo = entry_novo.get("1.0", tk.END).strip()
            if not novo:
                messagebox.showwarning("Aviso", "O texto novo não pode ser vazio.")
                return
            
            sucesso = editar_anotacao(idx, novo)
            if sucesso:
                messagebox.showinfo("Sucesso", "Anotação editada com sucesso!")
                janela.destroy()
            else:
                messagebox.showerror("Erro", "Índice inválido.")
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido para o índice.")

    btn_salvar = tk.Button(janela, text="Salvar Alteração", command=salvar_edicao)
    btn_salvar.pack(pady=10)

#Funcao para a janela de exclusao
def abrir_janela_excluir(pai):
    janela = tk.Toplevel(pai)
    janela.title("Excluir Anotação")
    janela.geometry("550x450")

    linhas = ler_anotacoes().splitlines()
    if not linhas:
        messagebox.showinfo("Info", "Não há anotações para excluir.")
        janela.destroy()
        return

    texto_anotacoes = ""
    for i, linha in enumerate(linhas):
        texto_anotacoes += f"{i}: {linha}\n"

    tk.Label(janela, text="Anotações:").pack()

    txt_anotacoes = tk.Text(janela, width=70, height=15)
    txt_anotacoes.insert(tk.END, texto_anotacoes)
    txt_anotacoes.config(state="disabled")
    txt_anotacoes.pack(pady=5)

    tk.Label(janela, text="Digite o número da anotação que deseja excluir:").pack()
    entry_indice = tk.Entry(janela)
    entry_indice.pack()

    def confirmar_exclusao():
        try:
            idx = int(entry_indice.get())
            confirmado = messagebox.askyesno("Confirmação", "Tem certeza que quer excluir esta anotação?")
            if not confirmado:
                return

            sucesso = excluir_anotacao(idx)
            if sucesso:
                messagebox.showinfo("Sucesso", "Anotação excluída com sucesso!")
                janela.destroy()
            else:
                messagebox.showerror("Erro", "Índice inválido.")
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido para o índice.")

    tk.Button(janela, text="Excluir", command=confirmar_exclusao).pack(pady=10)
