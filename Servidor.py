from socket import *
import random

# Configuração do servidor
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('O servidor está pronto para receber conexões')

# Lista de produtos disponíveis
produtos = {
    1: {'nome': 'Notebook', 'preco': 2500},
    2: {'nome': 'Smartphone', 'preco': 1500},
    3: {'nome': 'Tablet', 'preco': 1000}
}

# Lista de mensagens aleatórias para negociação
mensagens_negociacao = [
    "Aí cê me quebra né amigo, e meu lucro vai onde? Faz uma nova oferta aí meu patrão.",
    "Essa oferta tá muito baixa, meu camarada! Vamos melhorar isso aí.",
    "Desse jeito eu não fecho negócio, tente um valor mais próximo do original.",
    "Amigo, assim fica difícil... vamos tentar uma nova oferta, mais justa.",
    "Essa oferta não dá, pense em algo mais próximo do preço inicial!"
]

def negociar_preco(preco_inicial, oferta):
    if oferta >= preco_inicial * 0.9:  # Aceita ofertas acima de 90% do preço inicial
        return True
    return False

while True:
    # Aguarda uma conexão
    connectionSocket, addr = serverSocket.accept()

    # Envia a lista de produtos para o cliente
    produtos_info = "\n".join([f"{codigo} - {info['nome']} - R${info['preco']}" for codigo, info in produtos.items()])
    connectionSocket.send(produtos_info.encode())

    # Recebe o código do produto escolhido
    codigo_produto = int(connectionSocket.recv(1024).decode())

    # Envia o nome e o preço inicial do produto escolhido
    produto = produtos.get(codigo_produto)
    connectionSocket.send(f"Você escolheu {produto['nome']} com preço inicial de R${produto['preco']}".encode())

    # Inicia a negociação
    for _ in range(3):  # Limita a negociação a 3 tentativas
        oferta = float(connectionSocket.recv(1024).decode())
        if negociar_preco(produto['preco'], oferta):
            connectionSocket.send("Oferta aceita!".encode())
            break
        else:
            # Escolhe uma mensagem aleatória da lista e envia
            mensagem = random.choice(mensagens_negociacao)
            connectionSocket.send(mensagem.encode())
    else:
        connectionSocket.send("Limite de tentativas alcançado. Negociação encerrada.".encode())

    connectionSocket.close()