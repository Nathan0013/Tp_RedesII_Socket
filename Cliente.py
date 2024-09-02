from socket import *

# Configuração do cliente
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Recebe a lista de produtos disponíveis
produtos = clientSocket.recv(1024).decode()
print("Produtos disponíveis:\n", produtos)

# Escolhe o produto
codigo_produto = input("Digite o código do produto que deseja comprar: ")
clientSocket.send(codigo_produto.encode())

# Recebe a confirmação do produto escolhido
produto_info = clientSocket.recv(1024).decode()
print(produto_info)

# Inicia a negociação
for _ in range(3):  # Limita a negociação a 3 tentativas
    oferta = input("Digite sua oferta: R$")
    clientSocket.send(oferta.encode())
    resposta = clientSocket.recv(1024).decode()
    print(resposta)
    if "aceita" in resposta:
        break

clientSocket.close()