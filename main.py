# #############################################################################
# Imports
# #############################################################################

import database
import socket


# #############################################################################
# Methods
# #############################################################################

def start_web_server():
    HOST, PORT = "localhost", 80

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.settimeout(1)
    sock.listen(5)

    print("Serveur web prêt, en attente de connexion")

    run = True
    while run:

        try:
            conn, address = sock.accept()

            req = str(conn.recv(2048))[2:-1]

            data = req.split("\\r\\n")
            asked = data[0].split(" ")

            url = asked[1].split("?")

            if url[0][-1] == '/':
                url[0] += 'index.html'
            if url[0] == '/stop':
                run = False

            print(url)

            try:
                file = open(f'www{url[0]}', "rb")
                conn.send(file.read())
                file.close()
            except FileNotFoundError as err:
                print(err)

            conn.close()
        except socket.timeout:
            None

    print("[server] stop")


# #############################################################################
# Main
# #############################################################################


if __name__ == "__main__":

    start_web_server()
