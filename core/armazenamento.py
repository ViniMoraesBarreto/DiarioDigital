from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

import os

BASE_DIR = "dados_usuarios"
usuario_atual = None

def set_usuario(usuario):
    global usuario_atual
    usuario_atual = usuario

def get_usuario():
    return usuario_atual

def caminho_arquivo():
    """Retorna o caminho do arquivo do usuário atual."""
    if not usuario_atual:
        raise ValueError("Usuário não está definido.")
    
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    
    return os.path.join(BASE_DIR, f"{usuario_atual}_anotacoes.txt")

# Salvar anotacoes
def salvar_anotacao(texto):
    if not texto.strip():
        return False
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(caminho_arquivo(), "a", encoding="utf-8") as f:
        f.write(f"[{data}] {texto.strip()}\n")
    return True

# Ler anotacoes
def ler_anotacoes():
    try:
        with open(caminho_arquivo(), "r", encoding="utf-8") as f:
            return f.read() or "O diário está vazio."
    except FileNotFoundError:
        return "Nenhuma anotação encontrada."

# Buscar anotacoes
def buscar_por_palavra(palavra):
    try:
        with open(caminho_arquivo(), "r", encoding="utf-8") as f:
            linhas = f.readlines()
        resultados = [linha for linha in linhas if palavra.lower() in linha.lower()]
        return "".join(resultados) if resultados else "Nenhum resultado encontrado."
    except FileNotFoundError:
        return "Nenhuma anotação encontrada."

# Editar anotacoes
def editar_anotacao(indice, novo_texto):
    try:
        with open(caminho_arquivo(), "r", encoding="utf-8") as f:
            linhas = f.readlines()

        if indice < 0 or indice >= len(linhas):
            return False

        data = linhas[indice][:21]  # mantém a data/hora original
        linhas[indice] = data + novo_texto.strip() + "\n"

        with open(caminho_arquivo(), "w", encoding="utf-8") as f:
            f.writelines(linhas)

        return True
    except FileNotFoundError:
        return False

# Excluir anotacoes
def excluir_anotacao(indice):
    try:
        with open(caminho_arquivo(), "r", encoding="utf-8") as f:
            linhas = f.readlines()

        if indice < 0 or indice >= len(linhas):
            return False

        linhas.pop(indice)

        with open(caminho_arquivo(), "w", encoding="utf-8") as f:
            f.writelines(linhas)

        return True
    except FileNotFoundError:
        return False

def exportar_para_pdf(texto_widget):
    from datetime import datetime
    conteudo = texto_widget.get("1.0", tk.END).strip()
    if not conteudo:
        messagebox.showinfo("Exportar PDF", "Não há conteúdo para exportar.")
        return

    nome_padrao = f"anotacoes_{get_usuario()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    caminho_pdf = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        initialfile=nome_padrao,
        title="Salvar como PDF"
    )

    if not caminho_pdf:
        return

    try:
        c = canvas.Canvas(caminho_pdf, pagesize=A4)
        largura, altura = A4
        y = altura - 40
        for linha in conteudo.splitlines():
            if y <= 40:
                c.showPage()
                y = altura - 40
            c.drawString(40, y, linha)
            y -= 15
        c.save()
        messagebox.showinfo("Sucesso", f"Anotações exportadas para {caminho_pdf}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao exportar PDF: {e}")
