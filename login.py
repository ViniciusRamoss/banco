import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
import menu

def fazer_login():
    cpf = entry_cpf.get()
    senha = entry_senha.get()

    if not os.path.exists("cadastros.csv"):
        messagebox.showerror("Erro", "Nenhum cadastro encontrado. Por favor, cadastre-se primeiro.")
        return

    try:
        df = pd.read_csv("cadastros.csv", dtype=str)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ler o arquivo de cadastros: {e}")
        return

    usuario = df[df["CPF"] == cpf]

    if usuario.empty:
        messagebox.showinfo("Cadastro não encontrado", "CPF não cadastrado. Por favor, faça seu cadastro.")
    else:
        senha_correta = usuario.iloc[0]["Senha"]
        if senha == senha_correta:
            messagebox.showinfo("Acesso Liberado", "Login realizado com sucesso!")
            root.destroy()
            menu.menu_principal(cpf)
        else:
            messagebox.showerror("Erro", "Senha incorreta.")

def abrir_cadastro():
    root.destroy()
    os.system('python cadastro.py')

root = tk.Tk()
root.title("Login")

tk.Label(root, text="CPF").grid(row=0, column=0, sticky="e")
entry_cpf = tk.Entry(root, width=30)
entry_cpf.grid(row=0, column=1)

tk.Label(root, text="Senha").grid(row=1, column=0, sticky="e")
entry_senha = tk.Entry(root, show="*", width=30)
entry_senha.grid(row=1, column=1)

frame_botoes = tk.Frame(root)
frame_botoes.grid(row=2, column=0, columnspan=2, pady=10)

tk.Button(frame_botoes, text="Entrar", command=fazer_login).pack(side="left", padx=5)
tk.Button(frame_botoes, text="Cadastro", command=abrir_cadastro).pack(side="left", padx=5)

root.mainloop()