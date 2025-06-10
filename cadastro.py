import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random
import os

cadastros = []

def gerar_agencia():
    return f"{random.randint(1000, 9999)}"

def gerar_conta():
    numero = random.randint(10000000, 99999999)
    digito = random.randint(0, 9)
    return f"{numero:08d}-{digito}"

def conta_existe(conta):
    if os.path.exists("cadastros.csv"):
        df = pd.read_csv("cadastros.csv", dtype=str)
        return not df[df["Conta"] == conta].empty
    return False

def salvar_cadastro():
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    nascimento = entry_nascimento.get()
    cpf = entry_cpf.get()
    endereco = entry_endereco.get()
    senha = entry_senha.get()
    confirmacao = entry_confirmacao.get()
    saldo = 0

    if senha != confirmacao:
        messagebox.showerror("Erro", "As senhas não são iguais!")
        return

    agencia = gerar_agencia()
    conta = gerar_conta()
    tentativas = 0
    while conta_existe(conta):
        conta = gerar_conta()
        tentativas += 1
        if tentativas > 1000:
            messagebox.showerror("Erro", "Não foi possível gerar uma conta única. Tente novamente.")
            return

    cadastros.append({
        "Nome Completo": nome,
        "Email": email,
        "Telefone": telefone,
        "Data de Nascimento": nascimento,
        "CPF": cpf,
        "Endereço": endereco,
        "Senha": senha,
        "Agencia": agencia,
        "Conta": conta,
        "Saldo": saldo
    })

    if os.path.exists("cadastros.csv"):
        df_existente = pd.read_csv("cadastros.csv", dtype=str)
        df = pd.concat([df_existente, pd.DataFrame(cadastros)], ignore_index=True)
    else:
        df = pd.DataFrame(cadastros)

    df.to_csv("cadastros.csv", index=False)

    messagebox.showinfo("Sucesso", f"Cadastro realizado!\nAgência: {agencia}\nConta: {conta}")
    limpar_campos()
    cadastros.clear()

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_nascimento.delete(0, tk.END)
    entry_cpf.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)
    entry_senha.delete(0, tk.END)
    entry_confirmacao.delete(0, tk.END)

def abrir_login():
    root.destroy()
    os.system('python login.py')

root = tk.Tk()
root.title("Cadastro de Usuário")

tk.Label(root, text="Nome Completo").grid(row=0, column=0, sticky="e")
entry_nome = tk.Entry(root, width=40)
entry_nome.grid(row=0, column=1)

tk.Label(root, text="Email").grid(row=1, column=0, sticky="e")
entry_email = tk.Entry(root, width=40)
entry_email.grid(row=1, column=1)

tk.Label(root, text="Telefone").grid(row=2, column=0, sticky="e")
entry_telefone = tk.Entry(root, width=40)
entry_telefone.grid(row=2, column=1)

tk.Label(root, text="Data de Nascimento").grid(row=3, column=0, sticky="e")
entry_nascimento = tk.Entry(root, width=40)
entry_nascimento.grid(row=3, column=1)

tk.Label(root, text="CPF").grid(row=4, column=0, sticky="e")
entry_cpf = tk.Entry(root, width=40)
entry_cpf.grid(row=4, column=1)

tk.Label(root, text="Endereço").grid(row=5, column=0, sticky="e")
entry_endereco = tk.Entry(root, width=40)
entry_endereco.grid(row=5, column=1)

tk.Label(root, text="Senha").grid(row=6, column=0, sticky="e")
entry_senha = tk.Entry(root, show="*", width=40)
entry_senha.grid(row=6, column=1)

tk.Label(root, text="Confirmação de Senha").grid(row=7, column=0, sticky="e")
entry_confirmacao = tk.Entry(root, show="*", width=40)
entry_confirmacao.grid(row=7, column=1)

tk.Button(root, text="Cadastrar", command=salvar_cadastro).grid(row=8, column=0, pady=10)
tk.Button(root, text="Login", command=abrir_login).grid(row=8, column=1, pady=10)

root.mainloop()