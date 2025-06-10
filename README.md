# Documentação do Sistema de Cadastro, Login e Gerenciamento Bancário

## Visão Geral

Este sistema é uma aplicação desktop desenvolvida em Python com interface gráfica utilizando `tkinter`. Ele simula um sistema bancário simples, permitindo cadastro de usuários, login, criação de múltiplas contas por CPF, depósitos, transferências, pagamentos e consulta de extrato.

---

## Funcionalidades

### 1. Cadastro de Usuário
- **Campos obrigatórios:** Nome Completo, Email, Telefone, Data de Nascimento, CPF, Endereço, Senha e Confirmação de Senha.
- **Validação:** Senha e confirmação devem ser iguais.
- **Geração automática:** Cada cadastro gera uma agência (4 dígitos) e uma conta (9 dígitos no formato xxxxxxxx-x) únicos.
- **Saldo inicial:** Sempre começa em 0.
- **Persistência:** Dados são salvos em `cadastros.csv`.

### 2. Login
- **Campos:** CPF e Senha.
- **Validação:** Verifica se o CPF existe e se a senha está correta.
- **Acesso:** Após login bem-sucedido, abre o menu principal do usuário.

### 3. Menu Principal
- **Saudação:** Exibe "Bem vindo! {Nome Completo}".
- **Contas:** Lista todas as contas do CPF logado, mostrando agência, conta e saldo.
- **Ações disponíveis por conta:**
  - **Depósito:** Abre janela para informar valor (>0). Atualiza saldo e extrato.
  - **Transferência:** Abre janela para informar agência, conta de destino e valor (>0 e <= saldo). Atualiza saldo das duas contas e extratos.
  - **Pagamento:** Abre janela para informar valor (>0 e <= saldo). Atualiza saldo e extrato.
  - **Extrato:** Mostra todas as movimentações da conta.

### 4. Extrato
- **Formato das movimentações:**
  - Depósito: `Deposito: +R${valor}`
  - Transferência: `Transferencia: -R${valor}` (origem) / `Deposito: +R${valor}` (destino)
  - Pagamento: `Pagamento: -R${valor}`
- **Armazenamento:** Cada conta tem seu próprio arquivo de extrato no formato `extrato_{cpf}_{conta}.txt`.

---

## Estrutura dos Arquivos

- **cadastros.csv:** Armazena todos os dados dos usuários e contas.
- **extrato_{cpf}_{conta}.txt:** Armazena o extrato de cada conta individualmente.

---

## Fluxo de Uso

1. **Cadastro:** Usuário preenche os dados e cria uma conta.
2. **Login:** Usuário entra com CPF e senha.
3. **Menu:** Usuário pode gerenciar todas as suas contas.
4. **Operações:** Depósito, transferência, pagamento e consulta de extrato são feitos por conta.
5. **Persistência:** Todas as operações atualizam os arquivos correspondentes.

---

## Observações Técnicas

- **Múltiplas contas:** Um CPF pode ter várias contas e agências.
- **Conta única:** O número da conta é único no sistema.
- **Interface:** Todas as operações são feitas por janelas do tkinter.
- **Validações:** O sistema valida valores, existência de contas e saldo suficiente para operações.

---

## Dependências

- Python 3.13.3
- pandas 2.3.0
- tkinter (já incluso no Python padrão)

---

## Execução

Execute o arquivo principal (`login.py`)
