import socket
import threading
clients = {}
clients_lock = threading.Lock()

def handle_client(client_socket, client_address):
    """
    Função para gerenciar a comunicação com um cliente específico.
    """
    print(f"[NOVA CONEXÃO] {client_address} conectado. Aguardando apelido...")

    nickname = None
    try:
        proposed_nick = client_socket.recv(1024).decode('utf-8')
        if not proposed_nick:
            print(f"[DESCONEXÃO] {client_address} desconectou antes de enviar o apelido.")
            client_socket.close()
            return
        with clients_lock:
            if proposed_nick in clients:
                print(f"[APELIDO RECUSADO] {client_address} tentou usar '{proposed_nick}' (em uso).")
                client_socket.send("ERR apelido_em_uso".encode('utf-8'))
                client_socket.close()
                return
            else:
                nickname = proposed_nick
                clients[nickname] = client_socket
                print(f"[APELIDO ACEITO] {client_address} agora é {nickname}.")
                client_socket.send(f"User {nickname} joined".encode('utf-8'))
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"[{nickname}]: {message}")
            client_socket.send(f"Mensagem recebida".encode('utf-8'))
            
    except ConnectionResetError:
        print(f"[DESCONEXÃO] {nickname} ({client_address}) desconectou abruptamente.")
    except Exception as e:
        print(f"[ERRO] {e}")
    finally:
        if nickname:
            with clients_lock:
                if nickname in clients:
                    del clients[nickname]
                    print(f"[LIMPEZA] {nickname} removido do chat.")
                    
        print(f"[CONEXÃO ENCERRADA] {client_address}")
        client_socket.close()

def start_server():
    """
    Função principal para iniciar o servidor de chat.
    """
    HOST = '127.0.0.1'
    PORT = 55556        

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[ESCUTANDO] Servidor escutando em {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    start_server()