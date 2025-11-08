Projeto Mini-Chat TCP
Este é um sistema de chat multiusuário simples implementado em Python usando a biblioteca socket. Ele permite que múltiplos clientes se conectem a um servidor central e conversem via broadcast ou mensagens diretas (DMs), seguindo um protocolo de texto simples.

O sistema utiliza TCP para transporte e Threads para gerenciar múltiplos clientes de forma concorrente.


⚙️ Configuração (Importante!)
Antes de executar, você precisa garantir que o cliente consiga encontrar o servidor na rede.

O servidor (server.py) usa socket.gethostbyname(socket.gethostname()) para tentar encontrar o IP da máquina na rede local. O cliente (client.py) está configurado com um IP estático (SERVER = "10.1.8.70").
