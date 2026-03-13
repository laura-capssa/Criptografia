from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


# gerar chave publica e privada
def gerar_chaves():

    chave_privada = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    chave_publica = chave_privada.public_key()

    # salvar chave privada
    with open("chave_privada.pem", "wb") as f:
        f.write(
            chave_privada.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # salvar chave pública
    with open("chave_publica.pem", "wb") as f:
        f.write(
            chave_publica.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    print("Chaves geradas com sucesso!")


# criptografar arquivo
def criptografar_arquivo(nome_arquivo):

    # carregar chave pública
    with open("chave_publica.pem", "rb") as f:
        chave_publica = serialization.load_pem_public_key(f.read())

    with open(nome_arquivo, "rb") as f:
        dados = f.read()

    criptografado = chave_publica.encrypt(
        dados,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(nome_arquivo + ".enc", "wb") as f:
        f.write(criptografado)

    print("Arquivo criptografado!")


# descriptografar arquivo
def descriptografar_arquivo(nome_arquivo):

    # carregar chave privada
    with open("chave_privada.pem", "rb") as f:
        chave_privada = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    with open(nome_arquivo, "rb") as f:
        dados = f.read()

    descriptografado = chave_privada.decrypt(
        dados,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open("arquivo_recuperado.txt", "wb") as f:
        f.write(descriptografado)

    print("Arquivo descriptografado!")


# menu
def menu():

    while True:

        print("\n--- Criptografia Assimétrica ---")
        print("1 - Gerar chaves")
        print("2 - Criptografar arquivo")
        print("3 - Descriptografar arquivo")
        print("4 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            gerar_chaves()

        elif opcao == "2":
            nome = input("Nome do arquivo: ")
            criptografar_arquivo(nome)

        elif opcao == "3":
            nome = input("Arquivo criptografado: ")
            descriptografar_arquivo(nome)

        elif opcao == "4":
            break

        else:
            print("Opção inválida")


menu()