from cryptography.fernet import Fernet
import os

# função para gerar chave
def gerar_chave():
    chave = Fernet.generate_key()
    with open("chave.key", "wb") as arquivo_chave:
        arquivo_chave.write(chave)


# função para carregar chave
def carregar_chave():
    if not os.path.exists("chave.key"):
        print("Chave não encontrada. Gere uma chave primeiro.")
        return None

    with open("chave.key", "rb") as f:
        return f.read()


# função para criptografar arquivo
def criptografar_arquivo(nome_arquivo):

    chave = carregar_chave()
    if chave is None:
        return

    fernet = Fernet(chave)

    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

        linhas_criptografadas = []

        # criptografa linha por linha
        for linha in linhas:
            criptografado = fernet.encrypt(linha.encode())
            linhas_criptografadas.append(criptografado.decode() + "\n")

        with open(nome_arquivo + ".enc", "w", encoding="utf-8") as arquivo:
            arquivo.writelines(linhas_criptografadas)

        print("Arquivo criptografado com sucesso!")

    except FileNotFoundError:
        print("Arquivo não encontrado.")


# função para descriptografar
def descriptografar_arquivo(nome_arquivo):

    chave = carregar_chave()
    if chave is None:
        return

    fernet = Fernet(chave)

    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

        linhas_descriptografadas = []

        # descriptografa linha por linha
        for linha in linhas:
            descriptografado = fernet.decrypt(linha.strip().encode())
            linhas_descriptografadas.append(descriptografado.decode())

        nome_original = nome_arquivo.replace(".enc", "_recuperado.txt")

        with open(nome_original, "w", encoding="utf-8") as arquivo:
            arquivo.writelines(linhas_descriptografadas)

        print("Arquivo descriptografado com sucesso!")

    except FileNotFoundError:
        print("Arquivo não encontrado.")


# menu
def menu():

    while True:

        print("\n--- Sistema de Criptografia de Arquivos ---")
        print("1 - Gerar chave")
        print("2 - Criptografar arquivo")
        print("3 - Descriptografar arquivo")
        print("4 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            gerar_chave()
            print("Chave gerada com sucesso!")

        elif opcao == "2":
            arquivo = input("Digite o nome do arquivo: ")
            criptografar_arquivo(arquivo)

        elif opcao == "3":
            arquivo = input("Digite o nome do arquivo criptografado: ")
            descriptografar_arquivo(arquivo)

        elif opcao == "4":
            print("Encerrando programa.")
            break

        else:
            print("Opção inválida!")


menu()