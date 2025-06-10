import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

def atualizar_saldo(cpf, conta, novo_saldo):
    df = pd.read_csv("cadastros.csv", dtype=str)
    df.loc[(df["CPF"] == cpf) & (df["Conta"] == conta), "Saldo"] = str(novo_saldo)
    df.to_csv("cadastros.csv", index=False)

def adicionar_extrato(cpf, conta, texto):
    extrato_arquivo = f"extrato_{cpf}_{conta}.txt"
    with open(extrato_arquivo, "a", encoding="utf-8") as f:
        f.write(texto + "\n")

def ler_extrato(cpf, conta):
    extrato_arquivo = f"extrato_{cpf}_{conta}.txt"
    if os.path.exists(extrato_arquivo):
        with open(extrato_arquivo, "r", encoding="utf-8") as f:
            return f.read()
    return "Nenhuma movimentação."

def abrir_deposito(cpf, conta, saldo_var):
    def concluir():
        try:
            valor = float(entry_valor.get().replace(",", "."))
            if valor <= 0:
                messagebox.showerror("Erro", "O valor deve ser maior que 0.")
                return
            saldo_atual = float(saldo_var.get())
            novo_saldo = saldo_atual + valor
            saldo_var.set(f"{novo_saldo:.2f}")
            atualizar_saldo(cpf, conta, novo_saldo)
            adicionar_extrato(cpf, conta, f"Deposito: +R${valor:.2f}")
            messagebox.showinfo("Sucesso", "Depósito realizado com sucesso!")
            janela.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor válido.")

    janela = tk.Toplevel()
    janela.title("Depósito")
    tk.Label(janela, text="Valor do depósito:").pack(padx=10, pady=5)
    entry_valor = tk.Entry(janela)
    entry_valor.pack(padx=10, pady=5)
    tk.Button(janela, text="Concluir Depósito", command=concluir).pack(pady=10)

def abrir_transferencia(cpf, conta_origem, saldo_var):
    def concluir():
        try:
            valor = float(entry_valor.get().replace(",", "."))
            agencia_dest = entry_agencia_dest.get().strip()
            conta_dest = entry_conta_dest.get().strip()
            saldo_atual = float(saldo_var.get())

            if valor <= 0:
                messagebox.showerror("Erro", "O valor deve ser maior que 0.")
                return
            if valor > saldo_atual:
                messagebox.showerror("Erro", "Saldo insuficiente.")
                return
            if not agencia_dest or not conta_dest:
                messagebox.showerror("Erro", "Informe agência e conta de destino.")
                return

            df = pd.read_csv("cadastros.csv", dtype=str)
            destino = df[(df["Agencia"] == agencia_dest) & (df["Conta"] == conta_dest)]
            if destino.empty:
                messagebox.showerror("Erro", "Conta/agência de destino não encontrada.")
                return
            if agencia_dest == df[df["Conta"] == conta_origem].iloc[0]["Agencia"] and conta_dest == conta_origem:
                messagebox.showerror("Erro", "Não é possível transferir para a mesma conta.")
                return

            novo_saldo_origem = saldo_atual - valor
            atualizar_saldo(cpf, conta_origem, novo_saldo_origem)
            adicionar_extrato(cpf, conta_origem, f"Transferencia: -R${valor:.2f}")

            cpf_dest = destino.iloc[0]["CPF"]
            saldo_dest_atual = float(destino.iloc[0]["Saldo"])
            novo_saldo_dest = saldo_dest_atual + valor
            atualizar_saldo(cpf_dest, conta_dest, novo_saldo_dest)
            adicionar_extrato(cpf_dest, conta_dest, f"Deposito: +R${valor:.2f}")

            df_atualizado = pd.read_csv("cadastros.csv", dtype=str)
            saldo_atualizado = df_atualizado[(df_atualizado["CPF"] == cpf) & (df_atualizado["Conta"] == conta_origem)].iloc[0]["Saldo"]
            saldo_var.set(saldo_atualizado)

            messagebox.showinfo("Sucesso", "Transferência realizada com sucesso!")
            janela.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor válido.")

    janela = tk.Toplevel()
    janela.title("Transferência")
    tk.Label(janela, text="Agência de destino:").pack(padx=10, pady=2)
    entry_agencia_dest = tk.Entry(janela)
    entry_agencia_dest.pack(padx=10, pady=2)
    tk.Label(janela, text="Conta de destino:").pack(padx=10, pady=2)
    entry_conta_dest = tk.Entry(janela)
    entry_conta_dest.pack(padx=10, pady=2)
    tk.Label(janela, text="Valor da transferência:").pack(padx=10, pady=2)
    entry_valor = tk.Entry(janela)
    entry_valor.pack(padx=10, pady=2)
    tk.Button(janela, text="Concluir Transferência", command=concluir).pack(pady=10)

