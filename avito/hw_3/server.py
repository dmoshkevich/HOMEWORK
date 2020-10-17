import socket
import random


if __name__ == "__main__":
    secretnumber = random.randint(0, 100)
    print(secretnumber)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 8000))
        s.listen(10)
        conn, addr = s.accept()

        with conn:
            conn.send(b"game begins")
            while True:
                data = conn.recv(7)
                guess = int(data.decode("utf-8"))
                if guess == secretnumber:
                    conn.send(b"correct")
                    conn.close()
                    exit(1)
                elif guess > secretnumber:
                    conn.send(b"less")
                elif guess < secretnumber:
                    conn.send(b"more")
