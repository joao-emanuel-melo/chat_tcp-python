import socket
import threading
import sys

def receive_messages(client_socket):
    """
    Thread para receber mensagens do servidor.
    """
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("\n[CONEXÃO PERDIDA] Você foi desconectado do servidor.")
                break
            print(f"\r{message}\n> ", end="")
            
    except ConnectionResetError:
        print("\n[ERRO] Conexão com o servidor foi perdida.")
    except Exception as e:
        if "closed" not in str(e):
            print(f"\n[ERRO NO RECEBIMENTO] {e}")
    finally:
        print("\n[INFO] Thread de recebimento encerrada.")

def send_messages(client_socket):
    """
    Loop principal para ENVIAR mensagens (roda na thread principal).
    O apelido JÁ FOI validado.
    """
    try:
        while True:
            message = input("> ")
            if not message:
                continue
                
            client_socket.send(message.encode('utf-8'))
            
            if message.lower() == 'quit':
                print("Saindo...")
                break
            
    except EOFError:
        print("Saindo...")
        client_socket.send("QUIT".encode('utf-8'))
    except Exception as e:
        if "closed" not in str(e):
            print(f"[ERRO AO ENVIAR] {e}")
    finally:
        print("\n[INFO] Loop de envio encerrado.")


def start_client():
    HOST = '127.0.0.1'
    PORT = 55556

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # --- ETAPA 1: CONECTAR ---
        client.connect((HOST, PORT))
        print(f"[CONECTADO] Conectado ao servidor em {HOST}:{PORT}")

        nickname = input("Escolha seu apelido: ")
        if not nickname:
            print("Apelido não pode ser vazio. Desconectando.")
            client.close()
            return

        client.send(nickname.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')

        if response.startswith("ERR"):
            print(f"[ERRO DO SERVIDOR] {response}")
            print("Desconectando...")
            client.close()
            return
        else:
            print(response)
        
        recv_thread = threading.Thread(target=receive_messages, args=(client,))
        recv_thread.daemon = True 
        recv_thread.start()
        send_messages(client)

    except ConnectionRefusedError:
        print("[ERRO] Não foi possível conectar ao servidor. Ele está online?")
    except Exception as e:
        print(f"[ERRO INESPERADO] {e}")
    finally:
        print("[FINAL] Encerrando conexão.")
        client.close()
        sys.exit()

if __name__ == "__main__":
    start_client()