def abrir_pagamento(cpf, conta, saldo_var):
    def concluir():
        try:
            valor = float(entry_valor.get().replace(",", "."))
            saldo_atual = float(saldo_var.get())
            if valor <= 0:
                messagebox.showerror("Erro", "O valor deve ser maior que 0.")
                return
            if valor > saldo_atual:
                messagebox.showerror("Erro", "Saldo insuficiente.")
                return
            novo_saldo = saldo_atual - valor
            saldo_var.set(f"{novo_saldo:.2f}")
            atualizar_saldo(cpf, conta, novo_saldo)
            adicionar_extrato(cpf, conta, f"Pagamento: -R${valor:.2f}")
            messagebox.showinfo("Sucesso", "Pagamento realizado com sucesso!")
            janela.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor válido.")

    janela = tk.Toplevel()
    janela.title("Pagamento")
    tk.Label(janela, text="Valor do pagamento:").pack(padx=10, pady=5)
    entry_valor = tk.Entry(janela)
    entry_valor.pack(padx=10, pady=5)
    tk.Button(janela, text="Concluir Pagamento", command=concluir).pack(pady=10)

def abrir_extrato(cpf, conta):
    janela = tk.Toplevel()
    janela.title("Extrato")
    extrato_texto = ler_extrato(cpf, conta)
    tk.Label(janela, text="Extrato da Conta", font=("Arial", 12, "bold")).pack(pady=5)
    text = tk.Text(janela, width=40, height=15)
    text.pack(padx=10, pady=5)
    text.insert(tk.END, extrato_texto)
    text.config(state=tk.DISABLED)

def menu_principal(cpf):
    df = pd.read_csv("cadastros.csv", dtype=str)
    contas_usuario = df[df["CPF"] == cpf]
    nome_completo = contas_usuario.iloc[0]["Nome Completo"] if not contas_usuario.empty else "Usuário"

    root = tk.Tk()
    root.title("Menu")

    tk.Label(root, text=f"Bem vindo! {nome_completo}", font=("Arial", 14, "bold")).pack(pady=10)

    for idx, row in contas_usuario.iterrows():
        frame = tk.LabelFrame(root, text=f"Agência: {row['Agencia']} | Conta: {row['Conta']}", padx=10, pady=10)
        frame.pack(padx=10, pady=5, fill="x")

        saldo_var = tk.StringVar(value=row["Saldo"])
        tk.Label(frame, text="Saldo: R$").grid(row=0, column=0, sticky="e")
        tk.Label(frame, textvariable=saldo_var).grid(row=0, column=1, sticky="w")

        tk.Button(frame, text="Depósito", command=lambda c=row['Conta'], s=saldo_var: abrir_deposito(cpf, c, s)).grid(row=1, column=0, pady=5)
        tk.Button(frame, text="Transferência", command=lambda c=row['Conta'], s=saldo_var: abrir_transferencia(cpf, c, s)).grid(row=1, column=1, pady=5)
        tk.Button(frame, text="Pagamento", command=lambda c=row['Conta'], s=saldo_var: abrir_pagamento(cpf, c, s)).grid(row=1, column=2, pady=5)
        tk.Button(frame, text="Extrato", command=lambda c=row['Conta']: abrir_extrato(cpf, c)).grid(row=1, column=3, pady=5)

    root.mainloop()
