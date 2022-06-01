import socket 
import threading

HEADER = 64
PORT = 5050
#SERVER = "192.168.0.6" #cmd에서 ipconfig 후 나타는 정보중에 IPv4 주소를 가져옴
SERVER = socket.gethostbyname(socket.gethostname())#이 코드로도 IP주소 가져올 수 있음
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socket.AF_INET over the internet>Family ||socket.SOCK_STREAM > Type
server.bind(ADDR)

def handle_client(conn, addr):#서버와 클라이언트의 통신 모든 것을 handle 함
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)#client로부터 무엇을 받아들임, HEADER 만큼의 크기만큼 받아들임
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()
        

def start(): #어떤 정보를 어디로 보낼지 handl
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()#addr 연결된 것의 정보를 가져옴
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()



