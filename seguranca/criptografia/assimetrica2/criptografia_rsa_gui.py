import tkinter as tk
from tkinter import filedialog, messagebox

#Instalar com python -m pip install pycryptodomex --force-reinstall
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

# -------------------------
# Gerar chaves RSA
# -------------------------
def gerar_chaves():
    chave = RSA.generate(2048)

    with open("private.pem", "wb") as f:
        f.write(chave.export_key())

    with open("public.pem", "wb") as f:
        f.write(chave.publickey().export_key())

    messagebox.showinfo("Sucesso", "Chaves geradas!")

# -------------------------
# Criptografar arquivo
# -------------------------
def criptografar():
    arquivo = filedialog.askopenfilename(title="Selecionar arquivo")

    if not arquivo:
        return

    try:
        with open("public.pem", "rb") as f:
            chave_publica = RSA.import_key(f.read())

        cipher = PKCS1_OAEP.new(chave_publica)

        with open(arquivo, "rb") as f:
            dados = f.read()

        bloco = 190
        criptografado = b''

        for i in range(0, len(dados), bloco):
            parte = dados[i:i+bloco]
            criptografado += cipher.encrypt(parte)

        salvar = filedialog.asksaveasfilename(defaultextension=".bin")

        if salvar:
            with open(salvar, "wb") as f:
                f.write(criptografado)

        messagebox.showinfo("Sucesso", "Arquivo criptografado!")

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# -------------------------
# Descriptografar arquivo
# -------------------------
def descriptografar():
    arquivo = filedialog.askopenfilename(title="Selecionar arquivo criptografado")

    if not arquivo:
        return

    try:
        with open("private.pem", "rb") as f:
            chave_privada = RSA.import_key(f.read())

        cipher = PKCS1_OAEP.new(chave_privada)

        descriptografado = b''

        with open(arquivo, "rb") as f:
            while True:
                bloco = f.read(256)
                if not bloco:
                    break
                descriptografado += cipher.decrypt(bloco)

        salvar = filedialog.asksaveasfilename()

        if salvar:
            with open(salvar, "wb") as f:
                f.write(descriptografado)

        messagebox.showinfo("Sucesso", "Arquivo descriptografado!")

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# -------------------------
# Interface gráfica
# -------------------------
janela = tk.Tk()
janela.title("Sistema de Criptografia RSA")
janela.geometry("400x250")

titulo = tk.Label(
    janela,
    text="Criptografia de Arquivos (RSA)",
    font=("Arial", 14)
)
titulo.pack(pady=20)

botao_chaves = tk.Button(
    janela,
    text="Gerar Chaves",
    width=25,
    command=gerar_chaves
)
botao_chaves.pack(pady=10)

botao_criptografar = tk.Button(
    janela,
    text="Criptografar Arquivo",
    width=25,
    command=criptografar
)
botao_criptografar.pack(pady=10)

botao_descriptografar = tk.Button(
    janela,
    text="Descriptografar Arquivo",
    width=25,
    command=descriptografar
)
botao_descriptografar.pack(pady=10)

botao_sair = tk.Button(
    janela,
    text="Sair",
    width=25,
    command=janela.quit
)
botao_sair.pack(pady=10)

janela.mainloop()
